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
        arr[lc] = 1
        t = flood_fill(arr, start, 1, connectivity=1)
        if np.any(t == 0):
            arr[lc] = 0

    return arr


def braillepixels(a):
    "return braille text version of array"
    braille = []
    # padded matrix to avoid IndexErrors
    pa = np.pad(a, ((0, 7), (0, 1)))
    for y in range(0, len(a), 4):
        braille.append(''.join(
            chr(0x2800
                + 1 * bool(pa[y, x])
                + 2 * bool(pa[y + 1, x])
                + 4 * bool(pa[y + 2, x])
                + 8 * bool(pa[y, x + 1])
                + 16 * bool(pa[y + 1, x + 1])
                + 32 * bool(pa[y + 2, x + 1])
                + 64 * bool(pa[y + 3, x])
                + 128 * bool(pa[y + 3, x + 1])
            ) for x in range(0, a.shape[1], 2)
        ))
    return braille


for p in braillepixels(generate(100, 100)):
    print(p)
