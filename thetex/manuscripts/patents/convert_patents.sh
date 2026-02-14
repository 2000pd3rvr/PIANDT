#!/bin/bash
# Convert markdown patent files to PDF via LaTeX using pandoc

cd "$(dirname "$0")"

# Author information matching manuscripts
AUTHOR="A. Akuoko, D. Chitnis, and I. Gyongy"

for md_file in GB_Patent_Application_1_Spatiotemporal_Fusion.md GB_Patent_Application_2_Food_Safety.md; do
    if [ -f "$md_file" ]; then
        base_name="${md_file%.md}"
        tex_file="${base_name}.tex"
        pdf_file="${base_name}.pdf"
        
        echo "Converting $md_file to $tex_file..."
        
        # Extract title from markdown (first line after **TITLE:**)
        TITLE=$(grep -A 1 "^\*\*TITLE:\*\*" "$md_file" | tail -1 | sed 's/^[[:space:]]*//')
        
        # Use pandoc if available, otherwise create manual LaTeX
        if command -v pandoc &> /dev/null; then
            # Convert markdown to LaTeX using pandoc
            pandoc "$md_file" -o "$tex_file" \
                --standalone \
                --from=markdown \
                --to=latex \
                --template=/dev/stdin << 'PANDOC_TEMPLATE'
\documentclass[11pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{geometry}
\geometry{margin=1in}
\usepackage{graphicx}
\usepackage{hyperref}
\usepackage{enumitem}
\usepackage{amsmath}
\usepackage{longtable}
\usepackage{booktabs}
\usepackage{xcolor}

\title{$title$}
\author{$author$}
\date{\today}

\begin{document}
\maketitle
\newpage
$body$
\end{document}
PANDOC_TEMPLATE
            
            # Replace author in generated LaTeX
            sed -i '' "s/\\author{.*}/\\author{$AUTHOR}/" "$tex_file"
            if [ -z "$(grep '\\author' "$tex_file")" ]; then
                # Add author if not present
                sed -i '' "/\\title/a\\
\\author{$AUTHOR}" "$tex_file"
            fi
        else
            # Manual LaTeX generation if pandoc not available
            cat > "$tex_file" << LATEX_HEADER
\\documentclass[11pt,a4paper]{article}
\\usepackage[utf8]{inputenc}
\\usepackage[T1]{fontenc}
\\usepackage{geometry}
\\geometry{margin=1in}
\\usepackage{graphicx}
\\usepackage{hyperref}
\\usepackage{enumitem}
\\usepackage{amsmath}
\\usepackage{longtable}
\\usepackage{booktabs}
\\usepackage{xcolor}

\\title{$TITLE}
\\author{$AUTHOR}
\\date{\\today}

\\begin{document}
\\maketitle
\\newpage

LATEX_HEADER
            
            # Convert markdown to LaTeX manually
            sed -E '
                s/^# (.+)$/\\section{\1}/
                s/^## (.+)$/\\subsection{\1}/
                s/^### (.+)$/\\subsubsection{\1}/
                s/^#### (.+)$/\\paragraph{\1}/
                s/\*\*(.+?)\*\*/\\textbf{\1}/g
                s/`([^`]+)`/\\texttt{\1}/g
                s/^---$/\\hrule/
                s/^(\*\*)([^*]+)(\*\*)$/\\textbf{\2}/
                s/μ/\\$\\mu\$/g
                s/σ/\\$\\sigma\$/g
                s/Σ/\\$\\sum\$/g
                s/√/\\$\\sqrt\$/g
                s/π/\\$\\pi\$/g
                s/²/\\$^2\$/g
                s/×/\\$\\times\$/g
            ' "$md_file" | grep -v "^\*\*TITLE:\*\*" | grep -v "^\*\*APPLICANT:\*\*" | grep -v "^\*\*INVENTOR:\*\*" | grep -v "^\*\*PRIORITY DATE:\*\*" | grep -v "^\[Address" | grep -v "^\[Date" >> "$tex_file"
            
            echo '\end{document}' >> "$tex_file"
        fi
        
        # Compile to PDF
        echo "Compiling $tex_file to PDF..."
        pdflatex -interaction=nonstopmode -output-directory="$(dirname "$tex_file")" "$tex_file" > /dev/null 2>&1
        pdflatex -interaction=nonstopmode -output-directory="$(dirname "$tex_file")" "$tex_file" > /dev/null 2>&1
        
        if [ -f "$pdf_file" ]; then
            echo "✓ Created $pdf_file"
        else
            echo "✗ Failed to create PDF for $md_file"
        fi
    fi
done

echo ""
echo "All patent applications processed."
