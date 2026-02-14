#!/usr/bin/env python3
"""
Convert markdown patent files to LaTeX and compile to PDF
"""

import re
import subprocess
import sys
from pathlib import Path

AUTHOR = "A. Akuoko, D. Chitnis, and I. Gyongy"

def markdown_to_latex(md_content):
    """Convert markdown content to LaTeX"""
    lines = md_content.split('\n')
    result = []
    skip_until_abstract = True
    
    for i, line in enumerate(lines):
        # Skip the metadata section until we reach ABSTRACT
        if skip_until_abstract:
            if line.strip().startswith('## ABSTRACT'):
                skip_until_abstract = False
            elif line.strip().startswith('**TITLE:**'):
                # Skip TITLE line but extract title
                continue
            else:
                continue
        
        # Skip other metadata lines
        if any(pattern in line for pattern in [
            '**TITLE:**', '**APPLICANT:**', '**INVENTOR:**', 
            '**PRIORITY DATE:**', '[Address', '[Date',
            'UK PATENT APPLICATION', 'GB Patent Application No'
        ]):
            continue
        
        # Skip duplicate title/author lines that appear between horizontal rules
        if i > 0 and i < len(lines) - 1:
            prev_line = lines[i-1].strip() if i > 0 else ""
            next_line = lines[i+1].strip() if i+1 < len(lines) else ""
            # Skip lines that are between horizontal rules and look like duplicates
            if prev_line == "---" and next_line == "---":
                # Check if this looks like a title or author (long line or contains "Akuoko")
                if len(line.strip()) > 50 or "Akuoko" in line:
                    continue
        
        result.append(line)
    
    latex = '\n'.join(result)
    
    # Extract title from original content
    title_match = re.search(r'^\*\*TITLE:\*\*\s*\n(.+?)\n', md_content, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else "UK Patent Application"
    
    # Headers
    latex = re.sub(r'^## (.+)$', r'\\subsection{\1}', latex, flags=re.MULTILINE)
    latex = re.sub(r'^### (.+)$', r'\\subsubsection{\1}', latex, flags=re.MULTILINE)
    latex = re.sub(r'^#### (.+)$', r'\\paragraph{\1}', latex, flags=re.MULTILINE)
    
    # Bold text
    latex = re.sub(r'\*\*([^*]+)\*\*', r'\\textbf{\1}', latex)
    
    # Code/inline code
    latex = re.sub(r'`([^`]+)`', r'\\texttt{\1}', latex)
    
    # Handle special placeholder for Figure 1.1 TikZ
    latex = latex.replace('[FIGURE_1_1_TIKZ]', '\\TIKZ_FIGURE_1_1_HERE')
    
    # Images - handle markdown image syntax ![alt](path) - but skip 1.1.png
    def replace_image(match):
        alt_text = match.group(1)
        img_path = match.group(2)
        # Skip 1.1.png - it will be replaced with TikZ
        if '1.1' in img_path or '1_1' in img_path:
            return '\\TIKZ_FIGURE_1_1_HERE'
        # Adjust path if it's relative
        if img_path.startswith('../'):
            img_path = img_path.replace('../figures/', '../../figures/')
        elif img_path.startswith('figures/'):
            img_path = img_path.replace('figures/', '../../figures/')
        return f'\\begin{{figure}}[H]\n\\centering\n\\includegraphics[width=0.8\\textwidth]{{{img_path}}}\n\\caption{{{alt_text}}}\n\\end{{figure}}'
    
    latex = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', replace_image, latex)
    
    # Horizontal rules - convert to proper spacing
    latex = re.sub(r'^---\s*$', r'\\vspace{0.5em}', latex, flags=re.MULTILINE)
    
    # Fix math equations - handle the per-bin Gaussian mixture model properly
    latex = re.sub(
        r'μ_i = Σ\(m=1 to M\) \[S_m / √\(2πσ_m²\)\] × exp\(-\(t_i - t_\{0,m\}\)² / \(2σ_m²\)\) \+ b',
        r'$\\mu_i = \\sum_{m=1}^{M} \\frac{S_m}{\\sqrt{2\\pi\\sigma_m^2}} \\exp\\left(-\\frac{(t_i - t_{0,m})^2}{2\\sigma_m^2}\\right) + b$',
        latex
    )
    
    # Fix other math symbols
    latex = latex.replace('μ', '$\\mu$')
    latex = latex.replace('σ', '$\\sigma$')
    latex = latex.replace('Σ', '$\\sum$')
    latex = latex.replace('√', '$\\sqrt$')
    latex = latex.replace('π', '$\\pi$')
    latex = latex.replace('²', '$^2$')
    latex = latex.replace('×', '$\\times$')
    
    # Fix inline math that's broken
    latex = re.sub(r'\$([^$]+)\$_([a-z0-9]+)', r'$\1_{\2}$', latex)
    latex = re.sub(r'\$([^$]+)\$\^([0-9]+)', r'$\1^{\2}$', latex)
    
    # Handle lists - need to handle nested structure (a) with - subitems)
    lines = latex.split('\n')
    result = []
    in_enumerate = False
    in_itemize = False
    
    for i, line in enumerate(lines):
        # Check for numbered items (a), b), c), etc.)
        enum_match = re.match(r'^([a-z])\)\s+(.+)$', line)
        if enum_match:
            # Close any open itemize
            if in_itemize:
                result.append('\\end{itemize}')
                in_itemize = False
            
            # Start enumerate if not already in one
            if not in_enumerate:
                result.append('\\begin{enumerate}[leftmargin=*,label=\\alph*)]')
                in_enumerate = True
            
            item_text = enum_match.group(2)
            result.append(f'\\item {item_text}')
            continue
        
        # Check for bullet points (sub-items under enum items)
        bullet_match = re.match(r'^\s*-\s+(.+)$', line)
        if bullet_match:
            if not in_itemize:
                result.append('\\begin{itemize}[leftmargin=*]')
                in_itemize = True
            item_text = bullet_match.group(1)
            result.append(f'\\item {item_text}')
            continue
        
        # Regular line - close itemize if open, but keep enumerate open
        if in_itemize:
            result.append('\\end{itemize}')
            in_itemize = False
        
        result.append(line)
    
    # Close any remaining lists
    if in_itemize:
        result.append('\\end{itemize}')
    if in_enumerate:
        result.append('\\end{enumerate}')
    
    latex = '\n'.join(result)
    
    # Remove empty enumerate blocks
    latex = re.sub(r'\\begin\{enumerate\}\[.*?\]\s*\\end\{enumerate\}', '', latex)
    
    # Clean up multiple consecutive blank lines
    latex = re.sub(r'\n{3,}', r'\n\n', latex)
    
    # Remove duplicate title/author lines at the start
    lines = latex.split('\n')
    result = []
    seen_title = False
    seen_author = False
    for line in lines:
        # Skip duplicate title
        if not seen_title and len(line.strip()) > 50 and "System and Method" in line:
            seen_title = True
            continue
        # Skip duplicate author
        if not seen_author and "Akuoko" in line and "Chitnis" in line:
            if seen_author:
                continue
            seen_author = True
        result.append(line)
    latex = '\n'.join(result)
    
    # Check if figure 1.1 should be included
    include_fig1 = '\\TIKZ_FIGURE_1_1_HERE' in latex or 'Figure 1' in latex or 'Figure 1:' in latex
    
    return title, latex, include_fig1

def create_latex_file(md_file, output_tex):
    """Create LaTeX file from markdown"""
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    title, latex_body, include_fig1 = markdown_to_latex(md_content)
    
    # TikZ code for Figure 1.1
    tikz_figure_one = """\\begin{figure}[H]
\\centering
\\resizebox{0.56\\textwidth}{!}{%
\\begin{tikzpicture}[
    node distance=2.2cm, 
    auto,
    every node/.style={font=\\scriptsize},
    main node/.style={rectangle, draw=black!60, fill=gray!10, text width=2.5cm, align=center, minimum height=0.9cm, rounded corners=3pt, line width=0.8pt, font=\\scriptsize},
    item node/.style={rectangle, draw=black!60, fill=gray!10, text width=1.8cm, align=center, minimum height=0.9cm, rounded corners=3pt, line width=0.8pt, font=\\scriptsize},
    process node/.style={rectangle, draw=black!60, fill=gray!10, text width=2.2cm, align=center, minimum height=0.7cm, rounded corners=3pt, line width=0.8pt, font=\\scriptsize}
]
    % Define nodes vertically
    \\node[main node] (scene) {Observed scene};
    \\node[main node, below of=scene] (signal) {Measured signal};
    \\node[main node, below of=signal] (pawd) {PAWD framework};
    
    % Draw arrows vertically with gaps (not touching boxes)
    \\draw[->, line width=1.2pt, color=black!70] ([yshift=-0.3cm]scene.south) -- ([yshift=0.3cm]signal.north);
    \\draw[->, line width=1.2pt, color=black!70] ([yshift=-0.3cm]signal.south) -- ([yshift=0.3cm]pawd.north);
    
    % Short vertical line from PAWD framework
    \\draw[line width=0.8pt, color=black!60] (pawd.south) -- ++(0,-0.5cm) coordinate (pawd_bottom);
    
    % Horizontal line spanning 4 items
    \\draw[line width=0.8pt, color=black!60] ([xshift=-3.5cm, yshift=0cm]pawd_bottom) -- ([xshift=3.5cm, yshift=0cm]pawd_bottom);
    
    % Four items arranged horizontally
    \\node[item node, below of=pawd_bottom, xshift=-3.5cm, yshift=1.0cm] (item1) {Intensity\\\\spectral};
    \\node[item node, below of=pawd_bottom, xshift=-1.2cm, yshift=1.0cm] (item2) {Intensity\\\\non-spectral};
    \\node[item node, below of=pawd_bottom, xshift=1.2cm, yshift=1.0cm] (item3) {Temporal\\\\spectral};
    \\node[item node, below of=pawd_bottom, xshift=3.5cm, yshift=1.0cm] (item4) {Temporal\\\\non-spectral};
    
    % Short vertical lines from horizontal line to each item
    \\draw[line width=0.8pt, color=black!60] ([xshift=-3.5cm, yshift=0cm]pawd_bottom) -- ++(0,-0.4cm);
    \\draw[line width=0.8pt, color=black!60] ([xshift=-1.2cm, yshift=0cm]pawd_bottom) -- ++(0,-0.4cm);
    \\draw[line width=0.8pt, color=black!60] ([xshift=1.2cm, yshift=0cm]pawd_bottom) -- ++(0,-0.4cm);
    \\draw[line width=0.8pt, color=black!60] ([xshift=3.5cm, yshift=0cm]pawd_bottom) -- ++(0,-0.4cm);
    
    % Second horizontal line below the 4 items
    \\coordinate (items_bottom) at ([yshift=-1.0cm]item2.south);
    
    % Four vertical lines pointing upward
    \\draw[line width=0.8pt, color=black!60] ([xshift=-2.4cm, yshift=0.8cm]items_bottom) -- ++(0,-0.7cm);
    \\draw[line width=0.8pt, color=black!60] ([xshift=-0.1cm, yshift=0.8cm]items_bottom) -- ++(0,-0.7cm);
    \\draw[line width=0.8pt, color=black!60] ([xshift=2.2cm, yshift=0.8cm]items_bottom) -- ++(0,-0.7cm);
    \\draw[line width=0.8pt, color=black!60] ([xshift=4.5cm, yshift=0.8cm]items_bottom) -- ++(0,-0.7cm);
    
    % Horizontal lines below items (just below the bottom vertical lines)
    % First horizontal line connecting the first 2 bottom vertical lines
    \\draw[line width=0.8pt, color=black!60] ([xshift=-2.4cm, yshift=0.1cm]items_bottom) -- ([xshift=-0.1cm, yshift=0.1cm]items_bottom);
    % Second horizontal line connecting the 3rd and 4th bottom vertical lines
    \\draw[line width=0.8pt, color=black!60] ([xshift=2.2cm, yshift=0.1cm]items_bottom) -- ([xshift=4.5cm, yshift=0.1cm]items_bottom);
    
    % Items under first bottom horizontal line (spatial)
    \\node[process node, below of=items_bottom, xshift=-1.25cm, yshift=-0.7cm] (spatial_features) {Spatial features};
    \\node[process node, below of=spatial_features] (spatial_pattern) {Spatial pattern\\\\processing};
    \\node[process node, below of=spatial_pattern] (spatial_decisions) {Spatial decisions};
    
    % Arrow from horizontal line to spatial features (matching gap between items)
    \\draw[->, line width=1.2pt, color=black!70] ([xshift=-1.25cm, yshift=-0.2cm]items_bottom) -- ([yshift=0.3cm]spatial_features.north);
    % Arrows for spatial flow
    \\draw[->, line width=1.2pt, color=black!70] ([yshift=-0.3cm]spatial_features.south) -- ([yshift=0.3cm]spatial_pattern.north);
    \\draw[->, line width=1.2pt, color=black!70] ([yshift=-0.3cm]spatial_pattern.south) -- ([yshift=0.3cm]spatial_decisions.north);
    
    % Items under second bottom horizontal line (structural)
    \\node[process node, below of=items_bottom, xshift=3.35cm, yshift=-0.7cm] (structural_features) {Structural features};
    \\node[process node, below of=structural_features] (structural_pattern) {Structural pattern\\\\processing};
    \\node[process node, below of=structural_pattern] (structural_decisions) {Structural decisions};
    
    % Arrow from horizontal line to structural features (matching gap between items)
    \\draw[->, line width=1.2pt, color=black!70] ([xshift=3.35cm, yshift=-0.2cm]items_bottom) -- ([yshift=0.3cm]structural_features.north);
    % Arrows for structural flow
    \\draw[->, line width=1.2pt, color=black!70] ([yshift=-0.3cm]structural_features.south) -- ([yshift=0.3cm]structural_pattern.north);
    \\draw[->, line width=1.2pt, color=black!70] ([yshift=-0.3cm]structural_pattern.south) -- ([yshift=0.3cm]structural_decisions.north);
    
    % Connect the last two items (spatial decisions and structural decisions)
    % Two vertical lines going up from each decision box
    \\draw[line width=0.8pt, color=black!60] ([yshift=-0.3cm]spatial_decisions.south) -- ++(0,-0.5cm) coordinate (spatial_decisions_bottom);
    \\draw[line width=0.8pt, color=black!60] ([yshift=-0.3cm]structural_decisions.south) -- ++(0,-0.5cm) coordinate (structural_decisions_bottom);
    
    % Horizontal line connecting the two vertical lines
    \\draw[line width=0.8pt, color=black!60] (spatial_decisions_bottom) -- (structural_decisions_bottom);
    
    % Vertical line from centre of horizontal line (single continuous line, 0.5cm like first vertical line)
    % Create coordinate at midpoint: spatial at x=-1.25cm, structural at x=3.35cm, midpoint at x=1.05cm
    \\path (spatial_decisions_bottom) -- (structural_decisions_bottom) coordinate[midway] (horizontal_mid);
    \\draw[line width=0.8pt, color=black!60] (horizontal_mid) -- ++(0,-0.5cm) coordinate (spatiotemporal_top);
    
    % Spatiotemporal decision item (positioned below the vertical line)
    \\node[process node, below of=spatiotemporal_top, yshift=0.2cm] (spatiotemporal_decision) {Spatiotemporal decision};
    
    % Arrow from vertical line to spatiotemporal decision (single continuous arrow)
    \\draw[->, line width=1.2pt, color=black!70] (spatiotemporal_top) -- (spatiotemporal_decision.north);
\\end{tikzpicture}
}
\\caption[Flow chart showing the processing pipeline from observed scene through measured signal to the PAWD framework.]{Flow chart showing the processing pipeline from observed scene through measured signal to the PAWD framework. Intensity measured signal is often spatially resolved to represent scenes. Nevertheless, time resolved signal may also be spatially resolved. This is termed space resolved temporal measurements (SRTM). SRTM are not useful for structural decisions. However, they may play key roles in spatial decisions like pose estimation, scale estimation and others. A true spatiotemporal solution is one that combines the crude time resolved signal with intensity resolved signal for decision making.}
\\label{fig:1_1}
\\end{figure}"""
    
    # Replace placeholder or broken PNG figure with TikZ
    if include_fig1:
        # Replace placeholder
        latex_body = latex_body.replace('\\TIKZ_FIGURE_1_1_HERE', tikz_figure_one)
        # Also replace any broken includegraphics figure - use string replace to avoid regex issues
        # Find the pattern manually
        pattern_start = '\\begin{figure}[H]'
        pattern_end = '\\end{figure}'
        start_idx = latex_body.find(pattern_start)
        if start_idx != -1:
            # Check if this figure contains 1.1.png
            end_idx = latex_body.find(pattern_end, start_idx)
            if end_idx != -1:
                figure_block = latex_body[start_idx:end_idx + len(pattern_end)]
                if '1.1.png' in figure_block or '1_1.png' in figure_block:
                    latex_body = latex_body.replace(figure_block, tikz_figure_one)
    else:
        # Remove placeholder if not needed
        latex_body = latex_body.replace('\\TIKZ_FIGURE_1_1_HERE', '')
    
    latex_doc = f"""\\documentclass[11pt,a4paper]{{article}}
\\usepackage[utf8]{{inputenc}}
\\usepackage[T1]{{fontenc}}
\\usepackage[margin=1in,top=1.2in,bottom=1.2in]{{geometry}}
\\usepackage{{microtype}}
\\usepackage{{graphicx}}
\\usepackage{{hyperref}}
\\usepackage{{enumitem}}
\\usepackage{{amsmath}}
\\usepackage{{amsfonts}}
\\usepackage{{amssymb}}
\\usepackage{{longtable}}
\\usepackage{{booktabs}}
\\usepackage{{xcolor}}
\\usepackage{{parskip}}
\\usepackage{{float}}
\\usepackage{{tikz}}
\\usetikzlibrary{{positioning, arrows.meta}}

% Better line breaking
\\sloppy
\\emergencystretch=3em
\\hyphenpenalty=1000
\\tolerance=1000

% Title formatting - handle long titles
\\makeatletter
\\renewcommand{{\\@maketitle}}{{
  \\begin{{center}}
  {{\\Large \\bfseries \\begin{{minipage}}{{0.9\\textwidth}} \\centering \\@title \\end{{minipage}} \\par}}
  \\vspace{{1em}}
  {{\\large \\@author \\par}}
  \\vspace{{0.5em}}
  {{\\normalsize \\@date \\par}}
  \\end{{center}}
  \\vspace{{1em}}
}}
\\makeatother

\\title{{{title}}}
\\author{{{AUTHOR}}}
\\date{{\\today}}

\\begin{{document}}
\\maketitle
\\newpage

{latex_body}

\\end{{document}}
"""
    
    with open(output_tex, 'w', encoding='utf-8') as f:
        f.write(latex_doc)
    
    return title

def compile_latex(tex_file):
    """Compile LaTeX to PDF"""
    base_name = Path(tex_file).stem
    output_dir = Path(tex_file).parent
    
    try:
        subprocess.run(
            ['pdflatex', '-interaction=nonstopmode', f'-output-directory={output_dir}', str(tex_file)],
            capture_output=True,
            check=False
        )
        subprocess.run(
            ['pdflatex', '-interaction=nonstopmode', f'-output-directory={output_dir}', str(tex_file)],
            capture_output=True,
            check=False
        )
        pdf_file = output_dir / f'{base_name}.pdf'
        return pdf_file.exists()
    except Exception as e:
        print(f"Error compiling {tex_file}: {e}", file=sys.stderr)
        return False

def main():
    """Main conversion function"""
    script_dir = Path(__file__).parent
    
    patent_files = [
        'GB_Patent_Application_1_Spatiotemporal_Fusion.md',
        'GB_Patent_Application_2_Food_Safety.md'
    ]
    
    for md_file in patent_files:
        md_path = script_dir / md_file
        if not md_path.exists():
            print(f"Warning: {md_file} not found, skipping...")
            continue
        
        base_name = md_path.stem
        tex_file = script_dir / f'{base_name}.tex'
        pdf_file = script_dir / f'{base_name}.pdf'
        
        print(f"Converting {md_file} to {tex_file.name}...")
        title = create_latex_file(md_path, tex_file)
        print(f"  Title: {title}")
        
        print(f"Compiling {tex_file.name} to PDF...")
        if compile_latex(tex_file):
            print(f"✓ Created {pdf_file.name}")
        else:
            print(f"✗ Failed to create PDF for {md_file}")
    
    print("\nAll patent applications processed.")

if __name__ == '__main__':
    main()
