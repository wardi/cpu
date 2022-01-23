#!/usr/bin/env python3

import sys
import gzip
from itertools import zip_longest, repeat

SRC_FRAMES = 6586
SRC_FPS = 30
EEPROM_SIZE = 32768 - 5 # init
BYTES_PER_FRAME = EEPROM_SIZE / SRC_FRAMES # 4.974 bytes/frame allowance

PIXELS = 5  # horizontal pixels per cgram character
LINES = 8  # vertical pixels per cgram character
COLS = 8
ROWS = 4

ALL_0 = b'\x00' * 8
ALL_1 = b'\x1f' * 8

# strategy:
# if cursor already on cell that needs to be all 0s or all 1s
# - (advance 1): ' ' or '\xff'
# choose the next cell that needs to be all 0s or all 1s next in order (leftmost applicable)
# - (advance 2): position, ' ' or '\xff'
# if none choose the cell with delta > 2 next in order
# - if assigned (advance 7):  * or update-in-place (advance <7)
#     cgposition, 8 * bit pattern
# - if unassigned, 1+ available (advance 9):
#     cgposition, 8 * bit pattern, position, cgchar
# - else (advance 11):
#     reorder oldest assigned to last
#     position of oldest assigned, ' ' or '\xff'
#     cgposition, 8 * bit pattern, position, cgchar
# if none choose the cell delta > 0 next in order
# - if assigned (advance 7):
#     cgposition, 8 * bit pattern
# - if unassigned, 1+ available (advance 9):
#     cgposition, 8 * bit pattern, position, cgchar
# if none emit NOP (advance 1)

order = """
6sekbpi8
q91mw4ug
j3hv7rdn
co5ft2la
"""


w = sys.stdout.write

w('CLR +\n')

pos = 0   #  0-7 row 1,  10-17 row 2,  20-27 row 3,  30-37 row 4,  40+ cgram
display_pixels = bytearray(COLS * ROWS * LINES)
bytes_sent = 0
file_frame = 0
frame_pixels = None

input_file = gzip.open(sys.argv[1], 'rb')

def read_frame():
    return input_file.read(COLS * ROWS * LINES)

def intpixels(pixels):
    "return [[0/1, ...],...] pixel values from top left to bottom right"
    ipx = []
    for y in range(LINES * ROWS + ROWS - 1):
        if y % (LINES + 1) == LINES:
            ipx.append([0] * (PIXELS * COLS + COLS - 1))
            continue
        cell_y = y // (LINES + 1)
        line = y % (LINES + 1)
        row = []
        ipx.append([int(b) for b in
            '0'.join(
                '{:05b}'.format(pixels[
                    cell_y * (LINES * COLS) + x * LINES + line
                ])
                for x in range(COLS)
            )
        ])
    return ipx

def braillepixels(ipx):
    "return braille text version of intpixel matrix"
    braille = []
    # padded intpixel matrix to avoid IndexErrors
    pipx = [r + [0] for r in ipx] + [[0] * (len(ipx[0]) + 1)] * 7
    for y in range(0, len(ipx), 4):
        braille.append(''.join(
            chr(0x2800
                + 1 * pipx[y][x]
                + 2 * pipx[y + 1][x]
                + 4 * pipx[y + 2][x]
                + 8 * pipx[y][x + 1]
                + 16 * pipx[y + 1][x + 1]
                + 32 * pipx[y + 2][x + 1]
                + 64 * pipx[y + 3][x]
                + 128 * pipx[y + 3][x + 1]
            ) for x in range(0, len(ipx[0]), 2)
        ))
    return braille

def pixeldelta(a, b):
    return bin(
        int.from_bytes(a, 'little') ^ int.from_bytes(b, 'little')
    ).count('1')

def print_state():
    for cols in zip_longest(
            braillepixels(intpixels(frame_pixels)),
            [],
            braillepixels(intpixels(display_pixels)),
            [
                f'frame {file_frame}',
                f'position {pos}',
                'delta {}'.format(
                    pixeldelta(frame_pixels, display_pixels))
            ],
            fillvalue = '',
        ):
        print('#', *cols)

def cell(p, pixels, cgram=b''):
    "Return 8 pixel-bytes at position p"
    if p >= 40:
        if p > 103:
            raise IndexError()
        return cgram[p - 40:][:8]
    if p >= 30:
        if p > 37:
            raise IndexError()
        return pixels[LINES * COLS * 3 + (p - 30) * LINES:][:8]
    if p >= 20:
        if p > 27:
            raise IndexError()
        return pixels[LINES * COLS * 2 + (p - 20) * LINES:][:8]
    if p >= 10:
        if p > 17:
            raise IndexError()
        return pixels[LINES * COLS * 1 + (p - 10) * LINES:][:8]
    if p > 7:
        raise IndexError()
    return pixels[p * LINES:][:8]

def writecell(pat, p, pixels):
    "Set 8 pixel-bytes at position p to pat"
    assert len(pat) == 8
    if p >= 40:
        if p > 103:
            raise IndexError()
        cgram[p - 40:p - 40 + 8] = pat
        return
    if p >= 30:
        if p > 37:
            raise IndexError()
        off = LINES * COLS * 3 + (p - 30) * LINES
    elif p >= 20:
        if p > 27:
            raise IndexError()
        off = LINES * COLS * 2 + (p - 20) * LINES
    elif p >= 10:
        if p > 17:
            raise IndexError()
        off = LINES * COLS * 1 + (p - 10) * LINES
    elif p > 7:
        raise IndexError()
    else:
        off = p * LINES
    pixels[off:off + 8] = pat

def sim(b):
    global pos, display_pixels, bytes_sent
    w(f'{repr(b)} +\n')
    if b == b'\xff':
        writecell(ALL_1, pos, display_pixels)
    elif b == b' ':
        writecell(ALL_0, pos, display_pixels)
    bytes_sent += 1
    pos += 1

while True:
    frame_pixels = read_frame()
    file_frame += 1
    if not frame_pixels:
        break
    while bytes_sent / EEPROM_SIZE < file_frame / SRC_FRAMES:
# if cursor already on cell that needs to be all 0s or all 1s
# - (advance 1): ' ' or '\xff'
        try:
            here = cell(pos, frame_pixels)
        except IndexError:
            pass
        else:
            if here in (ALL_0, ALL_1) and here != cell(pos, display_pixels):
                sim(b'\xff' if here == ALL_1 else b' ')
                continue
# choose the next cell that needs to be all 0s or all 1s next in order (leftmost applicable)
        break

    print_state()

