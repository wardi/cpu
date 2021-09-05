#!/usr/bin/env python3

import sys

words = open(
    '/usr/share/dict/words',
    'r',
    encoding='utf-8',
)

data = b''.join(
    [
        bytes(
            [
                0b10111000, # function set
                0b10001110, # Display on, cursor
                0b10000110, # Edit mode
            ]
        ),
        *(
            w.strip().encode('ascii', 'replace') + b' '
            for w in words if not w.endswith("'s\n")
        ),
    ]
)

sys.stdout.buffer.write(data[:32768])
