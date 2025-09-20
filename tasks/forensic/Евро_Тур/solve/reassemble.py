#!/usr/bin/env python3
import re, base64, sys

ZONE = "eurotour.com"
pat_seq = re.compile(r'(?i)^(\d{5})\.(.+?)\.' + re.escape(ZONE) + r'\.?$')
b32lab = re.compile(r'(?i)^[A-Z2-7]+$')

def pad_b32(s: str) -> str:
    return s + '=' * ((8 - len(s) % 8) % 8)

chunks = {}
with open('qnames.txt', 'r', errors='ignore') as f:
    for line in f:
        name = line.strip()
        m = pat_seq.match(name)
        if not m: 
            continue
        seq = int(m.group(1))
        middle = m.group(2).split('.')
        labels = [x for x in middle if b32lab.fullmatch(x)]
        if not labels:
            continue
        data_b32 = ''.join(x.upper() for x in labels)
        chunks[seq] = data_b32

if not chunks:
    print("no data chunks found", file=sys.stderr); sys.exit(1)

# проверка целостности
maxseq = max(chunks.keys())
missing = [i for i in range(maxseq+1) if i not in chunks]
if missing:
    print(f"missing chunks: {len(missing)} (e.g. {missing[:10]})", file=sys.stderr)
    sys.exit(2)

# склейка и декодирование
all_b32 = ''.join(chunks[i] for i in range(maxseq+1))
data = base64.b32decode(pad_b32(all_b32))
open('restored.bin','wb').write(data)
print(f"OK: wrote restored.bin ({len(data)} bytes)")
