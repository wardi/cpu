#!/usr/bin/python3

import re
import sys
import math
import random
import struct
from argparse import ArgumentParser, RawDescriptionHelpFormatter

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

def hazard(n):
    for j in range(1, 5):
        yield [int(i % 8 < j) for i in range(n)]
    for j in range(1, 25):
        yield [int((i - j) % 8 < 4) for i in range(n)]
    for j in range(4):
        yield [int(j < i % 8 < 4) for i in range(n)]

def static(n, rand=RAND):
    # fade in
    for j in range(1, 6):
        yield [int(rand.random() < j / 12) for i in range(n)]
    for j in range(24):
        yield [int(rand.random() < 0.5) for i in range(n)]
    # fade out
    for j in reversed(range(6)):
        yield [int(rand.random() < j / 12) for i in range(n)]

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

def rev(fn):
    def _rev(n):
        return (reversed(x) for x in fn(n))
    _rev.__name__ = fn.__name__ + ' reversed'
    return _rev


CMDS = {
    'b': blink,
    's': sweep,
    'S': rev(sweep),
    'a': shadow,
    'A': rev(shadow),
    'w': wave,
    'W': rev(wave),
    'h': hazard,
    'H': rev(hazard),
    'd': ducklings,
    'D': rev(ducklings),
}


def main():
    parser = ArgumentParser(
        formatter_class=RawDescriptionHelpFormatter,
        epilog='commands:\n' + '\n'.join(
            f'  {c}: {CMDS[c].__name__}' for c in CMDS)
    )
    parser.add_argument(
        'commands',
        metavar='CMDS',
        nargs='+',
        help='e.g. "10 5b3s h" will output 10 times: (5 blinks, 3 sweeps) then 1 hazard',
    )
    parser.add_argument('-b', '--bits', default=8, type=int, help='bits in pattern [default: 8]')
    parser.add_argument('-o', '--bin-output', metavar='FILE', help='output packed binary data to a file')
    parser.add_argument('-f', '--bin-format', metavar='FMT', default='B', help='packed binary data format [default: B]')
    args = parser.parse_args()

    if args.bin_output:
        with open(args.bin_output, 'wb') as f:
            for fn in commands(args.commands):
                for x in fn(args.leds):
                    f.write(struct.pack(args.bin_format, sum(
                        b * 2**i for i, b in enumerate(x))))
    else:
        for fn in commands(args.commands):
            for x in fn(args.bits):
                print(''.join('<>' if i else '..' for i in x))


def commands(cmds):
    repeat_group = 1

    for cmd in cmds:
        if cmd.isnumeric():
            repeat_group = int(cmd)
            continue
        for i in range(repeat_group):
            ci = iter(re.split('(\d+)', cmd))
            c = next(ci)
            if c:
                yield CMDS[c]
            for n, c in zip(ci, ci):
                for ni in range(int(n)):
                    yield CMDS[c]
        repeat_group = 1


if __name__ == '__main__':
    main()
