#!/usr/bin/python3

import math
import random

RAND = random.Random()


def blink(n):
    yield [1] * n
    yield [0] * n

def sweep(n):
    for r in range(n):
        yield [int(i == r) for i in range(n)]
    yield [0] * n

def shadow(n):
    for r in range(n):
        yield [int(r <= i <= r*2) for i in range(n)]
    yield [0] * n

def wave(n):
    for r in range(1, n):
        yield [
            int(i < math.sin(math.pi * r / n) * n)
            for i in range(n)
        ]
    yield [0] * n

def ducklings(n, rand=RAND):
    # initial positions
    pos = list(range(0, int(-2 * n / 3), -3))
    offset = list(pos)
    target = 0.0
    while any(p < n for p in pos):
        yield [int(i in pos) for i in range(n)]

        # advance desired position
        target += 0.3
        # wander towards desired position
        for i, o in enumerate(offset):
            move = pos[i] - target - o + rand.random() * 3
            if move < 1:
                pos[i] += 1
            elif move >= 2:
                pos[i] -= 1
    yield [0] * n


LEDS = 28
PROGRAM = (
    blink,
    blink,
    sweep,
    lambda n: (reversed(x) for x in sweep(n)),
    shadow,
    lambda n: (reversed(x) for x in shadow(n)),
    wave,
    lambda n: (reversed(x) for x in wave(n)),
    ducklings,
)

if __name__ == '__main__':
    for fn in PROGRAM:
        for x in fn(LEDS):
            print(''.join('<>' if i else '..' for i in x))
