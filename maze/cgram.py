CGTXT = {
    'player_vertical_1': [
        '[]  ',
        '[][]',
        '[][]',
        '  []',
        '[][]',
    ],
    'player_vertical_2': [
        '  []',
        '[][]',
        '[][]',
        '[]  ',
        '[][]',
    ],
    'player_right': [
        '  []',
        '[]  ',
        '  []',
        '[]  ',
        '[][]',
    ],
    'player_left': [
        '[]  ',
        '  []',
        '[]  ',
        '  []',
        '[][]',
    ],
    'wall': [
        '[][]',
        '[][]',
        '[][]',
        '[][]',
        '[][]',
    ],
}

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


def _load(txt):
    '''rotate txt dict format into binary data and store opcode'''
    op = {}
    data = []
    for i, (cgtitle, cgvalue) in enumerate(txt.items()):
        op[cgtitle] = f'CG{i}'
        for y in reversed(range(0, 16, 2)):
            data.append(
                'B{:02d}'.format(
                    sum(
                        2**j if v[y:y+2] == '[]' else 0
                        for j, v in enumerate(reversed(cgvalue))
                    )
                )
            )
    return op, data

CG, CGDATA = _load(CGTXT)

CGINTRO, CGINTRODATA = _load(CGINTROTXT)