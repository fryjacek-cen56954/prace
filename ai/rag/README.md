# Základní RAG

Tento příklad načte Markdownové podklady ze složek `funsel/` a `funsels/`,
rozdělí je na části, vyhledá relevantní části pomocí embeddingů a odpoví na
jeden dotaz pomocí LangChain a OpenAI. Při každém spuštění se index vytváří
znovu v paměti; žádný vektorový index se neukládá do repozitáře.

## Spuštění

Vyžaduje Python 3.10 nebo novější a proměnnou prostředí `OPENAI_API_KEY`.

```sh
python -m venv .venv
. .venv/bin/activate
pip install -r ai/rag/requirements.txt
export OPENAI_API_KEY="..."
python ai/rag/rag.py "Co víme o úkolu DFM-219963?"
```

Ve Windows aktivujte prostředí příkazem `.venv\Scripts\activate` a nastavte
klíč způsobem obvyklým pro daný shell. Volby `--source`, `--model` a `--k`
umožňují změnit zdrojové adresáře, model a počet načtených částí; podrobnosti
zobrazí `python ai/rag/rag.py --help`.

Výsledek obsahuje odpověď a seznam citovaných zdrojových cest. Pro produkční
nasazení doplňte trvalé úložiště, aktualizaci indexu a správu přístupů k
podkladům i API klíči.
