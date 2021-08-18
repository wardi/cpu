#!/usr/bin/env python3

from enum import IntEnum
import time
import sys
import random
import os

from RPi import GPIO

EEPROM_SIZE = 2**15

WRITE_ENABLE_DELAY = 1e-6
WRITE_SETTLE_DELAY = 10e-3
READ_DELAY = 1e-6

REPEAT_READ = False

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

    GPIO.setup(tuple(IO), GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.output((Control.CE_, Control.OE_), 0)

    time.sleep(READ_DELAY)
    d = 0
    for i, p in enumerate(IO):
        d |= GPIO.input(p) << i
    if REPEAT_READ:
        for n in range(10):
            for i, p in enumerate(IO):
                if (d >> i) & 1 != GPIO.input(p):
                    assert 0, f'bit {i} error'

    GPIO.output((Control.OE_, Control.CE_), 1)
    GPIO.setup(tuple(IO), GPIO.OUT, initial=0)

    return d

def read(addr, n):
    return bytes(read1(addr + i) for i in range(n))


init()

if '-d' in sys.argv:
    sys.stdout.buffer.write(read(0,EEPROM_SIZE))
else:

    if '-1' in sys.argv:
        testdata = b'\xff' * EEPROM_SIZE
        print('all 1s')
    elif '-0' in sys.argv:
        testdata = b'\x00' * EEPROM_SIZE
        print('all 0s')
    elif '-i' in sys.argv:
        testdata = sys.stdin.buffer.read(EEPROM_SIZE)
    else:
        seed = (sys.argv + [
            str(int.from_bytes(os.urandom(3), byteorder='little'))
        ])[1]
        print('using seed: %r' % seed)
        r = random.Random(seed)
        testdata = bytes(r.getrandbits(8) for i in range(EEPROM_SIZE))

    write(0, testdata)
    t = read(0, EEPROM_SIZE)

    if t == testdata:
        print('test ok')
    else:
        print('test failed:', ','.join(
            '%04x' % i for (i, (a, b)) in enumerate(zip(testdata, t)) if a != b)
        )

cleanup()
