#!/usr/bin/env python3
"""
Batch crop white borders from ALL product detail images and update HTML references.
Processes all 322 product directories under product/.
"""

import os
import re
from pathlib import Path
from PIL import Image

BASE_DIR = Path(r"C:\Users\ADMIN\.jvs\.openclaw\workspace\kunde-website")
PRODUCT_DIR = BASE_DIR / "product"
WHITE_THRESHOLD = 240


def crop_white_borders(image_path, output_path=None):
    """Crop pure white borders by scanning rows/columns."""
    img = Image.open(image_path).convert('RGB')
    width, height = img.size
    pixels = img.load()

    def is_white(x, y):
        r, g, b = pixels[x, y]
        return r >= WHITE_THRESHOLD and g >= WHITE_THRESHOLD and b >= WHITE_THRESHOLD

    # Scan top
    top = 0
    for y in range(height):
        if not all(is_white(x, y) for x in range(width)):
            top = y
            break

    # Scan bottom
    bottom = height - 1
    for y in range(height - 1, -1, -1):
        if not all(is_white(x, y) for x in range(width)):
            bottom = y
            break

    # Scan left
    left = 0
    for x in range(width):
        if not all(is_white(x, y) for y in range(height)):
            left = x
            break

    # Scan right
    right = width - 1
    for x in range(width - 1, -1, -1):
        if not all(is_white(x, y) for y in range(height)):
            right = x
            break

    # Add 1% padding
    pad_x = max(1, int(width * 0.01))
    pad_y = max(1, int(height * 0.01))
    left = max(0, left - pad_x)
    top = max(0, top - pad_y)
    right = min(width - 1, right + pad_x)
    bottom = min(height - 1, bottom + pad_y)

    cropped = img.crop((left, top, right + 1, bottom + 1))

    if output_path is None:
        base, ext = os.path.splitext(str(image_path))
        output_path = f"{base}_cropped{ext}"

    cropped.save(output_path, quality=95)
    return True


def extract_detail_image_src(html_content):
    """Extract the detail image src from product HTML (non-digit-named images in .detail-grid)."""
    # Match <img ... class="detail-image" src="..." ...>
    pattern = r'<img[^>]+class="detail-image"[^>]+src="([^"]+)"'
    match = re.search(pattern, html_content)
    if match:
        return match.group(1)
    # Fallback: try without class attribute order variation
    pattern2 = r'<img[^>]+src="([^"]+)"[^>]+class="detail-image"'
    match2 = re.search(pattern2, html_content)
    if match2:
        return match2.group(1)
    return None


def update_html_detail_image(html_content, old_filename, new_filename):
    """Replace detail image filename in HTML content."""
    # Replace occurrences of the old filename with _cropped version
    # Handle both direct filename and full path references
    updated = html_content.replace(old_filename, new_filename)
    return updated


def process_product_dir(product_dir):
    """Process a single product directory: crop detail image and update HTML."""
    index_html = product_dir / "index.html"
    if not index_html.exists():
        return False, "No index.html"

    html_content = index_html.read_text(encoding='utf-8')
    detail_src = extract_detail_image_src(html_content)

    if not detail_src:
        return False, "No detail image found"

    # Resolve absolute path
    if detail_src.startswith('/'):
        abs_path = BASE_DIR / detail_src.lstrip('/')
    else:
        abs_path = product_dir / detail_src

    if not abs_path.exists():
        return False, f"Image not found: {abs_path}"

    # Generate cropped filename
    base, ext = os.path.splitext(str(abs_path))
    cropped_path = f"{base}_cropped{ext}"

    # Skip if already cropped
    if os.path.exists(cropped_path):
        # Still need to check if HTML references it
        cropped_filename = os.path.basename(cropped_path)
        if cropped_filename in html_content:
            return True, "Already processed"
        # Update HTML to reference existing cropped file
        original_filename = os.path.basename(str(abs_path))
        updated_html = update_html_detail_image(html_content, original_filename, cropped_filename)
        index_html.write_text(updated_html, encoding='utf-8')
        return True, "HTML updated (cropped image existed)"

    # Crop the image
    try:
        crop_white_borders(str(abs_path), cropped_path)
    except Exception as e:
        return False, f"Crop failed: {e}"

    # Update HTML reference
    original_filename = os.path.basename(str(abs_path))
    cropped_filename = os.path.basename(cropped_path)
    updated_html = update_html_detail_image(html_content, original_filename, cropped_filename)
    index_html.write_text(updated_html, encoding='utf-8')

    return True, f"Cropped and HTML updated"


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

    print(f"Processing {total} product directories...\n")

    for i, product_dir in enumerate(product_dirs, 1):
        status, message = process_product_dir(product_dir)
        if status:
            success_count += 1
            print(f"[{i}/{total}] ✓ {product_dir.name}: {message}")
        else:
            fail_count += 1
            errors.append((product_dir.name, message))
            print(f"[{i}/{total}] ✗ {product_dir.name}: {message}")

    print(f"\n{'='*60}")
    print(f"Summary:")
    print(f"  Total:     {total}")
    print(f"  Success:   {success_count}")
    print(f"  Failed:    {fail_count}")
    if errors:
        print(f"\nFailed products:")
        for name, msg in errors[:20]:  # Show first 20 errors
            print(f"  - {name}: {msg}")
        if len(errors) > 20:
            print(f"  ... and {len(errors) - 20} more")


if __name__ == '__main__':
    main()
