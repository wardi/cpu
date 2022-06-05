#!/usr/bin/env python3
from RPi import GPIO
import time
import itertools

from cmdconsts import *
import hello

D0 = 18
D1 = 16
D2 = 15
D3 = 13
D4 = 12
D5 = 11
D6 = 10
D7 = 8
RS = 22
RW = 21
E = 19
PINS = (D0, D1, D2, D3, D4, D5, D6, D7, RS, RW, E)
D_PINS = PINS[:8]
D_BITS = tuple(range(8))
#READY_TIME = 0.00001
READY_TIME = 0.005

def init():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(PINS, GPIO.OUT)
    GPIO.output(PINS, 0)

def cleanup():
    GPIO.output(RS, 0)
    GPIO.output(RW, 1)
    GPIO.setup(PINS, GPIO.IN)

def wait():
    GPIO.setup(D_PINS, GPIO.IN)
    GPIO.output(RS, 0)
    GPIO.output(RW, 1)
    while True:
        GPIO.output(E, 1)
        time.sleep(READY_TIME)
        busy = GPIO.input(D7)
        GPIO.output(E, 0)
        if not busy:
            break

    GPIO.setup(D_PINS, GPIO.OUT)


def command(b):
    wait()
    GPIO.output(D_PINS, tuple((ord(b) >> j) & 1 for j in D_BITS))
    GPIO.output(RS, 0)
    GPIO.output(RW, 0)
    enable()

def enable():
    GPIO.output(E, 1)
    GPIO.output(E, 0)

def write(s):
    for ch in s:
        b = hello.ROM_A00_JP.get(ch, ord(ch))
        wait()
        GPIO.output(D_PINS, tuple((b >> j) & 1 for j in D_BITS))
        GPIO.output(RS, 1)
        GPIO.output(RW, 0)
        enable()


WIDTH = 20
HEIGHT = 4

if __name__ == '__main__':
    try:
        init()
        command(INI)
        command(CUR)
        command(EIN)
        command(CLR)

        ex, ey = hello.HELLO_EN_POS
        edx, edy = hello.HELLO_EN_DIR
        jx, jy = hello.HELLO_JP_POS
        jdx, jdy = hello.HELLO_JP_DIR

        for i in itertools.count():
            bg = hello.BG_PATTERNS[(i // 2) % len(hello.BG_PATTERNS)] * 2
            field = i % 2

            if field == ey % 2:
                x = ex
                if ey > 1:
                    x += WIDTH
                write(bg[:x] + hello.HELLO_EN + bg[x + len(hello.HELLO_EN):])
            else:
                x = jx
                if jy > 1:
                    x += WIDTH
                write(bg[:x] + hello.HELLO_JP + bg[x + len(hello.HELLO_JP):])

            if i % 12 == 11:
                if (edy > 0 and ey == HEIGHT - 1) or (edy < 0 and ey == 0):
                    edy = -edy
                if (edx > 0 and ex + len(hello.HELLO_EN) == WIDTH) or (edx < 0 and ex == 0):
                    edx = -edx
                ex += edx
                ey += edy
                if (jdy > 0 and jy == HEIGHT - 1) or (jdy < 0 and jy == 0):
                    jdy = -jdy
                if (jdx > 0 and jx + len(hello.HELLO_JP) == WIDTH) or (jdx < 0 and jx == 0):
                    jdx = -jdx
                jx += jdx
                jy += jdy

    finally:
        cleanup()

