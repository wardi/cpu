

order = """
6sekbpi8
q91mw4ug
j3hv7rdn
co5ft2la
"""

# strategy:
# choose the next cell that needs to be all 0s or all 1s next in order
# - (advance 2): position, ' ' or '\xff'
# if none choose the cell with delta > 2 next in order
# - if assigned (advance 7):
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
