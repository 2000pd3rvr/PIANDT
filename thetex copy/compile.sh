#!/bin/bash

# Compilation script for thesis
# This script runs pdflatex and bibtex in the correct order

echo "Compiling thesis..."

# First pass
pdflatex -interaction=nonstopmode thesis.tex

# Bibliography
if [ -f thesis.aux ]; then
    bibtex thesis
fi

# Second pass
pdflatex -interaction=nonstopmode thesis.tex

# Third pass (to resolve all references)
pdflatex -interaction=nonstopmode thesis.tex

echo "Compilation complete! Check thesis.pdf"











