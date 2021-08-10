#!/usr/bin/env python3

##### ##### ##### ## character cells are 5x8 with 1 pixel gap in between
OPPONENT_TEXT = '''
    XXX   XXXXXX
   XXX XXXXXXX  X
  XXX XXXXXXX    XX
 XXX XXXXXXX    XXXX
XXXXXXXXXXXXXXXXXXXX
 XXXXXXXXXXXXXXXXXX
 X X  X XX X  X XX
    XX      XX
'''

##### ##### ##### keep within 3 chars to reserve 1 byte of cgram
PLAYER_TEXT = '''
    XX  XXXXXX
   X  XX      XX
  X       XXXX  X
 X  X X  XXXX   X
X              X
 X XX    XX   X
  XXXXXXXXXXXX
   XX    XX
'''

def text_to_bin(t):
    '''
    text graphic -> list of integers, 1 per row, 1 bit per pixel
    '''
    lines = t.strip('\n').split('\n')
    width = max(len(l) for l in lines)
    o = []
    for l in lines:
        p = 2 ** (width - 1)
        n = 0
        for c in l:
            if c == 'X':
                n |= p
            p >>= 1
        o.append(n)
    return o

def bin_to_grid(b):
    '''
    break down binary graphic into 5x8 cells, 1 per horizontal bit shift
    '''
    o = []
    shift = 1
    while True:
        g = [row << 5 >> shift for row in b]
        if not any(row for row in g):
            break
        o.append(bytes([row & 0x1f for row in g]))
        shift += 1
    return o

OPPONENT = bin_to_grid(text_to_bin(OPPONENT_TEXT))
# pad arrays to same length
PLAYER = bin_to_grid(text_to_bin(PLAYER_TEXT)) + [b'\x00'*8] * 3

