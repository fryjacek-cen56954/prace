# Custom agent a RAG

## Rozcestník

- [agent.md](agent.md) — stručný návrh vyhledávacího agenta a jeho nástrojů.
- [rag.py](rag.py) — základní LangChain pipeline: validace, indexace, hledání a odpověď.
- [requirements.txt](requirements.txt) — závislosti pro Python 3.11+.
- [.env.example](.env.example) — nastavení modelů a lokálního indexu.
- [test_rag.py](test_rag.py) — offline testy metadat, filtrů a aktualizace indexu.

## Architektura

```text
funsel|funsels/<KÓD>/**/*.md
  → validace YAML + metadata z README úkolu
  → sekce podle nadpisů → menší překrývající se chunky
  → OpenAI embeddings → lokální Chroma knowledge base
  → hledání s filtry aplikace/kódu → zdrojové úryvky pro custom agenta
  → volitelně LLM odpověď s citacemi (příkaz ask)
```

Indexují se pouze Markdown soubory uvnitř úkolů. Kořenové README, indexy aplikací,
šablony a návrh agenta se neindexují; agent je čte přímo jako navigaci.
Obrázky, EA exporty a další přílohy vyžadují [textový popis](../templates/asset-description.md).
Odkaz na Jira se uloží do metadat; pipeline obsah Atlassian nestahuje.

## Spuštění

Příkazy spouštějte z kořene repozitáře:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r ai/requirements.txt
cp ai/.env.example ai/.env
# Vyplňte OPENAI_API_KEY v ai/.env.
python ai/rag.py validate
python ai/rag.py index
python ai/rag.py search "Jaké jsou otevřené otázky?" --app funsel --task DFM-219963
python ai/rag.py ask "Shrň potvrzená rozhodnutí a rozpory" --app funsel
```

Výchozí embeddingy a generování používají OpenAI API: při indexaci se odesílá
text podkladů, při dotazu text otázky a při `ask` také vybrané úryvky.
`search` vrací JSON s úryvky a metadaty bez generování odpovědi.
`validate` a testy nepotřebují API klíč. Konfigurace se načítá z `ai/.env`,
existující proměnné prostředí mají přednost.

## Aktualizace a citace

`index` znovu vypočítá embeddingy všech chunků a pak odstraní záznamy, které
už v podkladech nejsou; pokrývá také smazání a přejmenování souborů.
Neplatná metadata zastaví indexaci před zápisem. Prázdný repozitář je platný
a index neobsahuje žádné úryvky. Indexaci a dotazy spouštějte postupně;
základní implementace nemá transakční výměnu celého indexu.

Chunk nese `application`, `task_id`, `status`, `jira_url`, `title`,
`document_type`, `updated`, `source`, `heading` a `chunk_index`.
Citace má podobu `funsel/DFM-219963/analyza.md — Závěry`.
Výsledky jsou podklady, nikoli potvrzená fakta: agent ověřuje stav v README,
schválení v textu a podle potřeby načte celé zdrojové sekce.

Při změně embeddingového modelu nastavte také novou hodnotu `RAG_COLLECTION`
a spusťte `index`; starou kolekci kód s jiným modelem odmítne použít.
API klíč a lokální Chroma data ignoruje Git.

## Ověření

```bash
python -m unittest discover -s ai -p 'test_*.py'
```

Testy používají dočasné úkoly, lokální Chroma a deterministické testovací embeddingy.
Pro ověření skutečné relevance po naplnění repo spusťte několik známých otázek
s očekávaným úkolem a zdrojovou sekcí. Samotný úspěšný běh není měřením relevance.

## Možná rozšíření

Inkrementální embeddingy podle hashů souborů, hybridní fulltextové a vektorové
hledání, reranking a sada referenčních otázek. Samostatný autorizovaný Atlassian
konektor může ukládat snapshoty s datem a původem. OCR a převod EA diagramů
mají vytvářet kontrolovatelný textový popis vedle původní přílohy.
