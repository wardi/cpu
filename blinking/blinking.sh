#!/bin/bash

./pattern.py HdhDssRbnbSSrWwWw -s 42 -o blinking.bin
[ $(stat -c%s blinking.bin) -eq 256 ] || echo generated wrong size
(for i in {0..2047}; do cat blinking.bin; done) > blinking512k.bin
