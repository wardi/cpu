#!/usr/bin/env python3

from RPi import GPIO
import datetime

A = 11
B = 12
UP = 13
DOWN = 14
LEFT = 15
RIGHT = 16

NUM_PINS = 6
ALL_PINS = range(A, A + NUM_PINS)

def init():
    GPIO.setmode(GPIO.BCM)
    for p in ALL_PINS:
        GPIO.setup(p, GPIO.IN)
        GPIO.output(p, 0)

def read():
    b = []
    for p in ALL_PINS:
        b.append(GPIO.input(p))
    return b


buttons = read()

while True:
    b = read()
    if b == buttons:
        continue

    print(datetime.datetime.now().isoformat()), end=' ')
    for state, label in zip(b, 'ABUDLR'):
        if state:
            print(label, end=' ')
        else:
            print(' ', end=' ')
    print()
    buttons = b
