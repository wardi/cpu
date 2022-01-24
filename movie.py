#!/usr/bin/env python3

from constants import *

with open('movie.bin', 'wb') as f:
    f.write(

INI + # function set: initial setup
HID + # hidden cursor
EI0 + # entry incrementing, no shift
CLR + # clear screen

b'Hello from EEPROM' +

HLT # halt

)
