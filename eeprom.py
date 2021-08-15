#!/usr/bin/env python3

from enum import IntEnum

from RPi import GPIO
import time

WRITE_TIME = 100e-9
READ_TIME = 150e-9

class Control(IntEnum):
    OE_ = 17
    CE_ = 27
    WE_ = 2

class Address(IntEnum):
    A0 = 19
    A1 = 13
    A2 = 12
    A3 = 6
    A4 = 5
    A5 = 1
    A6 = 0
    A7 = 7
    A8 = 4
    A9 = 14
    A10 = 18
    A11 = 15
    A12 = 8
    A13 = 3
    A14 = 11

class IO(IntEnum):
    IO0 = 16
    IO1 = 26
    IO2 = 20
    IO3 = 9
    IO4 = 10
    IO5 = 24
    IO6 = 23
    IO7 = 22


def init():
    GPIO.setmode(GPIO.BCM)
    for p in Control:
        GPIO.setup(p, GPIO.OUT)
        GPIO.output(p, 1)

    for p in (*Address, *IO):
        GPIO.setup(p, GPIO.OUT)
        GPIO.output(p, 0)

def cleanup():
    for p in (*Address, *IO, *Control):
        GPIO.setup(p, GPIO.IN)


def write1(addr, data):
    for i, p in enumerate(Address):
        GPIO.output(p, (addr >> i) & 1)
    for i, p in enumerate(IO):
        GPIO.output(p, (data >> i) & 1)
    GPIO.output(Control.CE_, 0)
    GPIO.output(Control.WE_, 0)
    time.sleep(WRITE_TIME)
    GPIO.output(Control.WE_, 1)
    GPIO.output(Control.CE_, 1)

def write(addr, data):
    for i, d in enumerate(data):
        write1(addr + i, d)

def read1(addr):
    for i, p in enumerate(Address):
        GPIO.output(p, (addr >> i) & 1)
    for i, p in enumerate(IO):
        GPIO.setup(p, GPIO.IN)
    GPIO.output(Control.CE_, 0)
    GPIO.output(Control.OE_, 0)
    time.sleep(READ_TIME)
    d = 0
    for i, p in enumerate(IO):
        d |= GPIO.input(p) << i
    GPIO.output(Control.OE_, 1)
    GPIO.output(Control.CE_, 1)
    for i, p in enumerate(IO):
        GPIO.setup(p, GPIO.OUT)

    return d

def read(addr, n):
    return bytes(read1(addr + i) for i in range(n))


init()
write(0x0000, b'hello')
print(read(0x0000, 5))
cleanup()
