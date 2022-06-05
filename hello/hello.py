#!/usr/bin/env python3

HELLO_EN = 'Hello World'
HELLO_JP = 'ﾊﾛｰﾜｰﾙﾄﾞ'

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
}

BG_PATTERNS = [
    '                    ',
    '  .   .   .   .   . ',
    '. . . . . . . . . . ',
    '....................',
    ' . . . . . . . . . .',
    '   .   .   .   .   .',
    '                    ',
    '              ______',
    '       _____________',
    '____________________',
    '_______________ _ _ ',
    '_______ _ _ _ _ _ _ ',
    '_ _ _ _ _ _ _ _ _ _ ',
    '_ _ _ _ _ _ _       ',
    '_ _ _               ',
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
#   0 D Hello World.........
#   1 E ....................
#   2 D ....................
#   3 E .........ﾊﾛｰﾜｰﾙﾄﾞ...

HELLO_EN_POS = (0, 0)
HELLO_EN_DIR = (1, 1)
HELLO_JP_POS = (9, 3)
HELLO_JP_DIR = (1, -1)

# D-E field sequence:

# D write hello (0)
# E                  write ﾊﾛｰ (3)
# D erase hello
# E write hello (1), erase ﾊﾛｰ
# D                  write ﾊﾛｰ (2)
# E erase hello
# D write hello (2), erase ﾊﾛｰ
# E                  write ﾊﾛｰ (1)
# ...

