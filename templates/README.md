# Šablony a metadata

Šablony zkopírujte do adresáře úkolu a nahraďte všechny hodnoty v `<…>`.
Samotné šablony se neindexují.

| Šablona | Použití |
| --- | --- |
| [task-README.md](task-README.md) | Povinný rozcestník každého úkolu |
| [document.md](document.md) | Zadání, analýza, rozhodnutí nebo poznámky |
| [asset-description.md](asset-description.md) | Textový popis UI nebo diagramu vedle přílohy |

## YAML front matter

Každý Markdown v adresáři úkolu začíná YAML blokem mezi `---`.

| Pole | Kde | Význam |
| --- | --- | --- |
| `title` | Všechny dokumenty | Výstižný název, ideálně v uvozovkách |
| `document_type` | Všechny dokumenty | `task`, `assignment`, `analysis`, `decision`, `note`, `ui`, `diagram` |
| `updated` | Všechny dokumenty | Datum poslední věcné změny `YYYY-MM-DD` |
| `application` | README úkolu | `funsel` nebo `funsels`, musí odpovídat cestě |
| `task_id` | README úkolu | Kód odpovídající názvu adresáře |
| `status` | README úkolu | `new`, `analysis`, `in_progress`, `blocked`, `done`, `archived` |
| `jira_url` | README úkolu | `https://csas.atlassian.net/browse/<task_id>` |

Kořenový README úkolu má `document_type: task`. Ostatní dokumenty aplikaci, kód
a aktuální stav dědí z něj, aby se metadata nerozcházela. RAG přidává `source`
(relativní cestu), `heading` a `chunk_index` pro citace. Datum dokumentu není datem indexace.

## Obsah vhodný pro vyhledávání

- Jeden dokument pro jedno téma, nadpisy `#` až `###`, zkratky při prvním použití vysvětlete.
- Analýza uvádí autora (člověk / agent a model, je-li znám), zdroje, předpoklady,
  závěry a otevřené otázky. Schválení zaznamenejte výslovně včetně osoby a data.
- Rozhodnutí označte jako návrh, potvrzené nebo nahrazené; doplňte odkazy na souvislosti.
- UI popisuje prvky, stavy, validace a chování, nejen vzhled. Diagram popisuje uzly,
  vztahy, směry, podmínky a výjimky; u EA uveďte balíček, název a GUID, pokud je znáte.
- Odkazy na jiné úkoly i přílohy jsou relativní. README eviduje i soubory v podadresářích.
