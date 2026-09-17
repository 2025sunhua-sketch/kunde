#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fix blog post titles and improve typography."""

import os
import re

WORKSPACE = r"C:\Users\ADMIN\.jvs\.openclaw\workspace\kunde-website"
BLOG_DIR = os.path.join(WORKSPACE, "blog")

# Title mapping for the 3 new posts
TITLE_MAP = {
    "mechanical-reliability-wedge-vs-bolt-tension-clamps.html": 
        "Mechanical Reliability of Wedge vs. Bolt-Type Tension Clamps in ACSR Line Operations | Kunde Electric Blog",
    "metallurgical-integrity-bimetallic-cable-lugs.html": 
        "Metallurgical Integrity in Bimetallic Cable Lugs: Preventing Galvanic Degradation | Kunde Electric Blog",
    "avoiding-crimp-failure-heavy-duty-copper-lugs.html": 
        "Avoiding Crimp Failure in Heavy-Duty Copper Cable Terminals | Kunde Electric Blog",
}

TYPOGRAPHY_CSS = '''
/* Blog article typography improvements */
.article-container {
  max-width: 800px;
  margin: 40px auto;
  padding: 0 20px;
}

.back-link {
  display: inline-block;
  color: var(--primary-blue, #1a73e8);
  text-decoration: none;
  font-weight: 500;
  margin-bottom: 24px;
  font-size: 15px;
}
.back-link:hover { text-decoration: underline; }

.article-header {
  margin-bottom: 32px;
  border-bottom: 1px solid #e0e0e0;
  padding-bottom: 24px;
}

.article-date {
  color: #666;
  font-size: 14px;
  margin-bottom: 8px;
}

.article-title {
  font-size: 32px;
  line-height: 1.3;
  color: #1a1a1a;
  margin: 0;
  font-weight: 700;
}

.article-content h2 {
  font-size: 24px;
  color: #1a1a1a;
  margin-top: 40px;
  margin-bottom: 16px;
  font-weight: 600;
}

.article-content h3 {
  font-size: 20px;
  color: #2a2a2a;
  margin-top: 32px;
  margin-bottom: 12px;
  font-weight: 600;
}

.article-content p {
  font-size: 17px;
  line-height: 1.8;
  color: #333;
  margin-bottom: 20px;
}

.article-content ul, .article-content ol {
  margin-bottom: 20px;
  padding-left: 24px;
}

.article-content li {
  font-size: 17px;
  line-height: 1.8;
  color: #333;
  margin-bottom: 8px;
}

.article-content strong {
  color: #1a1a1a;
  font-weight: 600;
}

.cta-box {
  background: #f8f9fa;
  border-left: 4px solid var(--primary-blue, #1a73e8);
  padding: 20px 24px;
  margin-top: 40px;
  border-radius: 4px;
}

.cta-box p {
  margin: 0 !important;
  font-size: 16px !important;
}

@media (max-width: 768px) {
  .article-container { margin: 24px auto; padding: 0 16px; }
  .article-title { font-size: 26px; }
  .article-content h2 { font-size: 22px; }
  .article-content p, .article-content li { font-size: 16px; }
}
'''

for filename, correct_title in TITLE_MAP.items():
    filepath = os.path.join(BLOG_DIR, filename)
    if not os.path.exists(filepath):
        print(f"NOT FOUND: {filepath}")
        continue
    
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Fix title tag
    old_title_match = re.search(r'<title>.*?</title>', content)
    if old_title_match:
        content = content.replace(old_title_match.group(0), f'<title>{correct_title}</title>')
    
    # Inject typography CSS before </head>
    if '.article-container' not in content:
        css_block = f'\n<style>\n{TYPOGRAPHY_CSS}\n</style>\n'
        content = content.replace('</head>', f'{css_block}</head>')
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"Fixed: {filename}")

print("\nDone. All 3 blog posts updated with correct titles and improved typography.")
