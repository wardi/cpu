#!/usr/bin/python3

import math

def blink(n):
    yield [1] * n
    yield [0] * n

def strobe(n):
    for r in range(n):
        yield [int(i == r) for i in range(n)]
    yield [0] * n

    for r in range(n):
        yield [int(i == r) for i in reversed(range(n))]
    yield [0] * n

def sweep(n):
    for r in range(n):
        yield [int(r <= i <= r*2) for i in range(n)]
    yield [0] * n

    for r in range(n):
        yield [int(r <= i <= r*2) for i in reversed(range(n))]
    yield [0] * n

def wave(n):
    for r in range(1, n):
        yield [
            int(i < math.sin(math.pi * r / n) * n)
            for i in range(n)
        ]
    yield [0] * n

    for r in range(1, n):
        yield [
            int(i < math.sin(math.pi * r / n) * n)
            for i in reversed(range(n))
        ]
    yield [0] * n

LEDS = 8
PROGRAM = (
    blink,
    blink,
    strobe,
    sweep,
    wave,
)

if __name__ == '__main__':
    for fn in PROGRAM:
        for x in fn(LEDS):
            print(x)
