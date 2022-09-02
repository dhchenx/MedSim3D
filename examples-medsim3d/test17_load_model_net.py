from medsim3d.datasets.model_net import *
from medsim3d.models.viewer3d import *
from medsim3d.models.off_reader import *

mnd=ModelNetDataset(dataset_folder='../visible_human/deep_learning/gans/3dgan/simple-pytorch-3dgan-master/ModelNet/ModelNet10/ModelNet10')

print(mnd.get_categories())

list_object_files=mnd.get_object_files_by_category(category='bed',split='train')

# show the first model
print(list_object_files[0])
v,f = OFFReader(model_file=list_object_files[0]).read()
print(v[:10])
print(f[:10])
Viewer3D().show_triangle_mesh_by_vf(vertices=v,faces=f)
