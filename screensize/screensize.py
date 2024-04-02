#!/usr/bin/env python3

import sys
import itertools
import cmdconsts
from cmdconsts import *

from cgram import CGLIKE, CGLIKE_DATA, CGLIKED, CGLIKED_DATA

ROM_SIZE = 512 * 1024
WIDTH = 20
HEIGHT = 4


def out(b):
    out.written += len(b)
    sys.stdout.buffer.write(b)

out.written = 0

def pause():
    out(INI * 60)

def opx(op):
    return getattr(cmdconsts, op)

if __name__ == '__main__':
    if sys.stdout.isatty():
        sys.stderr.write('Usage: screensize.py > prog.bin\n')
        sys.exit(1)
    # INIT
    out(INI)
    out(HID)
    out(EIN)
    out(CLR)
    pause()

    # define cgram
    out(C00)
    out(B31)     # 0b11111
    out(B17 * 6) # 0b10001
    out(B31)     # 0b11111

    for i in range(6):
        pause()
        for pos in [D00, E00, D20, E20]:
            out(pos)
            out(BLK * WIDTH)
            pause()

        pause()
        for pos in [D00, E00, D20, E20]:
            out(pos)
            out(CG0 * WIDTH)
            pause()

    out(CLR)
    for i in range(25):
        pause()

    for i in range(4):
        for j in range(WIDTH):
            pause()
            out(bytes([ord(E20) + j]))
            out(BLK)
            out(bytes([ord(D20) + j]))
            out(BLK)
            out(bytes([ord(E00) + j]))
            out(BLK)
            out(bytes([ord(D00) + j]))
            out(BLK)

        for j in range(WIDTH):
            pause()
            out(bytes([ord(E20) + j]))
            out(CG0)
            out(bytes([ord(D20) + j]))
            out(CG0)
            out(bytes([ord(E00) + j]))
            out(CG0)
            out(bytes([ord(D00) + j]))
            out(CG0)

    # define cgram
    out(C10)
    out(b''.join(opx(d) for d in CGLIKE_DATA))

    out(D07 + b'  ' + opx(CGLIKE['f1']) + opx(CGLIKE['f2']) + b' ')
    out(E07 + b' ' + opx(CGLIKE['t1']) + opx(CGLIKE['t2']) + opx(CGLIKE['t3']) + b' ')
    out(D27 + b'  ' + opx(CGLIKE['w1']) + opx(CGLIKE['w2']) + b' ')
    out(E27 + b'     ')

    for i in range(25):
        pause()

    for j in range(20):
        # define cgram
        out(C10)
        out(b''.join(opx(d) for d in CGLIKED_DATA))
        for i in range(25):
            pause()

        # define cgram
        out(C10)
        out(b''.join(opx(d) for d in CGLIKE_DATA))
        for i in range(25):
            pause()

    while out.written < ROM_SIZE:
        out(INI)
