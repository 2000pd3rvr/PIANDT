# Thesis LaTeX Project

This is the LaTeX source for my thesis.

## Structure

- `thesis.tex` - Main LaTeX document
- `references.bib` - Bibliography file
- `samples/` - Sample PDFs and figures

## Compilation

To compile the thesis to PDF:

```bash
pdflatex thesis.tex
bibtex thesis
pdflatex thesis.tex
pdflatex thesis.tex
```

Or use the compile script:

```bash
./compile.sh
```

## Requirements

- MacTeX (installed)
- LaTeX packages as specified in `thesis.tex`

## Notes

- Update the title, author, and abstract in `thesis.tex`
- Add references to `references.bib`
- Add figures to appropriate directories
- Compile multiple times to resolve all cross-references











