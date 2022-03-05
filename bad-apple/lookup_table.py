#!/usr/bin/env python3
'''
usage:
    lookup_table.py > baconsts.py

overwrites ltable.bin
'''

# byte order from top->bottom, left->right
# (mnemonic:)hex-value
hex_map = """
C00:04 C20:05 12 13 14 15 16 17 D00:08 D16:09 D32:0a C40:06 E00:0c E16:0d E32:0e C60:07
CLR:00 C21:05 12 13 14 15 16 17 D01:08 D17:09 C01:04 C41:06 E01:0c E17:0d E33:0e C61:07
HOM:00 C22:05 12 13 14 15 16 17 D02:08 D18:09 C02:04 C42:06 E02:0c E18:0d E34:0e C62:07
CRT:01 C23:05 12 13 14 15 16 17 D03:08 D19:09 C03:04 C43:06 E03:0c E19:0d E35:0e C63:07
ED0:00 C24:05 12 13 14 15 16 17 D04:08 D20:09 C04:04 C44:06 E04:0c E20:0d E36:0e C64:07
ED1:00 C25:05 12 13 14 15 16 17 D05:08 D21:09 C05:04 C45:06 E05:0c E21:0d E37:0e C65:07
EI0:00 C26:05 12 13 14 15 16 17 D06:08 D22:09 C06:04 C46:06 E06:0c E22:0d E38:0e C66:07
EI1:00 CLF:01 12 13 14 15 16 17 D07:08 D23:09 C07:04 C47:06 E07:0c E23:0d C27:05 C67:07
CG0:10 INI:03 12 13 14 15 16 17 D08:08 D24:09 C10:04 C50:06 E08:0c E24:0d C30:05 C70:07
CG1:10 SRT:01 12 13 14 15 16 17 D09:08 D25:09 C11:04 C51:06 E09:0c E25:0d C31:05 C71:07
CG2:10 HLT:80 12 13 14 15 16 17 D10:08 D26:09 C12:04 C52:06 E10:0c E26:0d C32:05 C72:07
CG3:10 OFF:00 12 13 14 15 16 17 D11:08 D27:09 C13:04 C53:06 E11:0c E27:0d C33:05 C73:07
CG4:10 HID:00 12 13 14 15 16 17 D12:08 D28:09 C14:04 C54:06 E12:0c E28:0d C34:05 C74:07
CG5:10 BLI:00 12 13 14 15 16 17 D13:08 D29:09 C15:04 C55:06 E13:0c E29:0d C35:05 C75:07
CG6:10 CUR:00 12 13 14 15 16 17 D14:08 D30:09 C16:04 C56:06 E14:0c E30:0d C36:05 C76:07
CG7:10 C77:07 12 13 14 15 16 17 D15:08 D31:09 C17:04 C57:06 E15:0c E31:0d C37:05 1f
"""

rows = hex_map.strip().split('\n')
assert len(rows) == 16, f'Expecting 16 rows, found {len(rows)}'

for i, r in enumerate(rows):
    cells = r.split()
    assert len(cells) == 16, f'Row {i} should have 16 cells: {cells}'

columns = zip(*(r.split() for r in rows))

with open('ltable.bin', 'wb') as f:
    for i, cell in enumerate(cell for col in columns for cell in col):
        mnemonic, sep, code = cell.rpartition(':')
        if sep:
           print(rf'{mnemonic} = b"\x{i:02x}"')
        f.write(bytes([int(code, 16)]))
