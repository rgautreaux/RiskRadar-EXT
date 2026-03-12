import os
from PIL import Image
import numpy as np

frontend_dir = r'c:\Users\rebec\OneDrive\Documents\GitHub\Team6-SeniorProject\frontend'

png_files = []
for root, dirs, files in os.walk(frontend_dir):
    for f in files:
        if f.lower().endswith('.png'):
            png_files.append(os.path.join(root, f))

print(f'Found {len(png_files)} PNG files\n')

needs_fix = []

for path in png_files:
    img = Image.open(path).convert('RGBA')
    data = np.array(img)
    h, w = data.shape[:2]

    # Check all 4 corners for white/near-white opaque pixels
    corners = [data[0, 0], data[0, w-1], data[h-1, 0], data[h-1, w-1]]
    corner_white = any(
        int(px[0]) >= 240 and int(px[1]) >= 240 and int(px[2]) >= 240 and int(px[3]) >= 200
        for px in corners
    )

    # Count near-white opaque pixels across whole image
    white_mask = (
        (data[:, :, 0] >= 240) &
        (data[:, :, 1] >= 240) &
        (data[:, :, 2] >= 240) &
        (data[:, :, 3] >= 200)
    )
    white_count = int(np.sum(white_mask))

    rel = os.path.relpath(path, frontend_dir)
    status = "WHITE_BG" if corner_white else "OK"
    print(f'[{status:8s}] {rel}  white_pixels={white_count}')

    if corner_white:
        needs_fix.append(path)

print(f'\n{len(needs_fix)} file(s) need background removal.')
