#!/usr/bin/env python3

import sys
import itertools

import cmdconsts
from cmdconsts import *
from cgram import CGDATA, CG, CGINTRODATA, CGINTRO
from song import SEQ


ROM_SIZE = 512 * 1024
WIDTH = 20
SCROLL_WINDOW = 40
HEIGHT = 4

if sys.stdout.isatty():
    sys.stderr.write('Usage: rythm.py > rythm.bin\n')
    sys.exit(1)

def out(b):
    sys.stdout.buffer.write(b)
    out.written += len(b)
out.written = 0

def opx(op):
    '''expand opcode to byte'''
    return op if isinstance(op, bytes) else getattr(cmdconsts, op)

def _scroll(delta):
    assert delta in (-1, 1)
    out(SL if delta == -1 else SR)
    _scroll.pos = (_scroll.pos + delta) % SCROLL_WINDOW
_scroll.pos = 0

def clr():
    out(CLR)
    _scroll.pos = 0

def up():
    '''scroll up (intro text)'''
    _scroll(1)

def down():
    '''scroll down (main game)'''
    _scroll(-1)

def top():
    '''return the 4 positions at the top of the screen'''
    a = _scroll.pos
    b = (a + WIDTH) % SCROLL_WINDOW
    return f'E{b:02d}', f'D{b:02d}', f'E{a:02d}', f'D{a:02d}'

def bottom():
    '''return the 4 positions at the bottom of the screen'''
    a = (_scroll.pos + WIDTH - 1) % SCROLL_WINDOW
    b = (a + WIDTH) % SCROLL_WINDOW
    return f'E{b:02d}', f'D{b:02d}', f'E{a:02d}', f'D{a:02d}'

# INIT
out(INI)
out(HID)
out(EIN)
clr()

# INTRO
out(C00)
for op in CGINTRODATA:
    out(opx(op))

out(D25)
for ch in 'RrYyTyHhMh':
    out(opx(CGINTRO[ch]))

for i in range(17 * 4):
    out(INI)
clr()

# GAME
out(C00)
for op in CGDATA:
    out(opx(op))

for bar in SEQ:
    tempo = out.written
    p0, p1, p2, p3 = top()
    out(opx(p0))
    out(opx(CG['lf'] if 'L' in bar else b' '))
    out(opx(p1))
    if 'U' in bar:
        out(opx(CG['updn' if 'D' in bar else 'up']))
    else:
        out(opx(CG['dn']) if 'D' in bar else b' ')
    out(opx(p2))
    out(opx(CG['rt'] if 'R' in bar else b' '))
    out(opx(p3))
    if 'B' in bar:
        out(opx(CG['ba' if 'A' in bar else 'b']))
    else:
        out(opx(CG['a']) if 'A' in bar else b' ')
    for pos in bottom():
        out(opx(pos))
        out(b' ')
    down()
    assert out.written - tempo == 17




out(INI * (ROM_SIZE - out.written))
sys.exit(0)

