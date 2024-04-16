#!/usr/bin/python

import argparse
from enum import IntEnum

LOOKUP_SIZE = 256

RS = 1 << 0  # LCD Register Select  0: command, 1: data transfer
HC = 1 << 1  # Halt Clock  0: run, 1: halt


class Op(IntEnum):
    HLT = 0b0000_0000  # Halt
    CLR = 0b0000_0001  # Clear display
    HOM = 0b0000_0010  # Home position
    EDN = 0b0000_0100  # Cursor decrementing
    EIN = 0b0000_0110  # Cursor incrementing
    CUR = 0b0000_1110  # Display on, line cursor
    INI = 0b0011_1011  # Initialize display
    # Cursor positioning:
    D20 = 0b1001_0100
    D38 = 0b1010_0110
    D39 = 0b1010_0111
    E00 = 0b1100_0000
    E19 = 0b1101_0011
    E39 = 0b1110_0111


p = argparse.ArgumentParser(description='Generate Opcode binaries')
p.add_argument( '-l', dest='lookup', type=argparse.FileType('wb'))
p.add_argument( '-p', dest='program', type=argparse.FileType('wb'))
args = p.parse_args()

if args.lookup:
    table = bytearray([RS] * LOOKUP_SIZE)
    for op in Op:
        table[op.value] = 0
    table[Op.HLT] = HC
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
