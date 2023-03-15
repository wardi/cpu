#!/usr/bin/env python3

import itertools

from mido import MidiFile

mid = MidiFile('1117893_2.mid')

TIME_PER_LINE = 192
MIN_NOTE = 35
MAX_NOTE = 93

def note_iter(track):
    now = 0
    notes = set()
    for msg in track:
        now += msg.time
        while now >= TIME_PER_LINE:
            yield notes
            notes = set()
            now -= TIME_PER_LINE
        if msg.type == 'note_on':
            notes.add(msg.note)
    yield notes

for i, (t1, t2) in enumerate(itertools.zip_longest(
        note_iter(mid.tracks[1]),
        note_iter(mid.tracks[2]),
        fillvalue=set(),
    )):
    print(
        (
            '#' + ''.join(
                '1' if i in t1 else '2' if i in t2 else ' '
                for i in range(MIN_NOTE, MAX_NOTE + 1)
            ) + (
                f' #{i // 8 + 1}' if i % 8 == 0 else ''
            )
        ).rstrip()
    )

