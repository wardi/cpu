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
BOTTOM_Y = 120 #140


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
    label('intro')
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

            draw_map(pos_y, pos_x, out, label, jmp)
            label(f'input {pos_y},{pos_x}')
            if pos_y > TOP_Y and map_[pos_y - 1][pos_x] == '0':
                out(HXU)
                jmp(f'pos {pos_y - 1},{pos_x} v')
            if map_[pos_y][pos_x + 1] == '0':
                out(HXR)
                jmp(f'pos {pos_y},{pos_x + 1} r')
            if map_[pos_y + 1][pos_x] == '0':
                out(HXD)
                if pos_y < BOTTOM_Y:
                    jmp(f'pos {pos_y + 1},{pos_x} v')
                else:
                    jmp('intro')
            if map_[pos_y][pos_x - 1] == '0':
                out(HXL)
                jmp(f'pos {pos_y},{pos_x - 1} l')
            jmp(f'input {pos_y},{pos_x}')



def draw_map(pos_y, pos_x, out, label, jmp):
    CPOS_TOP = [D20, E20, E00, D00]
    XDELTA = [-2, -5, 1, 4]

    def glyph(plr):
        g = [
            int(map_[pos_y][pos_x - 2]) * cgram.WALL_0[r]
            + int(map_[pos_y][pos_x - 1]) * cgram.WALL_1[r]
            + plr[r]
            for r in range(8)
        ]
        out(C00)
        for b in g:
            out(opx(f'B{b:02d}'))

    dirty = False
    if map_[pos_y][pos_x - 1] == '0':
        label(f'pos {pos_y},{pos_x} r')
        glyph(cgram.PLAYER_RIGHT)
        dirty = True

    if map_[pos_y][pos_x + 1] == '0':
        if dirty:
            jmp(f'pos {pos_y},{pos_x}')
        label(f'pos {pos_y},{pos_x} l')
        glyph(cgram.PLAYER_LEFT)
        dirty = True

    if map_[pos_y - 1][pos_x] == '0' or map_[pos_y + 1][pos_x] == '0':
        if dirty:
            jmp(f'pos {pos_y},{pos_x}')
        label(f'pos {pos_y},{pos_x} v')
        glyph([
            cgram.PLAYER_VERTICAL_1, cgram.PLAYER_VERTICAL_2
            ][(pos_x + pos_y) % 2])

    label(f'pos {pos_y},{pos_x}')
    for xd, cpos in zip(XDELTA, CPOS_TOP):
        x = pos_x + xd
        out(cpos)
        for y in range(pos_y - 9, pos_y + 11):
            if x + 2 == pos_x and y == pos_y:
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
    maze_intro,
    press_any_button,
    init_cgram,
    main_loop,
])

with open(output_name, 'wb') as output:
    output.write(image)
    output.write(INI * (ROM_SIZE - len(image)))
    sys.stderr.write(f'{ROM_SIZE - len(image)} bytes remaining\n')
