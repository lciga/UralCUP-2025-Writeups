from PIL import Image
import numpy as np

img = Image.open('extracted/chlorophyll_map_3.png')
pixels = np.array(img)
red_bits = ''.join(str(p & 1) for p in pixels[:,:,0].ravel())
text = b''
i = 0
while i < len(red_bits):
    byte = red_bits[i:i+8]
    if len(byte) == 8:
        char = int(byte, 2)
        text += bytes([char])
        if char == 0:
            break
    else:
        break
    i += 8
print(text.decode('utf-8'))