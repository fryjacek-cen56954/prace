# prace


## Poslat agentovi
V tomto repu budu mít podklady k pracovnim ukolum. Ukoly budou rozdelene podle aplikaci (funsel, funsels) a pak v podadresarich. Kazdy ukol má kod ve formátu CSO-xxxxxx nebo DFM-xxxxxx (x je číslo) a tyto kódy je možné dohledat ve Atlassian (např. https://csas.atlassian.net/browse/DFM-219963).
K úkoly si budu ukládat dokuementy v markdown, kde budou výsledky analýz agentů AI, moje zadání pro agenty, obrázky s UI, diagramy z Enterprise Architect.
V adresářích s aplikacemi bude markdown s názevm <aplikace>-TASKS.md, kde bude na jednu řádku popis úkolu a odkaz na adresář s ukolem.
Každý úkol bude mít ve svém adresář soubor README.md, kde bude základní popis, současný stav, rozcestník a vysvětlení obsahu ostatních souborů v adresáři.

Důležité: tato struktura musí sloužit jak pro člověka, tak pro custom agenta a RAG. Custom agent bude v ukolech hledat a těžit informace. RAG bude informace doplnovat do knowledgebase pro toho agenta.
Pro agenta a RAG udělej složku "ai" a v ní navrhni stručně toho custom agenta a také záklaní RAG postavené na Langchain v python.
