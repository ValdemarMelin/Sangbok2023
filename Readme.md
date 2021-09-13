# Fysiksektionens sångbok
Du letar förmodligen efter [Fysiksektionen/Sangbok](https://github.com/Fysiksektionen/Sangbok). Detta repo är enbart för privat bruk, då Overleaf enbart kan pulla från main-branchen (vilken jag inte vill röra i originalrepot).

## Att fixa
* Epsilon - Omega

## Förändringar
För att underlätta parsing, är det bra om saker är standardiserade. Denna branch har därför ändrat:
* Alla titlar, så att bokstäver efteråt hamnar _efter_ dollartecknena, och att `\Large` är en för-modifier, utan måsvingar.
* Bytt namn Jesus lever till Ny-18 (Ny-17 var dubblett.).
* Fler ändringar kommer, och det återstår att testa så att resultatet blir likvärdigt.

### Användbar RegEx
(För manuell ändring till digital version.)
* `\\huge\{(\w{0,2}(\$.*?\$)?)\s(.*)\}` => `\chaptertitle{$1}{$3}` - kapiteltitel
* * `\\Large\s([\$]\\[a-z]+?[,\d\.]*?\$[a-z]?)\.\s([^\\]*?)\s?\\{2}` => `\songtitle{$1}{$2}` vanliga låttitlar
* `\\Large\s([\$]\\[a-z]+?[,\d\.]*?\$[a-z]?)\.\s([^\\]*).*` => `\songtitle{$1}{$2}` - vanliga låttitlar (utan nyrad på slutet)
* `\\Large\s[\$]\\[\w\/]+?\\[a-z]+?\$\.` - numrerade med specialsymboler
* `\\Large\so\d+?[a-z]?\. ` - omikron
* `\\begin\{flushright\}\n?\s{0,8}\\textit\{(.*)\}\n?\\end\{flushright\}` => `\auth{$1}` - upphovsperson