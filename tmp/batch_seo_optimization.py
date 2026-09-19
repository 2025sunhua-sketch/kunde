#!/usr/bin/env python3
"""Batch SEO optimization for Kunde Electric static site.
1. Replace hardcoded meta description with dynamic product-specific content
2. Regenerate complete sitemap.xml including all 322 products + blog posts
3. Enhance existing Schema.org Product JSON-LD with additional fields
"""
import os
import re
import json
from pathlib import Path
from datetime import date

BASE_DIR = Path(r"C:\Users\ADMIN\.jvs\.openclaw\workspace\kunde-website")
PRODUCTS_DIR = BASE_DIR / "product"
BLOG_DIR = BASE_DIR / "blog"

# ========================================
# STEP 1: Fix Meta Descriptions (322 products)
# ========================================
def fix_meta_descriptions():
    """Replace generic meta description with product-specific content."""
    fixed_count = 0
    
    for product_dir in sorted(PRODUCTS_DIR.glob("product-*")):
        html_file = product_dir / "index.html"
        if not html_file.exists():
            continue
        
        try:
            content = html_file.read_text(encoding='utf-8')
            
            # Extract product name from <h1 class="product-name"> or title tag
            name_match = re.search(r'<h1[^>]*class="product-name"[^>]*>(.*?)</h1>', content)
            if not name_match:
                print(f"  SKIP {product_dir.name}: no product-name found")
                continue
            
            product_name = name_match.group(1).strip()
            
            # Extract category from span.category-badge
            cat_match = re.search(r'<span[^>]*class="category-badge"[^>]*>(.*?)</span>', content)
            category = cat_match.group(1).strip() if cat_match else "Power Fittings"
            
            # Extract product ID from filename or content
            product_id = product_dir.name  # e.g., "product-0001"
            
            # Generate unique meta description (130-160 chars)
            new_desc = f"{product_name} ({category}) by Kunde Electric. High-quality power fittings for transmission & distribution systems. Factory-direct pricing, fast delivery. Request a quote today."
            
            # Truncate to 155 chars max (Google's display limit)
            if len(new_desc) > 155:
                new_desc = new_desc[:152] + "..."
            
            # Replace old meta description
            old_meta_pattern = r'<meta name="description" content="[^"]*">'
            new_meta = f'<meta name="description" content="{new_desc}">'
            
            if re.search(old_meta_pattern, content):
                content = re.sub(old_meta_pattern, new_meta, content)
                html_file.write_text(content, encoding='utf-8')
                fixed_count += 1
                print(f"  FIXED {product_id}: {product_name[:50]}...")
            else:
                print(f"  SKIP {product_id}: no meta description found")
                
        except Exception as e:
            print(f"  ERROR {product_dir.name}: {e}")
    
    print(f"\nMeta descriptions fixed: {fixed_count}/322\n")
    return fixed_count


# ========================================
# STEP 2: Regenerate Complete Sitemap
# ========================================
def regenerate_sitemap():
    """Generate complete sitemap.xml with all pages."""
    today = date.today().isoformat()
    
    urls = []
    
    # Core pages
    core_pages = [
        ("", "1.0", "weekly"),
        ("products.html", "0.9", "weekly"),
        ("blog.html", "0.9", "weekly"),
        ("about.html", "0.8", "monthly"),
        ("faq.html", "0.8", "monthly"),
        ("contact.html", "0.8", "monthly"),
        ("production.html", "0.7", "monthly"),
        ("privacy-policy.html", "0.5", "yearly"),
        ("warranty-policy.html", "0.5", "yearly"),
    ]
    
    for path, priority, freq in core_pages:
        loc = f"https://kdelec.com/{path}" if path else "https://kdelec.com/"
        urls.append({
            "loc": loc,
            "lastmod": today,
            "changefreq": freq,
            "priority": priority
        })
    
    # Category pages
    categories = [
        "category/cable-lugs-and-connectors/index.html",
        "category/insulated-terminals/index.html",
        "category/cable-clamps/index.html",
    ]
    
    for cat_path in categories:
        urls.append({
            "loc": f"https://kdelec.com/{cat_path}",
            "lastmod": today,
            "changefreq": "weekly",
            "priority": "0.8"
        })
    
    # All product pages (322 items)
    for product_dir in sorted(PRODUCTS_DIR.glob("product-*")):
        if (product_dir / "index.html").exists():
            urls.append({
                "loc": f"https://kdelec.com/product/{product_dir.name}/",
                "lastmod": today,
                "changefreq": "monthly",
                "priority": "0.6"
            })
    
    # Blog posts
    for blog_file in sorted(BLOG_DIR.glob("*.html")):
        if blog_file.name != "article-template.html":
            urls.append({
                "loc": f"https://kdelec.com/blog/{blog_file.name}",
                "lastmod": today,
                "changefreq": "monthly",
                "priority": "0.7"
            })
    
    # Build XML
    xml_lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml_lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    xml_lines.append('')
    
    for url_data in urls:
        xml_lines.append('  <url>')
        xml_lines.append(f'    <loc>{url_data["loc"]}</loc>')
        xml_lines.append(f'    <lastmod>{url_data["lastmod"]}</lastmod>')
        xml_lines.append(f'    <changefreq>{url_data["changefreq"]}</changefreq>')
        xml_lines.append(f'    <priority>{url_data["priority"]}</priority>')
        xml_lines.append('  </url>')
        xml_lines.append('')
    
    xml_lines.append('</urlset>')
    
    sitemap_path = BASE_DIR / "sitemap.xml"
    sitemap_path.write_text('\n'.join(xml_lines), encoding='utf-8')
    
    print(f"Sitemap regenerated: {len(urls)} URLs")
    print(f"  - Core pages: {len(core_pages)}")
    print(f"  - Categories: {len(categories)}")
    print(f"  - Products: {sum(1 for _ in PRODUCTS_DIR.glob('product-*/index.html'))}")
    print(f"  - Blog posts: {sum(1 for f in BLOG_DIR.glob('*.html') if f.name != 'article-template.html')}")
    print()


# ========================================
# STEP 3: Enhance Schema.org JSON-LD
# ========================================
def enhance_schema_org():
    """Add enhanced Product schema to all product pages."""
    enhanced_count = 0
    
    for product_dir in sorted(PRODUCTS_DIR.glob("product-*")):
        html_file = product_dir / "index.html"
        if not html_file.exists():
            continue
        
        try:
            content = html_file.read_text(encoding='utf-8')
            
            # Extract product data
            name_match = re.search(r'<h1[^>]*class="product-name"[^>]*>(.*?)</h1>', content)
            desc_match = re.search(r'<p[^>]*class="product-description"[^>]*>(.*?)</p>', content)
            cat_match = re.search(r'<span[^>]*class="category-badge"[^>]*>(.*?)</span>', content)
            
            if not name_match:
                continue
            
            product_name = name_match.group(1).strip()
            product_desc = desc_match.group(1).strip() if desc_match else product_name
            category = cat_match.group(1).strip() if cat_match else "Power Fittings"
            product_id = product_dir.name
            
            # Build enhanced JSON-LD
            schema = {
                "@context": "https://schema.org",
                "@type": "Product",
                "name": product_name,
                "description": product_desc,
                "sku": product_id,
                "brand": {
                    "@type": "Brand",
                    "name": "KUNDE ELECTRIC"
                },
                "manufacturer": {
                    "@type": "Organization",
                    "name": "Kunde Electric",
                    "url": "https://www.kdelec.com"
                },
                "offers": {
                    "@type": "Offer",
                    "url": f"https://www.kdelec.com/product/{product_id}/",
                    "priceCurrency": "USD",
                    "availability": "https://schema.org/InStock",
                    "seller": {
                        "@type": "Organization",
                        "name": "Kunde Electric"
                    }
                },
                "category": category
            }
            
            schema_json = json.dumps(schema, ensure_ascii=False)
            new_script = f'<script type="application/ld+json">{schema_json}</script>'
            
            # Replace existing schema or add before </head>
            old_schema_pattern = r'<script type="application/ld\+json">\{.*?\}</script>'
            
            if re.search(old_schema_pattern, content, re.DOTALL):
                content = re.sub(old_schema_pattern, new_script, content, flags=re.DOTALL)
            else:
                # Insert before </head>
                content = content.replace('</head>', f'{new_script}\n</head>')
            
            html_file.write_text(content, encoding='utf-8')
            enhanced_count += 1
            
        except Exception as e:
            print(f"  ERROR {product_dir.name}: {e}")
    
    print(f"Schema.org enhanced: {enhanced_count}/322 products\n")


# ========================================
# MAIN EXECUTION
# ========================================
if __name__ == "__main__":
    print("=" * 60)
    print("Kunde Electric SEO Optimization Batch Script")
    print("=" * 60)
    print()
    
    print("[1/3] Fixing meta descriptions...")
    fix_meta_descriptions()
    
    print("[2/3] Regenerating sitemap.xml...")
    regenerate_sitemap()
    
    print("[3/3] Enhancing Schema.org JSON-LD...")
    enhance_schema_org()
    
    print("=" * 60)
    print("SEO optimization complete!")
    print("=" * 60)
