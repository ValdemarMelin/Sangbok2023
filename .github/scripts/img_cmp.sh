#!/usr/bin/env bash

echo -e "\e[1;36mExtraherar\e[0m originalbilder...";
mkdir -p cmp/
tar -xJ -C cmp/ -f .github/assets/original.90c.txz

# Remove old diff files.
rm **/*.pdf-*diff.png

AE_TOT=0
FILE_COUNT=0
NF_FILE_COUNT=0
NE_FILE_COUNT=0

for file in *\ -\ */*.pdf-*.png
do
    if [ ! -f "cmp/$file" ]; then
        echo -e "  \e[31mFEL:\e[0m Antalet png-filer skiljer sig från originalet."
        NF_FILE_COUNT=$((NF_FILE_COUNT + 1))
        continue
    fi

    AE=$(compare -metric AE "$file" "cmp/$file" "$file.diff.png" &> /dev/stdout)
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

if [[ "$NF_FILE_COUNT" -gt 1 ]]; then
    exit 1
fi