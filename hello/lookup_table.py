#!/usr/bin/env python3
'''
usage:
    lookup_table.py > cmdconsts.py

overwrites ltable.bin
'''

# byte order from top->bottom, left->right
# (opcode:)hex-value
hex_map = """
    1 1 1     1 1 1 1 1 1 1 1 1 1 1 1 1
CLR:0 1 1     1 1 1 1 1 1 1 1 1 1 1 1 1
    1 1 1     1 1 1 1 1 1 1 1 1 1 1 1 1
    1 1 1     1 1 1 1 1 1 1 1 1 1 1 1 1
    1 1 1     1 1 1 1 1 1 1 1 1 1 1 1 1
    1 1 1     1 1 1 1 1 1 1 1 1 1 1 1 1
EIN:0 1 1     1 1 1 1 1 1 1 1 1 1 1 1 1
    1 1 1     1 1 1 1 1 1 1 1 1 1 1 1 1
    1 1 1     1 1 1 1 1 1 1 1 1 1 1 1 1
    1 1 1     1 1 1 1 1 1 1 1 1 1 1 1 1
    1 1 1     1 1 1 1 1 1 1 1 1 1 1 1 1
    1 1 1 INI:0 1 1 1 1 1 1 1 1 1 1 1 1
    1 1 1     1 1 1 1 1 1 1 1 1 1 1 1 1
    1 1 1     1 1 1 1 1 1 1 1 1 1 1 1 1
CUR:0 1 1     1 1 1 1 1 1 1 1 1 1 1 1 1
    1 1 1     1 1 1 1 1 1 1 1 1 1 1 1 1
"""

rows = hex_map.strip().split('\n')
assert len(rows) == 16, f'Expecting 16 rows, found {len(rows)}'

for i, r in enumerate(rows):
    cells = r.split()
    assert len(cells) == 16, f'Row {i} should have 16 cells: {cells}'

columns = zip(*(r.split() for r in rows))

with open('ltable.bin', 'wb') as f:
    for i, cell in enumerate(cell for col in columns for cell in col):
        opcode, sep, code = cell.rpartition(':')
        if sep:
           print(rf'{opcode} = b"\x{i:02x}"')
        f.write(bytes([int(code, 16)]))
