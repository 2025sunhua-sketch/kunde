#!/usr/bin/env python3
"""
Crop white borders from product detail images by scanning rows/columns.
Saves cropped version as <original_name>_cropped.<ext> in the same directory.
"""

import os
from PIL import Image

def crop_white_borders(image_path, output_path=None, white_threshold=240):
    """
    Crop pure white borders by scanning from each edge inward.
    
    Args:
        image_path: Path to source image
        output_path: Path for cropped output
        white_threshold: Pixel value >= this is considered "white" (0-255)
    """
    img = Image.open(image_path).convert('RGB')
    width, height = img.size
    pixels = img.load()
    
    def is_white(x, y):
        r, g, b = pixels[x, y]
        return r >= white_threshold and g >= white_threshold and b >= white_threshold
    
    # Scan from top to find first non-white row
    top = 0
    for y in range(height):
        # Check if entire row is white
        row_all_white = all(is_white(x, y) for x in range(width))
        if not row_all_white:
            top = y
            break
    
    # Scan from bottom
    bottom = height - 1
    for y in range(height - 1, -1, -1):
        row_all_white = all(is_white(x, y) for x in range(width))
        if not row_all_white:
            bottom = y
            break
    
    # Scan from left
    left = 0
    for x in range(width):
        col_all_white = all(is_white(x, y) for y in range(height))
        if not col_all_white:
            left = x
            break
    
    # Scan from right
    right = width - 1
    for x in range(width - 1, -1, -1):
        col_all_white = all(is_white(x, y) for y in range(height))
        if not col_all_white:
            right = x
            break
    
    # Add small padding (1% of dimension)
    pad_x = max(1, int(width * 0.01))
    pad_y = max(1, int(height * 0.01))
    
    left = max(0, left - pad_x)
    top = max(0, top - pad_y)
    right = min(width - 1, right + pad_x)
    bottom = min(height - 1, bottom + pad_y)
    
    cropped = img.crop((left, top, right + 1, bottom + 1))
    
    if output_path is None:
        base, ext = os.path.splitext(image_path)
        output_path = f"{base}_cropped{ext}"
    
    cropped.save(output_path, quality=95)
    
    print(f"  Original: {img.size}")
    print(f"  Cropped:  {cropped.size}")
    print(f"  Removed:  top={top}px, bottom={height-1-bottom}px, left={left}px, right={width-1-right}px")
    print(f"  Saved to: {output_path}")
    
    return True


if __name__ == '__main__':
    test_image = r"C:\Users\ADMIN\.jvs\.openclaw\workspace\kunde-website\images\products\product\1 Cable Lugs and Connectors\ACL Bolt Type Bimetal Cable Lugs\Cable Lugs and Connectors-Kunde Electric_15.jpg"
    
    if not os.path.exists(test_image):
        print(f"Error: File not found: {test_image}")
        exit(1)
    
    print(f"Processing: {os.path.basename(test_image)}")
    success = crop_white_borders(test_image)
    
    if success:
        print("\nDone! Verify the cropped version visually.")
