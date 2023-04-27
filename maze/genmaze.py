#!/usr/bin/env python3

import sys
import numpy as np
from skimage.segmentation import flood_fill


room = np.array([
    [0, 1, 1, 0, 1, 1, 0],
    [1, 2, 2, 2, 2, 2, 1],
    [1, 2, 2, 2, 2, 2, 1],
    [0, 2, 2, 1, 2, 2, 0],
    [1, 2, 2, 2, 2, 2, 1],
    [1, 2, 2, 2, 2, 2, 1],
    [0, 1, 1, 0, 1, 1, 0],
], dtype=np.uint8)

lanes = np.array([
    [1, 0, 1, 0, 1, 0, 1],
    [1, 2, 1, 2, 1, 2, 1],
    [0, 2, 1, 2, 1, 2, 0],
    [1, 1, 1, 2, 1, 1, 1],
    [0, 2, 1, 2, 1, 2, 0],
    [1, 2, 1, 2, 1, 2, 1],
    [1, 0, 1, 0, 1, 0, 1],
], dtype=np.uint8)

spiral = np.array([
    [0, 0, 2, 2, 2, 0, 0],
    [1, 2, 2, 1, 1, 1, 0],
    [1, 2, 1, 2, 2, 2, 1],
    [1, 2, 1, 2, 1, 2, 1],
    [1, 2, 2, 2, 1, 2, 1],
    [0, 1, 1, 1, 2, 2, 1],
    [0, 0, 2, 2, 2, 0, 0],
], dtype=np.uint8)

def box(width, height):
    arr = np.zeros((height, width), dtype=np.uint8)
    # walls
    arr[0] = 1
    arr[-1] = 1
    arr[..., 0] = 1
    arr[..., -1] = 1
    start = (0, 1)
    end = (-1, -2)
    arr[start] = 2
    arr[end] = 2
    return arr


def ant_nest(arr, generator=None):
    if not generator:
        generator = np.random.default_rng()

    locs = np.swapaxes(np.where(arr == 0), 0, 1)
    generator.shuffle(locs)

    start = next(zip(*np.where(arr == 2)))
    arr[arr == 2] = 0

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


if __name__ == '__main__':
    mz = ant_nest(box(35,35), np.random.default_rng(42))
    try:
        output_name = sys.argv[1]
    except IndexError:
        for l in braillepixels(mz):
            print(l)
    else:
        np.save(output_name, mz, allow_pickle=False)
