from medsim3d.models.viewer3d import *
import open3d as o3d
# https://ieee-dataport.org/open-access/dataset-ieee-ic-3dbp-comparative-analysis-anthropometric-methods
root_path="../visible_human/deep_learning/human_body_shape/3DLOOK"

obj_file1=root_path+"/IEEEP2_63_R1_3DLOOK_3DLOOK_20200622.obj"
obj_file2=root_path+"/IEEEP2_63_R2_3DLOOK_3DLOOK_20200622.obj"

textured_mesh = o3d.io.read_triangle_mesh(obj_file1)
o3d.visualization.draw_geometries([textured_mesh])

textured_mesh = o3d.io.read_triangle_mesh(obj_file2)
o3d.visualization.draw_geometries([textured_mesh])
