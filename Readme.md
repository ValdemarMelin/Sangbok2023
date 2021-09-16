# Fysiksektionens sångbok
[![Build LaTeX documents](https://github.com/oskarr/Sangbok/actions/workflows/compile.yml/badge.svg)](https://github.com/oskarr/Sangbok/actions/workflows/compile.yml) [![Parse into JSON](https://github.com/oskarr/Sangbok/actions/workflows/json-parse.yml/badge.svg)](https://github.com/oskarr/Sangbok/actions/workflows/json-parse.yml)

Du letar förmodligen efter [Fysiksektionen/Sangbok](https://github.com/Fysiksektionen/Sangbok). Detta repo är enbart för privat bruk, då Overleaf enbart kan pulla från main-branchen (vilken jag inte vill röra i originalrepot). Notera att "Parse into JSON" ovan enbart beskriver om alla låtar kunde läsas av, inte om de lästes av korrekt.

## Användning
Skriptet `compile.sh` kompilerar alla .tex-filer i huvudmappens direkta undermappar (dvs. inte de som är i Äldre-mappen). Notera att då detta repo _inte_ innehåller .aux-filer, måste allt kompileras **2 gånger** för att sidspalten ska komma med ordentligt om det görs manuellt (du behöver dock inte tänka på detta om du använder `compile.sh`).

## Att fixa
* Parsing av tabeller
* Inläsning av upphovsperson och melodi.
* Fixa MathMode-ersättningar för ODE till en husvagn.
* Idiotsäkra parsningen av fetstilt och kursiv text, samt gör något liknande för `\mcode{...}`.
* CI-Kompileringen av innehållet är inte helt som originalet.
 * sidspaltHack fungerar ej.
* Formatet för Système International är ej standardiserat.
* Intro, My och Sigmas sidmarginaler är följer ej standarden.

## Förändringar
För att underlätta parsing, är det bra om saker är standardiserade. Denna branch har därför ändrat:
* Alla titlar, så att bokstäver efteråt hamnar _efter_ dollartecknena, och att `\Large` är en för-modifier, utan måsvingar.
* Bytt namn Jesus lever till Ny-18 (Ny-17 var dubblett.).
* Textregistrets sida 2, samt namnregistrets sida 2 och 4 har nu samma marginal som resten av sidorna i registret.
* Fler ändringar kommer, och det återstår att testa så att resultatet blir likvärdigt.

### Användbar RegEx
(För manuell ändring till digital version.)
* `\\huge\{(\w{0,2}(\$.*?\$)?)\s(.*)\}` => `\chaptertitle{$1}{$3}` - kapiteltitel
* * `\\Large\s([\$]\\[a-z]+?[,\d\.]*?\$[a-z]?)\.\s([^\\]*?)\s?\\{2}` => `\songtitle{$1}{$2}` vanliga låttitlar
* `\\Large\s([\$]\\[a-z]+?[,\d\.]*?\$[a-z]?)\.\s([^\\]*).*` => `\songtitle{$1}{$2}` - vanliga låttitlar (utan nyrad på slutet)
* `\\Large\s[\$]\\[\w\/]+?\\[a-z]+?\$\.` - numrerade med specialsymboler
* `\\Large\so\d+?[a-z]?\. ` - omikron
* `\\begin\{flushright\}\n?\s{0,8}\\textit\{(.*)\}\n?\\end\{flushright\}` => `\auth{$1}` - upphovsperson