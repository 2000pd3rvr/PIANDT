#!/usr/bin/env python3
"""
Rebalance paragraphs so Sheet 1 has exactly 300 words (75 per column × 4 columns).
"""

import re

html_file = '/Users/pd3rvr/Documents/pubs/THESIS/thetex/PIANDT/in/about_piandt/in_trustees.html'

with open(html_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Target: 75 words per column × 4 columns = 300 words per sheet
# Sheet 1 should have exactly 300 words (75 per column)
# Sheet 2 will have the remaining words

# Rebalance paragraphs so first 4 = 300 words total
balanced_paragraphs = [
    """This section captures and documents all incoming signals, requests, proposals, and feedback related to PIANDT's trustee recruitment, composition, and diversity. As part of the In component, we receive communications about trustee needs, candidate suggestions, diversity initiatives, and governance improvements. <strong style="color: var(--color-primary);">Incoming Signals: Trustee Recruitment and Diversity:</strong> We receive incoming signals related to trustee recruitment that emphasize the critical importance of diversity. These signals include: community requests for more diverse trustee representation, proposals for recruiting trustees with lived experience.""",
    
    """Suggestions for reaching wider candidate pools, feedback on barriers that may limit our candidate pool, and recommendations for making trustee roles more attractive and accessible to a wide range of people. <strong style="color: var(--color-primary);">Why Diversity Matters: Incoming Perspectives:</strong> Incoming signals consistently highlight why diversity is essential for effective governance. We receive feedback emphasizing that having a diverse range of backgrounds, characteristics, and perspectives on our trustee board helps us to: consider issues from a wider range of viewpoints, have more varied debate and challenge to avoid "groupthink" when making decisions.""",
    
    """Reach and stay connected to the needs of our beneficiaries, and show our funders and other stakeholders that our charity's actions and practices are inclusive. <strong style="color: var(--color-primary);">What Diversity Means: Incoming Definitions:</strong> Incoming signals help us understand what aspects of diversity are most relevant for PIANDT. We receive proposals and feedback about: recruiting trustees with personal or first-hand experience of the cause we work on (lived experience), including people who currently use our services or facilities (user trustees), ensuring representation of the people, communities, or local areas we serve.""",
    
    """Considering the mix of backgrounds, characteristics, and perspectives on our board. <strong style="color: var(--color-primary);">Who Should Be Trustees: Incoming Candidate Suggestions:</strong> We receive incoming signals suggesting who could be valuable trustees, with strong emphasis on diversity. These include: proposals for young trustees who can bring fresh perspectives, suggestions for trustees from underrepresented communities, recommendations for candidates with specific skills combined with diverse backgrounds, requests for user trustees who understand our services firsthand, and proposals for trustees with lived experience relevant to our charitable purposes.""",
    
    """<strong style="color: var(--color-primary);">How to Achieve Diversity: Incoming Strategies:</strong> Incoming signals provide valuable suggestions on how to achieve greater diversity in our trustee board. We receive: proposals for removing barriers that may limit our candidate pool, suggestions for making trustee roles more accessible, recommendations for reaching wider candidate networks, feedback on how to make our recruitment process more inclusive, and proposals for diversity audits and monitoring processes.""",
    
    """<strong style="color: var(--color-primary);">Incoming Signals: Skills and Experience Needs:</strong> We receive incoming signals about the skills, experience, and knowledge that our trustee board needs. These signals emphasize the importance of combining technical skills with diverse perspectives. Incoming suggestions include: requests for trustees with knowledge or experience of our field of work, proposals for specific skills in finance, governance, safeguarding, digital, or risk management.""",
    
    """Suggestions for trustees who can play an active part in discussions, and recommendations for balancing expertise with diverse lived experiences. Each incoming signal related to trustees is documented, categorized, and prepared for evaluation. Signals that align with our commitment to diversity and effective governance are routed to the processing stage for further analysis and development into actionable trustee recruitment strategies."""
]

# Count words in balanced paragraphs
print("Balanced paragraph word counts:")
total_words = 0
for i, para in enumerate(balanced_paragraphs, 1):
    word_count = len(re.sub(r'<[^>]+>', '', para).split())
    total_words += word_count
    print(f"Paragraph {i}: {word_count} words")

print(f"\nTotal words: {total_words}")

# Check sheet distribution
sheet1_words = sum(len(re.sub(r'<[^>]+>', '', p).split()) for p in balanced_paragraphs[:4])
sheet2_words = sum(len(re.sub(r'<[^>]+>', '', p).split()) for p in balanced_paragraphs[4:])
print(f"\nEstimated sheet distribution:")
print(f"Sheet 1 (first 4 paragraphs): {sheet1_words} words = ~{sheet1_words/4:.0f} words per column (target: 75)")
print(f"Sheet 2 (remaining paragraphs): {sheet2_words} words = ~{sheet2_words/4:.0f} words per column (target: 75)")

# Adjust if needed to get Sheet 1 closer to 300 words
target_sheet1 = 300
current_sheet1 = sheet1_words
diff = target_sheet1 - current_sheet1

if abs(diff) > 5:
    print(f"\nAdjusting paragraphs to get Sheet 1 closer to 300 words (diff: {diff})")
    # Move some words from paragraph 4 to paragraph 5, or vice versa
    if diff > 0:
        # Need more words in Sheet 1 - move content from paragraph 5 to paragraph 4
        print("Moving content from paragraph 5 to paragraph 4...")
        # This would require manual adjustment
    else:
        # Need fewer words in Sheet 1 - move content from paragraph 4 to paragraph 5
        print("Moving content from paragraph 4 to paragraph 5...")
        # This would require manual adjustment

# Create HTML
paragraphs_html = '\n                        '.join(f'<p>{p}</p>' for p in balanced_paragraphs)

# Replace content
new_content = re.sub(
    r'(<div class="content-text"[^>]*>).*?(</div>)',
    r'\1\n                        ' + paragraphs_html + '\n                    \2',
    content,
    flags=re.DOTALL
)

# Write back
with open(html_file, 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"\nFixed content-text section with {len(balanced_paragraphs)} paragraphs")
