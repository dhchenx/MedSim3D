from medsim3d.models.obj_parser import ObjRawParser
from medsim3d.models.viewer3d import Viewer3D

obj_parser=ObjRawParser(model_file="../examples-netlogo/netlogo-models/models/cube.obj")
obj_parser.parse(to_triangle_mesh=False,split=' ')

obj_parser.save_to_off(save_off_file='outputs/cube.off')
Viewer3D().show_object(obj_file="outputs/cube.off")