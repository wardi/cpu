CGTXT = {
    'up': [
        '    []          ',
        '  [][][]        ',
        '[][][][][]      ',
        '[][]  [][]      ',
        '[]      []      ',
    ],
    'dn': [
        '        [][][]  ',
        '      []  []  []',
        '      []      []',
        '      [][]  [][]',
        '        [][][]  ',
    ],
    'updn': [
        '    []  [][][]  ',
        '  [][][]  []  []',
        '[][][][]      []',
        '[][]  [][]  [][]',
        '[]      [][][]  ',
    ],
    'lf': [
        '      [][][]    ',
        '    [][][]      ',
        '  [][][]        ',
        '    [][][]      ',
        '      [][][]    ',
    ],
    'rt': [
        '    [][][]      ',
        '      [][][]    ',
        '        [][][]  ',
        '      [][][]    ',
        '    [][][]      ',
    ],
    'b': [
        '[][][][]        ',
        '[][]  [][]      ',
        '[][][][]        ',
        '[][]  [][]      ',
        '[][][][]        ',
    ],
    'a': [
        '        [][][]  ',
        '      [][]  [][]',
        '      [][][][][]',
        '      [][]  [][]',
        '      [][]  [][]',
    ],
    'ba': [
        '[][][]    [][]  ',
        '[][]  [][]  [][]',
        '[][][]  [][][][]',
        '[][]  [][]  [][]',
        '[][][]  []  [][]',
    ]
}

CGGRIDTXT = {
    'O..': [
        '[][]            ',
        '[][]            ',
        '[][]            ',
        '[][]            ',
        '[][]            ',
    ],
    'OO.': [
        '[][]  [][]      ',
        '[][]  [][]      ',
        '[][]  [][]      ',
        '[][]  [][]      ',
        '[][]  [][]      ',
    ],
    'OOO': [
        '[][]  [][]  [][]',
        '[][]  [][]  [][]',
        '[][]  [][]  [][]',
        '[][]  [][]  [][]',
        '[][]  [][]  [][]',
    ],
    '.OO': [
        '      [][]  [][]',
        '      [][]  [][]',
        '      [][]  [][]',
        '      [][]  [][]',
        '      [][]  [][]',
    ],
    '..O': [
        '            [][]',
        '            [][]',
        '            [][]',
        '            [][]',
        '            [][]',
    ],
    'O.O': [
        '[][]        [][]',
        '[][]        [][]',
        '[][]        [][]',
        '[][]        [][]',
        '[][]        [][]',
    ],
}

INTRO = [
    '.OOOOOOOOOO.',
    '.OOOOOOOOOO.',
    '.OOO.....OOO',
    '.OOO.....OOO',
    '.OOOOOOOOOO.',
    '.OOOOOOOOOO.',
    '.OOO...OOO..',
    '.OOO....OOO.',
    '.OOO.....OOO',
    '.OOO.....OOO',
    '............',
    '............',
    '.OOO.....OOO',
    '.OOO.....OOO',
    '..OOO...OOO.',
    '...OOO.OOO..',
    '....OOOOO...',
    '.....OOO....',
    '.....OOO....',
    '.....OOO....',
    '............',
    '............',
    '.OOOOOOOOOOO',
    '.OOOOOOOOOOO',
    '.OOOOOOOOOOO',
    '.....OOO....',
    '.....OOO....',
    '.....OOO....',
    '.....OOO....',
    '.....OOO....',
    '.....OOO....',
    '............',
    '............',
    '.OOO.....OOO',
    '.OOO.....OOO',
    '.OOO.....OOO',
    '.OOOOOOOOOOO',
    '.OOOOOOOOOOO',
    '.OOOOOOOOOOO',
    '.OOO.....OOO',
    '.OOO.....OOO',
    '.OOO.....OOO',
    '............',
    '............',
    '.OOOO...OOOO',
    '.OOOO...OOOO',
    '.OOOOO.OOOOO',
    '.OOOOO.OOOOO',
    '.OOOOOOOOOOO',
    '.OOOOOOOOOOO',
    '.OOO.OOO.OOO',
    '.OOO.OOO.OOO',
    '.OOO.OOO.OOO',
    '.OOO.OOO.OOO',
    '............',
    '............',
    '............',
    '............',
]

def _load(txt):
    '''rotate txt dict format into binary data and store mnemonic'''
    mne = {}
    data = []
    for i, (cgtitle, cgvalue) in enumerate(txt.items()):
        mne[cgtitle] = f'CG{i}'
        for y in reversed(range(0, 16, 2)):
            data.append(
                'B{:02d}'.format(
                    sum(
                        2**j if v[y:y+2] == '[]' else 0
                        for j, v in enumerate(reversed(cgvalue))
                    )
                )
            )
    return mne, data

CG, CGDATA = _load(CGTXT)

CGGRID, CGGRIDDATA = _load(CGGRIDTXT)
CGGRID['...'] = b' '
