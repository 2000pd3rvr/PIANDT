#!/usr/bin/env python3
"""
Fix the trustees HTML file by cleaning up the content-text section
and splitting into properly balanced paragraphs.
"""

import re

html_file = '/Users/pd3rvr/Documents/pubs/THESIS/thetex/PIANDT/in/about_piandt/in_trustees.html'

with open(html_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Find and replace the content-text section
# The paragraphs should be approximately 70 words each to fill one column with 20 lines

new_paragraphs = [
    """This section captures and documents all incoming signals, requests, proposals, and feedback related to PIANDT's trustee recruitment, composition, and diversity. As part of the In component, we receive communications about trustee needs, candidate suggestions, diversity initiatives, and governance improvements. <strong style="color: var(--color-primary);">Incoming Signals: Trustee Recruitment and Diversity:</strong> We receive incoming signals related to trustee recruitment that emphasize the critical importance of diversity. These signals include: community requests for more diverse trustee representation, proposals for recruiting trustees with lived experience of the causes we work on, suggestions for reaching wider candidate pools, feedback on barriers that may limit our candidate pool, and recommendations for making trustee roles more attractive and accessible to a wide range of people.""",
    
    """<strong style="color: var(--color-primary);">Why Diversity Matters: Incoming Perspectives:</strong> Incoming signals consistently highlight why diversity is essential for effective governance. We receive feedback emphasizing that having a diverse range of backgrounds, characteristics, and perspectives on our trustee board helps us to: consider issues from a wider range of viewpoints, have more varied debate and challenge to avoid "groupthink" when making decisions, reach and stay connected to the needs of our beneficiaries, and show our funders and other stakeholders that our charity's actions and practices are inclusive.""",
    
    """<strong style="color: var(--color-primary);">What Diversity Means: Incoming Definitions:</strong> Incoming signals help us understand what aspects of diversity are most relevant for PIANDT. We receive proposals and feedback about: recruiting trustees with personal or first-hand experience of the cause we work on (lived experience), including people who currently use our services or facilities (user trustees), ensuring representation of the people, communities, or local areas we serve, and considering the mix of backgrounds, characteristics, and perspectives on our board.""",
    
    """<strong style="color: var(--color-primary);">Who Should Be Trustees: Incoming Candidate Suggestions:</strong> We receive incoming signals suggesting who could be valuable trustees, with strong emphasis on diversity. These include: proposals for young trustees who can bring fresh perspectives, suggestions for trustees from underrepresented communities, recommendations for candidates with specific skills combined with diverse backgrounds, requests for user trustees who understand our services firsthand, and proposals for trustees with lived experience relevant to our charitable purposes.""",
    
    """<strong style="color: var(--color-primary);">How to Achieve Diversity: Incoming Strategies:</strong> Incoming signals provide valuable suggestions on how to achieve greater diversity in our trustee board. We receive: proposals for removing barriers that may limit our candidate pool, suggestions for making trustee roles more accessible, recommendations for reaching wider candidate networks, feedback on how to make our recruitment process more inclusive, and proposals for diversity audits and monitoring processes.""",
    
    """<strong style="color: var(--color-primary);">Incoming Signals: Skills and Experience Needs:</strong> We receive incoming signals about the skills, experience, and knowledge that our trustee board needs. These signals emphasize the importance of combining technical skills with diverse perspectives. Incoming suggestions include: requests for trustees with knowledge or experience of our field of work, proposals for specific skills in finance, governance, safeguarding, digital, or risk management, suggestions for trustees who can play an active part in discussions, and recommendations for balancing expertise with diverse lived experiences.""",
    
    """Each incoming signal related to trustees is documented, categorized, and prepared for evaluation. Signals that align with our commitment to diversity and effective governance are routed to the processing stage for further analysis and development into actionable trustee recruitment strategies."""
]

# Create the HTML for paragraphs
paragraphs_html = '\n                        '.join(f'<p>{p}</p>' for p in new_paragraphs)

# Replace the content-text section
pattern = r'(<div class="content-text"[^>]*>).*?(</div>)'
replacement = r'\1\n                        ' + paragraphs_html + '\n                    \2'

new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

# Write back
with open(html_file, 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"Fixed content-text section with {len(new_paragraphs)} paragraphs")
for i, para in enumerate(new_paragraphs, 1):
    word_count = len(re.sub(r'<[^>]+>', '', para).split())
    print(f"Paragraph {i}: {word_count} words")


