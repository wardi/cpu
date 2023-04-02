import numpy as np
from skimage.segmentation import flood_fill

def generate(width, height):
    arr = np.zeros((height, width), dtype=np.uint8)
    # walls
    arr[0] = 9
    arr[-1] = 9
    arr[..., 0] = 9
    arr[..., -1] = 9
    locs = np.swapaxes(np.where(arr == 0), 0, 1)
    # start/end
    start = (0, 1)
    end = (-1, -2)
    arr[start] = 0
    arr[end] = 0

    np.random.shuffle(locs)

    for lc in locs:
        lc = tuple(lc)
        y, x = lc
        if sum(e == 0 for e in (arr[y-1,x], arr[y+1,x], arr[y,x-1], arr[y, x+1])) < 2:
            continue
        arr[lc] = 8
        t = flood_fill(arr, start, 1, connectivity=1)
        if np.any(t == 0):
            arr[lc] = 0

    return arr


print(generate(10, 10))
