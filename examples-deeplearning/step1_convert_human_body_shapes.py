import os
from tqdm import tqdm
from medsim3d.models.mat_creator import MatCreator
from medsim3d.models.obj_reader import *
from medsim3d.models.viewer3d import *

model_root="../examples-med3dsim/datasets/human_body_shapes/3DLOOK_3DLOOK/models"
save_root="datasets/human-body-shape/30/train"
csv_root="datasets/human-body-shape/points"
for file in tqdm(os.listdir(model_root)):
    model_file=model_root+"/"+file
    save_mat_file=save_root+"/"+file.replace(".obj",".mat")
    vertices, faces = ObjReader(model_file=model_file).read()
    MatCreator("").create_by_points(list_points=vertices, save_mat_path=save_mat_file,size_scale=1.5,dim=30,
                                    save_points_csv=csv_root+"/"+file.replace(".obj",".csv"))

    Viewer3D().show_mat_file(mat_file=save_mat_file)
