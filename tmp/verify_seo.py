import re
from pathlib import Path

BASE = Path(r"C:\Users\ADMIN\.jvs\.openclaw\workspace\kunde-website")
samples = [
    "product/product-0001/index.html",
    "product/product-0150/index.html",
    "index.html",
    "products-category-1.html",
    "about.html",
]

print("=" * 70)
for rel in samples:
    p = BASE / rel
    if not p.exists():
        print(f" {rel} — file not found")
        continue
    html = p.read_text(encoding="utf-8")
    ld_count = len(re.findall(r'application/ld\+json', html))
    desc_count = len(re.findall(r'<meta\s+name=["\']description["\']', html))
    kw_count = len(re.findall(r'<meta\s+name=["\']keywords["\']', html))
    title_m = re.search(r'<title>(.*?)</title>', html)
    title = title_m.group(1)[:60] + "..." if title_m else "(missing)"
    print(f"✅ {rel}")
    print(f"   Title:       {title}")
    print(f"   JSON-LD:     {ld_count} block(s)")
    print(f"   Description: {'present' if desc_count else 'MISSING'}")
    print(f"   Keywords:    {'present' if kw_count else 'MISSING'}")
    print()
print("=" * 70)
