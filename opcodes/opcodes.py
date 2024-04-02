#!/usr/bin/python

import argparse
from enum import IntEnum


class Fl(IntEnum):
    RS = 0b00000001  # Register Select  0: command, 1: data transfer
    HC = 0b00000010  # Halt Clock  0: run, 1: halt

LOOKUP_SIZE = 256


class Op(IntEnum):
    HLT = 0b00000000
    CLR = 0b00000001
    EDN = 0b00000100
    EIN = 0b00000110
    INI = 0b00111011


p = argparse.ArgumentParser(description='Opcode example')
p.add_argument( '--lookup', dest='lookup', type=argparse.FileType('wb'))
p.add_argument( '--program', dest='program', type=argparse.FileType('wb'))
args = p.parse_args()

if args.lookup:
    table = bytearray([Fl.RS] * LOOKUP_SIZE)
    for op in Op:
        table[op.value] = 0
    table[Op.HLT] = Fl.HC
    args.lookup.write(table)

if args.program:
    def out(c:bytes | Op):
        args.program.write(bytes([c]) if isinstance(c, Op) else c)
    out(Op.INI)
    out(Op.CLR)
    out(Op.EIN)
    out(b'hello world')
    out(Op.HLT)
