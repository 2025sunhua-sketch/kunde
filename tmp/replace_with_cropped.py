#!/usr/bin/env python3
"""
Replace original detail images with cropped versions and update HTML references.
Steps:
1. For each product, find the _cropped file referenced in index.html
2. Rename _cropped file to original filename (overwrite)
3. Update HTML reference back to original filename (remove _cropped suffix)
4. Delete the now-redundant _cropped file
"""

import os
import re
from pathlib import Path

BASE_DIR = Path(r"C:\Users\ADMIN\.jvs\.openclaw\workspace\kunde-website")
PRODUCT_DIR = BASE_DIR / "product"


def extract_detail_image_src(html_content):
    """Extract the detail image src from product HTML."""
    pattern = r'<img[^>]+class="detail-image"[^>]+src="([^"]+)"'
    match = re.search(pattern, html_content)
    if match:
        return match.group(1)
    pattern2 = r'<img[^>]+src="([^"]+)"[^>]+class="detail-image"'
    match2 = re.search(pattern2, html_content)
    if match2:
        return match2.group(1)
    return None


def process_product_dir(product_dir):
    """Process a single product directory."""
    index_html = product_dir / "index.html"
    if not index_html.exists():
        return False, "No index.html"

    html_content = index_html.read_text(encoding='utf-8')
    detail_src = extract_detail_image_src(html_content)

    if not detail_src:
        return False, "No detail image found"

    # Resolve absolute path of the currently referenced file (should be _cropped)
    if detail_src.startswith('/'):
        abs_path = BASE_DIR / detail_src.lstrip('/')
    else:
        abs_path = product_dir / detail_src

    if not abs_path.exists():
        return False, f"Referenced image not found: {abs_path}"

    filename = abs_path.name
    if '_cropped' not in filename:
        return True, "Already using original filename"

    # Derive original filename
    base, ext = os.path.splitext(filename)
    original_name = base.replace('_cropped', '') + ext
    original_path = abs_path.parent / original_name

    # Step 1: Overwrite original file with cropped version
    import shutil
    shutil.copy2(str(abs_path), str(original_path))

    # Step 2: Update HTML reference to original filename
    updated_html = html_content.replace(filename, original_name)
    index_html.write_text(updated_html, encoding='utf-8')

    # Step 3: Delete the _cropped file
    abs_path.unlink()

    return True, f"Overwritten {original_name}, HTML updated, _cropped deleted"


def main():
    if not PRODUCT_DIR.exists():
        print(f"Error: Product directory not found: {PRODUCT_DIR}")
        return

    product_dirs = sorted([d for d in PRODUCT_DIR.iterdir() if d.is_dir()])
    total = len(product_dirs)
    success_count = 0
    skip_count = 0
    fail_count = 0
    errors = []

    print(f"Replacing originals with cropped versions for {total} products...\n")

    for i, product_dir in enumerate(product_dirs, 1):
        status, message = process_product_dir(product_dir)
        if status:
            success_count += 1
            print(f"[{i}/{total}] OK {product_dir.name}: {message}")
        else:
            fail_count += 1
            errors.append((product_dir.name, message))
            print(f"[{i}/{total}] FAIL {product_dir.name}: {message}")

    print(f"\n{'='*60}")
    print(f"Summary:")
    print(f"  Total:     {total}")
    print(f"  Success:   {success_count}")
    print(f"  Failed:    {fail_count}")
    if errors:
        print(f"\nFailed products:")
        for name, msg in errors[:20]:
            print(f"  - {name}: {msg}")
        if len(errors) > 20:
            print(f"  ... and {len(errors) - 20} more")


if __name__ == '__main__':
    main()
