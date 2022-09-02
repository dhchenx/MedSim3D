from medsim3d.models.off_writer import OFFWriter
from medsim3d.models.ply_parser import *
from medsim3d.models.viewer3d import Viewer3D

Viewer3D().show_object(obj_file='datasets/ply/male-ascii.ply')

ply_parser=PLYParser(model_file="datasets/ply/male-ascii.ply")

v,f=ply_parser.parse()

Viewer3D().show_triangle_mesh_by_vf(v,f)

OFFWriter(model_file="datasets/ply/male.off",vertices=v,faces=f).write()