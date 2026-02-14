#!/bin/bash
# Script to create PDF from HTML using macOS print functionality

HTML_FILE="pages.html"
PDF_FILE="pages.pdf"

# Check if we're on macOS
if [[ "$OSTYPE" == "darwin"* ]]; then
    # Use macOS's built-in print-to-PDF
    echo "Creating PDF using macOS print functionality..."
    
    # Open HTML in default browser and print to PDF
    # Note: This requires manual interaction or automation
    open -a "Safari" "$HTML_FILE" 2>/dev/null || open "$HTML_FILE" 2>/dev/null
    
    echo ""
    echo "To create PDF:"
    echo "1. The HTML file should open in your browser"
    echo "2. Press Cmd+P (or File > Print)"
    echo "3. Click 'Save as PDF'"
    echo "4. Save as: $PDF_FILE"
    echo ""
    echo "Alternatively, if you have wkhtmltopdf installed:"
    echo "  brew install wkhtmltopdf"
    echo "  wkhtmltopdf --page-size A4 --orientation Landscape $HTML_FILE $PDF_FILE"
else
    echo "For non-macOS systems, use:"
    echo "  - wkhtmltopdf: wkhtmltopdf --page-size A4 --orientation Landscape $HTML_FILE $PDF_FILE"
    echo "  - weasyprint: weasyprint $HTML_FILE $PDF_FILE"
    echo "  - Or open in browser and use Print > Save as PDF"
fi



