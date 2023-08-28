CGINTROTXT = {
    'M': [
        '[][]        [][]',
        '[][][]    [][][]',
        '[][][][][][][][]',
        '[][][][][][][][]',
        '[][]  [][]  [][]',
    ],
    'm': [
        '[][]        [][]',
        '[][]        [][]',
        '[][]        [][]',
        '[][]        [][]',
        '                ',
    ],
    'A': [
        '    [][][][]    ',
        '[][][][][][][][]',
        '[][]        [][]',
        '[][][][][][][][]',
        '[][][][][][][][]',
    ],
    'Z': [
        '[][][][][][][][]',
        '[][][][][][][][]',
        '            [][]',
        '    [][][][][][]',
        '[][][][][][]    ',
    ],
    'z': [
        '[][]            ',
        '[][]            ',
        '[][][][][][][][]',
        '[][][][][][][][]',
        '                ',
    ],
    'E': [
        '[][][][][][][][]',
        '[][][][][][][][]',
        '[][]            ',
        '[][][][][]      ',
        '[][][][][]      ',
    ],
    'G': [
        '    [][][][]    ',
        '[][][][][][][][]',
        '[][]        [][]',
        '[][]            ',
        '[][]            ',
    ],
    'g': [
        '[][]      [][][]',
        '[][]        [][]',
        '[][][][][][][][]',
        '    [][][][]    ',
        '                ',
    ],
}


def _rotate(glyph):
    data = []
    for y in reversed(range(0, 16, 2)):
        data.append(
            sum(
                2**j if v[y:y+2] == '[]' else 0
                for j, v in enumerate(reversed(glyph))
            )
        )
    return data


def _load(txt):
    '''rotate txt dict format into binary data and store opcode'''
    op = {}
    data = []
    for i, (cgtitle, cgvalue) in enumerate(txt.items()):
        op[cgtitle] = f'CG{i}'
        data.extend([f'B{d:02d}' for d in _rotate(cgvalue)])
    return op, data


CGINTRO, CGINTRODATA = _load(CGINTROTXT)


PLAYER_VERTICAL_1 = _rotate([
    '            []  ',
    '            [][]',
    '            [][]',
    '              []',
    '            [][]',
])

PLAYER_VERTICAL_2 = _rotate([
    '              []',
    '            [][]',
    '            [][]',
    '            []  ',
    '            [][]',
])

PLAYER_RIGHT = _rotate([
    '              []',
    '            []  ',
    '              []',
    '            []  ',
    '            [][]',
])

PLAYER_LEFT = _rotate([
    '            []  ',
    '              []',
    '            []  ',
    '              []',
    '            [][]',
])

WALL_0 = _rotate([
    '[][]            ',
    '[][]            ',
    '[][]            ',
    '[][]            ',
    '[][]            ',
])

WALL_1 = _rotate([
    '      [][]      ',
    '      [][]      ',
    '      [][]      ',
    '      [][]      ',
    '      [][]      ',
])

WALL_2 = _rotate([
    '            [][]',
    '            [][]',
    '            [][]',
    '            [][]',
    '            [][]',
])

WALLS = [
    [
        WALL_0[j] * bool(i & 1)
        | WALL_1[j] * bool(i & 2)
        | WALL_2[j] * bool(i & 4)
        for j in range(8)
    ]
    for i in range(1, 8)
]