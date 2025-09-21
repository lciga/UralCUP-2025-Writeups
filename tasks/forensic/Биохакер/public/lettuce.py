
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

first_pt = data['spiral'][0]
offset_x, offset_y, offset_z = first_pt['x'], first_pt['y'], first_pt['z']
spline = curve.splines.new(type='BEZIER')
spline.bezier_points.add(len(data['spiral']) - 1)
for i, coord in enumerate(data['spiral']):
    point = spline.bezier_points[i]
    rel_x = coord['x'] - offset_x
    rel_y = coord['y'] - offset_y
    rel_z = coord['z'] - offset_z
    point.co = (rel_x, rel_y, rel_z)
    point.handle_left = (rel_x - 0.1, rel_y - 0.1, rel_z - 0.1)
    point.handle_right = (rel_x + 0.1, rel_y + 0.1, rel_z + 0.1)
    point.handle_left_type = 'AUTO'
    point.handle_right_type = 'AUTO'

full_flag = ''.join(chr(c['z']) for c in data['spiral'])
first_pt = data['spiral'][0]
text_add = bpy.ops.object.text_add
text_add(location=(0, 0, 0))
text_obj = bpy.context.active_object
text_obj.data.body = full_flag
text_obj.data.size = 0.5
text_obj.data.extrude = 0.05
text_obj.data.align_x = 'LEFT'
text_obj.rotation_euler = (0, 0, math.radians(90))
mesh_add = bpy.ops.object.convert
mesh_add(target='MESH')
mesh_obj = bpy.context.active_object
solidify = mesh_obj.modifiers.new(name='Solidify', type='SOLIDIFY')
solidify.thickness = 0.02

helix_curve = bpy.data.curves.new(name='TextSpiral', type='CURVE')
helix_curve.dimensions = '3D'
helix_obj = bpy.data.objects.new('TextSpiral', helix_curve)
bpy.context.collection.objects.link(helix_obj)
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
curve_mod.object = helix_obj  
curve_mod.deform_axis = 'POS_Y'  
mat = bpy.data.materials.new(name="SaladGlow")
mat.use_nodes = True
bsdf = mat.node_tree.nodes["Principled BSDF"]
bsdf.inputs[0].default_value = (0, 1, 0, 1)
obj.data.materials.append(mat)
text_obj.data.materials.append(mat)

bpy.ops.object.camera_add(location=(0, -10, 0), rotation=(1.57, 0, 0))
camera = bpy.context.active_object
bpy.context.scene.camera = camera

output_model = 'dna_flag_model.glb'
bpy.ops.export_scene.gltf(filepath=output_model, export_format='GLB')
print(f'3D model exported: {output_model}')
