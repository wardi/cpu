#!/usr/bin/env python3

import sys
import itertools
import struct

import cmdconsts
from cmdconsts import *
from cgram import CGDATA, CG, CGINTRODATA, CGINTRO


ROM_SIZE = 512 * 1024
WIDTH = 20
SCROLL_WINDOW = 40
HEIGHT = 4

if sys.stdout.isatty():
    sys.stderr.write('Usage: rhythm.py > prog.bin\n')
    sys.exit(1)

def out(b):
    sys.stdout.buffer.write(b)
    out.written += len(b)
out.written = 0

def label():
    return out.written

def jmp(lb):
    out(opx(f'JM{lb >> 16}'))
    out(struct.pack('>H', lb & 0xffff))

def opx(op):
    '''expand opcode to byte'''
    return op if isinstance(op, bytes) else getattr(cmdconsts, op)

# INIT
out(INI)
out(HID)
out(EIN)
clr()

# INTRO
out(C00)
for op in CGINTRODATA:
    out(opx(op))
out(E27)
for ch in 'Mm':
    out(opx(CGINTRO[ch]))
out(D27)
for ch in 'Am':
    out(opx(CGINTRO[ch]))
out(E07)
for ch in 'Zz':
    out(opx(CGINTRO[ch]))
out(D07)
for ch in 'Ez':
    out(opx(CGINTRO[ch]))
out(E31)
for ch in 'Gg':
    out(opx(CGINTRO[ch]))
out(D31)
for ch in 'Am':
    out(opx(CGINTRO[ch]))
out(E11)
for ch in 'Mm':
    out(opx(CGINTRO[ch]))
out(D11)
for ch in 'Ez':
    out(opx(CGINTRO[ch]))


# pause
loop = label()

jmp(loop)
clr()

# TBD: GAME



out(INI * (ROM_SIZE - out.written))
sys.exit(0)

