from PIL import Image


def decode(image_path):
    img = Image.open(image_path)
    pixels = img.load()
    width, height = img.size

    bits = []
    for y in range(height):
        for x in range(width):
            r, g, b, a = pixels[x, y]
            if a == 254:
                bits.append(r & 1)
                bits.append(g & 1)
                bits.append(b & 1)

    byte_array = []
    for i in range(0, len(bits), 8):
        byte = bits[i:i + 8]
        if len(byte) == 8:
            byte_val = int(''.join(map(str, byte)), 2)
            byte_array.append(byte_val)
    flag = ''.join(map(chr, byte_array))
    return flag


img = 'restored.png'
flag = decode(img)
print(flag)
