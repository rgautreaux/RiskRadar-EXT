"""
Remove white backgrounds from PNG files using flood-fill from image corners.
Only pixels connected to corners (by color tolerance) are made transparent.
"""
import os
import numpy as np
from PIL import Image
from collections import deque

TOLERANCE = 15  # how close to white a pixel must be to be treated as background


def is_near_white(pixel, tol=TOLERANCE):
    r, g, b, a = int(pixel[0]), int(pixel[1]), int(pixel[2]), int(pixel[3])
    return a >= 200 and r >= (255 - tol) and g >= (255 - tol) and b >= (255 - tol)


def flood_fill_alpha(data: np.ndarray, tol: int = TOLERANCE) -> np.ndarray:
    """BFS flood fill from all 4 corners; marks near-white background pixels transparent."""
    h, w = data.shape[:2]
    visited = np.zeros((h, w), dtype=bool)
    result = data.copy()

    queue = deque()

    # Seed from all 4 corners
    seeds = [(0, 0), (0, w - 1), (h - 1, 0), (h - 1, w - 1)]
    for r, c in seeds:
        if not visited[r, c] and is_near_white(data[r, c], tol):
            queue.append((r, c))
            visited[r, c] = True

    # BFS
    while queue:
        r, c = queue.popleft()
        # Make transparent
        result[r, c, 3] = 0

        # Check 4-connected neighbors
        for nr, nc in [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]:
            if 0 <= nr < h and 0 <= nc < w and not visited[nr, nc]:
                if is_near_white(data[nr, nc], tol):
                    visited[nr, nc] = True
                    queue.append((nr, nc))

    return result


files_to_fix = [
    r'c:\Users\rebec\OneDrive\Documents\GitHub\Team6-SeniorProject\frontend\RiskRadar\assets\icons\navigation\RiskRadar_ALERT_HomeBttn.png',
    r'c:\Users\rebec\OneDrive\Documents\GitHub\Team6-SeniorProject\frontend\RiskRadar\assets\images\wireframes\RiskRadar_MobileApp_Wireframe.png',
]

for path in files_to_fix:
    print(f'Processing: {os.path.basename(path)}')
    img = Image.open(path).convert('RGBA')
    data = np.array(img, dtype=np.uint8)

    result_data = flood_fill_alpha(data)

    result_img = Image.fromarray(result_data, 'RGBA')
    result_img.save(path, 'PNG')

    # Report how many pixels were made transparent
    orig_alpha = data[:, :, 3]
    new_alpha = result_data[:, :, 3]
    made_transparent = int(np.sum((orig_alpha >= 200) & (new_alpha == 0)))
    print(f'  -> Made {made_transparent} background pixels transparent. Saved.')

print('\nDone.')
