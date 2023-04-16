import struct
from typing import List, Callable, Dict
import cmdconsts

Assemblable = Callable[
    [
        Callable[[bytes], None],
        Callable[[str], None],
        Callable[[str], None],
    ],
    None
]

def assemble(fns: List[Assemblable]):
    '''
    assemble list of functions taking (out, label, jmp) parameters.

    functions are called once to calculate label positions then again
    to output final byte values.
    '''
    position = 0
    shared_labels: Dict[str, int] = {}
    local_labels: List[Dict[str, int]] = []

    def count_bytes(b: bytes) -> None:
        nonlocal position
        position += len(b)

    def record_label(l: str) -> None:
        if l.startswith('_'):
            local_labels[-1][l] = position
        else:
            shared_labels[l] = position

    def jmp_placeholder(l: str) -> None:
        nonlocal position
        position += 3

    for fn in fns:
        local_labels.append({})
        fn(count_bytes, record_label, jmp_placeholder)

    output: List[bytes] = []

    def ignore_label(l: str) -> None:
        return

    for fn, labels in zip(fns, local_labels):

        def jmp(l: str) -> None:
            addr = labels.get(l, shared_labels.get(l))
            assert addr is not None, f'label {l} not found'
            op = getattr(cmdconsts, f'JM{addr >> 16}')
            output.append(op + struct.pack('>H', addr & 0xffff))

        fn(output.append, ignore_label, jmp)

    return b''.join(output)
