#!/usr/bin/env python3
"""
Generate PDF from the pages table
"""
import sys
from pathlib import Path

base_dir = Path(__file__).parent

# Try different PDF libraries
try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib import colors
    HAS_REPORTLAB = True
except ImportError:
    HAS_REPORTLAB = False

try:
    from fpdf import FPDF
    HAS_FPDF = True
except ImportError:
    HAS_FPDF = False

# Read the HTML file to get data
html_file = base_dir / 'pages.html'
if not html_file.exists():
    print("Error: pages.html not found. Run extract_content.py first.")
    sys.exit(1)

# Parse HTML to extract table data
import re
from html import unescape

with open(html_file, 'r', encoding='utf-8') as f:
    html_content = f.read()

# Extract table rows
rows = re.findall(r'<tr>\s*<td[^>]*>(.*?)</td>\s*<td[^>]*>(.*?)</td>\s*<td[^>]*>(.*?)</td>\s*</tr>', html_content, re.DOTALL)

pages_data = []
for row in rows:
    url = unescape(re.sub(r'<[^>]+>', '', row[0]).strip())
    desc = unescape(re.sub(r'<[^>]+>', '', row[1]).strip())
    pages_data.append((url, desc))

if HAS_REPORTLAB:
    # Generate PDF using reportlab
    pdf_file = base_dir / 'pages.pdf'
    doc = SimpleDocTemplate(str(pdf_file), pagesize=letter)
    elements = []
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.HexColor('#1a1a1a'),
        alignment=1,  # Center
        spaceAfter=30
    )
    
    # Title
    elements.append(Paragraph("PIANDT Website Pages", title_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Create table data
    table_data = [['1. Page URL', '2. Page Description', '3. Page Content']]
    
    for url, desc in pages_data:
        # Truncate description if too long
        if len(desc) > 200:
            desc = desc[:200] + "..."
        table_data.append([url, desc, ''])
    
    # Create table
    table = Table(table_data, colWidths=[2*inch, 3.5*inch, 1.5*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a1a1a')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
    ]))
    
    elements.append(table)
    doc.build(elements)
    print(f"Generated PDF file: {pdf_file}")
    
elif HAS_FPDF:
    # Generate PDF using fpdf
    pdf_file = base_dir / 'pages.pdf'
    pdf = FPDF(orientation='L', unit='mm', format='A4')  # Landscape for wider table
    
    for url, desc in pages_data:
        pdf.add_page()
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, 'PIANDT Website Pages', 0, 1, 'C')
        pdf.ln(5)
        
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(60, 8, 'Page URL', 1, 0, 'C')
        pdf.cell(100, 8, 'Page Description', 1, 0, 'C')
        pdf.cell(30, 8, 'Page Content', 1, 1, 'C')
        
        pdf.set_font('Arial', '', 8)
        # Truncate if too long
        if len(desc) > 150:
            desc = desc[:150] + "..."
        pdf.cell(60, 8, url[:40] + '...' if len(url) > 40 else url, 1, 0)
        pdf.cell(100, 8, desc, 1, 0)
        pdf.cell(30, 8, '', 1, 1)
    
    pdf.output(str(pdf_file))
    print(f"Generated PDF file: {pdf_file}")
    
else:
    print("No PDF library available (reportlab or fpdf).")
    print("To generate PDF, you can:")
    print("1. Install reportlab: pip3 install reportlab")
    print("2. Or open pages.html in a browser and use Print > Save as PDF")
    print("3. Or use: pip3 install fpdf2")
    sys.exit(1)



