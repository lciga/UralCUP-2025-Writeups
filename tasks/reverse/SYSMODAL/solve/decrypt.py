def transform(data: bytes) -> bytes:
    key = [0x07, 0x4E, 0x21, 0x06, 0x4D]
    pos = 0
    out = bytearray()

    for b in data:
        out.append(b ^ key[pos])
        pos += 1
        if pos >= len(key):
            pos = 0
    return bytes(out)

with open("file", "rb") as f:
    raw = f.read()
processed = transform(raw)
with open("file.out", "wb") as f:
    f.write(processed)