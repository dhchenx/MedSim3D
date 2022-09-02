from medsim3d.models.viewer3d import Viewer3D
from medsim3d.models.obj_reader import *

# v,f=ObjReader(model_file='models/male.obj').read()

#Viewer3D().show_triangle_mesh_by_vf(v,f)

Viewer3D().show_object(obj_file='models/earth.obj')