#!/usr/bin/python3.11

import argparse
from dataclasses import dataclass, field
from enum import Enum
from random import Random
import re

LOOKUP_SIZE = 256
PAUSE_LENGTH = 200

RS = 1 << 0  # LCD Register Select  0: command, 1: data transfer
HC = 1 << 1  # Halt Clock  0: run, 1: halt


@dataclass
class LookupTableData:
    code: int
    output: int = field(default=0)
    description: str = field(default='')


class Op(LookupTableData, Enum):
    def __str__(self):
        "code as string for output (0x00-0xff encode as latin1 for binary)"
        return chr(self.code)

    def __add__(self, other):
        return str(self) + str(other)

    def __radd__(self, other):
        return str(other) + str(self)

    CG0 = 0b0000_0000, RS

    CLR = 0b0000_0001, 0, 'clear display'
    #CG1 = 0b0000_0001, RS

    HOM = 0b0000_0010, 0, 'home position'
    #CG2 = 0b0000_0010, RS

    #HOM = 0b0000_0011, 0, 'home position'
    #CG3 = 0b0000_0011, RS
    HLT = 0b0000_0011, HC, 'halt clock'

    EDN = 0b0000_0100, 0, 'cursor decrementing'
    #CG4 = 0b0000_0100, RS

    EDS = 0b0000_0101, 0, 'cursor decrementing + shift'
    #CG5 = 0b0000_0101, RS

    EIN = 0b0000_0110, 0, 'cursor incrementing'
    #CG6 = 0b0000_0110, RS

    EIS = 0b0000_0111, 0, 'cursor incrementing + shift'
    #CG7 = 0b0000_0111, RS

    OFF = 0b0000_1000, 0, 'display off'
    #CG0 = 0b0000_1000, RS

    #OFF = 0b0000_1001, 0, 'display off'
    CG1 = 0b0000_1001, RS

    #OFF = 0b0000_1010, 0, 'display off'
    CG2 = 0b0000_1010, RS

    #OFF = 0b0000_1011, 0, 'display off'
    CG3 = 0b0000_1011, RS

    HID = 0b0000_1100, 0, 'display on, hidden cursor'
    #CG4 = 0b0000_1100, RS

    BLI = 0b0000_1101, 0, 'display on, blinking cursor'
    #CG5 = 0b0000_1101, RS

    CUR = 0b0000_1110, 0, 'display on, underline cursor'
    #CG6 = 0b0000_1110, RS

    BCR = 0b0000_1111, 0, 'display on, blinking + underline cursor'
    #CG7 = 0b0000_1111, RS

    L = 0b0001_0000, 0, 'cursor left'
    #L = 0b0001_0001, 0, 'cursor left'
    #L = 0b0001_0010, 0, 'cursor left'
    #L = 0b0001_0011, 0, 'cursor left'
    R = 0b0001_0100, 0, 'cursor right'
    #R = 0b0001_0101, 0, 'cursor right'
    #R = 0b0001_0110, 0, 'cursor right'
    #R = 0b0001_0111, 0, 'cursor right'
    SL = 0b0001_1000, 0, 'shift left'
    #SL = 0b0001_1001, 0, 'shift left'
    #SL = 0b0001_1010, 0, 'shift left'
    #SL = 0b0001_1011, 0, 'shift left'
    SR = 0b0001_1100, 0, 'shift right'
    #SR = 0b0001_1101, 0, 'shift right'
    #SR = 0b0001_1110, 0, 'shift right'
    #SR = 0b0001_1111, 0, 'shift right'

    # these conflict with '8', '9', ':', and ';'
    #INI = 0b0011_1000, 0, 'initialize display'
    #INI = 0b0011_1001, 0, 'initialize display'
    #INI = 0b0011_1010, 0, 'initialize display'
    INI = 0b0011_1011, 0, 'initialize display'

    # CGRAM positioning
    # these conflict with ascii letters,
    # trade '@' sign for jump to start of CGRAM
    C00 = 0x40  # CG0 top row
    #C01 = 0x41
    #C02 = 0x42
    #C03 = 0x43
    #C04 = 0x44
    #C05 = 0x45
    #C06 = 0x46
    #C07 = 0x47
    #C10 = 0x48  # CG1 top row
    #C11 = 0x49
    #C12 = 0x4a
    #C13 = 0x4b
    #C14 = 0x4c
    #C15 = 0x4d
    #C16 = 0x4e
    #C17 = 0x4f
    #C20 = 0x50  # CG2 top row
    #C21 = 0x51
    #C22 = 0x52
    #C23 = 0x53
    #C24 = 0x54
    #C25 = 0x55
    #C26 = 0x56
    #C27 = 0x57
    #C30 = 0x58  # CG3 top row
    #C31 = 0x59
    #C32 = 0x5a
    #C33 = 0x5b
    #C34 = 0x5c
    #C35 = 0x5d
    #C36 = 0x5e
    #C37 = 0x5f
    #C40 = 0x60  # CG4 top row
    B_____ = 0x60, RS
    #C41 = 0x61
    B____X = 0x61, RS
    #C42 = 0x62
    B___X_ = 0x62, RS
    #C43 = 0x63
    B___XX = 0x63, RS
    #C44 = 0x64
    B__X__ = 0x64, RS
    #C45 = 0x65
    B__X_X = 0x65, RS
    #C46 = 0x66
    B__XX_ = 0x66, RS
    #C47 = 0x67
    B__XXX = 0x67, RS
    #C50 = 0x68  # CG5 top row
    B_X___ = 0x68, RS
    #C51 = 0x69
    B_X__X = 0x69, RS
    #C52 = 0x6a
    B_X_X_ = 0x6a, RS
    #C53 = 0x6b
    B_X_XX = 0x6b, RS
    #C54 = 0x6c
    B_XX__ = 0x6c, RS
    #C55 = 0x6d
    B_XX_X = 0x6d, RS
    #C56 = 0x6e
    B_XXX_ = 0x6e, RS
    #C57 = 0x6f
    B_XXXX = 0x6f, RS
    #C60 = 0x70  # CG6 top row
    BX____ = 0x70, RS
    #C61 = 0x71
    BX___X = 0x71, RS
    #C62 = 0x72
    BX__X_ = 0x72, RS
    #C63 = 0x73
    BX__XX = 0x73, RS
    #C64 = 0x74
    BX_X__ = 0x74, RS
    #C65 = 0x75
    BX_X_X = 0x75, RS
    #C66 = 0x76
    BX_XX_ = 0x76, RS
    #C67 = 0x77
    BX_XXX = 0x77, RS
    #C70 = 0x78  # CG7 top row
    BXX___ = 0x78, RS
    #C71 = 0x79
    BXX__X = 0x79, RS
    #C72 = 0x7a
    BXX_X_ = 0x7a, RS
    #C73 = 0x7b
    BXX_XX = 0x7b, RS
    #C74 = 0x7c
    BXXX__ = 0x7c, RS
    #C75 = 0x7d
    BXXX_X = 0x7d, RS
    #C76 = 0x7e
    BXXXX_ = 0x7e, RS
    #C77 = 0x7f
    BXXXXX = 0x7f, RS

    # DDRAM positioning:
    D00 = 0x80  # start of 1st row after HOM/CLR
    D01 = 0x81
    D02 = 0x82
    D03 = 0x83
    D04 = 0x84
    D05 = 0x85
    D06 = 0x86
    D07 = 0x87
    D08 = 0x88
    D09 = 0x89
    D10 = 0x8a
    D11 = 0x8b
    D12 = 0x8c
    D13 = 0x8d
    D14 = 0x8e
    D15 = 0x8f
    D16 = 0x90
    D17 = 0x91
    D18 = 0x92
    D19 = 0x93  # end of 1st row after HOM/CLR
    D20 = 0x94  # start of 3rd row after HOM/CLR
    D21 = 0x95
    D22 = 0x96
    D23 = 0x97
    D24 = 0x98
    D25 = 0x99
    D26 = 0x9a
    D27 = 0x9b
    D28 = 0x9c
    D29 = 0x9d
    D30 = 0x9e
    D31 = 0x9f
    D32 = 0xa0
    D33 = 0xa1
    D34 = 0xa2
    D35 = 0xa3
    D36 = 0xa4
    D37 = 0xa5
    D38 = 0xa6
    D39 = 0xa7  # end of 3rd row after HOM/CLR

    E00 = 0xc0  # start of 2nd row after HOM/CLR
    E01 = 0xc1
    E02 = 0xc2
    E03 = 0xc3
    E04 = 0xc4
    E05 = 0xc5
    E06 = 0xc6
    E07 = 0xc7
    E08 = 0xc8
    E09 = 0xc9
    E10 = 0xca
    E11 = 0xcb
    E12 = 0xcc
    E13 = 0xcd
    E14 = 0xce
    E15 = 0xcf
    E16 = 0xd0
    E17 = 0xd1
    E18 = 0xd2
    E19 = 0xd3  # end of 2nd row after HOM/CLR
    E20 = 0xd4  # start of 4th row after HOM/CLR
    E21 = 0xd5
    E22 = 0xd6
    E23 = 0xd7
    E24 = 0xd8
    E25 = 0xd9
    E26 = 0xda
    E27 = 0xdb
    E28 = 0xdc
    E29 = 0xdd
    E30 = 0xde
    E31 = 0xdf
    E32 = 0xe0
    E33 = 0xe1
    E34 = 0xe2
    E35 = 0xe3
    E36 = 0xe4
    E37 = 0xe5
    E38 = 0xe6
    E39 = 0xe7  # end of 4th row after HOM/CLR


p = argparse.ArgumentParser(description='Generate Features binaries')
p.add_argument( '-l', dest='ltable', type=argparse.FileType('wb'))
p.add_argument( '-p', dest='prog', type=argparse.FileType('wb'))
args = p.parse_args()

if args.ltable:
    table = bytearray([RS] * LOOKUP_SIZE)
    for op in Op:
        table[op.value.code] = op.value.output
    args.ltable.write(table)

if args.prog:
    def out(c:str | Op):
        args.prog.write(
            str(c).replace('█', '\xff')  ## HD44780 CGROM character set 0
                  .replace('→', '\x7e')
                  .replace('←', '\x7f')
                  .replace('▝', str(Op.CG0))  ## CGRAM chars
                  .replace('▀', str(Op.CG1))
                  .replace('▘', str(Op.CG2))
                  .replace('▖', str(Op.CG3))
                  .encode('latin1')
        )

    def pause(n=1):
        out(str(Op.INI) * int(PAUSE_LENGTH * n))

    def cgram_init():
        out(Op.C00)
        out(Op.BXXXXX)  # CG0 "▝"
        out(Op.BXXXXX)
        out(Op.BXXXXX)
        out(Op.B_XXXX)
        out(Op.B__XXX)
        out(Op.B_____)
        out(Op.B_____)
        out(Op.B_____)
        out(Op.BXXXXX)  # CG1 "▀"
        out(Op.BXXXXX)
        out(Op.BXXXXX)
        out(Op.BXXXXX)
        out(Op.BXXXXX)
        out(Op.B_____)
        out(Op.B_____)
        out(Op.B_____)
        out(Op.BXXXXX)  # CG2 "▘"
        out(Op.BXXXXX)
        out(Op.BXXXXX)
        out(Op.BXXXX_)
        out(Op.BXXX__)
        out(Op.B_____)
        out(Op.B_____)
        out(Op.B_____)
        out(Op.B_____)  # CG3 "▖"
        out(Op.B_____)
        out(Op.B_____)
        out(Op.BXXX__)
        out(Op.BXXXX_)
        out(Op.BXXXXX)
        out(Op.BXXXXX)
        out(Op.BXXXXX)

    out(Op.INI + Op.CLR + Op.EIN + Op.HID)
    out('starting..')
    cgram_init()
    out(Op.CLR)
    pause()

    out(Op.D00 + ' CLR ▝▀▀▀▀▀▀▀▀▘ 0x01')
    out(Op.E00 + '▖ clear all & reset ')
    out(Op.D20 + '█ display shift,    ')
    out(Op.E20 + '█ cursor to top left')
    pause()
    out(Op.CLR)
    pause(.4)
    out(Op.D00 + ' HOM ▝▀▀▀▀▀▀▀▀▘ 0x02')
    out(Op.E00 + '▖ reset display     ')
    out(Op.D20 + '█ shift, cursor to  ')
    out(Op.E20 + '█ top left          ')
    out(Op.E00 + '^' + Op.HOM + Op.BLI)
    pause()
    out(Op.CLR)
    out(Op.BLI)
    out(Op.D00 + ' EIN ▝▀▀▀▀▀▀▀▀▘ 0x06')
    out(Op.E00 + '▖ increment after   ')
    out(Op.D20 + '█ each data transfer')
    out(Op.E20 + '█                   ')
    for i in range(2 * PAUSE_LENGTH // 36):
        out(Op.E22 + '→ → → → → → → → →')
        out(Op.E22 + '                 ')
    out(Op.CLR)
    out(Op.EDN)
    out(Op.D19 + ' EDN ▝▀▀▀▀▀▀▀▀▘ 0x04'[::-1])
    out(Op.E19 + '▖ decrement after   '[::-1])
    out(Op.D39 + '█ each data transfer'[::-1])
    out(Op.E39 + '█                   '[::-1])
    for i in range(2 * PAUSE_LENGTH // 36):
        out(Op.E39 + '← ← ← ← ← ← ← ← ←')
        out(Op.E39 + '                 ')
    out(Op.CLR)
    out(Op.EIS + Op.CUR)
    out(Op.D00 + ' EIS ▝▀▀▀▀▀▀▀▀▘ 0x07')
    out(Op.E00 + '▖ increment & shift ')
    out(Op.D20 + '█ display after each')
    out(Op.E20 + '█ data transfer     ')
    out(Op.HID)
    pause()
    out(Op.CUR)
    out(Op.D00 + ' ' * 80)
    out(Op.EDS)
    out(Op.D19 + ' EDS ▝▀▀▀▀▀▀▀▀▘ 0x05'[::-1])
    out(Op.E19 + '▖ decrement & shift '[::-1])
    out(Op.D39 + '█ display after each'[::-1])
    out(Op.E39 + '█ data transfer     '[::-1])
    out(Op.HID)
    pause()
    out(Op.D39 + ' ' * 80)
    out(Op.EIN)
    out(Op.D00 + ' OFF ▝▀▀▀▀▀▀▀▀▘ 0x08')
    out(Op.E00 + '▖ display off       ')
    out(Op.D20 + '█                   ')
    out(Op.E20 + '█                   ')
    pause(.2)
    out(Op.CUR)
    out(Op.E23 + '3, ')
    pause(.2)
    out('2, ')
    pause(.2)
    out('1, ')
    pause(.2)
    out(Op.OFF)
    pause(.4)
    out(Op.HID)
    out('back')
    pause(.3)
    out(op.CLR)
    out(Op.D00 + ' HID ▝▀▀▀▀▀▀▀▀▘ 0x08')
    out(Op.E00 + '▖ display on, hidden')
    out(Op.D20 + '█ cursor            ')
    out(Op.E20 + '█                → ←')
    out(Op.E38)
    pause()
    out(op.CLR + op.BLI)
    out(Op.D00 + ' BLI ▝▀▀▀▀▀▀▀▀▘ 0x0d')
    out(Op.E00 + '▖ display on,       ')
    out(Op.D20 + '█ blinking block    ')
    out(Op.E20 + '█ cursor         → ←')
    out(Op.E38)
    pause()
    out(op.CLR + op.CUR)
    out(Op.D00 + ' CUR ▝▀▀▀▀▀▀▀▀▘ 0x0e')
    out(Op.E00 + '▖ display on,       ')
    out(Op.D20 + '█ underline cursor  ')
    out(Op.E20 + '█                → ←')
    out(Op.E38)
    pause()
    out(op.CLR + op.BCR)
    out(Op.D00 + ' BCR ▝▀▀▀▀▀▀▀▀▘ 0x0f')
    out(Op.E00 + '▖ display on,       ')
    out(Op.D20 + '█ blinking block &  ')
    out(Op.E20 + '█ underline curs.→ ←')
    out(Op.E38)
    pause()
    out(op.CLR + op.BCR)
    out(Op.D00 + ' L ▝▀▀▀▀▀▀▀▀▀▀▘ 0x10')
    out(Op.E00 + '▖ move cursor left  ')
    out(Op.D20 + '█                   ')
    out(Op.E20 + '█                   ')
    out(op.D00)
    for i in range(80):
        out(Op.L + str(Op.INI) * (PAUSE_LENGTH // 80))
    out(Op.CLR)
    out(Op.D00 + ' R ▝▀▀▀▀▀▀▀▀▀▀▘ 0x14')
    out(Op.E00 + '▖ move cursor right ')
    out(Op.D20 + '█                   ')
    out(Op.E20 + '█                   ')
    out(op.E39)
    for i in range(80):
        out(Op.R + str(Op.INI) * (PAUSE_LENGTH // 80))
    out(Op.CLR + Op.HID)
    out(Op.D00 + ' SL ▝▀▀▀▀▀▀▀▀▀▘ 0x18')
    out(Op.E00 + '▖ shift display left')
    out(Op.D20 + '█                   ')
    out(Op.E20 + '█                   ')
    pause(.4)
    for i in range(40):
        out(Op.SL + str(Op.INI) * (PAUSE_LENGTH // 40))
    pause(.4)
    out(Op.CLR + Op.HID)
    out(Op.D00 + ' SR ▝▀▀▀▀▀▀▀▀▀▘ 0x1c')
    out(Op.E00 + '▖ shift display     ')
    out(Op.D20 + '█ right             ')
    out(Op.E20 + '█                   ')
    pause(.4)
    for i in range(40):
        out(Op.SR + str(Op.INI) * (PAUSE_LENGTH // 40))
    pause(.4)
    out(Op.CLR + Op.HID)
    out(Op.D00 + ' Cxy ▝▀▀▀▀▀▘ 0x40-7f')
    out(Op.E00 + '▖ set CGRAM address ')
    out(Op.D20 + '█ x = char. (0-7)   ')
    out(Op.E20 + '█ y = row (0-7)     ')

    for i in range(3 * PAUSE_LENGTH // 14):
        out(Op.C00)
        out(Op.BXXX_X)  # CG0 "▝"
        out(Op.BXXX_X)
        out(Op.BXXX_X)
        out(Op.BXXX_X)
        out(Op.BXXX_X)
        out(Op.BXXX_X)
        out(Op.B_____)
        out(Op.B_____)
        out(Op.BXXXXX)  # CG1 "▀"
        out(Op.BXXXXX if i % 3 == 2 else Op.B_____)
        out(Op.BXXXXX if i % 3 == 0 else Op.B_____)
        out(Op.BXXXXX if i % 3 == 1 else Op.B_____)
        out(Op.BXXXXX if i % 3 == 2 else Op.B_____)
        if i:
            continue
        out(Op.BXXXXX)
        out(Op.B_____)
        out(Op.B_____)
        out(Op.BXX___)  # CG2 "▘"
        out(Op.B_XX__)
        out(Op.B_XXXX)
        out(Op.B_XXXX)
        out(Op.B_XX__)
        out(Op.BXX___)
        out(Op.B_____)
        out(Op.B_____)
    cgram_init()

    out(Op.CLR + Op.HID)
    out(Op.D00 + ' Dxx ▝▀▀▀▀▀▘ 0x80-a7')
    out(Op.E00 + '▖ set DDRAM address ')
    out(Op.D20 + '█ bank 1 (rows 1,3) ')
    out(Op.E20 + '█ xx = pos. (00-39) ')
    rnd = Random(42)
    ops = [op for op in Op if re.match(r'D\d\d', op.name)]
    rnd.shuffle(ops)
    out(Op.BCR)
    for op in ops:
        out(op + str(Op.INI) * (PAUSE_LENGTH // 40))

    out(Op.CLR + Op.HID)
    out(Op.D00 + ' Exx ▝▀▀▀▀▀▘ 0xc0-e7')
    out(Op.E00 + '▖ set DDRAM address ')
    out(Op.D20 + '█ bank 2 (rows 2,4) ')
    out(Op.E20 + '█ xx = pos. (00-39) ')
    ops = [op for op in Op if re.match(r'E\d\d', op.name)]
    rnd.shuffle(ops)
    out(Op.BCR)
    for op in ops:
        out(op + str(Op.INI) * (PAUSE_LENGTH // 40))

    out(Op.HID)
    out(Op.HLT)
