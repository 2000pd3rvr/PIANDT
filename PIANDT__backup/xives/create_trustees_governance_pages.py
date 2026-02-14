#!/usr/bin/env python3
"""
Create trustees and governance pages for Proc and Out triads
"""
import os
from pathlib import Path

base_dir = Path(__file__).parent.parent

# Template for page structure
def create_page(triad, page_type, title_suffix, content_sections):
    if triad == "proc":
        triad_name = "Proc"
        triad_path = "processing"
        triad_link = "processing.html"
    elif triad == "out":
        triad_name = "Out"
        triad_path = "out"
        triad_link = "out.html"
    else:
        return None
    
    page_name = f"{triad}_{page_type}.html"
    file_path = base_dir / triad_path / "about_piandt" / page_name
    
    # Breadcrumb path
    breadcrumb_path = f"../../{triad_link}"
    
    # Content based on triad
    if triad == "proc":
        lead_text = f"This section documents initiatives currently in progress related to PIANDT's {page_type}. These initiatives are actively being developed, evaluated, and refined based on incoming signals and community needs, with particular emphasis on diversity and inclusion."
        main_text = f"Current initiatives in progress include: development of {page_type} strategies that prioritize diversity, evaluation of how diverse perspectives strengthen our {page_type}, refinement of {page_type} processes to be more inclusive, and active work on removing barriers to diverse participation in {page_type}."
    else:  # out
        lead_text = f"This section presents the finalized and published {page_type} documentation that has been processed, verified, and delivered. The {page_type} materials represent established organizational frameworks that have been completed and are now available as authoritative documentation, with strong emphasis on diversity and inclusion."
        main_text = f"The published {page_type} documentation has been finalized through the processing stage and is now delivered as a completed output. It serves as the official reference for PIANDT's {page_type} practices, having been verified and formatted for distribution. This delivered output emphasizes the importance of diversity in {page_type} and represents completed work that has been processed through the system."
    
    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_suffix} - PIANDT - {triad_name} - PIANDT</title>
            <script>
        // CRITICAL: Apply theme BEFORE anything else to prevent flash
        (function() {{
            try {{
                const savedTheme = localStorage.getItem('theme') || 'light';
                if (savedTheme === 'dark') {{
                    const html = document.documentElement;
                    html.classList.add('dark-theme');
                    html.style.backgroundColor = '#1a1a1a';
                    html.style.setProperty('background-color', '#1a1a1a', 'important');
                    if (document.body) {{
                        const body = document.body;
                        body.classList.add('dark-theme');
                        body.style.backgroundColor = '#1a1a1a';
                        body.style.setProperty('background-color', '#1a1a1a', 'important');
                    }} else {{
                        const observer = new MutationObserver(function(mutations) {{
                            if (document.body) {{
                                const body = document.body;
                                body.classList.add('dark-theme');
                                body.style.backgroundColor = '#1a1a1a';
                                body.style.setProperty('background-color', '#1a1a1a', 'important');
                                observer.disconnect();
                            }}
                        }});
                        observer.observe(document.documentElement, {{ childList: true, subtree: true }});
                        document.addEventListener('DOMContentLoaded', function() {{
                            if (document.body) {{
                                const body = document.body;
                                body.classList.add('dark-theme');
                                body.style.backgroundColor = '#1a1a1a';
                                body.style.setProperty('background-color', '#1a1a1a', 'important');
                            }}
                        }});
                        if (document.readyState === 'complete' || document.readyState === 'interactive') {{
                            setTimeout(function() {{
                                if (document.body) {{
                                    const body = document.body;
                                    body.classList.add('dark-theme');
                                    body.style.backgroundColor = '#1a1a1a';
                                    body.style.setProperty('background-color', '#1a1a1a', 'important');
                                }}
                            }}, 0);
                        }}
                    }}
                }}
            }} catch(e) {{
                console.error('Theme initialization error:', e);
            }}
        }})();
    </script>
        <style>
        html.dark-theme {{ background-color: #1a1a1a !important; }}
        html.dark-theme body {{ background-color: #1a1a1a !important; }}
        html:not(.dark-theme) {{ background-color: #ffffff; }}
        body:not(.dark-theme) {{ background-color: #ffffff; }}
    </style>
    <link rel="stylesheet" href="../../styles.css?v=59">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;0,600;1,400&family=Allura&family=Dancing+Script:wght@400;500;600;700&display=swap" rel="stylesheet">
</head>
<body>
    <nav class="navbar">
        <div class="nav-container">
            <div class="logo-container">
                <a href="../../index.html" class="logo">PI<span class="logo-and">and</span>T</a>
                <p class="logo-subtitle">
                    <span class="word">people,</span>
                    <span class="word">innovation</span>
                    <span class="word">and</span>
                    <span class="word">technology</span>
                </p>
            </div>
            <span class="logo-suffix"><a href="{breadcrumb_path}" style="text-decoration: none; color: inherit;">{triad_name}</a>-&gt;<a href="../about_piandt/{triad}_about_piandt.html" style="text-decoration: none; color: inherit;">about PIANDT</a>-&gt;<a href="{page_name}" style="text-decoration: none; color: inherit;">{page_type}</a></span>
            <ul class="nav-menu">
                <li class="dropdown">
                    <a href="../about_piandt/{triad}_about_piandt.html" class="nav-link">about PIANDT <span class="dropdown-arrow">▼</span></a>
                    <ul class="dropdown-menu">
                        <li><a href="proc_mission_vision.html" class="dropdown-link">our mission and vision</a></li>
                        <li><a href="proc_charitable_purposes.html" class="dropdown-link">charitable purposes</a></li>
                        <li><a href="proc_our_approach.html" class="dropdown-link">Our approach</a></li>
                        <li><a href="{triad}_trustees.html" class="dropdown-link">trustees</a></li>
                        <li><a href="{triad}_governance.html" class="dropdown-link">governance</a></li>
                    </ul>
                </li>
            </ul>
            <button class="theme-toggle" id="themeToggle" aria-label="Toggle dark/light theme">
                <span class="theme-icon">🌙</span>
            </button>
            <div class="hamburger">
                <span></span>
                <span></span>
                <span></span>
            </div>
        </div>
    </nav>

    <main>
        <section id="{page_type}" class="section" style="padding-top: 8rem;">
            <div class="container">
                <div class="content-grid">
                    <h1>{title_suffix}</h1>
                    <div class="content-text">
                        <p class="lead">
                            {lead_text}
                        </p>
                        {content_sections}
                    </div>
                </div>
            </div>
        </section>
    </main>

    <!-- Chat Agent Button -->
    <img src="../../images/agent.png" alt="Speak to an agent" class="chat-agent-btn" id="chatAgentBtn">

    <!-- Chat Window -->
    <div class="chat-window" id="chatWindow">
        <div class="chat-messages" id="chatMessages">
            <div class="chat-message bot-message">
                <div class="message-content">
                    <p>Hello! I'm here to help you find information on our website. You can ask me about:</p>
                    <ul>
                        <li>Our services and products</li>
                        <li>Machine Intelligence Unit (MIU)</li>
                        <li>In, Proc, or Out stages</li>
                        <li>Specific pages or sections</li>
                    </ul>
                    <p>What would you like to know?</p>
                    <p style="margin-top: 1rem; font-size: 0.9em; color: #666;">
                        💡 <strong>Tip:</strong> To enable Mistral AI for smarter responses, type: <code>/setkey your-api-key</code>
                    </p>
                </div>
            </div>
        </div>
        <div class="chat-input-wrapper">
            <input type="text" class="chat-input" id="chatInput" placeholder="Type your question here..." autocomplete="off">
            <button class="chat-send" id="chatSend" aria-label="Send message">↑</button>
        </div>
    </div>

    <script src="../../script.js?v=14"></script>
</body>
</html>'''
    
    return html_content, file_path

# Create Proc trustees page
proc_trustees_content = '''<h2>Initiatives in Progress: Trustee Recruitment and Diversity</h2>
                        <p>
                            Current initiatives actively being developed include: creating trustee recruitment strategies that prioritize diversity, developing processes to remove barriers that limit our candidate pool, evaluating how diverse trustee boards improve decision-making, and actively working on making trustee roles more attractive and accessible to a wide range of people.
                        </p>
                        
                        <h2>Why Diversity: Active Development</h2>
                        <p>
                            We are actively developing our understanding of why diversity is essential. Current work includes: analyzing how diverse perspectives prevent "groupthink" in trustee decisions, developing strategies to ensure diverse trustees can contribute fully, evaluating how diverse representation strengthens connections to beneficiaries, and creating processes to demonstrate inclusive practices to stakeholders.
                        </p>
                        
                        <h2>What Diversity Means: In Progress</h2>
                        <p>
                            We are actively defining what diversity means for PIANDT's trustees. Current initiatives include: developing criteria for recruiting trustees with lived experience, creating processes for including user trustees, evaluating how to represent the communities we serve, and developing approaches to consider diverse backgrounds, characteristics, and perspectives.
                        </p>
                        
                        <h2>Who Should Be Trustees: Active Recruitment</h2>
                        <p>
                            We are actively working on identifying who should be trustees. Current initiatives include: developing strategies to recruit young trustees, creating processes to reach underrepresented communities, evaluating how to combine specific skills with diverse backgrounds, and developing approaches to include trustees with lived experience relevant to our charitable purposes.
                        </p>
                        
                        <h2>How to Achieve Diversity: Active Strategies</h2>
                        <p>
                            We are actively developing strategies on how to achieve greater diversity. Current work includes: creating processes to remove barriers to trustee participation, developing approaches to make trustee roles more accessible, evaluating how to reach wider candidate networks, and creating inclusive recruitment processes that attract diverse candidates.
                        </p>
                        
                        <p>
                            Each initiative is actively being analyzed, developed, and refined. These processes involve stakeholder engagement, evidence gathering, iterative design, and continuous evaluation to ensure that our trustee recruitment strategies prioritize diversity and align with our commitment to inclusive governance.
                        </p>'''

# Create Proc governance page
proc_governance_content = '''<h2>Initiatives in Progress: Governance and Diversity</h2>
                        <p>
                            Current initiatives actively being developed include: creating governance structures that ensure diverse voices are heard, developing inclusive meeting practices that enable all trustees to contribute, evaluating how diverse perspectives improve governance decisions, and actively working on governance processes that reflect the communities we serve.
                        </p>
                        
                        <h2>Why Diverse Governance Matters: Active Development</h2>
                        <p>
                            We are actively developing our understanding of why diversity strengthens governance. Current work includes: analyzing how diverse governance improves decision-making quality, developing strategies to maintain connections to beneficiary needs, evaluating how diverse representation demonstrates inclusive practices, and creating processes to ensure governance reflects our communities.
                        </p>
                        
                        <h2>What Inclusive Governance Looks Like: In Progress</h2>
                        <p>
                            We are actively defining what inclusive governance means for PIANDT. Current initiatives include: developing governance structures that enable diverse participation, creating meeting formats that accommodate different communication styles, evaluating decision-making processes that value diverse perspectives, and developing governance documentation that is accessible to all trustees.
                        </p>
                        
                        <h2>Who Should Participate: Active Development</h2>
                        <p>
                            We are actively working on identifying who should participate in governance. Current initiatives include: developing strategies to include user trustees in governance decisions, creating processes to represent beneficiary communities, evaluating how to ensure diverse voices in all governance processes, and developing approaches to include underrepresented groups.
                        </p>
                        
                        <h2>How to Achieve Inclusive Governance: Active Strategies</h2>
                        <p>
                            We are actively developing strategies on how to make governance more inclusive. Current work includes: creating processes to remove barriers to governance participation, developing approaches to make governance roles accessible, evaluating how to structure governance to enable diverse contributions, and creating monitoring processes for governance diversity and effectiveness.
                        </p>
                        
                        <p>
                            Each initiative is actively being analyzed, developed, and refined. These processes involve stakeholder engagement, evidence gathering, iterative design, and continuous evaluation to ensure that our governance improvements prioritize diversity and align with our commitment to inclusive and effective governance.
                        </p>'''

# Create Out trustees page
out_trustees_content = '''<h2>Published Trustee Recruitment and Diversity Framework</h2>
                        <p>
                            The finalized trustee recruitment framework has been processed, verified, and delivered. This established documentation emphasizes the critical importance of diversity in trustee recruitment and serves as the official reference for PIANDT's trustee practices.
                        </p>
                        
                        <h2>Why Diversity Matters: Published Framework</h2>
                        <p>
                            The published framework documents why diversity is essential for effective governance. The finalized documentation establishes that diverse trustee boards help us to: consider issues from wider viewpoints, have more varied debate and challenge to avoid "groupthink", reach and stay connected to beneficiary needs, and demonstrate inclusive practices to funders and stakeholders.
                        </p>
                        
                        <h2>What Diversity Means: Established Definition</h2>
                        <p>
                            The published framework defines what diversity means for PIANDT's trustees. The finalized documentation establishes criteria for: recruiting trustees with lived experience, including user trustees who use our services, ensuring representation of the communities we serve, and considering diverse backgrounds, characteristics, and perspectives.
                        </p>
                        
                        <h2>Who Should Be Trustees: Published Criteria</h2>
                        <p>
                            The published framework establishes who should be trustees. The finalized documentation includes criteria for: recruiting young trustees, reaching underrepresented communities, combining specific skills with diverse backgrounds, and including trustees with lived experience relevant to our charitable purposes.
                        </p>
                        
                        <h2>How to Achieve Diversity: Published Strategies</h2>
                        <p>
                            The published framework documents how to achieve greater diversity. The finalized documentation establishes processes for: removing barriers that limit candidate pools, making trustee roles more accessible, reaching wider candidate networks, and creating inclusive recruitment processes.
                        </p>
                        
                        <p>
                            This published framework has been finalized through the processing stage and is now delivered as a completed output. It has been verified, formatted, and published for public reference, serving as the definitive statement of PIANDT's commitment to diverse and inclusive trustee recruitment.
                        </p>'''

# Create Out governance page
out_governance_content = '''<h2>Published Governance and Diversity Framework</h2>
                        <p>
                            The finalized governance framework has been processed, verified, and delivered. This established documentation emphasizes how diversity strengthens governance and serves as the official reference for PIANDT's governance practices.
                        </p>
                        
                        <h2>Why Diverse Governance Matters: Published Framework</h2>
                        <p>
                            The published framework documents why diversity is fundamental to effective governance. The finalized documentation establishes that diverse governance helps us to: make better decisions by considering wider viewpoints, maintain stronger connections to beneficiary needs, demonstrate inclusive practices to stakeholders, ensure governance reflects our communities, and create accessible governance structures.
                        </p>
                        
                        <h2>What Inclusive Governance Looks Like: Established Definition</h2>
                        <p>
                            The published framework defines what inclusive governance means for PIANDT. The finalized documentation establishes structures for: enabling diverse trustees to participate fully, accommodating different communication styles in meetings, valuing diverse perspectives in decision-making, creating accessible governance documentation, and evaluating governance effectiveness through diverse lenses.
                        </p>
                        
                        <h2>Who Should Participate: Published Framework</h2>
                        <p>
                            The published framework establishes who should participate in governance. The finalized documentation includes criteria for: including user trustees in governance decisions, representing beneficiary communities, ensuring diverse voices in all governance processes, and including underrepresented groups in governance participation.
                        </p>
                        
                        <h2>How to Achieve Inclusive Governance: Published Strategies</h2>
                        <p>
                            The published framework documents how to make governance more inclusive. The finalized documentation establishes processes for: removing barriers to governance participation, making governance roles accessible, structuring governance to enable diverse contributions, and monitoring governance diversity and effectiveness.
                        </p>
                        
                        <p>
                            This published framework has been finalized through the processing stage and is now delivered as a completed output. It has been verified, formatted, and published for public reference, serving as the definitive statement of PIANDT's commitment to diverse and inclusive governance.
                        </p>'''

# Create all pages
pages_to_create = [
    ("proc", "trustees", "Trustees - In Progress", proc_trustees_content),
    ("proc", "governance", "Governance - In Progress", proc_governance_content),
    ("out", "trustees", "Trustees - Delivered Outputs", out_trustees_content),
    ("out", "governance", "Governance - Delivered Outputs", out_governance_content),
]

for triad, page_type, title, content in pages_to_create:
    html, file_path = create_page(triad, page_type, title, content)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Created: {file_path.relative_to(base_dir)}")

print("\n✓ All pages created!")



