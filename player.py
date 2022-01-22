#!/usr/bin/env python3

SRC_FRAMES = 6586
SRC_FPS = 30
EEPROM_SIZE = 32768 - 5 # init
BYTES_PER_FRAME = EEPROM_SIZE / SRC_FRAMES # 4.974 bytes/frame allowance

PIXELS = 5  # horizontal pixels per cgram character
LINES = 8  # vertical pixels per cgram character
COLS = 8
ROWS = 4

order = """
6sekbpi8
q91mw4ug
j3hv7rdn
co5ft2la
"""

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


import sys
w = sys.stdout.write

w('CLR +\n')

pos = 0   #  0-7 row 1,  10-17 row 2,  20-27 row 3,  30-37 row 4,  40+ cgram
display_pixels = bytearray(COLS * ROWS * LINES)
bytes_sent = 0
file_frame = 0

frame_pixels = sys.stdin.buffer.read(COLS * ROWS * LINES)

def draw(pixels):
    #print('\x1b[H', end='')
    for y in range(LINES * ROWS + ROWS - 1):
        if y % (LINES + 1) == LINES:
            print('-' * (PIXELS * COLS + COLS - 1))
            continue
        cell_y = y // (LINES + 1)
        line = y % (LINES + 1)
        print('-'.join(
            '{:05b}'.format(pixels[cell_y * (LINES * COLS) + x * LINES + line])
            .replace('0', ' ')
            .replace('1', 'X')
            for x in range(COLS)
        ))

draw(frame_pixels)
