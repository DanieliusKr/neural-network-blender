import bpy
from mathutils import Vector
import numpy as np

#10x10X128
inputs = np.load("/Users/macbookpro/Documents/MMIST_training/inputs.npy")
#1x10x128
outputs = np.load("/Users/macbookpro/Documents/MMIST_training/outputs.npy")
#100x10x128
weights = np.load("/Users/macbookpro/Documents/MMIST_training/weights.npy")

def set_material_colors(obj, values, frame_num):
    # Create a new material for the object
    mat = bpy.data.materials.new(name="ColorMat")
    obj.data.materials.append(mat)
    
    # Loop through the values and set the material color for each one
    for i, val in enumerate(values):
        # Create a new color and set it on the material
        color = (val, val, val, 1.0) 
        mat.diffuse_color = color
        
        # Insert a keyframe for the material color every frame_num frames
        frame = i * frame_num
        mat.keyframe_insert(data_path="diffuse_color", frame=frame)

def create_cube_grid(n, colours, spacing, size, y_position=0):
    cube_locations = []
    for i in range(n[0]):
        for j in range(n[1]):
            x = j * (spacing + size) - (n[1] - 1) * (spacing + size) / 2
            y = y_position
            z =  (n[0] - 1) * (spacing + size) / 2 - i * (spacing + size)
            
            # Create a new cube
            bpy.ops.mesh.primitive_cube_add(location=(x, y, z))
            cube = bpy.context.active_object
            cube.scale = (size, size, size)
            
            cube_locations.append(Vector((x, y, z, 0)))
            set_material_colors(cube, colours[i][j], 20)
    return cube_locations

def create_curve_object(point_a, point_b, colours, thickness):
    # Create a new curve
    curve_data = bpy.data.curves.new('Curve', 'CURVE')
    curve_data.dimensions = '3D'
    
    # Create a new spline
    spline = curve_data.splines.new('POLY')
    spline.points.add(1)
    spline.points[0].co = point_a
    spline.points[1].co = point_b
    
    # Set the thickness of the curve
    curve_data.bevel_depth = thickness
    
    # Create a new object and link it to the scene
    obj = bpy.data.objects.new('Curve', curve_data)
    bpy.context.scene.collection.objects.link(obj)
    
    # Set the object to use the curve as its data
    obj.data = curve_data
    set_material_colors(obj, colours, 20)
    
    
    return obj

def create_curves_between_points(point_list_1, point_list_2, colours, thickness):
    # Loop through all combinations of points in the two lists
    for i, point_a in enumerate(point_list_1):
        for j, point_b in enumerate(point_list_2):
            # Create a curve object between each pair of points
            create_curve_object(point_a, point_b, colours[i][j], thickness)




l2 = create_cube_grid((10, 10), inputs, 1, 0.5, y_position=-10)
l1 = create_cube_grid((1, 10), outputs, 1, 0.5, y_position=10)


#weights should be 100x10x128
create_curves_between_points(l2, l1, weights, 0.005)
