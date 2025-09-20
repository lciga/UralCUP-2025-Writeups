#!/usr/bin/env python3
import mmap, re, sys, os

if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} <dump.raw>", file=sys.stderr)
    sys.exit(1)

path = sys.argv[1]
if not os.path.isfile(path):
    print("File not found", file=sys.stderr); sys.exit(1)

# Регексы:
# ASCII: UralCTF{...} — внутри любые символы до } кроме нулей/переводов строки (ограничим длину до 256)
re_ascii = re.compile(rb'UralCTF\{[^}\x00\r\n]{0,256}\}')
# UTF-16LE: U r a l C T F { ... } с нулевыми байтами между
def w(s: str) -> bytes: return s.encode('utf-16le')
re_utf16 = re.compile(w('UralCTF{') + rb'(?:[^\x00}\r\n]\x00){0,256}' + w('}'))

replacements = 0

with open(path, 'r+b') as f:
    with mmap.mmap(f.fileno(), 0) as mm:
        # ASCII
        for m in re_ascii.finditer(mm):
            L = m.end() - m.start()
            # Требовали "*****" — но длину сохраняем, дополняя остальными '*'
            mm[m.start():m.end()] = b'*' * L
            replacements += 1

        # UTF-16LE
        for m in re_utf16.finditer(mm):
            L = m.end() - m.start()
            # В UTF-16LE звёздочка — b'*\x00'
            star2 = b'*\x00'
            mm[m.start():m.end()] = star2 * (L // 2)  # чётная длина гарантирована
            replacements += 1

print(f"Replaced {replacements} occurrences.")
