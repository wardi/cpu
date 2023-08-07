#!/usr/bin/env python3

import sys
import numpy as np
from skimage.segmentation import flood_fill
from skimage.io import imread
from skimage.color import rgb2gray


# mask for cells above, below, left and right
neighbours = np.array([
    [0, 1, 0],
    [1, 0, 1],
    [0, 1, 0]], dtype=np.uint8)

def maze3(arr, gen):
    if not gen:
        gen = np.random.default_rng()

    unfilled = np.swapaxes(np.where(arr == 0), 0, 1)
    gen.shuffle(unfilled)

    start = tuple(coord[0] for coord in np.where(arr == 2))
    arr = np.copy(arr)
    arr[arr == 2] = 0

    for lc in unfilled:
        lc = tuple(lc)

        y, x = lc
        # protect dead-ends from becoming walls
        if np.sum(neighbours * arr[y-1:y+2, x-1:x+2]) > 2:
            continue

        arr[lc] = 1
        t = flood_fill(arr, start, 1, connectivity=1)
        if np.any(t == 0):
            arr[lc] = 0

    return arr


def maze_from_template(fname, gen=None):
    n = imread(fname)
    n = np.array((n[...,0] == 188) + (n[...,0] == 252) * 2, dtype=np.uint8)
    return maze3(n, gen)


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
    mz = maze_from_template(sys.argv[1], np.random.default_rng(int(sys.argv[2])))
    try:
        output_name = sys.argv[3]
    except IndexError:
        for l in braillepixels(mz):
            print(l)
    else:
        np.savetxt(output_name, mz, '%1d', '')
