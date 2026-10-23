"""Small command-line RAG over this repository's Markdown task documents."""

import argparse
import os
from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]


def load_documents(source_dirs: list[Path]) -> list[Document]:
    documents = []
    for source_dir in source_dirs:
        if not source_dir.is_dir():
            raise ValueError(f"Zdrojový adresář neexistuje: {source_dir}")
        for path in sorted(source_dir.rglob("*.md")):
            if not path.is_file():
                continue
            absolute_path = path.resolve()
            try:
                content = absolute_path.read_text(encoding="utf-8")
            except (OSError, UnicodeError) as error:
                raise ValueError(f"Nelze načíst Markdown soubor {absolute_path}: {error}") from error
            if content.strip():
                try:
                    source = absolute_path.relative_to(REPOSITORY_ROOT).as_posix()
                except ValueError:
                    source = absolute_path.as_posix()
                documents.append(
                    Document(
                        page_content=content,
                        metadata={"source": source},
                    )
                )
    return documents


def answer_question(question: str, source_dirs: list[Path], model: str, k: int) -> None:
    if not os.environ.get("OPENAI_API_KEY"):
        raise ValueError("Nastavte proměnnou prostředí OPENAI_API_KEY.")

    documents = load_documents(source_dirs)
    if not documents:
        raise ValueError("Ve zvolených adresářích nebyly nalezeny žádné Markdownové podklady.")

    splitter = RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=150)
    chunks = splitter.split_documents(documents)
    vector_store = FAISS.from_documents(chunks, OpenAIEmbeddings())
    matches = vector_store.as_retriever(search_kwargs={"k": k}).invoke(question)
    context = "\n\n".join(
        f"[Zdroj: {doc.metadata['source']}]\n{doc.page_content}" for doc in matches
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Odpovídej podle kontextu, jazykem dotazu. Pokud kontext odpověď "
                "nepodporuje, řekni to. Zachovej rozdíl mezi fakty a předpoklady.",
            ),
            ("human", "Dotaz: {question}\n\nKontext:\n{context}"),
        ]
    )
    response = (prompt | ChatOpenAI(model=model, temperature=0)).invoke(
        {"question": question, "context": context}
    )

    print(response.content)
    print("\nZdroje:")
    for source in dict.fromkeys(doc.metadata["source"] for doc in matches):
        print(f"- {source}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("question", help="Otázka k podkladům")
    parser.add_argument(
        "--source",
        nargs="+",
        type=Path,
        default=[REPOSITORY_ROOT / "funsel", REPOSITORY_ROOT / "funsels"],
        help="Adresáře s Markdownovými podklady (výchozí: funsel/ funsels/)",
    )
    parser.add_argument("--model", default="gpt-4o-mini", help="Název OpenAI chat modelu")
    parser.add_argument("--k", type=int, default=4, help="Počet načtených částí kontextu")
    args = parser.parse_args()

    if args.k < 1:
        parser.error("--k musí být alespoň 1.")
    try:
        answer_question(args.question, args.source, args.model, args.k)
    except ValueError as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
