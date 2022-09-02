from medsim3d.models.obj_reader import *
from medsim3d.models.viewer3d import *

vertices, faces = ObjReader(model_file='datasets/obj/IEEEP2_01_R1_3DLOOK_3DLOOK_20200622.obj').read()
Viewer3D().show_triangle_mesh_by_vf(vertices,faces)
