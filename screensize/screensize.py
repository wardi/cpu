#!/usr/bin/env python3

import sys
import itertools
from cmdconsts import *

ROM_SIZE = 512 * 1024
WIDTH = 20
HEIGHT = 4

show = [
b'XXXXXXXXXXXXXXXXXXXX',
b'X X X X X X X X X XX',
b'XX X X X X X X X X X',
b'XXXXXXXXXXXXXXXXXXXX',
]

def out(b):
    out.written += len(b)
    sys.stdout.buffer.write(b)

out.written = 0

if __name__ == '__main__':
    if sys.stdout.isatty():
        sys.stderr.write('Usage: screensize.py > prog.bin\n')
        sys.exit(1)
    # INIT
    out(INI)
    out(CUR)
    out(EIN)
    out(CLR)

    for r in [0, 2, 1, 3]:
        out(show[r].replace(b'X', b'\xff'))

    while out.written < ROM_SIZE:
        out(INI)
