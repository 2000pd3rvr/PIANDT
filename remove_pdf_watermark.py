#!/usr/bin/env python3
"""
Remove watermarks from PDF files.

This script attempts to remove watermarks from PDF files using various methods:
1. Removing text annotations
2. Removing image overlays
3. Removing form XObjects that might contain watermarks
4. Removing optional content groups (layers)
5. Advanced: Removing watermarks from content stream using PyMuPDF

Usage:
    python3 remove_pdf_watermark.py input.pdf output.pdf
"""

import sys
import re
from pathlib import Path

def remove_watermark_pypdf(input_path, output_path):
    """Remove watermark using pypdf library with content stream editing."""
    try:
        from pypdf import PdfReader, PdfWriter
        import io
    except ImportError:
        print("Error: pypdf library not found.")
        print("Install it with: pip3 install pypdf")
        return False
    
    try:
        reader = PdfReader(input_path)
        writer = PdfWriter()
        
        watermark_text = "This is not an official statement"
        watermark_variations = [
            watermark_text,
            watermark_text.lower(),
            watermark_text.upper(),
            watermark_text + ".",
            watermark_text.lower() + ".",
        ]
        
        print(f"Processing {len(reader.pages)} pages...")
        
        for page_num, page in enumerate(reader.pages, 1):
            print(f"  Processing page {page_num}...")
            
            # Remove annotations
            if '/Annots' in page:
                page.pop('/Annots')
            
            # Remove optional content groups
            if '/OCProperties' in page:
                page.pop('/OCProperties')
            
            # Try to filter content stream (advanced - may not work for all PDFs)
            # This is complex and may not preserve structure perfectly either
            # For now, just remove annotations and let PyMuPDF handle content stream
            
            writer.add_page(page)
        
        # Write output
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
        
        print(f"✓ Successfully created: {output_path}")
        return True
        
    except Exception as e:
        print(f"Error processing PDF: {e}")
        return False

def remove_watermark_pypdf2(input_path, output_path):
    """Remove watermark using PyPDF2 library (alternative)."""
    try:
        import PyPDF2
    except ImportError:
        print("Error: PyPDF2 library not found.")
        print("Install it with: pip3 install PyPDF2")
        return False
    
    try:
        with open(input_path, 'rb') as input_file:
            reader = PyPDF2.PdfReader(input_file)
            writer = PyPDF2.PdfWriter()
            
            print(f"Processing {len(reader.pages)} pages...")
            
            for page_num, page in enumerate(reader.pages, 1):
                print(f"  Processing page {page_num}...")
                
                # Remove annotations
                if '/Annots' in page:
                    if hasattr(page, 'get'):
                        page[PyPDF2.generic.NameObject('/Annots')] = PyPDF2.generic.ArrayObject()
                
                writer.add_page(page)
            
            with open(output_path, 'wb') as output_file:
                writer.write(output_file)
        
        print(f"✓ Successfully created: {output_path}")
        return True
        
    except Exception as e:
        print(f"Error processing PDF: {e}")
        return False

def remove_watermark_pymupdf(input_path, output_path):
    """Advanced watermark removal using PyMuPDF (fitz) - most powerful method."""
    try:
        import fitz  # PyMuPDF
    except ImportError:
        print("Error: PyMuPDF library not found.")
        print("Install it with: pip3 install PyMuPDF")
        return False
    
    try:
        doc = fitz.open(input_path)
        print(f"Processing {len(doc)} pages...")
        
        # Target only the specific watermark text
        watermark_text = "This is not an official statement"
        watermark_texts = {watermark_text}
        
        # Also check for variations (case-insensitive, with/without period)
        watermark_variations = [
            watermark_text,
            watermark_text.lower(),
            watermark_text.upper(),
            watermark_text.capitalize(),
            watermark_text + ".",
            watermark_text.lower() + ".",
            "This is not an official stateme",  # Partial (in case of truncation)
        ]
        
        print(f"  Targeting watermark text: '{watermark_text}'")
        print(f"  Checking for {len(watermark_variations)} variations")
        
        # Process each page
        for page_num in range(len(doc)):
            page = doc[page_num]
            print(f"  Processing page {page_num + 1}...")
            
            # Method 1: Remove annotations
            annots = page.annots()
            if annots:
                for annot in annots:
                    annot.delete()
            
            # Method 2: Use redaction annotations (structure-preserving)
            # Redactions are designed to preserve PDF structure while removing content
            watermark_rects = []
            processed_keys = set()
            
            for text_variant in watermark_variations:
                if not text_variant or len(text_variant.strip()) < 5:
                    continue
                try:
                    # Find text instances
                    text_instances = page.search_for(text_variant, flags=fitz.TEXT_DEHYPHENATE)
                    for inst in text_instances:
                        key = (round(inst.x0, 2), round(inst.y0, 2), round(inst.x1, 2), round(inst.y1, 2))
                        if key not in processed_keys:
                            watermark_rects.append(inst)
                            processed_keys.add(key)
                    
                    # Also check text blocks
                    blocks = page.get_text("blocks")
                    for block in blocks:
                        if len(block) < 5:
                            continue
                        block_text = block[4]
                        if text_variant.lower() in block_text.lower():
                            block_text_clean = block_text.strip()
                            if (text_variant.lower() in block_text_clean.lower() and 
                                len(block_text_clean) <= len(text_variant) + 10):
                                rect = fitz.Rect(block[:4])
                                key = (round(rect.x0, 2), round(rect.y0, 2), round(rect.x1, 2), round(rect.y1, 2))
                                if key not in processed_keys:
                                    watermark_rects.append(rect)
                                    processed_keys.add(key)
                except Exception as e:
                    pass
            
            # Apply redactions (these are designed to preserve structure)
            if watermark_rects:
                for wm_rect in watermark_rects:
                    try:
                        # Use redaction annotations - these preserve structure better than draw_rect
                        page.add_redact_annot(wm_rect, fill=(1, 1, 1))
                    except:
                        pass
                
                # Apply all redactions at once
                try:
                    page.apply_redactions()
                    print(f"    Redacted {len(watermark_rects)} watermark instances")
                except Exception as e:
                    print(f"    Warning: Redaction failed, trying overlay: {e}")
                    # Fallback to overlay if redaction fails
                    for wm_rect in watermark_rects:
                        try:
                            page.draw_rect(wm_rect, color=(1, 1, 1), fill=(1, 1, 1), width=0)
                        except:
                            pass
                    print(f"    Used overlay fallback for {len(watermark_rects)} instances")
            else:
                print(f"    No watermark instances found")
            
            # Method 3: SKIPPED - Only remove the specific watermark text, not all light-colored text
            # This preserves legitimate content that might be light-colored
            
            # Method 4: Remove image watermarks (if watermark is an image overlay)
            try:
                image_list = page.get_images()
                # Check for images that might be watermarks
                # Watermark images are often:
                # - Large and covering significant area
                # - Semi-transparent
                # - Repeated across pages
                for img_index, img in enumerate(image_list):
                    xref = img[0]
                    # Get image properties
                    try:
                        base_image = doc.extract_image(xref)
                        # If image is very large relative to page, might be watermark
                        # This is a heuristic - adjust as needed
                        page_rect = page.rect
                        page_area = page_rect.width * page_rect.height
                        
                        # For now, we'll be conservative and not remove images automatically
                        # But we can add logic here if needed
                    except:
                        pass
            except Exception as e:
                pass  # Images are optional to process
        
        # Save with structure preservation settings
        # Try incremental first (best for structure), then fallback to minimal changes
        try:
            # Incremental save appends changes without rewriting entire file
            doc.save(output_path, incremental=True, garbage=0)
        except:
            try:
                # Fallback: minimal changes, no compression, no cleanup
                doc.save(output_path, garbage=0, deflate=False, clean=False, ascii=False)
            except:
                # Last resort: default save
                doc.save(output_path)
        doc.close()
        
        print(f"✓ Successfully created: {output_path}")
        return True
        
    except Exception as e:
        print(f"Error processing PDF: {e}")
        import traceback
        traceback.print_exc()
        return False

def remove_watermark_advanced(input_path, output_path):
    """Advanced watermark removal using pdfrw."""
    try:
        from pdfrw import PdfReader as PdfReaderRw, PdfWriter as PdfWriterRw
    except ImportError:
        print("Error: pdfrw library not found.")
        print("Install it with: pip3 install pdfrw")
        return False
    
    try:
        reader = PdfReaderRw(input_path)
        
        print(f"Processing {len(reader.pages)} pages...")
        
        for page_num, page in enumerate(reader.pages, 1):
            print(f"  Processing page {page_num}...")
            
            # Remove annotations
            if hasattr(page, 'Annots') and page.Annots:
                page.Annots = None
            
            # Remove optional content
            if hasattr(page, 'OCProperties'):
                page.OCProperties = None
        
        writer = PdfWriterRw()
        writer.write(output_path, reader)
        
        print(f"✓ Successfully created: {output_path}")
        return True
        
    except Exception as e:
        print(f"Error processing PDF: {e}")
        return False

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 remove_pdf_watermark.py <input.pdf> <output.pdf>")
        print("\nExample:")
        print("  python3 remove_pdf_watermark.py input.pdf output.pdf")
        sys.exit(1)
    
    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])
    
    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}")
        sys.exit(1)
    
    if output_path.exists():
        # Auto-overwrite in non-interactive mode, or prompt if interactive
        try:
            response = input(f"Output file {output_path} already exists. Overwrite? (y/n): ")
            if response.lower() != 'y':
                print("Cancelled.")
                sys.exit(0)
        except (EOFError, KeyboardInterrupt):
            # Non-interactive mode - auto-overwrite
            print(f"Output file exists. Overwriting: {output_path}")
    
    print(f"Removing watermark from: {input_path}")
    print(f"Output will be saved to: {output_path}\n")
    
    # Try different methods in order of preference
    # Note: All methods that modify PDFs can potentially affect structure
    # The best approach depends on how the watermark is embedded
    methods = [
        ("PyMuPDF (Advanced)", remove_watermark_pymupdf),
        ("pypdf (Annotations only)", remove_watermark_pypdf),
        ("PyPDF2", remove_watermark_pypdf2),
        ("pdfrw", remove_watermark_advanced),
    ]
    
    for method_name, method_func in methods:
        print(f"\nTrying method: {method_name}...")
        if method_func(input_path, output_path):
            print(f"\n✓ Watermark removal completed using {method_name}!")
            return
    
    print("\n✗ Failed to remove watermark. None of the PDF libraries are available.")
    print("\nPlease install one of the following:")
    print("  pip3 install PyMuPDF    (recommended for content stream manipulation)")
    print("  pip3 install pypdf")
    print("  pip3 install PyPDF2")
    print("  pip3 install pdfrw")
    sys.exit(1)

if __name__ == "__main__":
    main()

