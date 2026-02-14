#!/bin/bash

# Auto-compile script using latexmk
# This will continuously watch thesis.tex and recompile when it changes

cd "$(dirname "$0")"
export PATH="/Library/TeX/texbin:$PATH"

echo "Starting auto-compilation of thesis.tex"
echo "Press Ctrl+C to stop"
echo ""

# Use latexmk in continuous preview mode
latexmk -pdf -pvc -interaction=nonstopmode thesis.tex











