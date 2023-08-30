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
BOTTOM_Y = 100  # 140


try:
    output_name = sys.argv[1]
except IndexError:
    sys.stderr.write('Usage: maze.py prog.bin\n')
    sys.exit(1)

with open('map.txt') as m:
    map_ = m.readlines()


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
    out(CLR)

    for pos_y, row in enumerate(map_[TOP_Y:BOTTOM_Y + 1], TOP_Y):
        for pos_x, cell in enumerate(row):
            if cell != '0':
                continue

            label(f'pos {pos_y},{pos_x}')
            draw_map(pos_y, pos_x, out)
            label(f'input {pos_y},{pos_x}')
            if pos_y > TOP_Y and map_[pos_y - 1][pos_x] == '0':
                out(HXU)
                jmp(f'pos {pos_y - 1},{pos_x}')
            if map_[pos_y][pos_x + 1] == '0':
                out(HXR)
                jmp(f'pos {pos_y},{pos_x + 1}')
            if pos_y < BOTTOM_Y and map_[pos_y + 1][pos_x] == '0':
                out(HXD)
                jmp(f'pos {pos_y + 1},{pos_x}')
            if map_[pos_y][pos_x - 1] == '0':
                out(HXL)
                jmp(f'pos {pos_y},{pos_x - 1}')
            jmp(f'input {pos_y},{pos_x}')



def draw_map(pos_y, pos_x, out):
    CPOS_TOP = [E20, D20, E00, D00]

    for x, cpos in zip(range(pos_x - 5, pos_x + 7, 3), CPOS_TOP):
        out(cpos)
        for y in range(pos_y - 9, pos_y + 11):
            if x + 2 == pos_x and y == pos_y:
                glyph = [
                    int(map_[y][x]) * cgram.WALL_0[r]
                    + int(map_[y][x + 1]) * cgram.WALL_1[r]
                    + cgram.PLAYER_VERTICAL_1[r]
                    for r in range(8)
                ]
                out(C00)
                for b in glyph:
                    out(opx(f'B{b:02d}'))
                out(D29)
                out(CG0)
            else:
                walls = (
                    int(map_[y][x])
                    + int(map_[y][x + 1]) * 2
                    + int(map_[y][x + 2]) * 4
                )
                if walls:
                    out(opx(f'CG{walls:01d}'))
                else:
                    out(b' ')


image = assemble([
    init_display,
#    maze_intro,
#    press_any_button,
    init_cgram,
    main_loop,
])

with open(output_name, 'wb') as output:
    output.write(image)
    output.write(INI * (ROM_SIZE - len(image)))
