#!/usr/bin/env python3
'''
usage:
    lookup_table.py > cmdconsts.py

overwrites ltable.bin
'''

# byte order from top->bottom, left->right
# (opcode:)hex-value
hex_map = """
    1 1 B00:1     1 C00:0 1 1 1 D00:0 D16:0 D32:0 B16:1 E00:0 E16:0 E32:0     1
CLR:0 1 B01:1     1     1 1 1 1 D01:0 D17:0 D33:0 B17:1 E01:0 E17:0 E33:0     1
    1 1 B02:1     1     1 1 1 1 D02:0 D18:0 D34:0 B18:1 E02:0 E18:0 E34:0     1
    1 1 B03:1     1     1 1 1 1 D03:0 D19:0 D35:0 B19:1 E03:0 E19:0 E35:0     1
CG4:1 1 B04:1     1     1 1 1 1 D04:0 D20:0 D36:0 B20:1 E04:0 E20:0 E36:0     1
    1 1 B05:1     1     1 1 1 1 D05:0 D21:0 D37:0 B21:1 E05:0 E21:0 E37:0     1
EIN:0 1 B06:1     1     1 1 1 1 D06:0 D22:0 D38:0 B22:1 E06:0 E22:0 E38:0     1
    1 1 B07:1     1     1 1 1 1 D07:0 D23:0 D39:0 B23:1 E07:0 E23:0 E39:0     1
CG0:1 1 B08:1     1 C10:0 1 1 1 D08:0 D24:0     1 B24:1 E08:0 E24:0     1     1
CG1:1 1 B09:1     1     1 1 1 1 D09:0 D25:0     1 B25:1 E09:0 E25:0     1     1
CG2:1 1 B10:1     1     1 1 1 1 D10:0 D26:0     1 B26:1 E10:0 E26:0     1     1
CG3:1 1 B11:1 INI:0     1 1 1 1 D11:0 D27:0     1 B27:1 E11:0 E27:0     1     1
HID:0 1 B12:1     1     1 1 1 1 D12:0 D28:0     1 B28:1 E12:0 E28:0     1     1
CG5:1 1 B13:1     1     1 1 1 1 D13:0 D29:0     1 B29:1 E13:0 E29:0     1     1
CG6:1 1 B14:1     1     1 1 1 1 D14:0 D30:0     1 B30:1 E14:0 E30:0     1     1
CG7:1 1 B15:1     1     1 1 1 1 D15:0 D31:0     1 B31:1 E15:0 E31:0     1 BLK:1
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
