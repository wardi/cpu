#!/usr/bin/env python3

import sys
import itertools
from cmdconsts import *

HELLO_EN = '"Hello World"'
HELLO_JP = '｢ﾊﾛｰﾜｰﾙﾄﾞ｣'


# some kanji character positions in our character ROM
ROM_A00_JP = {
    'ﾊ': 0b11001010,
    'ﾛ': 0b11011011,
    'ｰ': 0b10110000,
    'ﾜ': 0b11011100,
    'ﾙ': 0b11011001,
    'ﾄ': 0b11000100,
    'ﾞ': 0b11011110,
    '￫': 0b01111110,
    '｢': 0b10100010,
    '｣': 0b10100011,
}

BG_PATTERNS = [
    '                    ',
    '                    ',
    '       .       .    ',
    '   .       .       .',
    ' .   .   .   .   .  ',
    '. . . . . . . . . . ',
    ' . . . . . . . . . .',
    '  .   .   .   .   . ',
    '.       .       .   ',
    '    .       .       ',
    '                    ',
    '                    ',
    '                 ___',
    '              ______',
    '          __________',
    '       _____________',
    '   _________________',
    '____________________',
    '_________________   ',
    '______________      ',
    '__________          ',
    '_______             ',
    '___                 ',
    '                    ',
    '                    ',
    '￫                   ',
    '￫   ￫               ',
    '￫   ￫ ￫             ',
    '  ￫  ￫ ￫            ',
    '    ￫ ￫￫            ',
    '     ￫￫￫            ',
    '     ￫￫  ￫          ',
    '     ￫  ￫    ￫      ',
    '       ￫    ￫      ￫',
    '           ￫      ￫ ',
    '                 ￫  ',
]

# starting positions:

#       01234567890123456789
#   0 D "Hello World".......
#   1 E ....................
#   2 D ....................
#   3 E .........｢ﾊﾛｰﾜｰﾙﾄﾞ｣.

HELLO_EN_POS = (0, 0)
HELLO_EN_DIR = (1, 1)
HELLO_JP_POS = (9, 3)
HELLO_JP_DIR = (1, -1)


ROM_SIZE = 512 * 1024
WIDTH = 20
HEIGHT = 4

if __name__ == '__main__':
    if sys.stdout.isatty():
        sys.stderr.write('Usage: say_hello.py > hello.bin\n')
        sys.exit(1)
    out = sys.stdout.buffer.write
    # INIT
    out(INI)
    out(CUR)
    out(EIN)
    out(CLR)
    written = 4

    ex, ey = HELLO_EN_POS
    edx, edy = HELLO_EN_DIR
    jx, jy = HELLO_JP_POS
    jdx, jdy = HELLO_JP_DIR

    for i in itertools.count():
        bg = BG_PATTERNS[(i // 2) % len(BG_PATTERNS)] * 2
        field = i % 2

        if field == ey % 2:
            x = ex
            if ey > 1:
                x += WIDTH
            s = bg[:x] + HELLO_EN + bg[x + len(HELLO_EN):]
        else:
            x = jx
            if jy > 1:
                x += WIDTH
            s = bg[:x] + HELLO_JP + bg[x + len(HELLO_JP):]

        out(bytes(ROM_A00_JP.get(ch, ord(ch)) for ch in s)[:ROM_SIZE - written])
        written += len(s)
        if written >= ROM_SIZE:
            break

        if i % 12 == 11:
            if (edy > 0 and ey == HEIGHT - 1) or (edy < 0 and ey == 0):
                edy = -edy
            if (edx > 0 and ex + len(HELLO_EN) == WIDTH) or (edx < 0 and ex == 0):
                edx = -edx
            ex += edx
            ey += edy
            if (jdy > 0 and jy == HEIGHT - 1) or (jdy < 0 and jy == 0):
                jdy = -jdy
            if (jdx > 0 and jx + len(HELLO_JP) == WIDTH) or (jdx < 0 and jx == 0):
                jdx = -jdx
            jx += jdx
            jy += jdy

