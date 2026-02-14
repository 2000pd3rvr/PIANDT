#!/bin/bash

# Quick compilation script for thesis (2 passes only, for faster iteration)
# Use this during editing when you don't need perfect reference resolution
# For final compilation, use compile.sh (3 passes)

echo "Quick compiling thesis (2 passes)..."

# First pass
pdflatex -interaction=nonstopmode thesis.tex > /dev/null 2>&1

# Bibliography (only if aux file exists and is new)
if [ -f thesis.aux ]; then
    bibtex thesis > /dev/null 2>&1
fi

# Second pass
pdflatex -interaction=nonstopmode thesis.tex > /dev/null 2>&1

echo "Quick compilation complete! Check thesis.pdf"
echo "Note: For final version, use compile.sh for full 3-pass compilation"

