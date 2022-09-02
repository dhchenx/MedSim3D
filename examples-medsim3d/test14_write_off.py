from medsim3d.models.off_writer import *
from medsim3d.models.off_reader import OFFReader
from medsim3d.models.viewer3d import Viewer3D

v,f = OFFReader(model_file='datasets/off/bathtub_0001.off').read()

OFFWriter(model_file='datasets/off/bathtub-generated.off',vertices=v,faces=f).write()

v1,f1 = OFFReader(model_file='datasets/off/bathtub-generated.off').read()

Viewer3D().show_triangle_mesh_by_vf(vertices=v,faces=f)

