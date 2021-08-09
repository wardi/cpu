#!/usr/bin/env python3

from RPi import GPIO
import time

D0 = 0
D1 = 1
D2 = 2
D3 = 3
D4 = 4
D5 = 5
D6 = 6
D7 = 7
RS = 8
RW = 9
E = 10
NUM_PINS = 11

READY_TIME = 0.00001

def init():
    GPIO.setmode(GPIO.BCM)
    for p in range(NUM_PINS):
        GPIO.setup(p, GPIO.OUT)
        GPIO.output(p, 0)

def cleanup():
    GPIO.output(RS, 0)
    GPIO.output(RW, 1)
    for p in range(NUM_PINS):
        GPIO.setup(p, GPIO.IN)

def wait():
    for p in range(8):
        GPIO.setup(p, GPIO.IN)
    GPIO.output(RS, 0)
    GPIO.output(RW, 1)
    while True:
        GPIO.output(E, 1)
        time.sleep(READY_TIME)
        busy = GPIO.input(D7)
        GPIO.output(E, 0)
        if not busy:
            break

    for p in range(8):
        GPIO.setup(p, GPIO.OUT)


def command(b):
    wait()
    for p in range(8):
        GPIO.output(p, (b >> p) & 1)
    GPIO.output(RS, 0)
    GPIO.output(RW, 0)
    enable()

def enable():
    GPIO.output(E, 1)
    GPIO.output(E, 0)

def write(s):
    for c in s:
        wait()
        for p in range(8):
            GPIO.output(p, (ord(c) >> p) & 1)
        GPIO.output(RS, 1)
        GPIO.output(RW, 0)
        enable()

def read(n=1):
    for p in range(8):
        GPIO.setup(p, GPIO.IN)
    GPIO.output(RS, 1)
    GPIO.output(RW, 1)
    out = []
    for i in range(n):
        b = 0
        GPIO.output(E, 1)
        time.sleep(READY_TIME)
        for p in range(8):
            b |= GPIO.input(p) << p
        GPIO.output(E, 0)
        out.append(chr(b))
    GPIO.output(RW, 0)
    for p in range(8):
        GPIO.setup(p, GPIO.OUT)
    return ''.join(out)


try:
    init()
    command(0b00111000)
    command(0b00001110)  # cursor
    command(0b00000110)  # move direction, shift
    command(0b00000001)  # clear
    command(0b00000010)  # dram position

    command(0b01000000)  # cgram address 0
    write('\xaa\x55\xaa\x55\xaa\x55\xaa\x55')
    write('\x55\xaa\x55\xaa\x55\xaa\x55\xaa')
    command(0b01000000)  # cgram address 0
    print(repr(read(3)))

    command(0b10000000)
    write('\xa4\xa5'*40)
finally:
    pass
    #cleanup()

