#!/usr/bin/env python3
"""Insert two new blog article cards at the top of blog-grid in blog.html."""

from pathlib import Path

WORKSPACE = Path(__file__).parent
BLOG_HTML = WORKSPACE / 'blog.html'

NEW_CARDS = '''      <!-- Article New 1: Tensile Strength Testing (2026-09-19) -->
      <a href="blog/tensile-strength-testing-overhead-power-line-hardware.html" class="blog-card">
        <div class="blog-card-date">Sep 19, 2026</div>
        <h2 class="blog-card-title">Tensile Strength Testing for Overhead Power Line Hardware: Ensuring Zero Field Failures</h2>
        <p class="blog-card-excerpt">Learn how in-house mechanical tensile strength and breaking load testing guarantee reliability for overhead transmission line hardware in extreme environments.</p>
        <div class="blog-card-meta">
          <span>By Kunde Electric Engineering Team</span>
          <span class="read-more">Read More →</span>
        </div>
      </a>
      
      <!-- Article New 2: Galvanic Corrosion Prevention (2026-09-19) -->
      <a href="blog/preventing-galvanic-corrosion-bimetallic-cable-lugs.html" class="blog-card">
        <div class="blog-card-date">Sep 19, 2026</div>
        <h2 class="blog-card-title">Preventing Galvanic Corrosion in Bimetallic Cable Lugs: Friction Welding vs. Mechanical Crimp</h2>
        <p class="blog-card-excerpt">Discover how friction-welded copper-aluminum bimetallic cable lugs prevent galvanic corrosion in power distribution systems under high humidity and coastal environments.</p>
        <div class="blog-card-meta">
          <span>By Kunde Electric Quality Assurance</span>
          <span class="read-more">Read More →</span>
        </div>
      </a>
      
'''

def main():
    content = BLOG_HTML.read_text(encoding='utf-8')
    
    # Exact unique anchor: the opening <div class="blog-grid"> followed by newline + spaces + first existing comment
    anchor = '    <div class="blog-grid">\n      <!-- Article New 1: Wedge vs Bolt Tension Clamps (2026-09-16) -->'
    
    if anchor not in content:
        print('ERROR: Anchor not found. Content may have changed.')
        return
    
    replacement = f'    <div class="blog-grid">\n{NEW_CARDS}      <!-- Article New 1: Wedge vs Bolt Tension Clamps (2026-09-16) -->'
    new_content = content.replace(anchor, replacement, 1)
    
    BLOG_HTML.write_text(new_content, encoding='utf-8')
    print(f'✓ Inserted 2 new article cards into {BLOG_HTML.relative_to(WORKSPACE)}')

if __name__ == '__main__':
    main()
