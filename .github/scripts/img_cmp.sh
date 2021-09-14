#!/usr/bin/env bash

echo -e "\e[1;36mExtraherar\e[0m originalbilder...";
mkdir cmp/
tar -xJ -C cmp/ -f .github/assets/original.png.txz

AE_TOT=0
FILE_COUNT=0

for file in *\ -\ */*.pdf-*.png
do
    echo -e " - \e[35mBearbetar fil:\e[0m $file"
    compare -metric AE "$file" "cmp/$file" diff.png
    AE=$(compare -metric AE "$file" "cmp/$file" diff.png || echo 0)
    echo "AE: "$AE
    AE_TOT=$((AE_TOT + AE))
    FILE_COUNT=$((FILE_COUNT + 1))
done;
echo "Files checked: "$FILE_COUNT
echo "Total Absolute Error: "$AE_TOT
