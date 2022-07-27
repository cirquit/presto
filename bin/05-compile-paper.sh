#!/bin/bash

bold=$(tput bold)
normal=$(tput sgr0)

echo "${bold}5. Compiling the final paper${normal}"
echo "Downloading a Latex Docker image..."
cd ../paper

if [ ! -f latexdockercmd.sh ]; then
  wget -q --show-progress https://raw.githubusercontent.com/blang/latex-docker/master/latexdockercmd.sh
  chmod +x latexdockercmd.sh
fi
./latexdockercmd.sh /bin/sh -c "pdflatex -shell-escape --interaction=batchmode main 2>&1 > /dev/null && bibtex main && bibtex main"
./latexdockercmd.sh /bin/sh -c "pdflatex -shell-escape --interaction=batchmode main 2>&1 > /dev/null && pdflatex -shell-escape --interaction=batchmode main 2>&1"
make clean
echo "Paper should be saved at:${bold} $PRESTO_PATH/paper/main.pdf ${normal}"
echo "${bold}-- Finished compiling paper!${normal}"
