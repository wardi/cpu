#!/usr/bin/env python

##### ##### ##### ## character cells are 5x8 with 1 pixel gap in between
OPPONENT = '''
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
PLAYER = '''
    XX  XXXXXX
   X  XX      XX
  X       XXXX  X
 X  XXX  XXXX   X
X              X
 X XX    XX   X
  XXXXXXXXXXXX
   XX    XX
'''

def text_to_bin(t):
    lines = t.strip('\n').split('\n')
    width = max(len(l) for l in lines)
    for l in lines:
        p = 2**(width)
        n = 0
        for c in l:
            if c == 'X':
                n |= p
            p >>= 1

        print(bin(n).rjust(width+3))

text_to_bin(OPPONENT)
text_to_bin(PLAYER)
