#!/usr/bin/env python3
'''
usage:
    lookup_table.py > cmdconsts.py

overwrites ltable.bin
'''

additional_pins = {
    8: 'R',
    9: 'L',
    10: 'U',
    11: 'D',
    13: 'B',
    14: 'A',
    12: 'S2',
    15: 'S1',
    16: 'S0',
}

inputs = {i: 2**pin for pin, i in additional_pins.items() if len(i) == 1}
states = {i: 2**pin for pin, i in additional_pins.items() if len(i) == 2}


# byte order from top->bottom, left->right
# (opcode:)hex-value

# 0x80 -> RS=1
# 0x40 -> E on /clk
# 0x00-07 -> next state is 0-7

hex_map = """
    C0 JM0:01 B00:C0     C0 C00:40 C0 C0 C0 D00:40 D16:40 D32:40 B16:C0 E00:40 E16:40 E32:40 C0
CLR:40 JM1:01 B01:C0     C0     C0 C0 C0 C0 D01:40 D17:40 D33:40 B17:C0 E01:40 E17:40 E33:40 C0
HOM:40 JM2:01 B02:C0     C0     C0 C0 C0 C0 D02:40 D18:40 D34:40 B18:C0 E02:40 E18:40 E34:40 C0
JM3:01   R:40 B03:C0     C0     C0 C0 C0 C0 D03:40 D19:40 D35:40 B19:C0 E03:40 E19:40 E35:40 C0
CG4:C0 JM4:01 B04:C0     C0     C0 C0 C0 C0 D04:40 D20:40 D36:40 B20:C0 E04:40 E20:40 E36:40 C0
JM5:01   L:40 B05:C0     C0     C0 C0 C0 C0 D05:40 D21:40 D37:40 B21:C0 E05:40 E21:40 E37:40 C0
EIN:40 JM6:01 B06:C0     C0     C0 C0 C0 C0 D06:40 D22:40 D38:40 B22:C0 E06:40 E22:40 E38:40 C0
    C0 JM7:01 B07:C0     C0     C0 C0 C0 C0 D07:40 D23:40 D39:40 B23:C0 E07:40 E23:40 E39:40 C0
CG0:C0  SR:40 B08:C0     C0     C0 C0 C0 C0 D08:40 D24:40     C0 B24:C0 E08:40 E24:40     C0 C0
CG1:C0 HXU:04 B09:C0     C0     C0 C0 C0 C0 D09:40 D25:40     C0 B25:C0 E09:40 E25:40     C0 C0
CG2:C0 HXD:04 B10:C0     C0     C0 C0 C0 C0 D10:40 D26:40     C0 B26:C0 E10:40 E26:40     C0 C0
CG3:C0 HXL:04 B11:C0 INI:40     C0 C0 C0 C0 D11:40 D27:40     C0 B27:C0 E11:40 E27:40     C0 C0
HID:40  SL:40 B12:C0     C0     C0 C0 C0 C0 D12:40 D28:40     C0 B28:C0 E12:40 E28:40     C0 C0
CG5:C0 HXR:04 B13:C0     C0     C0 C0 C0 C0 D13:40 D29:40     C0 B29:C0 E13:40 E29:40     C0 C0
CG6:C0 HXB:04 B14:C0     C0     C0 C0 C0 C0 D14:40 D30:40     C0 B30:C0 E14:40 E30:40     C0 C0
CG7:C0 HXA:04 B15:C0     C0     C0 C0 C0 C0 D15:40 D31:40     C0 B31:C0 E15:40 E31:40     C0 C0
"""

rows = hex_map.strip().split('\n')
assert len(rows) == 16, f'Expecting 16 rows, found {len(rows)}'

for i, r in enumerate(rows):
    cells = r.split()
    assert len(cells) == 16, f'Row {i} should have 16 cells: {cells}'

with open('ltable.bin', 'wb') as f:
    for page in range(0, 2 ** (max(additional_pins) + 1), 256):
        columns = zip(*(r.split() for r in rows))
        for i, cell in enumerate(cell for col in columns for cell in col):
            state = (
                bool(page & states['S0']) * 1 +
                bool(page & states['S1']) * 2 +
                bool(page & states['S2']) * 4
            )
            if state == 1:
                # state 1: NOP and next is state 2
                code = 0x02
            elif state == 2:
                # state 2: NOP and next is state 3
                code = 0x03
            elif 4 <= state < 7:
                # state 4-6: NOP and next is state +1 (mod 8)
                code = 0x00 + state + 1
            else:
                opcode, sep, code = cell.rpartition(':')
                if not page and sep:
                   print(rf'{opcode} = b"\x{i:02x}"')

                code = int(code, 16)
                if opcode.startswith('HX'):
                    # inputs are active low
                    if not (page & inputs[opcode[2:]]):
                        # replace with NOP when input active
                        code = 0x00
                if state == 3 or state == 7:
                    # suppress enable for transition state
                    code &= ~0x40
            f.write(bytes([code]))
