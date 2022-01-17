#!/usr/bin/env python3

hex_map = """
c00:04 c20:05 12 13 14 15 16 17 d00:08 d16:09 d32:0a c40:06 e00:0c e16:0d e32:0e c60:07
clr:00 c21:05 12 13 14 15 16 17 d01:08 d17:09 d33:0a c41:06 e01:0c e17:0d e33:0e c61:07
hom:00 c22:05 12 13 14 15 16 17 d02:08 d18:09 d34:0a c42:06 e02:0c e18:0d e34:0e c62:07
crt:01 c23:05 12 13 14 15 16 17 d03:08 d19:09 d35:0a c43:06 e03:0c e19:0d e35:0e c63:07
ed0:00 c24:05 12 13 14 15 16 17 d04:08 d20:09 d36:0a c44:06 e04:0c e20:0d e36:0e c64:07
ed1:00 c25:05 12 13 14 15 16 17 d05:08 d21:09 d37:0a c45:06 e05:0c e21:0d e37:0e c65:07
ei0:00 c26:05 12 13 14 15 16 17 d06:08 d22:09 d38:0a c46:06 e06:0c e22:0d e38:0e c66:07
ei1:00 clf:01 12 13 14 15 16 17 d07:08 d23:09 d39:0a c47:06 e07:0c e23:0d e39:0e c67:07
cg0:10 set:03 12 13 14 15 16 17 d08:08 d24:09 c10:04 c50:06 e08:0c e24:0d c30:05 c70:07
cg1:10 srt:01 12 13 14 15 16 17 d09:08 d25:09 c11:04 c51:06 e09:0c e25:0d c31:05 c71:07
cg2:10 hlt:80 12 13 14 15 16 17 d10:08 d26:09 c12:04 c52:06 e10:0c e26:0d c32:05 c72:07
cg3:10 off:00 12 13 14 15 16 17 d11:08 d27:09 c13:04 c53:06 e11:0c e27:0d c33:05 c73:07
cg4:10 hid:00 12 13 14 15 16 17 d12:08 d28:09 c14:04 c54:06 e12:0c e28:0d c34:05 c74:07
cg5:10 bli:00 12 13 14 15 16 17 d13:08 d29:09 c15:04 c55:06 e13:0c e29:0d c35:05 c75:07
cg6:10 cur:00 12 13 14 15 16 17 d14:08 d30:09 c16:04 c56:06 e14:0c e30:0d c36:05 c76:07
cg7:10 slt:01 12 13 14 15 16 17 d15:08 d31:09 c17:04 c57:06 e15:0c e31:0d c37:05 1f
"""

rows = hex_map.strip().split('\n')
assert len(rows) == 16, f'Expecting 16 rows, found {len(rows)}'

for i, r in enumerate(rows):
    cells = r.split()
    assert len(cells) == 16, f'Row {i} should have 16 cells: {cells}'

columns = zip(*(r.split() for r in rows))

i = 0
for col in columns:
    for cell in col:
        mnemonic, sep, code = cell.rpartition(':')
        if sep:
           print(rf'{mnemonic.upper()} = b"\x{i:02x}"')
        i += 1

#with open('hexmap.bin', 'wb') as f:
