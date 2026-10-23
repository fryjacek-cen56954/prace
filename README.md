# Pracovní úkoly

Repozitář slouží jako přehledný archiv podkladů k pracovním úkolům. Obsahuje
analýzy, zadání pro AI agenty, obrázky uživatelského rozhraní a diagramy
z Enterprise Architect. Dokumentace je určená lidem i nástrojům AI/RAG.

## Struktura

```text
funsel/
  funsel-TASKS.md
  CSO-xxxxxx/
    README.md
    ...
funsels/
  funsels-TASKS.md
  DFM-xxxxxx/
    README.md
    ...
templates/
  task/
    README.md
ai/
  custom-agent.md
  rag/
```

Úkoly patří do složky příslušné aplikace a jejich adresář se jmenuje kódem
`CSO-` nebo `DFM-` následovaným šesti číslicemi. Každý úkol musí mít vlastní
`README.md`; jeho výchozí osnovu najdete v `templates/task/README.md`.

Do `funsel/funsel-TASKS.md` a `funsels/funsels-TASKS.md` se přidává jeden řádek
na úkol: kód, stručný popis a odkaz na jeho adresář. Podrobnosti o doporučeném
obsahu a pojmenování souborů jsou v šabloně úkolu.

Návrh custom agenta a základní implementaci RAG v Pythonu najdete ve složce
`ai/`.
