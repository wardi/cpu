#!/usr/bin/env python3

from enum import IntEnum
import time
import sys
import random
import os

from RPi import GPIO

class Pins(IntEnum):
    P0 = 2
    P1 = 3
    P2 = 14

def init():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(tuple(range(28)), GPIO.OUT, initial=0)
    #GPIO.setup(tuple(range(28)), GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #UP)



if __name__ == '__main__':
    init()
