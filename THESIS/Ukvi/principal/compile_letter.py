#!/usr/bin/env python3
"""
Compile LaTeX letter to PDF
"""
import subprocess
import sys
from pathlib import Path

def compile_latex(tex_file):
    """Compile LaTeX file to PDF."""
    tex_path = Path(tex_file)
    if not tex_path.exists():
        print(f"Error: {tex_file} not found")
        return False
    
    # Change to the directory containing the tex file
    work_dir = tex_path.parent
    tex_name = tex_path.name
    
    try:
        # Run pdflatex twice to resolve references
        for i in range(2):
            result = subprocess.run(
                ['pdflatex', '-interaction=nonstopmode', tex_name],
                cwd=work_dir,
                capture_output=True,
                text=True
            )
            if result.returncode != 0:
                print(f"Error compiling LaTeX (run {i+1}):")
                print(result.stdout)
                print(result.stderr)
                return False
        
        # Clean up auxiliary files
        aux_files = ['.aux', '.log', '.out']
        for ext in aux_files:
            aux_file = tex_path.with_suffix(ext)
            if aux_file.exists():
                aux_file.unlink()
        
        pdf_file = tex_path.with_suffix('.pdf')
        if pdf_file.exists():
            print(f"✅ PDF created successfully: {pdf_file}")
            return True
        else:
            print("Error: PDF file was not created")
            return False
            
    except FileNotFoundError:
        print("Error: pdflatex not found. Please install a LaTeX distribution (e.g., MacTeX, TeX Live)")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == '__main__':
    tex_file = 'Request_Recommendation_Letter_Principal.tex'
    if len(sys.argv) > 1:
        tex_file = sys.argv[1]
    
    success = compile_latex(tex_file)
    sys.exit(0 if success else 1)

