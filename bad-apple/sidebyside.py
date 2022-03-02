#!/usr/bin/env python3

import sys

fa = open(sys.argv[1])
fb = open(sys.argv[2])

for lna, lnb in zip(fa, fb):
    print(f'{lna.rstrip()[:70]:70} {lnb.rstrip()[:70]}')
