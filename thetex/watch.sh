#!/bin/bash

# File watcher script for automatic compilation
# Requires fswatch (install with: brew install fswatch)

cd "$(dirname "$0")"
export PATH="/Library/TeX/texbin:$PATH"

echo "Watching thesis.tex for changes..."
echo "Press Ctrl+C to stop"
echo ""

# Watch thesis.tex and compile on change
fswatch -o thesis.tex | while read f; do
    echo "File changed, compiling..."
    pdflatex -interaction=nonstopmode thesis.tex > /dev/null 2>&1
    echo "Compilation complete at $(date +%H:%M:%S)"
done











