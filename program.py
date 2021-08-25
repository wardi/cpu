#!/usr/bin/env python3

import sys

data = b''.join(
    [
        bytes(
            [
                0b10111000, # function set
                0b10001110, # Display on, cursor
                0b10000110, # Edit mode
            ]
        ),
        open(
            '/usr/share/dict/words',
            'r',
            encoding='utf-8',
        ).read(32768).encode('ascii', 'replace'),
    ]
)

sys.stdout.buffer.write(data[:32768])
