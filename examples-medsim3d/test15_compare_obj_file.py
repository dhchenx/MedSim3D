from medsim3d.models.viewer3d import *
import open3d as o3d
obj_file='datasets/obj/IEEEP2_01_R1_3DLOOK_3DLOOK_20200622.obj'
obj_file="datasets/obj/test1.obj"
textured_mesh = o3d.io.read_triangle_mesh(obj_file)
o3d.visualization.draw_geometries([textured_mesh])
