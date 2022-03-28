#!/usr/bin/env python3

from RPi import GPIO
import numpy as np
import time

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
READY_TIME = 0.00001

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
    GPIO.output(D_PINS, tuple((b >> j) & 1 for j in D_BITS))
    GPIO.output(RS, 0)
    GPIO.output(RW, 0)
    enable()

def enable():
    GPIO.output(E, 1)
    GPIO.output(E, 0)

def write(s):
    for b in s:
        wait()
        GPIO.output(D_PINS, tuple((b >> j) & 1 for j in D_BITS))
        GPIO.output(RS, 1)
        GPIO.output(RW, 0)
        enable()

delta = np.linspace(0, 1, 20)
mod = np.empty(20)
mod.fill(.5)

if __name__ == '__main__':
    try:
        init()
        command(0b00111000)
        command(0b00001100)  # no cursor
        command(0b00000110)  # move direction, shift
        command(0b00000001)  # clear

        while True:
            mod += delta # + np.random.randn(20)
            carry = np.clip(np.trunc(mod), 0, 1)
            mod -= carry
            # 0 -> b' ', 1 -> b'\xff'
            b = (carry*(255-32)+32).astype('b').tobytes()
            #command(0b00000010)  # home
            write(b*4)
            #input()
            #time.sleep(1/550)

    finally:
        cleanup()

