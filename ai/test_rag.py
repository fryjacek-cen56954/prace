"""Offline integrační testy nad dočasnými podklady a skutečnou lokální Chroma."""

from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from langchain_chroma import Chroma
from langchain_core.embeddings import DeterministicFakeEmbedding

import rag


class RagTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for app in rag.APPS:
            (self.root / app).mkdir()

    def task(self, app="funsel", code="DFM-219963"):
        directory = self.root / app / code
        directory.mkdir()
        (directory / "README.md").write_text(
            f"---\ntitle: Testovací úkol\ndocument_type: task\napplication: {app}\n"
            f"task_id: {code}\nstatus: analysis\nupdated: 2026-10-23\n"
            f"jira_url: https://csas.atlassian.net/browse/{code}\n---\n"
            "# Testovací úkol\n\n## Současný stav\n\nProbíhá analýza.\n",
            encoding="utf-8",
        )
        return directory

    def test_metadata_and_citations_survive_chunking(self):
        directory = self.task()
        (directory / "analyza.md").write_text(
            '---\ntitle: Analýza\ndocument_type: analysis\nupdated: "2026-10-23"\n'
            "---\n# Analýza\n\n## Závěry\n\n" + "Neověřený předpoklad. " * 200,
            encoding="utf-8",
        )
        chunks = rag.split_documents(rag.load_documents(self.root))
        analysis = [chunk for chunk in chunks if chunk.metadata["document_type"] == "analysis"]
        self.assertGreater(len(analysis), 1)
        self.assertEqual([c.metadata["chunk_index"] for c in analysis], list(range(len(analysis))))
        for chunk in analysis:
            self.assertEqual(chunk.metadata["application"], "funsel")
            self.assertEqual(chunk.metadata["task_id"], "DFM-219963")
            self.assertEqual(chunk.metadata["status"], "analysis")
            self.assertEqual(chunk.metadata["updated"], "2026-10-23")
            self.assertEqual(chunk.metadata["source"], "funsel/DFM-219963/analyza.md")
        self.assertIn("Závěry", analysis[-1].metadata["heading"])

    def test_conflicting_metadata_rejected(self):
        directory = self.task()
        (directory / "analyza.md").write_text(
            "---\ntitle: Analýza\ndocument_type: analysis\nupdated: 2026-10-23\n"
            "application: funsels\n---\n# Analýza\nText.", encoding="utf-8",
        )
        with self.assertRaisesRegex(ValueError, "rozchází"):
            rag.load_documents(self.root)

    def test_invalid_directory_and_missing_readme_rejected(self):
        directory = self.root / "funsel" / "DFM-12345"
        directory.mkdir()
        with self.assertRaisesRegex(ValueError, "neplatný kód"):
            rag.load_documents(self.root)
        directory.rename(directory.with_name("DFM-123456"))
        with self.assertRaises(FileNotFoundError):
            rag.load_documents(self.root)

    def test_sync_filters_updates_and_deletions(self):
        first = self.task()
        self.task(app="funsels")
        store = Chroma(
            collection_name="test_tasks", persist_directory=str(self.root / "db"),
            embedding_function=DeterministicFakeEmbedding(size=16),
        )
        chunks = rag.split_documents(rag.load_documents(self.root))
        rag.sync_index(store, chunks)
        rag.sync_index(store, chunks)
        self.assertEqual(len(store.get()["ids"]), len(chunks))
        hits = store.similarity_search("stav", k=10, filter=rag.make_filter("funsels", "DFM-219963"))
        self.assertTrue(hits)
        self.assertTrue(all(hit.metadata["application"] == "funsels" for hit in hits))
        self.assertEqual(len(store.get(where=rag.make_filter(None, "DFM-219963"))["ids"]), len(chunks))
        readme = first / "README.md"
        readme.write_text(readme.read_text(encoding="utf-8").replace("status: analysis", "status: done"), encoding="utf-8")
        rag.sync_index(store, rag.split_documents(rag.load_documents(self.root)))
        self.assertTrue(all(meta["status"] == "done" for meta in store.get(where=rag.make_filter("funsel", None))["metadatas"]))
        readme.unlink()
        first.rmdir()
        rag.sync_index(store, rag.split_documents(rag.load_documents(self.root)))
        self.assertEqual(store.get(where=rag.make_filter("funsel", None))["ids"], [])
        rag.sync_index(store, [])
        self.assertEqual(store.get()["ids"], [])

    def test_empty_repository(self):
        self.assertEqual(rag.split_documents(rag.load_documents(self.root)), [])
        self.assertIn("nebyly nalezeny", rag.answer("dotaz", []))

    def test_embedding_model_mismatch_rejected(self):
        with patch.dict("os.environ", {
            "RAG_DB_DIR": str(self.root / "model-db"),
            "RAG_COLLECTION": "model_test", "OPENAI_EMBEDDING_MODEL": "model-a",
        }), patch.object(rag, "OpenAIEmbeddings", return_value=DeterministicFakeEmbedding(size=16)):
            rag.open_store()
            with patch.dict("os.environ", {"OPENAI_EMBEDDING_MODEL": "model-b"}):
                with self.assertRaisesRegex(ValueError, "Jiný embeddingový model"):
                    rag.open_store()


if __name__ == "__main__":
    unittest.main()
