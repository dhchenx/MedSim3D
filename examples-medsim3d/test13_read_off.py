from medsim3d.models.off_reader import OFFReader
from medsim3d.models.viewer3d import Viewer3D

# Example 1:

v,f = OFFReader(model_file='datasets/off/bathtub_0001.off').read()

Viewer3D().show_triangle_mesh_by_vf(vertices=v,faces=f)

# Example 2:
Viewer3D().show_object(obj_file='datasets/off/bathtub_0001.off')



