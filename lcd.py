#!/usr/bin/env python3

from RPi import GPIO
import time

import car

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


if __name__ == '__main__':
    # test car animation
    try:
        init()
        command(0b00111000)
        command(0b00001100)  # no cursor
        command(0b00000110)  # move direction, shift
        command(0b00000001)  # clear
        command(0b00000010)  # dram position

        command(0b01000000)  # cgram address 0

        write(car.OPPONENT[19])
        write(car.OPPONENT[13])
        write(car.OPPONENT[7])
        write(car.OPPONENT[1])
        write(car.PLAYER[19])
        write(car.PLAYER[13])
        write(car.PLAYER[7])
        write(car.PLAYER[1])

        #command(0b01000000)  # cgram address 0
        #print(repr(read(3)))

        command(0b10000000)
        write(b'\x00\x01\x02\x03' * 5)
        command(0b10000000 + 20)
        write(b'\x04\x05\x06\x07' * 5)

        x = 19
        while True:
            time.sleep(0.1)
            command(0b01000000)  # cgram address 0
            write(car.OPPONENT[x % 24])
            write(car.OPPONENT[(x - 6) % 24])
            write(car.OPPONENT[(x - 12) % 24])
            write(car.OPPONENT[(x - 18) % 24])
            write(car.PLAYER[x % 24])
            write(car.PLAYER[(x - 6) % 24])
            write(car.PLAYER[(x - 12) % 24])
            write(car.PLAYER[(x - 18) % 24])
            x += 1


    finally:
        cleanup()

