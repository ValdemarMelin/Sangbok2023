#!/usr/bin/env bash

# This file cleans up a bunch of files that are ignored by .gitignore.

echo -e "\e[1;36mRensar upp\e[0m...";

echo -e " - \e[1;34mJämförelsebilder\e[0m";
rm **/*.pdf-*.png

echo -e " - \e[1;34mLoggfiler\e[0m";
rm **/*.aux
rm **/*.log