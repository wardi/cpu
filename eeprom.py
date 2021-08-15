#!/usr/bin/env python3

from enum import Enum

from RPi import GPIO
import datetime

class Control(Enum):
    OE_ = 17
    CE_ = 27
    WE_ = 2

class Address(Enum):
    A0 = 19
    A1 = 13
    A2 = 12
    A3 = 6
    A4 = 5
    A5 = 1
    A6 = 0
    A7 = 7
    A8 = 4
    A9 = 14
    A10 = 18
    A11 = 15
    A12 = 8
    A13 = 3
    A14 = 11

class IO(Enum):
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
    for p in Control:
        GPIO.setup(p, GPIO.OUT)
        GPIO.output(p, 1)

    for p in (*Address, *IO):
        GPIO.setup(p, GPIO.OUT)
        GPIO.output(p, 0)

init()
buttons = read()
