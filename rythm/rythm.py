#!/usr/bin/env python3

import sys
import itertools

import cmdconsts
from cmdconsts import INI, HID, EIN, CLR, C00, D00, SL, SR
from cgram import CGDATA, CG, CGGRID, CGGRIDDATA, INTRO


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

def mnec(mne):
    return mne if isinstance(mne, bytes) else getattr(cmdconsts, mne)

def _scroll(delta):
    assert delta in (-1, 1)
    out(SL if delta == -1 else SR)
    _scroll.pos = (_scroll.pos + delta) % SCROLL_WINDOW
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
    return f'E{a:02d}', f'D{a:02d}', f'E{b:02d}', f'D{b:02d}'

def bottom():
    '''return the 4 positions at the bottom of the screen'''
    a = (_scroll.pos - 1) % SCROLL_WINDOW
    b = (a + WIDTH) % SCROLL_WINDOW
    return f'E{a:02d}', f'D{a:02d}', f'E{b:02d}', f'D{b:02d}'

# INIT
out(INI)
out(HID)
out(EIN)
out(CLR)

out(C00)
for mne in CGGRIDDATA:
    out(mnec(mne))

for itxt in INTRO:
    for pos, tri in zip(bottom(), (itxt[:3], itxt[3:6], itxt[6:9], itxt[9:])):
        out(mnec(pos))
        out(mnec(CGGRID[tri]))
    for pos in top():
        out(mnec(pos))
        out(b' ')
    up()

out(INI * (ROM_SIZE - out.written))
sys.exit(0)

out(C00)
for mne in CGDATA:
    out(mnec(mne))
out(D00)
out(mnec(CG['up']))
out(mnec(CG['dn']))
out(mnec(CG['updn']))
out(mnec(CG['lf']))
out(mnec(CG['rt']))
out(mnec(CG['up']))
out(mnec(CG['b']))
out(mnec(CG['a']))
out(mnec(CG['ba']))

