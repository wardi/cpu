#!/usr/bin/env python3

from enum import IntEnum
import time
import sys
import random
import os

from RPi import GPIO

import pattern

# GPIO pins in order along connector
PINS = [
    2,
    3,
    4,
    14,
    15,
    18, # 17,
    17, # 18,
    27,
    22,
    23,
    24,
    10,
    9,
    25,
    11,
    8,
    7,
    0,
    1,
    5,
    12, # 6,
    6,  # 12,
    13,
    19,
    16,
    26,
    20,
    21,
]

class GPIOFunction(IntEnum):
    IN = GPIO.IN
    OUT = GPIO.OUT
    SPI = GPIO.SPI
    I2C = GPIO.I2C
    HARD_PWM = GPIO.HARD_PWM
    SERIAL = GPIO.SERIAL
    UNKNOWN = GPIO.UNKNOWN


def init():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

COMMANDS = {}

def command(fn):
    COMMANDS[fn.__name__] = fn

@command
def state():
    for i, p in enumerate(PINS):
        print(i, ':', GPIOFunction(GPIO.gpio_function(p)).name)

@command
def out_low():
    GPIO.setup(PINS, GPIO.OUT, initial=0)

@command
def out_high():
    GPIO.setup(PINS, GPIO.OUT, initial=1)

@command
def in_up():
    GPIO.setup(PINS, GPIO.IN, pull_up_down=GPIO.PUD_UP)

@command
def in_down():
    GPIO.setup(PINS, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

@command
def in_off():
    GPIO.setup(PINS, GPIO.IN, pull_up_down=GPIO.PUD_OFF)

@command
def read():
    GPIO.setup(PINS, GPIO.IN, pull_up_down=GPIO.PUD_OFF)
    for i, p in enumerate(PINS):
        print(i, ':', GPIO.input(p))

@command
def demo():    
    while True:
        for fn in pattern.PROGRAM:
            for x in fn(len(PINS)):
                GPIO.setup(PINS, GPIO.OUT)
                GPIO.output(PINS, list(x))
                time.sleep(0.05)
        

def main():
    init()
    for v in sys.argv[1:]:
        if v not in COMMANDS:
            continue
        return COMMANDS[v]()
    else:
        print('please specify one of:', ','.join(COMMANDS))
        return -1

if __name__ == '__main__':
    sys.exit(main())

