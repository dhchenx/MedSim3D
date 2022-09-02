import numpy as np
import open3d as o3d
from quickcsv import *
import pandas as pd
from pyntcloud import PyntCloud
class ModelViewerColor:
    def __init__(self,model_csv_file):
        self.model_csv_file=model_csv_file

    def convert_to_ply(self,save_ply_file):
        # 1. load data
        list_item = read_csv(self.model_csv_file)
        list_x=[]
        list_y=[]
        list_z=[]
        list_r=[]
        list_g=[]
        list_b=[]

        for item in list_item:
            x=float(item['x'])
            y=float(item['y'])
            z=float(item['z'])
            r=int(item['r'])
            g=int(item['g'])
            b=int(item['b'])
            list_x.append(x)
            list_y.append(y)
            list_z.append(z)
            list_r.append(r)
            list_g.append(g)
            list_b.append(b)

        data={
            'x':list_x,
        'y':list_y,
        'z':list_z,
            'red':  list_r,
            'blue': list_b,
            'green': list_g

        }

        # build a cloud
        cloud = PyntCloud(pd.DataFrame(data))

        # the argument for writing ply file can be found in
        # https://github.com/daavoo/pyntcloud/blob/7dcf5441c3b9cec5bbbfb0c71be32728d74666fe/pyntcloud/io/ply.py#L173
        cloud.to_file(save_ply_file, as_text=write_text)

    def show(self,ply_file):
        # 3. read ply file
        pcd = o3d.io.read_point_cloud(ply_file)
        # pcd.paint_uniform_color([0.5, 0.5, 0.5])

        # 4. visualize
        o3d.visualization.draw_geometries([pcd])