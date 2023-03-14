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
for op in CGINTRODATA[:16]:
    out(opx(op))
out(D25)
for ch in 'Rr':
    out(opx(CGINTRO[ch]))

out(C20)
for op in CGINTRODATA[16:32]:
    out(opx(op))
out(D27)
for ch in 'Yy':
    out(opx(CGINTRO[ch]))

out(C40)
for op in CGINTRODATA[32:48]:
    out(opx(op))
out(D29)
for ch in 'Ty':
    out(opx(CGINTRO[ch]))

out(C60)
for op in CGINTRODATA[48:64]:
    out(opx(op))
out(D31)
for ch in 'Hh':
    out(opx(CGINTRO[ch]))
for i in range(17):
    out(INI)
for ch in 'Mh':
    out(opx(CGINTRO[ch]))

# pause
for i in range(17 * 3):
    out(INI)
clr()

# GAME
out(C00)
for op in CGDATA:
    out(opx(op))

# shifted copy of sequence for what is scrolling off the screen
ESEQ = [''] * (WIDTH) + SEQ

for i, bar in enumerate(SEQ, 1):
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

    b0, b1, b2, b3 = bottom()
    for pos, button in zip((b0, b1, b1, b2, b3, b3), 'LUDRBA'):
        out(opx(pos))
        if button in ESEQ[i]:
            out(opx('Y' + button))
        elif button not in ESEQ[i - 1] and button not in ESEQ[i + 1]:
            out(opx('X' + button))
        else:
            out(b' ')
    down()
    assert out.written - tempo == 21




out(INI * (ROM_SIZE - out.written))
sys.exit(0)

