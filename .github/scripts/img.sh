#!/usr/bin/env bash

# This script compiles all .tex-files in the main directory (that is, not in Äldre/)
for dir in *\ -\ */
do
    echo -e "\e[1;36mBearbetar mapp:\e[0m $dir";
    cd "$dir";

    for file in *.pdf
    do
        echo -e " - \e[35mBearbetar fil:\e[0m $dir$file"
        pdftoppm $file $file -png -r 45
    done;
    cd ..;
done
#echo -e "\e[1;36mKomprimerar\e[0m till png.txz";
#tar -cJvf png.txz **/*.pdf-*.png
#echo -e "\e[1;36mRensar upp\e[0m...";
#rm **/*.pdf-*.png