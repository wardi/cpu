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

# 80 -> RS=1
# 40 -> no E on /clk
# 00-07 -> next state is 0-7

hex_map = """
    80 JM0:41 B00:80     80 C00:00 80 80 80 D00:00 D16:00 D32:00 B16:80 E00:00 E16:00 E32:00 80
CLR:00 JM1:41 B01:80     80     80 80 80 80 D01:00 D17:00 D33:00 B17:80 E01:00 E17:00 E33:00 80
HOM:00 JM2:41 B02:80     80     80 80 80 80 D02:00 D18:00 D34:00 B18:80 E02:00 E18:00 E34:00 80
JM3:41   R:00 B03:80     80     80 80 80 80 D03:00 D19:00 D35:00 B19:80 E03:00 E19:00 E35:00 80
CG4:80 JM4:41 B04:80     80     80 80 80 80 D04:00 D20:00 D36:00 B20:80 E04:00 E20:00 E36:00 80
JM5:41   L:00 B05:80     80     80 80 80 80 D05:00 D21:00 D37:00 B21:80 E05:00 E21:00 E37:00 80
EIN:00 JM6:41 B06:80     80     80 80 80 80 D06:00 D22:00 D38:00 B22:80 E06:00 E22:00 E38:00 80
    80 JM7:41 B07:80     80     80 80 80 80 D07:00 D23:00 D39:00 B23:80 E07:00 E23:00 E39:00 80
CG0:80  SR:00 B08:80     80     80 80 80 80 D08:00 D24:00     80 B24:80 E08:00 E24:00     80 80
CG1:80 HXU:44 B09:80     80     80 80 80 80 D09:00 D25:00     80 B25:80 E09:00 E25:00     80 80
CG2:80 HXD:44 B10:80     80     80 80 80 80 D10:00 D26:00     80 B26:80 E10:00 E26:00     80 80
CG3:80 HXL:44 B11:80 INI:00     80 80 80 80 D11:00 D27:00     80 B27:80 E11:00 E27:00     80 80
HID:00  SL:00 B12:80     80     80 80 80 80 D12:00 D28:00     80 B28:80 E12:00 E28:00     80 80
CG5:80 HXR:44 B13:80     80     80 80 80 80 D13:00 D29:00     80 B29:80 E13:00 E29:00     80 80
CG6:80 HXB:44 B14:80     80     80 80 80 80 D14:00 D30:00     80 B30:80 E14:00 E30:00     80 80
CG7:80 HXA:44 B15:80     80     80 80 80 80 D15:00 D31:00     80 B31:80 E15:00 E31:00     80 80
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
            state = page & sum(states.values())
            if state == states['S0']:
                # state 1: NOP and next is state 2
                code = 0x42
            elif state == states['S1']:
                # state 2: NOP and next is state 3
                code = 0x43
            elif state & states['S2']:
                # state 4+: NOP and next is state +1 (mod 8)
                state_num = 4
                state_num |= 1 if state & states['S1'] else 0
                state_num |= 2 if state & states['S2'] else 0
                code = 0x40 + ((state_num + 1) & 7)
            else:
                opcode, sep, code = cell.rpartition(':')
                if not page and sep:
                   print(rf'{opcode} = b"\x{i:02x}"')

                code = int(code, 16)
                if opcode.startswith('HX'):
                    # inputs are active low
                    if not (page & inputs[opcode[2:]]):
                        # replace with NOP when input active
                        code == 0x40
            f.write(bytes([code]))
