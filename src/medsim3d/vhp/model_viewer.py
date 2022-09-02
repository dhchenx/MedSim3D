import numpy as np
import open3d as o3d
from quickcsv import *

class ModelViewer:
    def __init__(self,model_csv_file):
        self.model_csv_file=model_csv_file

    def convert_to_ply(self,save_ply_file):
        # 1. load data
        list_item = read_csv(self.model_csv_file)
        list_points = []
        for item in list_item:
            x = float(item['x'])
            y = float(item['y'])
            z = float(item['z'])
            list_points.append([x, y, z])

        pts = np.array(list_points)

        # 2. create point cloud
        pcd = o3d.geometry.PointCloud()

        pcd.points = o3d.utility.Vector3dVector(pts)

        o3d.io.write_point_cloud(save_ply_file, pcd, write_ascii=True)

    def show(self,ply_file):

        # 3. read ply file
        pcd = o3d.io.read_point_cloud(ply_file)
        # pcd.paint_uniform_color([0.5, 0.5, 0.5])

        # 4. visualize
        o3d.visualization.draw_geometries([pcd])