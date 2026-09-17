#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Batch inject SEO meta tags (title/description/keywords) and JSON-LD Schema.org markup
into all HTML pages of the Kunde Electric static website.

Covers:
- Product detail pages: product/product-XXXX/index.html  → Product schema
- Category pages: products-category-{N}.html             → ItemList schema
- Homepage: index.html                                    → Organization + WebSite schema
- Other root-level pages: about/contact/etc.              → generic description only
"""

import os
import re
import json
from pathlib import Path

BASE_DIR = Path(r"C:\Users\ADMIN\.jvs\.openclaw\workspace\kunde-website")

# ─── Site-wide constants ────────────────────────────────────────────────
SITE_NAME = "Kunde Electric"
SITE_URL = "https://www.kdelec.com"
COMPANY_DESC = (
    "Kunde Electric is a professional manufacturer of cable lugs, terminals, "
    "connectors and power accessories based in Yiwu, China. We supply high-quality "
    "electrical components for global B2B buyers."
)

# ─── Page-type metadata templates ───────────────────────────────────────

def product_meta(name: str, product_id: str) -> dict:
    """Generate TDK + Product JSON-LD for a single product page."""
    title = f"{name} - {SITE_NAME}"
    desc = (
        f"{name} from {SITE_NAME}. High-quality electrical cable lug / terminal / connector "
        f"for industrial applications. Product ID: {product_id}. Request a factory-direct quote today."
    )
    keywords = (
        f"{name}, cable lug, electrical terminal, connector, {SITE_NAME}, "
        f"power fitting, Yiwu manufacturer, bimetal lug, aluminum lug, copper terminal"
    )
    schema = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": name,
        "sku": product_id,
        "description": desc,
        "brand": {"@type": "Brand", "name": SITE_NAME},
        "manufacturer": {
            "@type": "Organization",
            "name": SITE_NAME,
            "url": SITE_URL
        },
        "offers": {
            "@type": "Offer",
            "url": f"{SITE_URL}/product/{product_id}/",
            "priceCurrency": "USD",
            "availability": "https://schema.org/InStock",
            "seller": {"@type": "Organization", "name": SITE_NAME}
        }
    }
    return {"title": title, "desc": desc, "keywords": keywords, "schema": schema}


def category_meta(cat_name: str, cat_num: int) -> dict:
    """Generate TDK + ItemList JSON-LD for a category page."""
    title = f"{cat_name} - {SITE_NAME} | Electrical Cable Lugs & Terminals"
    desc = (
        f"Browse our full range of {cat_name.lower()} at {SITE_NAME}. "
        f"Professional manufacturer supplying high-quality electrical connectors, "
        f"cable lugs and terminals for global B2B buyers."
    )
    keywords = (
        f"{cat_name}, cable lugs, electrical terminals, connectors, {SITE_NAME}, "
        f"power fittings, Yiwu manufacturer, wholesale electrical components"
    )
    schema = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": cat_name,
        "description": desc,
        "url": f"{SITE_URL}/products-category-{cat_num}.html",
        "numberOfItems": 0  # will be filled dynamically if needed
    }
    return {"title": title, "desc": desc, "keywords": keywords, "schema": schema}


def homepage_meta() -> dict:
    """Generate TDK + Organization + WebSite JSON-LD for the homepage."""
    title = f"{SITE_NAME} — Professional Cable Lugs, Terminals & Connectors Manufacturer"
    desc = COMPANY_DESC
    keywords = (
        "cable lugs, electrical terminals, connectors, power fittings, "
        "bimetal lugs, aluminum lugs, copper terminals, insulated terminals, "
        "Yiwu manufacturer, B2B electrical components, wholesale power accessories"
    )
    org_schema = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": SITE_NAME,
        "url": SITE_URL,
        "logo": f"{SITE_URL}/images/logo.png",
        "description": COMPANY_DESC,
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "Yiwu Binwang Market A0-033~035",
            "addressLocality": "Yiwu",
            "addressRegion": "Zhejiang",
            "addressCountry": "CN"
        },
        "contactPoint": {
            "@type": "ContactPoint",
            "telephone": "+86-13566954989",
            "email": "sales@kdelec.com",
            "contactType": "sales",
            "availableLanguage": ["English", "Chinese"]
        }
    }
    web_schema = {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": SITE_NAME,
        "url": SITE_URL,
        "potentialAction": {
            "@type": "SearchAction",
            "target": f"{SITE_URL}/?s={chr(123)}search_term_string{chr(125)}",
            "query-input": "required name=search_term_string"
        }
    }
    return {
        "title": title, "desc": desc, "keywords": keywords,
        "schemas": [org_schema, web_schema]
    }


# ─── Category name lookup ───────────────────────────────────────────────

CATEGORY_NAMES = {
    1: "Cable Lugs and Connectors",
    2: "Insulated Terminals",
    3: "Cable Clamps",
}


# ─── Product name extractor ─────────────────────────────────────────────

def extract_product_name(html: str) -> str:
    """Extract the main <h1> product name from a product detail page."""
    m = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.DOTALL)
    if m:
        return re.sub(r'<[^>]+>', '', m.group(1)).strip()
    # fallback: try <title> and strip site suffix
    m = re.search(r'<title>(.*?)</title>', html)
    if m:
        raw = m.group(1).strip()
        return raw.replace(f" - {SITE_NAME}", "").replace(f" | {SITE_NAME}", "").strip()
    return "Electrical Component"


# ─── Injection helpers ──────────────────────────────────────────────────

META_TEMPLATE = (
    '<meta name="description" content="{desc}">\n'
    '  <meta name="keywords" content="{kw}">'
)

SCHEMA_TEMPLATE = '\n  <script type="application/ld+json">{json}</script>'


def inject_into_head(html: str, meta_desc: str, meta_kw: str, schemas: list[dict]) -> str:
    """Insert <meta description>, <meta keywords> and JSON-LD scripts before </head>."""
    meta_block = META_TEMPLATE.format(desc=meta_desc, kw=meta_kw)
    schema_blocks = "".join(
        SCHEMA_TEMPLATE.format(json=json.dumps(s, ensure_ascii=False))
        for s in schemas
    )
    injection = f"\n  {meta_block}{schema_blocks}\n"

    # Find </head> — it may be on the same line as other tags
    pattern = r'(</head>)'
    replacement = injection + r'\1'
    new_html = re.sub(pattern, replacement, html, count=1)

    if new_html == html:
        print("  ⚠️  WARNING: </head> not found — skipping injection")
    return new_html


def update_title(html: str, new_title: str) -> str:
    """Replace existing <title>...</title> with the new one."""
    pattern = r'<title>.*?</title>'
    replacement = f'<title>{new_title}</title>'
    return re.sub(pattern, replacement, html, flags=re.DOTALL, count=1)


# ─── Main processing ────────────────────────────────────────────────────

stats = {"processed": 0, "skipped": 0, "errors": 0}


def process_product_page(path: Path):
    """Process a single product detail page."""
    html = path.read_text(encoding="utf-8")
    product_id = path.parent.name  # e.g. "product-0001"
    name = extract_product_name(html)
    meta = product_meta(name, product_id)

    html = update_title(html, meta["title"])
    html = inject_into_head(html, meta["desc"], meta["keywords"], [meta["schema"]])

    path.write_text(html, encoding="utf-8")
    stats["processed"] += 1
    print(f"  ✅ {path.relative_to(BASE_DIR)}  |  {name}")


def process_category_page(path: Path):
    """Process a root-level category page (products-category-N.html)."""
    m = re.search(r'products-category-(\d+)\.html$', path.name)
    if not m:
        return
    num = int(m.group(1))
    cat_name = CATEGORY_NAMES.get(num, f"Category {num}")
    meta = category_meta(cat_name, num)

    html = path.read_text(encoding="utf-8")
    html = update_title(html, meta["title"])
    html = inject_into_head(html, meta["desc"], meta["keywords"], [meta["schema"]])

    path.write_text(html, encoding="utf-8")
    stats["processed"] += 1
    print(f"  ✅ {path.relative_to(BASE_DIR)}  |  {cat_name}")


def process_homepage(path: Path):
    """Process the homepage."""
    meta = homepage_meta()
    html = path.read_text(encoding="utf-8")
    html = update_title(html, meta["title"])
    html = inject_into_head(html, meta["desc"], meta["keywords"], meta["schemas"])
    path.write_text(html, encoding="utf-8")
    stats["processed"] += 1
    print(f"  ✅ {path.relative_to(BASE_DIR)}  |  Homepage")


def process_other_page(path: Path):
    """Add generic description to any remaining HTML page that lacks it."""
    html = path.read_text(encoding="utf-8")
    # Skip if already has description meta
    if re.search(r'<meta\s+name=["\']description["\']', html):
        stats["skipped"] += 1
        return
    kw = "Kunde Electric, electrical components, Yiwu manufacturer"
    html = inject_into_head(html, COMPANY_DESC, kw, [])
    path.write_text(html, encoding="utf-8")
    stats["processed"] += 1
    print(f"  ✅ {path.relative_to(BASE_DIR)}  |  generic meta added")


# ─── Entry point ────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 70)
    print("Kunde Electric — Batch SEO Meta + JSON-LD Injector")
    print("=" * 70)

    # 1. Homepage
    home = BASE_DIR / "index.html"
    if home.exists():
        print("\n Homepage:")
        process_homepage(home)

    # 2. Category pages (root level)
    print("\n📂 Category pages:")
    for f in sorted(BASE_DIR.glob("products-category-*.html")):
        process_category_page(f)

    # 3. Product detail pages
    print("\n Product detail pages:")
    product_dirs = sorted((BASE_DIR / "product").glob("product-*"))
    for d in product_dirs:
        idx = d / "index.html"
        if idx.exists():
            try:
                process_product_page(idx)
            except Exception as e:
                stats["errors"] += 1
                print(f"  ❌ {idx.relative_to(BASE_DIR)}  |  {e}")

    # 4. Remaining root-level HTML pages (about, contact, etc.)
    print("\n Other pages:")
    for f in sorted(BASE_DIR.glob("*.html")):
        if f.name in ("index.html",) or f.name.startswith("products-category"):
            continue
        if f.name.startswith(("deploy_", "update_", "optimize_", "cleanup_", "generate_")):
            continue
        try:
            process_other_page(f)
        except Exception as e:
            stats["errors"] += 1
            print(f"   {f.relative_to(BASE_DIR)}  |  {e}")

    # Summary
    print("\n" + "=" * 70)
    print(f"Done: {stats['processed']} processed | {stats['skipped']} skipped | {stats['errors']} errors")
    print("=" * 70)
