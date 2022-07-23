#!/usr/bin/env bash
# Needs pdflatex
# Tested on Debian 11 WSL with texlive-base, texlive-latex-extra, texlive-lang-european, texlive-latex-recommended

if [[ $*\  != *--logs\ * ]]; then
    echo -e "\e[34mINFO:\e[0m Loggfiler rensas som standard om inte pdfLaTeX stöter på olösliga problem. Använd flaggan --logs för att spara dem."
fi

# See https://stackoverflow.com/questions/15854559/looping-over-directories-in-bash
for path in *; do
    # if not a directory, skip
    [ -d "${path}" ] || continue

    # We remove some files to get a clean compilation.
    # (&>/dev/null discards any output message)
    rm *.aux &>/dev/null
    rm *.pdf-*.png &>/dev/null

    # Set working directory for proper output placement
    cd "$path"
    echo -e "\e[36mBearbetar mapp:\e[0m $path"

    # Tell LaTeX to look for .sty-files, etc. in the parent folder
    export TEXINPUTS=::$(pwd)/..

    # Compiles all .tex-files in the current directory
    if [[ ! -z `ls *.tex` ]]; then
        for file in *.tex
        do
            echo -e " - \e[35mBearbetar fil:\e[0m $file"
            # First run generates the aux file, then used by the second run (for "sidspalt" generation)
            pdflatex -halt-on-error "$file" &>/dev/null ||  { echo -e "\e[31mFel vid bearbetning av:\e[0m $path/$file. Se loggfilen för mer info." ; exit 1; }
            pdflatex -halt-on-error "$file" &>/dev/null ||  { echo -e "\e[31mFel vid bearbetning av:\e[0m $path/$file. Se loggfilen för mer info." ; exit 1; }
        done;
    fi

    # Optional cleanup (not run on pdflatex error, since the code above will force-exit the script)
    if [[ $*\  != *--logs\ * ]]; then
        rm *.log &>/dev/null
        rm *.aux &>/dev/null
    fi

    # Go back up
    cd ..
done