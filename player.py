#!/usr/bin/src python3

SRC_FRAMES = 6586
SRC_FPS = 30
EEPROM_SIZE = 32768 - 5 # init
BYTES_PER_FRAME = EEPROM_SIZE / SRC_FRAMES # 4.974 bytes/frame allowance

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
