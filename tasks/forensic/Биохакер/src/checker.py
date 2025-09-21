import os
from Bio import SeqIO
from PIL import Image
import numpy as np
import zipfile
from io import BytesIO
import json
import subprocess
import shutil

# Шаг 1: Читаем FASTQ и извлекаем все биты из A/T нуклеотидов
if not os.path.exists('alien_lettuce.fastq'):
    raise FileNotFoundError("Файл alien_lettuce.fastq не найден!")
signal_bits = ''
for rec in SeqIO.parse('alien_lettuce.fastq', 'fastq'):
    for base in str(rec.seq):
        if base in ('A', 'T'):
            signal_bits += '0' if base == 'A' else '1'
signal_bits = signal_bits[:len(signal_bits)//8*8]
binary_data = bytes(int(signal_bits[i:i+8], 2) for i in range(0, len(signal_bits), 8))
print(f"Извлечённые байты (первые 2): {binary_data[:2].hex()}")

# Шаг 2: Отрезаем возможный padding после EOCD и распаковываем ZIP
eocd_sig = b'PK\x05\x06'
idx = binary_data.rfind(eocd_sig)
if idx != -1 and len(binary_data) >= idx + 22:
    comment_len = int.from_bytes(binary_data[idx+20:idx+22], 'little')
    zip_end = idx + 22 + comment_len
    zip_bytes = binary_data[:zip_end]
else:
    zip_bytes = binary_data
try:
    with zipfile.ZipFile(BytesIO(zip_bytes), 'r') as zf:
        zf.extractall('extracted/')
except zipfile.BadZipFile:
    print(f"Ошибка распаковки ZIP: файл повреждён. Данные: {zip_bytes[:10].hex()}")
    raise

# Шаг 3: Проверка LSB в PNG
import glob
for png_path in sorted(glob.glob('extracted/chlorophyll_map_*.png')):
    try:
        img = Image.open(png_path)
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
        print(f"LSB Hint from {os.path.basename(png_path)}: {text.decode('utf-8')}")
    except Exception as e:
        print(f"Ошибка обработки {png_path}: {e}")

# Шаг 6: Проверка JSON и сбор флага
try:
    with open('extracted/data.json', 'r') as f:
        hidden_data = json.load(f)
    # Если JSON содержит flag_parts, берем их, иначе восстанавливаем из z-координат
    if 'flag_parts' in hidden_data:
        full_flag = ''.join(hidden_data['flag_parts'])
    else:
        # Восстанавливаем символы напрямую из z-координаты (целочисленной)
        full_flag = ''.join(
            chr(coord['z'])
            for coord in hidden_data['spiral']
        )
    print(f"Собранный флаг: {full_flag}")
except (FileNotFoundError, json.JSONDecodeError) as e:
    print(f"Ошибка обработки JSON: {e}")
    raise

# Шаг 5: Симуляция Blender (проверка валидности JSON)
try:
    json.loads(json.dumps(hidden_data))
    print("JSON валиден для Blender: Yes")
except json.JSONDecodeError:
    print("JSON невалиден для Blender!")
    raise

# Финальная проверка
expected_flag = "UralCTF{L377uС3_wiLL_74k3_0v3r_7h3_w0RLd_4ND_3n5L4V3_Y0u}"
if full_flag == expected_flag:
    print("Валидация успешна: Флаг совпадает!")
else:
    print(f"Ошибка валидации: Ожидался {expected_flag}, получен {full_flag}")