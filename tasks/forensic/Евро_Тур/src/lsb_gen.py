from PIL import Image
import random

def genflag(image_path, message, output_path='output.png'):
    img = Image.open(image_path).convert('RGBA')

    pixels = img.load()
    width, height = img.size

    bin = ''.join(format(ord(char), '08b') for char in message)
    msglength = len(bin)

    if msglength % 3 != 0:
        print('чек длину флага')
        return

    tomodify = msglength // 3
    pixelindex = random.sample(range(0, width), tomodify) # пиксели вдоль верха
    pixelindex.sort()

    bit_index = 0
    for i in range(tomodify):
        x = pixelindex[i]
        r, g, b, a = pixels[x, 0]

        if bit_index < msglength:
            r = (r & ~1) | int(bin[bit_index])
            bit_index += 1
        if bit_index < msglength:
            g = (g & ~1) | int(bin[bit_index])
            bit_index += 1
        if bit_index < msglength:
            b = (b & ~1) | int(bin[bit_index])
            bit_index += 1

        a = 254;

        pixels[x, 0] = (r, g, b, a)

    img.save(output_path, "PNG")
    print(f"чек {output_path}")

path = 'image.png'
flag = 'UralCTF{wH47_d035_7h3_M0v13_H4v3_70_d0_w17H_17?}'
genflag(path, flag)
