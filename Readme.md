# Fysiksektionens sångbok
## Loggbok
Loggboken är [flyttad](Logbook.md).

## Instruktioner för uppdatering av sångboken
(Instruktioner hämtat från gammal (men lite uppdaterad) fil i Fcom:s Drive)

När en ny sångbok skall göras, kopiera hela mappen från föregående år och gör en ny mapp för innevarande år. Gör sedan alla ändringar i den nya mappen. Var försiktig vid ändringar, layouten kan förstöras ganska mycket om det råkar bli en rad för mycket på sidan. Märks tydligast i innehåll och register där sidorna i princip redan är helt fyllda.

### Ändringar som behöver göras för varje år:
 - Sångbokens årtal på första sidan
 - Ny föhsarlogga
 - Ändra i Överföhssången utefter kön på Överföhs
 - Skriv till senaste årskurs i Årskursernas hederssång
 - (Uppdatera introduktionen)

### Struktur
Kapitlen är fördelade i mappar. I varje mapp finns en .tex-fil tillsammans med de bilder som behövs för att kompilera. Kompilera med pdfLatex (se [kompilering](#kompilering) nedan). Rör ej filerna greekcount och sidspaltHack, kontakta Mattias Olla (Frågvis?) om du vill ändra i dessa.

Mappen med kapitlet noter innehåller alla noter som .pdf och .sib. .sib-filerna är filer för notredigering och kräver ett speciellt program, Sibelius.

### Tryckning
När en .pdf-fil för varje kapitel har skapats, lägg alla pdf-filer samlade i en mapp. Totalt ska det vara 18 filer (19 med sigma), om inga kapitel har lags till eller tagits bort. Dessa filer skickas sedan via mail till tryckeriet (US-AB med mailadress <tryck@us-ab.com>). Filerna bör med fördel vara döpta efter vilken ordning de ska komma i och vilken färg de ska ha.

Traditionellt sett har varje kapitel haft en egen sidfärg. Det är dock inte alls nödvändigt utan de räcker med att det inte är samma färg på närliggande kapitel. Det kan vara svårt att läsa text på mörk bakgrund (mörkblå och mörkröd har varit problematiska) så ta endast ljusa färger. Viktigast är att "Visor till Fysiker" är <i>enda kaptlet i orange</i>. Är lite smått populärt att ha en passande färg till kapitlet, "Visor till gasque" i rosa för att matcha fkm*, "Visor till punsch" i ljusgul etc.

Antal som ska tryckas: ungefär två tredjedelar av antalet antagna. (2015 beställdes 80 sångböcker, sålda för 100 kr/st)
Nya tillskott  till sångboken får gärna tryckas upp i större antal så att de som redan har en sångbok kan köpa ett ex och sätta in i sin bok.

## Teknikaliteter
### Kompilering
 - Kompilering sker automatiskt när du pushar. Resultatet finns [här](https://github.com/Fysiksektionen/Sangbok/actions/workflows/compile.yml).
 - Offline-kompilering kräver `pdflatex`.
   - Har du bash bör du kunna köra `./compile.sh` i huvudmappen.
   - Vill du kompilera manuellt, kör `pdflatex [FILE]` i lämplig mapp. Om `pdflatex` inte hittar sty-filerna kan du testa att köra `export TEXINPUTS=::$(pwd)/..` innan du kör `pdflatex`.

### Låtformat
För fler kommandon och variationer på nedanstående, se [stilmallen](digital.sty). För frågor om denna, kontakta [Oskar](https://github.com/oskarr) (Fotnot).
```latex
\begin{center} % Låttitlar ska alltid vara centrerade
    \songtitle{$\upsilon 1$}{Lorem Ipsum} % Index och titel
    \course{SP0001 Elementär Kalasteori} % Kursbeteckning (iota-kapitlet)
    \songsubtitle{(Neque porro quisquam)} % Undertitlar
    \sheetmusicnotice{Noter till blandad kör finns i notkapitlet.} % Information om noter
    \instruction{Starkt är vackert!} % Ytterligare instruktioner
\end{center}
\begin{lyrics}
    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.\\
    Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.\\
    \digitalonly{
    % Extra vers som bara syns i den digitala versionen (använd \physicalonly för att bara visa saker i den fysiska versionen)
        \newline
        Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.\\
        Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
    }
\end{lyrics}
\auth{Originaltext: M.T. Cicero} % Upphovsperson, etc.
```