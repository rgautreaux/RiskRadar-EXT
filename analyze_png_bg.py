import os
from PIL import Image
import numpy as np

frontend_dir = r'c:\Users\rebec\OneDrive\Documents\GitHub\Team6-SeniorProject\frontend'

png_files = []
for root, dirs, files in os.walk(frontend_dir):
    # Skip node_modules and .expo cache
    if 'node_modules' in root or '.expo' in root:
        continue
    for f in files:
        if f.lower().endswith('.png'):
            png_files.append(os.path.join(root, f))

print(f'Found {len(png_files)} project PNG files (excluding node_modules)\n')

needs_fix = []

for path in png_files:
    img = Image.open(path).convert('RGBA')
    data = np.array(img, dtype=np.int32)
    h, w = data.shape[:2]
    total_pixels = h * w

    # Near-white opaque mask
    white_mask = (
        (data[:, :, 0] >= 240) &
        (data[:, :, 1] >= 240) &
        (data[:, :, 2] >= 240) &
        (data[:, :, 3] >= 200)
    )
    white_count = int(np.sum(white_mask))
    white_pct = 100.0 * white_count / total_pixels

    # Check corners
    corners = [data[0, 0], data[0, w-1], data[h-1, 0], data[h-1, w-1]]
    corner_white = sum(
        1 for px in corners
        if int(px[0]) >= 240 and int(px[1]) >= 240 and int(px[2]) >= 240 and int(px[3]) >= 200
    )

    # Check edges (5% band around perimeter)
    band = max(1, int(h * 0.05)), max(1, int(w * 0.05))
    top_band = white_mask[:band[0], :]
    bottom_band = white_mask[h-band[0]:, :]
    left_band = white_mask[:, :band[1]]
    right_band = white_mask[:, w-band[1]:]
    edge_white_pct = 100.0 * (
        int(np.sum(top_band)) + int(np.sum(bottom_band)) +
        int(np.sum(left_band)) + int(np.sum(right_band))
    ) / (2 * band[0] * w + 2 * band[1] * h)

    # Original mode before RGBA conversion
    orig_mode = Image.open(path).mode

    # Decision: likely white background if corners or edges are predominantly white
    has_white_bg = corner_white >= 2 or (corner_white >= 1 and edge_white_pct > 80)

    rel = os.path.relpath(path, frontend_dir)
    flag = "WHITE_BG" if has_white_bg else "OK"
    print(f'[{flag:8s}] {rel}')
    print(f'           mode={orig_mode}, size={w}x{h}, white={white_pct:.1f}%, corners_white={corner_white}/4, edge_white={edge_white_pct:.1f}%')

    if has_white_bg:
        needs_fix.append((path, rel))

print(f'\n{len(needs_fix)} file(s) need background removal:')
for path, rel in needs_fix:
    print(f'  {rel}')
