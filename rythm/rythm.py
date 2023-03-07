#!/usr/bin/env python3

import sys
import itertools

import cmdconsts
from cmdconsts import INI, HID, EIN, CLR, C00, D00
from cgram import CGDATA, CG


ROM_SIZE = 512 * 1024
WIDTH = 20
HEIGHT = 4

if sys.stdout.isatty():
    sys.stderr.write('Usage: rythm.py > rythm.bin\n')
    sys.exit(1)

def out(b):
    sys.stdout.buffer.write(b)
    out.written += len(b)
out.written = 0

def mnec(mne):
    return getattr(cmdconsts, mne)

# INIT
out(INI)
out(HID)
out(EIN)
out(CLR)
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

out(INI * (ROM_SIZE - out.written))
