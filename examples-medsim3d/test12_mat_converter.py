from medsim3d.models.mat_converter import *

mc=MatConverter(mat_path='datasets/mat/Male.mat')
mc.convert(output_csv_file='datasets/mat/Male.csv',
           output_ply_file='datasets/mat/Male.ply',
           output_v_file='datasets/mat/Male.points.pickle',
           output_f_file='datasets/mat/Male.faces.pickle',
           cube_len=64,threshold=0.5
           )

mc.show(ply_file='datasets/mat/Male.ply',)

mc.show_triangle_mesh(v_file='datasets/mat/Male.points.pickle',
          f_file='datasets/mat/Male.faces.pickle',)