from medsim3d.models.ply_parser import *
from medsim3d.models.viewer3d import Viewer3D

Viewer3D().show_object(obj_file='datasets/ply/test1.ply')

ply_parser=PLYParser(model_file="datasets/ply/test1.ply")

v,f=ply_parser.parse()

print(ply_parser.faces)

Viewer3D().show_triangle_mesh_by_vf(v,f)