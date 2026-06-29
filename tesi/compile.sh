#!/bin/sh
set -e
cd "$(dirname "$0")"

pdflatex tesi.tex
biber tesi
pdflatex tesi.tex
pdflatex tesi.tex
