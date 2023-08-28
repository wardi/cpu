#!/usr/bin/env python3

import sys

import cmdconsts
from cmdconsts import *
from cgram import CGDATA, CG, CGINTRODATA, CGINTRO
from assembler import assemble


ROM_SIZE = 512 * 1024
WIDTH = 20
HEIGHT = 4

try:
    output_name = sys.argv[1]
except IndexError:
    sys.stderr.write('Usage: maze.py prog.bin\n')
    sys.exit(1)


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
    for op in CGINTRODATA:
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
            out(opx(CGINTRO[ch]))


def input_test(out, label, jmp):
    out(CLR)
    out(D00)
    out(b'Press button(s)')
    label('_wait_press')
    out(E00)
    for hb, bn in [
            (HXU, 'up'),
            (HXD, 'down'),
            (HXL, 'left'),
            (HXR, 'right'),
            (HXB, 'b'),
            (HXA, 'a'),
            ]:
        out(hb)
        jmp(f'_{bn}_pressed')
        out(b' ' * len(bn))
        jmp(f'_after_{bn}')
        label(f'_{bn}_pressed')
        out(bn.encode('ascii').upper())
        label(f'_after_{bn}')
        out(b' ')
    jmp('_wait_press')


image = assemble([
    init_display,
    input_test,
])

with open(output_name, 'wb') as output:
    output.write(image)
    output.write(INI * (ROM_SIZE - len(image)))
