#!/usr/bin/env python3

from enum import IntEnum

from RPi import GPIO
import time

WRITE_ENABLE_DELAY = 1e-6
WRITE_SETTLE_DELAY = 1e-2
READ_DELAY = 1e-6

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
    A8 = 25 # 4 seems to be unusable, resetting to low
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
    GPIO.setup(tuple(Control), GPIO.OUT, initial=1)
    GPIO.setup((*Address, *IO), GPIO.OUT, initial=0)


def cleanup():
    GPIO.cleanup()


def write1(addr, data):
    for i, p in enumerate(Address):
        GPIO.output(p, (addr >> i) & 1)
    for i, p in enumerate(IO):
        GPIO.output(p, (data >> i) & 1)
    GPIO.output((Control.CE_, Control.WE_), 0)
    time.sleep(WRITE_ENABLE_DELAY)
    GPIO.output((Control.WE_, Control.CE_), 1)
    time.sleep(WRITE_SETTLE_DELAY)

def write(addr, data):
    for i, d in enumerate(data):
        write1(addr + i, d)

def read1(addr):
    for i, p in enumerate(Address):
        GPIO.output(p, (addr >> i) & 1)

    GPIO.setup(tuple(IO), GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.output((Control.CE_, Control.OE_), 0)

    time.sleep(READ_DELAY)
    d = 0
    for i, p in enumerate(IO):
        d |= GPIO.input(p) << i
    GPIO.output((Control.OE_, Control.CE_), 1)
    GPIO.setup(tuple(IO), GPIO.OUT, initial=0)

    return d

def read(addr, n):
    return bytes(read1(addr + i) for i in range(n))


init()
write(0x01a0, b'there')
print(read(0x01a0, 5))
cleanup()
