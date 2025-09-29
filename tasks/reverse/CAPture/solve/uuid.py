import hashlib
import struct

inp = "UmFrE|123e4567-e89b-12d3-a456-426614174000"
h = hashlib.sha256(inp.encode()).digest()

u64 = struct.unpack_from('<Q',h,0)[0]

seed = u64 - (1<<64) if u64>>63 else u64
state = seed & 0xFFFFFFFFFFFFFFFF
A = 1664525
C = 1013904223
M = 4294967296

text = inp.split('|',1)[1]
out = []

for ch in text:
    if ch == '-': out.append('-')
    else:
        state = (A*state + C) % M
        num = state % 26
        out.append(chr(97 + ((ord(ch) + num) % 26)))

print(''.join(out))
