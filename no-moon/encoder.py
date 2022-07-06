#!/usr/bin/env python3

import sys
import gzip
from itertools import zip_longest, repeat, cycle, islice

SRC_FPS = 29.97
EEPROM_SIZE = 512 * 1024 - 3  # init
NUM_LOOKAHEAD_FRAMES = 3
CLOSE_ENOUGH_PIXELS = 4
TRIM_START_FRAMES = 0
TRIM_END_FRAMES = 0

DISPLAY_COLS = 20  # full screen width

PIXELS = 5  # horizontal pixels per cgram character
LINES = 8  # vertical pixels per cgram character
COLS = 14  # video area width
ROWS = 4  # video area height
CGRAM = 8  # number of CGRAM characters available
MAX_DELTA = PIXELS * LINES * COLS * ROWS

ALL_0 = b'\x00' * 8
ALL_1 = b'\x1f' * 8

# 1-9, a-z, A-U order for display updates
order_as = '123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTU'
order = """
nz1HlLdDs6OoRg
8tMhT2vGfSxaAq
pPbCweQy3UiKu7
5IjF9rJcBkN4Em
"""

# convert to a list of positions
pos_order = [None] * (ROWS * COLS)
for y, ln in enumerate(order.strip().split('\n')):
    for x, ch in enumerate(ln):
        pos = y * DISPLAY_COLS + x
        idx = order_as.index(ch)
        pos_order[idx] = pos
assert None not in pos_order

pos_iter = cycle(pos_order)

def ovs(s):
    'convert bytes to array of single-byte reprs for output'
    return [repr(bytes([b])) for b in s]

output_override = {}
#output_override.update({i: b for (i, b) in enumerate(
#    ['E13'] + ovs(b'Bad') +
#    ['D32'] + ovs(b'Apple'),
#    start=35,
#)})
#output_override.update({i: b for (i, b) in enumerate(
#    ['D08'] + ovs(b'~1.2 kbit/s\x7f') +  # ~ is → and \xf7 is ←
#    ['E08'] + ovs(b'40x32 pixels') +
#    ['D28'] + ovs(b'8 cgram chrs') +
#    ['E28'] + ovs(b'HD44780 LCD'),
#    start=13696,
#)})
#output_override.update({i: b for (i, b) in enumerate(
#    ['D08'] + ovs(b'Bad Apple on') +
#    ['E08'] + ovs(b'32K EEPROM  ') +
#    ['D28'] + ovs(b' excess.org/') +
#    ['E28'] + ovs(b'   bad-apple'),
#    start=29586,
#)})


print('''#!/usr/bin/env python3

from mnconsts import *

with open('video.bin', 'wb') as f:
    f.write(
        INI + # function set: initial setup
        HID + # hidden cursor
        EIN # entry incrementing, no shift
    )''')

def w(x, comment=None):
    print(f'    f.write({x})' + (f' # {comment}' if comment else ''))

display_pos = 0   #  0-13 row 1, 20-33 row 2, 40-53 row 3, 60-73 row 4,  80+ cgram
display_pixels = bytearray(COLS * ROWS * LINES)
cg_pixels = bytearray([0x80] * CGRAM * LINES)  # 0x80 to force replacement of data
cg_assign = {}  # position where cgram character appears -> cgram number, ordered
bytes_sent = 0
file_frame = 0
frame_pixels = None

input_file = gzip.open(sys.argv[1], 'rb')

def read_frame():
    return input_file.read(COLS * ROWS * LINES)

def intpixels(pixels):
    "return [[0/1, ...],...] pixel values from top left to bottom right"
    ipx = []
    for y in range(LINES * ROWS + ROWS - 1):
        if y % (LINES + 1) == LINES:
            ipx.append([0] * (PIXELS * COLS + COLS - 1))
            continue
        cell_y = y // (LINES + 1)
        line = y % (LINES + 1)
        row = []
        ipx.append([int(b) for b in
            '0'.join(
                '{:05b}'.format(pixels[
                    cell_y * (LINES * COLS) + x * LINES + line
                ])
                for x in range(COLS)
            )
        ])
    return ipx

def braillepixels(ipx):
    "return braille text version of intpixel matrix"
    braille = []
    # padded intpixel matrix to avoid IndexErrors
    pipx = [r + [0] for r in ipx] + [[0] * (len(ipx[0]) + 1)] * 7
    for y in range(0, len(ipx), 4):
        braille.append(''.join(
            chr(0x2800
                + 1 * pipx[y][x]
                + 2 * pipx[y + 1][x]
                + 4 * pipx[y + 2][x]
                + 8 * pipx[y][x + 1]
                + 16 * pipx[y + 1][x + 1]
                + 32 * pipx[y + 2][x + 1]
                + 64 * pipx[y + 3][x]
                + 128 * pipx[y + 3][x + 1]
            ) for x in range(0, len(ipx[0]), 2)
        ))
    return braille

def pixeldelta(a, b):
    return bin(
        int.from_bytes(a, 'little') ^ int.from_bytes(b, 'little')
    ).count('1')

def pixel1s(a):
    return bin(int.from_bytes(a, 'little')).count('1')

def solid(a):
    n = pixel1s(a)
    if n <= CLOSE_ENOUGH_PIXELS:
        return b' '
    if n >= PIXELS * LINES - CLOSE_ENOUGH_PIXELS:
        return b'\xff'

def solid_exact(a):
    n = pixel1s(a)
    if n == 0:
        return b' '
    if n == PIXELS * LINES:
        return b'\xff'

def print_state():
    delta = pixeldelta(frame_pixels, display_pixels)
    for f, d, i in zip_longest(
            braillepixels(intpixels(frame_pixels)),
            braillepixels(intpixels(display_pixels)),
            [
                f'frame {file_frame}',
                f'bytes sent {bytes_sent}',
                f'position {position_mnemonic(display_pos)}',
                f'delta {delta}',
                '▴' * min(50, int(delta * 80 / MAX_DELTA)),
                f'cgram {len(cg_assign)}/{CGRAM}',
                ' '.join(
                    f'{position_mnemonic(p)}:CG{c}'
                    for p, c in cg_assign.items()
                ),
            ],
            fillvalue = '.',
        ):
        print('#', f, '»', d, i)

def cell(p, pixels, cgram=b''):
    "Return 8 pixel-bytes at position p"
    if p >= DISPLAY_COLS * 4:
        if p >= DISPLAY_COLS * 4 + COLS:
            raise IndexError()
        return cgram[p - DISPLAY_COLS * 4:][:8]
    if p >= DISPLAY_COLS * 3:
        if p >= DISPLAY_COLS * 3 + COLS:
            raise IndexError()
        return pixels[LINES * COLS * 3 + (p - DISPLAY_COLS * 3) * LINES:][:8]
    if p >= DISPLAY_COLS * 2:
        if p >= DISPLAY_COLS * 2 + COLS:
            raise IndexError()
        return pixels[LINES * COLS * 2 + (p - DISPLAY_COLS * 2) * LINES:][:8]
    if p >= DISPLAY_COLS:
        if p >= DISPLAY_COLS + COLS:
            raise IndexError()
        return pixels[LINES * COLS * 1 + (p - DISPLAY_COLS) * LINES:][:8]
    if p >= COLS or p < 0:
        raise IndexError(p)
    return pixels[p * LINES:][:8]

def writecell(pat, p, pixels):
    "Set 8 pixel-bytes at position p to pat"
    assert len(pat) == 8
    if p >= DISPLAY_COLS * 3:
        if p >= DISPLAY_COLS * 3 + COLS:
            raise IndexError()
        off = LINES * COLS * 3 + (p - DISPLAY_COLS * 3) * LINES
    elif p >= DISPLAY_COLS * 2:
        if p >= DISPLAY_COLS * 2 + COLS:
            raise IndexError()
        off = LINES * COLS * 2 + (p - DISPLAY_COLS * 2) * LINES
    elif p >= DISPLAY_COLS:
        if p >= DISPLAY_COLS + COLS:
            raise IndexError()
        off = LINES * COLS * 1 + (p - DISPLAY_COLS) * LINES
    elif p >= COLS:
        raise IndexError()
    else:
        off = p * LINES
    pixels[off:off + 8] = (b & 0x1f for b in pat)

def sim(b, comment=None):
    global display_pos, display_pixels, bytes_sent
    if bytes_sent in output_override:
        assert b == 'INI', (bytes_sent, b, output_override[bytes_sent])
        w(output_override[bytes_sent], comment)
        bytes_sent += 1

    elif isinstance(b, bytes):  # literal byte
        w(f'{repr(b)}', comment)
        if b == b'\xff':
            writecell(ALL_1, display_pos, display_pixels)
        elif b == b' ':
            writecell(ALL_0, display_pos, display_pixels)
        elif display_pos >= DISPLAY_COLS * 4:
            cg_pixels[display_pos - DISPLAY_COLS * 4] = ord(b)
            n = (display_pos - DISPLAY_COLS * 4) // LINES
            for k, v in cg_assign.items():
                if v == n:
                    writecell(cg_pixels[n * LINES:][:LINES], k, display_pixels)
                    break
        bytes_sent += 1
        display_pos += 1

    elif isinstance(b, str):  # mnemonic
        w(f'{b}', comment)
        bytes_sent += 1

        if b.startswith('CG'):
            n = int(b[2:])
            writecell(cg_pixels[n * LINES:][:LINES], display_pos, display_pixels)
            display_pos += 1

        if b == 'CLR':
            display_pos = 0
            display_pixels[:] = b'\x00' * len(display_pixels)

    elif isinstance(b, int):  # position (output mnemonic)
        w(position_mnemonic(b), comment)
        bytes_sent += 1
        display_pos = b

def position_mnemonic(pos):
    if pos >= DISPLAY_COLS * 4:
        return f'C{(pos - DISPLAY_COLS * 4) // LINES:01d}{(pos - DISPLAY_COLS * 4) % LINES:01d}'
    elif pos >= DISPLAY_COLS * 3:
        return f'E{pos - DISPLAY_COLS * 3 + 20:02d}'  # + 20 because line 4 is E20-E39
    elif pos >= DISPLAY_COLS * 2:
        return f'D{pos - DISPLAY_COLS * 2 + 20:02d}'  # + 20 because line 3 is D20-D39
    elif pos >= DISPLAY_COLS:
        return f'E{pos - DISPLAY_COLS:02d}'
    return f'D{pos:02d}'


def minimal_update(cgnum, arr, comment=None, sim_fn=sim):
    """
    yield minimal steps for update of cgram position (cgnum)
    with bytearray (arr)
    """
    cgpos = cgnum * LINES
    pos = None
    for i, (cg, b) in enumerate(zip(cg_pixels[cgpos:], arr)):
        if cg == b + 0x60:  # use printable characters from 0x60-0x7f
            continue
        if pos != i:
            yield sim_fn(cgpos + i + 80, comment)
            comment = None
        yield sim_fn(bytes([0x40 + b]))
        pos = i + 1


def encode():
    while True:

# if clear screen is better match than current display, clear it
# ** can't use CLR for this video: execution time is too long
        #delta = pixeldelta(frame_pixels, display_pixels)
        #if delta > MAX_DELTA / 2 and delta > 1.5 * pixel1s(frame_pixels):
        #    cg_assign.clear()
        #    yield sim('CLR')
        #    continue

# if cursor already on cell that needs to be all 0s or all 1s
# - (advance 1): ' ' or '\xff'
        try:
            here = cell(display_pos, frame_pixels)
        except IndexError:
            pass
        else:
            c = cell(display_pos, display_pixels)
            if (solid(here) and solid(here) != solid(c)
                    ) or (solid_exact(here) and not solid_exact(c)):
                if display_pos in cg_assign:
                    freed = cg_assign.pop(display_pos)
                    yield sim(solid(here), f'free CG{freed} at {position_mnemonic(display_pos)}')
                else:
                    yield sim(solid(here))
                continue

# choose the next cell that needs to be all 0s or all 1s next in order (leftmost applicable)
# - (advance 2): position, ' ' or '\xff'
        for pos in islice(pos_iter, COLS * ROWS):
            c = cell(pos, display_pixels)
            here = cell(pos, frame_pixels)
            if (solid(here) and solid(here) != solid(c)
                    ) or (solid_exact(here) and not solid_exact(c)):
                break
        else:
            pos = None
        if pos is not None:
            # found one, now scan left
            while True:
                p = pos - 1
                try:
                    left = cell(p, frame_pixels)
                except IndexError:
                    break
                if not solid(left) or solid(left) == solid(cell(p, display_pixels)):
                    break
                pos = p
            yield sim(pos)
            continue

# if none choose the cell with >delta next in order
        future = frame_at_bytes(bytes_sent + 10) # estimate of update cost
        future_pixels = all_frames[future]
        for pos in islice(pos_iter, COLS * ROWS):
            here = cell(pos, future_pixels)
            if pixeldelta(here, cell(pos, display_pixels)) > CLOSE_ENOUGH_PIXELS:
                # check that this cell doesn't go solid very soon afterwards
                if not any(
                        solid(cell(pos, all_frames[f]))
                        for f in range(future + 1, future + 1 + NUM_LOOKAHEAD_FRAMES)
                    ):
                    break
        else:
# if none choose the cell delta > 0 next in order
# - if assigned (advance 7):
#     cgposition, 8 * bit pattern
# - if unassigned, 1+ available (advance 9):
#     cgposition, 8 * bit pattern, position, cgchar
            for pos in islice(pos_iter, COLS * ROWS):
                here = cell(pos, future_pixels)
                if pixeldelta(here, cell(pos, display_pixels)):
                    # check that this cell doesn't go solid very soon afterwards
                    if not any(
                            solid_exact(cell(pos, all_frames[f]))
                            for f in range(future + 1, future + 1 + NUM_LOOKAHEAD_FRAMES)
                        ):
                        break
            else:
# if none emit NOP (advance 1)
                yield sim('INI')  # stand-in for "NOP"
                continue

# - if assigned (advance 7):  * or update-in-place (advance <7)
#     cgposition, 8 * bit pattern
        if pos in cg_assign:
            reorder = cg_assign.pop(pos)
            cg_assign[pos] = reorder  # move to last
            yield from minimal_update(
                reorder,
                cell(pos, future_pixels),
                f'update assigned CG{reorder} at {position_mnemonic(pos)}',
            )
            continue

# - if unassigned, 1+ available (advance 9):
#     cgposition, 8 * bit pattern, position, cgchar
        if len(cg_assign) < CGRAM:
            best = None
            shortest = None
            for i in range(CGRAM):
                if i in cg_assign.values():
                    continue
                steps = sum(1 for e in minimal_update(
                    i,
                    cell(pos, future_pixels),
                    sim_fn=(lambda x,y=0:x),
                ))
                if best is None or steps < shortest:
                    best = i
                    shortest = steps
            assert best is not None
            yield from minimal_update(
                best,
                cell(pos, future_pixels),
                f'assign CG{best} to {position_mnemonic(pos)} ({shortest} steps)',
            )
            yield sim(pos)
            cg_assign[pos] = best
            yield sim(f'CG{best}')

# - else (advance 13):
#     reorder oldest assigned to last
#     position of oldest assigned, ' ' or '\xff'
#     cgposition, 8 * bit pattern, position, cgchar
        else:
            oldpos, oldest = next(iter(cg_assign.items()))
            cg_assign.pop(oldpos)
            yield sim(oldpos, f'evict CG{oldest} at {position_mnemonic(oldpos)}')
            yield sim(
                b'\xff' if pixeldelta(
                    cell(oldpos, future_pixels), ALL_0) > (LINES * PIXELS / 2) else b' '
            )
            yield from minimal_update(
                oldest,
                cell(pos, future_pixels),
                f'reassign CG{oldest} to {position_mnemonic(pos)}'
            )
            yield sim(pos)
            cg_assign[pos] = oldest
            yield sim(f'CG{oldest}')




def frame_at_bytes(bsent):
    return num_src_frames * bsent // EEPROM_SIZE

encoder = encode()

all_frames = []
while True:
    frame_pixels = read_frame()
    if not frame_pixels:
        break
    all_frames.append(frame_pixels)
#all_frames = all_frames[TRIM_START_FRAMES:-TRIM_END_FRAMES]
num_src_frames = len(all_frames)
all_frames.extend([frame_pixels] * NUM_LOOKAHEAD_FRAMES)

while file_frame < num_src_frames:
    frame_pixels = all_frames[file_frame]
    next(encoder)
    if frame_at_bytes(bytes_sent) > file_frame:
        print_state()
        file_frame = frame_at_bytes(bytes_sent)
