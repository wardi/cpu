#!/usr/bin/env python3

import sys

import cmdconsts
from cmdconsts import *
import cgram
from assembler import assemble


ROM_SIZE = 512 * 1024

WIDTH = 4 * 3
HEIGHT = 20

# based on map.txt
TOP_Y = 15
BOTTOM_Y = 140
START_Y = 15
START_X = 17

try:
    output_name = sys.argv[1]
except IndexError:
    sys.stderr.write('Usage: maze.py prog.bin\n')
    sys.exit(1)

with open('map.txt') as m:
    map = m.readlines()


def opx(op):
    '''expand opcode to byte'''
    return op if isinstance(op, bytes) else getattr(cmdconsts, op)


def init_display(out, label, jmp):
    '''initialization sequence for HD44780 display'''
    out(INI)  # sw hack: 1st opcode may not be executed properly
    out(INI)  # so we do it again
    out(HID)
    out(EIN)


def maze_intro(out, label, jmp):
    '''MAZE GAME text'''
    out(CLR)
    out(C00)
    for op in cgram.CGINTRODATA:
        out(opx(op))
    for pos, chrs in [
            (E27, 'Mm'),
            (D27, 'Am'),
            (E07, 'Zz'),
            (D07, 'Ez'),
            (E31, 'Gg'),
            (D31, 'Am'),
            (E11, 'Mm'),
            (D11, 'Ez'),
            ]:
        out(pos)
        for ch in chrs:
            out(opx(cgram.CGINTRO[ch]))


def press_any_button(out, label, jmp):
    label('_wait_press')
    for hb, bn in [
            (HXU, 'up'),
            (HXD, 'down'),
            (HXL, 'left'),
            (HXR, 'right'),
            (HXB, 'b'),
            (HXA, 'a'),
            ]:
        out(hb)
        jmp('_button_pressed')
    jmp('_wait_press')
    label('_button_pressed')


def init_cgram(out, label, jmp):
    out(CLR)
    out(C00)
    for b in cgram.PLAYER_VERTICAL_1:
        out(opx(f'B{b:02d}'))

    for w in cgram.WALLS:
        for b in w:
            out(opx(f'B{b:02d}'))


def main_loop(out, label, jmp):
    pos_y = START_Y
    pos_x = START_X
    out(CLR)
    out(D00)
    out(CG1)
    out(CG2)
    out(CG3)
    out(CG4)
    out(CG5)
    out(CG6)
    out(CG7)
    out(E15)
    out(CG0)


image = assemble([
    init_display,
    maze_intro,
    press_any_button,
    init_cgram,
    main_loop,
])

with open(output_name, 'wb') as output:
    output.write(image)
    output.write(INI * (ROM_SIZE - len(image)))
