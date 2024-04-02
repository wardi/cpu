#!/usr/bin/python

import argparse
from enum import IntEnum


class Fl(IntEnum):
    RS = 0b00000001  # Register Select  0: command, 1: data transfer
    HC = 0b00000010  # Halt Clock  0: run, 1: halt

LOOKUP_SIZE = 256


class Op(IntEnum):
    HLT = 0b00000000  # Halt
    CLR = 0b00000001  # Clear display
    HOM = 0b00000010  # Home position
    EDN = 0b00000100  # Cursor decrementing
    EIN = 0b00000110  # Cursor incrementing
    CUR = 0b00001110  # Display on, line cursor
    INI = 0b00111011  # Initialize display
    # Cursor positioning:
    D20 = 0b10010100
    D38 = 0b10100110
    D39 = 0b10100111
    E00 = 0b11000000
    E19 = 0b11010011
    E39 = 0b11100111


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
    def out(c:str | Op):
        args.program.write(
            bytes([c]) if isinstance(c, Op) else c.encode('latin1')
        )
    out(Op.INI)
    out(Op.CUR)
    out(Op.CLR)
    for ch in 'SPIRAL PATTERN DEMO*=-!':
        out(Op.EIN)
        out(ch * 20)
        out(Op.E19)
        out(ch)
        out(Op.D39)
        out(ch)
        out(Op.E39)
        out(Op.EDN)
        out(ch * 20)
        out(Op.D20)
        out(ch)
        out(Op.E00)
        out(Op.EIN)
        out(ch * 19)
        out(Op.D38)
        out(Op.EDN)
        out(ch * 18)
        out(Op.HOM)
    out(Op.HLT)
