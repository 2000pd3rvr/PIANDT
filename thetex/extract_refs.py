#!/usr/bin/env python3
"""
Extract all references from Chapter 2 references section
Only extracts from the numbered list in section 2.1.8
"""

import docx
import re

doc = docx.Document('/Users/pd3rvr/Documents/pubs/THESIS/comments_addressed/thesis__7_12_25/revised_corrected/full references/ch2_14_11_25_commments_addressed.docx')

ref_section = False
all_refs = []
ref_map = {}

for para in doc.paragraphs:
    text = para.text.strip()
    
    # Start when we hit the references section
    if '2.1.8 Chapter 2 references' in text:
        ref_section = True
        continue
    
    # Stop if we hit next chapter
    if ref_section and text and ('Chapter 3' in text or 'Chapter 4' in text):
        break
    
    if ref_section and text:
        # Remove bullet points
        ref_text = text.replace('•', '').replace('\t', ' ').strip()
        
        # Skip section headers and body text paragraphs
        if any(skip in ref_text for skip in [
            'Chapter 2:', 'Table', 'Figure 2__', '2.1.', 'Introduction', 
            'Optical sensing', 'Spectroscopy', 'Material detection', 
            'Depth estimation', 'Role of SPAD', 'Conclusion', 'Summary',
            'The section presents', 'Besides optical', 'Following spectroscopy',
            'Finally, depth', 'Echolocation methods', 'Under role',
            'Material detection with SPADs', 'Finally, the chapter',
            'Several signal', 'From [18]', 'Previous material', 'In other instances',
            'Optical sensing for', 'All colours', 'Spectroscopy is', 'From section',
            'There is much', 'The signals', 'Two main', 'This could', 'Vacuum detectors',
            'Solid state', 'This section', 'The photodiode', 'The impact', 'SPADs belongs',
            'Single photon', 'SPAD imagers', 'The total', 'TDC jitter', 'SPAD jitter',
            'Coarse TDC', 'A commonly', 'Noise in ToF', 'SPAD detectors', 'Another significant',
            'Conventional photodiode', 'Dark counts', 'SPADs operate', 'Another form',
            'Existing depth', 'The human', 'There are two', 'Despite promising', 'Echolocation',
            'The history', 'Optical time-of-flight', 'Conventional ToF', 'Unlike stereoscopy',
            'Direct ToF', 'Indirect ToF', 'Pulsed indirect', 'Optical coherence'
        ]):
            continue
        
        # Look for numbered list items or references with author names
        # References typically have: Author names, year, title, journal/book, pages, DOI/URL
        if ref_text and len(ref_text) > 40:
            # Check if it's a reference entry (has author AND publication info)
            has_author = bool(re.search(r'\b([A-Z][a-z]+(?:-[A-Z][a-z]+)?)\s*[,&]', ref_text))
            has_year = bool(re.search(r'\b(19|20)\d{2}\b', ref_text))
            has_pub = any(marker in ref_text for marker in [
                'doi:', 'http', 'arxiv', 'Available at:', 'IEEE', 'Nature', 'Opt.', 
                'Adv.', 'Sensors', 'Journal', 'Proceedings', 'ArXiv', 'ACM', 
                'Springer', 'Elsevier', 'Oxford', 'Wiley', 'Available:', 'Accessed:',
                'vol.', 'pp.', 'arXiv', 'abs/', 'PM', 'PMID', 'et al.', 'In ',
                'Published', 'Accessed'
            ])
            
            # Must have author name pattern AND (year OR publication marker)
            if has_author and (has_year or has_pub):
                all_refs.append(ref_text)

# Now match references to numbers based on content
for ref in all_refs:
    if 'Turpin' in ref and 'Spatial images from temporal data' in ref:
        ref_map[1] = ref
    elif 'Elachi' in ref and 'Nature and Properties' in ref:
        ref_map[2] = ref
    elif 'Lyons' in ref and 'Computational time-of-flight' in ref:
        ref_map[3] = ref
    elif 'Tye' in ref and 'Time-resolved Raman' in ref:
        ref_map[4] = ref
    elif 'Redmon' in ref and 'YOLOv3' in ref:
        ref_map[5] = ref
    elif 'Lecun' in ref and 'Gradient-based learning' in ref:
        ref_map[6] = ref
    elif 'LeCun' in ref and 'Handwritten Digit Recognition' in ref:
        ref_map[7] = ref
    elif 'Redmon' in ref and 'You only look once' in ref and '2015' in ref:
        ref_map[8] = ref
    elif 'Redmon' in ref and 'YOLO9000' in ref:
        ref_map[9] = ref
    elif 'Tachella' in ref and 'Real-time 3D reconstruction' in ref:
        ref_map[10] = ref
    elif 'Jungerman' in ref and '3D scene inference' in ref:
        ref_map[11] = ref
    elif 'Becker' in ref and 'Plastic Classification' in ref:
        ref_map[12] = ref
    elif 'Goodfellow' in ref and 'Generative adversarial networks' in ref:
        ref_map[13] = ref
    elif 'Siméoni' in ref and 'DINOv3' in ref:
        ref_map[14] = ref
    elif 'Bozinovski' in ref and 'transfer learning' in ref:
        ref_map[15] = ref
    elif 'Tealab' in ref and 'Time series forecasting' in ref:
        ref_map[16] = ref
    elif 'Wei Liu' in ref or ('Liu' in ref and '1512.02325' in ref):
        ref_map[17] = ref
    elif 'Schwartz' in ref and 'Visual Material Traits' in ref:
        ref_map[18] = ref
    elif 'Sharan' in ref and 'Recognizing Materials' in ref:
        ref_map[19] = ref
    elif 'Sharma' in ref and 'Materialistic' in ref:
        ref_map[20] = ref
    elif 'Yang' in ref and 'Object pose and surface material' in ref and '2024' in ref:
        ref_map[21] = ref
    elif 'Tafone' in ref and 'Surface material recognition' in ref:
        ref_map[22] = ref
    elif 'Yang' in ref and 'Image-fusion-based object detection' in ref and '2023' in ref:
        ref_map[23] = ref
    elif 'Mora-Martín' in ref and 'High-speed object detection' in ref:
        ref_map[24] = ref
    elif 'Fasolino' in ref and 'Multiclass Object Classification' in ref:
        ref_map[25] = ref
    elif 'Chen' in ref and 'RGB-D Salient Object Detection' in ref:
        ref_map[26] = ref
    elif 'Su' in ref and 'Material Classification Using Raw Time-of-Flight' in ref:
        ref_map[27] = ref

# Also try to extract by order if they appear sequentially
# Print all found references first to see the pattern
print(f"Found {len(all_refs)} potential reference entries")
print("\nFirst 30 entries:")
for i, ref in enumerate(all_refs[:30], 1):
    print(f"{i}. {ref[:120]}...")

# Write to file
output_path = '/Users/pd3rvr/Documents/pubs/THESIS/thetex/ch2_ref_map.txt'
with open(output_path, 'w') as f:
    f.write("Chapter 2 Reference Map\n")
    f.write("=" * 80 + "\n\n")
    for num in sorted(ref_map.keys()):
        f.write(f"[{num}] {'-' * 20} {ref_map[num]}\n\n")

print(f"\n\nCreated {output_path} with {len(ref_map)} matched references")
print(f"Reference numbers found: {sorted(ref_map.keys())}")

