# Podklady k pracovním úkolům

Společný zdroj podkladů pro člověka, custom AI agenta a jeho RAG knowledge base.
Primárním zdrojem pravdy jsou soubory v Gitu; vektorový index je odvozený a lze jej znovu sestavit.

## Rozcestník

- [Úkoly funsel](funsel/funsel-TASKS.md)
- [Úkoly funsels](funsels/funsels-TASKS.md)
- [Šablony a metadata](templates/README.md)
- [Custom agent a RAG](ai/README.md)
- [Pravidla pro agenty](AGENTS.md)
- [Původní zadání](docs/zadani-repozitare.md)

## Struktura

```text
funsel/
  funsel-TASKS.md
  DFM-xxxxxx/                 # xxxxxx nahraďte šesti číslicemi
    README.md                # popis, stav, rozcestník všech podkladů
    zadani.md                # zadání člověka pro agenta
    analyza.md               # výsledek analýzy, zdroje a otevřené otázky
    rozhodnuti.md            # potvrzená rozhodnutí a jejich důvody
    assets/
      ui-prehled.png
      ui-prehled.md          # textový popis obrázku
      ea-proces.svg
      ea-proces.md           # textový přepis diagramu
funsels/
  funsels-TASKS.md
templates/
ai/
```

Ukázkové názvy výše nejsou skutečné úkoly. Adresář úkolu je přímo pod aplikací
a jmenuje se přesně `CSO-` nebo `DFM-` následované šesti číslicemi.
Stejný úkol může mít podklady v obou aplikacích; identita je dvojice aplikace + kód.

## Založení a údržba úkolu

1. Vytvořte například `funsel/DFM-219963/` a vložte do něj vyplněnou
   [šablonu README](templates/task-README.md). Jde jen o příklad kódu, nikoli o popis jeho skutečného obsahu.
2. Doplňte základní popis, aktuální stav a odkaz na Atlassian:
   `https://csas.atlassian.net/browse/DFM-219963`.
3. Do `funsel-TASKS.md` přidejte jednu odrážku na jeden řádek:
   `- [DFM-219963](DFM-219963/) — Stručný popis úkolu.`
4. Přidávejte podklady podle [šablon](templates/README.md). V README udržujte
   rozcestník s vysvětlením každého souboru, včetně příloh a jejich textových popisů.
5. Při změně dokumentu upravte `updated`. Při změně stavu úkolu upravte stav v jeho README.
   Odlište potvrzená fakta od návrhů AI; rozpory a nahrazená rozhodnutí označte přímo v textu.
6. Po změnách spusťte [obnovu RAG indexu](ai/README.md). Bez ní RAG pracuje s posledním indexovaným stavem.

Používejte UTF-8, relativní odkazy, smysluplné nadpisy a názvy souborů bez mezer.
Textový popis obrázku nebo diagramu patří vedle přílohy se stejným základem názvu.
