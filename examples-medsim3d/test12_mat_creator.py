from medsim3d.models.mat_creator import MatCreator
from medsim3d.models.viewer3d import *

MatCreator(point_csv_file='datasets/mat/Male.csv').create(save_mat_path='datasets/mat/Male-generated.mat')

Viewer3D().show_mat_file(mat_file='datasets/mat/Male-generated.mat')

Viewer3D().show_triangle_mesh(mat_file='datasets/mat/Male-generated.mat')

