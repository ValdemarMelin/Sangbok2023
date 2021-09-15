#!/usr/bin/env bash

echo -e "\e[1;36mExtraherar\e[0m originalbilder...";
mkdir cmp/
tar -xJ -C cmp/ -f .github/assets/original.png.txz

AE_TOT=0
FILE_COUNT=0
NF_FILE_COUNT=0

for file in *\ -\ */*.pdf-*.png
do
    echo -e "\e[35mBearbetar fil:\e[0m $file"
    if [ ! -f "cmp/$file" ]; then
        echo -e "  \e[31mFEL:\e[0m Antalet png-filer skiljer sig från originalet."
        NF_FILE_COUNT=$((NF_FILE_COUNT + 1))
        continue
    fi

    AE=$(compare -metric AE "$file" "cmp/$file" "$file.diff.png" &> /dev/stdout)
    echo "  Absolute error: $AE"
    AE_TOT=$((AE_TOT + AE))
    FILE_COUNT=$((FILE_COUNT + 1))
done;
echo "Files checked: $FILE_COUNT"
echo "Files not found in original: $NF_FILE_COUNT"
echo "Total Absolute Error: $AE_TOT"

# if [[ "$NF_FILE_COUNT" -gt 1 ]]; then
#     exit 1
# fi