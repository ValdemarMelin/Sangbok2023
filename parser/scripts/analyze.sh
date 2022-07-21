#!/usr/bin/env bash
# Needs: compare (imagemagick), pdftoppm (poppler-tools), pdflatex (texlive-latex-recommended & texlive-latex-extra)

export TEXINPUTS=::$(pwd)/..

# We remove some files to get a clean compilation.
rm *.aux
rm *.pdf-*.png


# This script compiles all .tex-files in the current directory
for file in *.tex
do
    echo -e " - \e[35mBearbetar fil:\e[0m $dir$file"
    # First run generates the aux file, then used by the second run.
    pdflatex -halt-on-error "$file" ||  { echo -e "\e[31mFel vid bearbetning av:\e[0m $dir/$file" ; exit 1; }
    pdflatex -halt-on-error "$file" ||  { echo -e "\e[31mFel vid bearbetning av:\e[0m $dir/$file" ; exit 1; }
done;

# This script compiles all pdf files current directory to png
for file in *.pdf
do
    echo -e " - \e[35mBearbetar fil:\e[0m $dir$file"
    pdftoppm $file $file -png -r 90
done;

#!/usr/bin/env bash

echo -e "\e[1;36mExtraherar\e[0m originalbilder...";
mkdir -p ../cmp/
tar -xJ -C ../cmp/ -f ../.github/assets/original.90c.txz

AE_TOT=0
FILE_COUNT=0
NF_FILE_COUNT=0
NE_FILE_COUNT=0

for file in *.pdf-*.png
do
    if [ ! -f "../cmp/${PWD##*/}/$file" ]; then
        echo -e "  \e[31mFEL:\e[0m Antalet png-filer skiljer sig från originalet. ../cmp/${PWD##*/}/$file"
        NF_FILE_COUNT=$((NF_FILE_COUNT + 1))
        continue
    fi

    AE=$(compare -metric AE "$file" "../cmp/${PWD##*/}/$file" "$file.diff.png" &> /dev/stdout)
    AE_TOT=$((AE_TOT + AE))
    FILE_COUNT=$((FILE_COUNT + 1))

    if [[ "$AE" -gt 0 ]]; then
        NE_FILE_COUNT=$((NE_FILE_COUNT + 1))
        echo -e "\e[35mFil:\e[0m $file "
        if [[ "$AE" -gt 20000 ]]; then
            echo -e "  Absolut fel: \e[31m$AE\e[0m"
        else
            echo "  Absolut fel: $AE"
        fi
    else
        rm "$file.diff.png"
    fi

done;

echo "Files checked: $FILE_COUNT"
echo "Files not found in original: $NF_FILE_COUNT"
echo "Files not matching: $NE_FILE_COUNT"
echo "Total Absolute Error: $AE_TOT"