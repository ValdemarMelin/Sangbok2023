#!/usr/bin/env bash

export TEXINPUTS=::$(pwd)

# This script compiles all .tex-files in the main directory (that is, not in Äldre/)
for dir in *\ -\ */
do
    echo -e "\e[1;36mBearbetar mapp:\e[0m $dir";
    cd "$dir";

    for file in *.tex
    do
        echo -e " - \e[35mBearbetar fil:\e[0m $dir$file"
        pdflatex -halt-on-error "$file" ||  { echo -e "\e[31mFel vid bearbetning av:\e[0m $dir/$file" ; exit 1; }
    done;
    cd ..;
done