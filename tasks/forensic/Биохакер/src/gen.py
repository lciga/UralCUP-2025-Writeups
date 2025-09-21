import random
import json
import zipfile
from io import BytesIO
import numpy as np
import matplotlib.pyplot as plt
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
import os
from PIL import Image  # Добавляем импорт Image из PIL для работы с img = Image.fromarray

# Флаг для таска
FLAG = "UralCTF{L377uС3_wiLL_74k3_0v3r_7h3_w0RLd_4ND_3n5L4V3_Y0u}"

# Параметры
NOISE_LEVEL = 0
NUM_READS = 1
READ_LENGTH = 150
PADDING_PER_READ = 30
FALSE_ANOMALY_RATE = 0

# Шаг 1: Подготовка скрытых данных
spiral_coords = []
for i, c in enumerate(FLAG):
    x = np.cos(i * 0.4)
    y = np.sin(i * 0.4)
    # Спрячем флаг в целочисленном коде символа
    z = ord(c)
    spiral_coords.append({'x': float(x), 'y': float(y), 'z': z})

hidden_data = {
    'spiral': spiral_coords,
    'hint': 'Салат нашептывает свои секреты в спираль, ищите зеленый свет.'
}
hidden_json = json.dumps(hidden_data).encode('utf-8')
print(f"Размер hidden_json: {len(hidden_json)} байт")

# Шаг 2: Генерация изображений (градиент)
def generate_spectral_image(width=256, height=256, text_to_hide=""):
    # Create an RGB array and pick a random gradient orientation and variation
    img_array = np.zeros((height, width, 3), dtype=np.uint8)
    orientation = random.choice(['vertical', 'horizontal', 'diagonal'])
    variation = random.randint(-50, 50)
    for i in range(height):
        for j in range(width):
            # Compute base gradient in green channel
            if orientation == 'vertical':
                base = int((i / height) * 255)
            elif orientation == 'horizontal':
                base = int((j / width) * 255)
            else:  # diagonal
                base = int(((i + j) / (width + height)) * 255)
            green = np.clip(base + variation, 0, 255)
            img_array[i, j] = [20, green, 20]  # primary green gradient
    
    if text_to_hide:
        # Кодируем в байты для поддержки UTF-8
        binary_text = ''.join(format(b, '08b') for b in text_to_hide.encode('utf-8') + b'\0')
        flat_red = img_array[:,:,0].ravel()
        for j in range(min(len(flat_red), len(binary_text))):
            current = flat_red[j]
            new_value = (current & 254) | int(binary_text[j])
            flat_red[j] = np.uint8(new_value)
        for j in range(len(binary_text), len(flat_red)):
            current = flat_red[j]
            new_value = (current & 254) | random.randint(0, 1)
            flat_red[j] = np.uint8(new_value)
        img_array[:,:,0] = flat_red.reshape(height, width)
    
    img = Image.fromarray(img_array, 'RGB')
    buf = BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return buf.getvalue()

image_texts = [
    "Листья выстраиваются в космическом порядке.",
    "Свет прячется в самых зеленых глубинах.",
    "Поверни спираль, чтобы увидеть вечность."
]
images = [generate_spectral_image(text_to_hide=text) for text in image_texts]
print(f"Размер первого изображения: {len(images[0])} байт")

# Шаг 3: Упаковка в ZIP
buf = BytesIO()
with zipfile.ZipFile(buf, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
    zf.writestr('data.json', hidden_json)
    for i, img in enumerate(images):
        zf.writestr(f'chlorophyll_map_{i+1}.png', img)
buf.seek(0)
zipped_data = buf.read()
print(f"Размер zipped_data: {len(zipped_data)} байт")

# Шаг 4: Стеганография в ДНК
def binary_to_dna(binary_data, noise_level):
    dna_seq = []
    for byte in binary_data:
        bin_str = format(byte, '08b')
        for bit in bin_str:
            base = 'A' if bit == '0' else 'T'
            if random.random() < noise_level:
                base = random.choice(['C', 'G'])
            dna_seq.append(base)
    return ''.join(dna_seq)

stego_dna = binary_to_dna(zipped_data, NOISE_LEVEL)
print(f"Длина stego_DNA: {len(stego_dna)} баз")

# Шаг 5: Разделение по ридам
chunk_size = max(1, len(stego_dna) // NUM_READS)
reads = []
for i in range(NUM_READS):
    start = i * chunk_size
    end = start + chunk_size if i < NUM_READS - 1 else len(stego_dna)
    chunk = stego_dna[start:end]
    padding_length = PADDING_PER_READ + random.randint(-10, 10)
    padding = ''.join(random.choice('ACGT') for _ in range(padding_length))
    full_seq = chunk + padding
    if len(full_seq) < READ_LENGTH:
        full_seq += ''.join(random.choice('ACGT') for _ in range(READ_LENGTH - len(full_seq)))
    
    record = SeqRecord(Seq(full_seq), id=f"read_{i+1}", description=f"Alien lettuce genome fragment {i+1}")
    record.letter_annotations["phred_quality"] = [random.randint(20, 40) for _ in range(len(full_seq))]
    reads.append(record)

# Шаг 6: Запись FASTQ
fastq_filename = "alien_lettuce.fastq"
with open(fastq_filename, "w") as output_handle:
    SeqIO.write(reads, output_handle, "fastq")

# Шаг 7: Blender-шаблон
blender_template = """
import math
import bpy
import json

data_str = '''JSON_DATA'''
data = json.loads(data_str)

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

curve = bpy.data.curves.new(name='DNA_Spiral', type='CURVE')
curve.dimensions = '3D'
obj = bpy.data.objects.new('DNA_Spiral', curve)
bpy.context.collection.objects.link(obj)
bpy.context.view_layer.objects.active = obj
obj.select_set(True)

# Compute offset to relocate curve start to origin for correct deformation
first_pt = data['spiral'][0]
offset_x, offset_y, offset_z = first_pt['x'], first_pt['y'], first_pt['z']
spline = curve.splines.new(type='BEZIER')
spline.bezier_points.add(len(data['spiral']) - 1)
for i, coord in enumerate(data['spiral']):
    point = spline.bezier_points[i]
    # Position points relative to the first point so curve origin aligns
    rel_x = coord['x'] - offset_x
    rel_y = coord['y'] - offset_y
    rel_z = coord['z'] - offset_z
    point.co = (rel_x, rel_y, rel_z)
    point.handle_left = (rel_x - 0.1, rel_y - 0.1, rel_z - 0.1)
    point.handle_right = (rel_x + 0.1, rel_y + 0.1, rel_z + 0.1)
    point.handle_left_type = 'AUTO'
    point.handle_right_type = 'AUTO'

full_flag = ''.join(chr(c['z']) for c in data['spiral'])
# Add text object at the first point of the spiral
first_pt = data['spiral'][0]
text_add = bpy.ops.object.text_add
# Place text at origin to align with relocated curve
text_add(location=(0, 0, 0))
text_obj = bpy.context.active_object
text_obj.data.body = full_flag
text_obj.data.size = 0.5
# Add slight extrusion and center alignment for visibility
text_obj.data.extrude = 0.05
text_obj.data.align_x = 'LEFT'
# Rotate text so its length axis aligns with curve deform axis
text_obj.rotation_euler = (0, 0, math.radians(90))
# Convert text to mesh and deform along the DNA spiral curve
mesh_add = bpy.ops.object.convert
mesh_add(target='MESH')
mesh_obj = bpy.context.active_object
# Move mesh origin to first spiral point so bending starts there
# Mesh now at origin; no manual relocation needed after curve offset
# Add solidify modifier for thickness
solidify = mesh_obj.modifiers.new(name='Solidify', type='SOLIDIFY')
solidify.thickness = 0.02

# Create helix curve for text deformation
helix_curve = bpy.data.curves.new(name='TextSpiral', type='CURVE')
helix_curve.dimensions = '3D'
helix_obj = bpy.data.objects.new('TextSpiral', helix_curve)
bpy.context.collection.objects.link(helix_obj)
# Build helix points
num_pts = len(data['spiral'])
turns = 3
radius = 1.5
pitch = 0.2
spline2 = helix_curve.splines.new(type='POLY')
spline2.points.add(num_pts - 1)
for i in range(num_pts):
    t = 2 * math.pi * turns * i / (num_pts - 1)
    x = radius * math.cos(t)
    y = radius * math.sin(t)
    z = i * pitch
    spline2.points[i].co = (x, y, z, 1)

curve_mod = mesh_obj.modifiers.new(name='CurveMod', type='CURVE')
curve_mod.object = helix_obj  # Use Helix curve to deform text mesh
curve_mod.deform_axis = 'POS_Y'  # Deform along Y axis for spiral wrapping

mat = bpy.data.materials.new(name="SaladGlow")
mat.use_nodes = True
bsdf = mat.node_tree.nodes["Principled BSDF"]
bsdf.inputs[0].default_value = (0, 1, 0, 1)
obj.data.materials.append(mat)
text_obj.data.materials.append(mat)

# Добавляем камеру
bpy.ops.object.camera_add(location=(0, -10, 0), rotation=(1.57, 0, 0))
camera = bpy.context.active_object
bpy.context.scene.camera = camera

### Export 3D model as GLB
# Remove rendering steps to speed up and avoid missing camera issues
# bpy.ops.render.render(write_still=True)
output_model = 'dna_flag_model.glb'
bpy.ops.export_scene.gltf(filepath=output_model, export_format='GLB')
print(f'3D model exported: {output_model}')
"""

with open("blender_render_template.py", "w") as f:
    f.write(blender_template)


# Шаг 9: ZIP
task_zip = "alien_salad_task.zip"
with zipfile.ZipFile(task_zip, 'w', compression=zipfile.ZIP_DEFLATED) as zipf:
    zipf.write(fastq_filename, "alien_lettuce.fastq")
    zipf.write("blender_render_template.py")
    zipf.write("README.md")

print("Таск сгенерирован! Артефакты:")
print(f"- FASTQ: {fastq_filename}")
print("- Blender шаблон: blender_render_template.py")
print("- README: README.md")
print(f"- ZIP архив: {task_zip}")
print(f"- Флаг: {FLAG}")