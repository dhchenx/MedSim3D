from quickcsv import *
import open3d as o3d
import numpy as np

class PointCSVReader:

    def __init__(self,model_file):
        self.model_file=model_file

    def read_to_point_cloud(self):
        list_item = read_csv(self.model_file)
        list_points = []

        for item in list_item:
            x = float(item['x'])
            y = float(item['y'])
            z = float(item['z'])

            list_points.append([x, y, z])
        pcd = o3d.geometry.PointCloud()

        pcd.points = o3d.utility.Vector3dVector(list_points)

        return pcd

    def create_point_cloud_by_points(self,list_item):
        # 1. load data
        # list_item = read_csv(self.model_file)
        list_points=[]
        list_colors=[]

        for item in list_item:
            x = float(item['x'])
            y = float(item['y'])
            z = float(item['z'])
            list_points.append([x,y,z])
            if len(item)<=4:
                continue
            r = float(item['r']) / 255
            g = float(item['g']) / 255
            b = float(item['b']) / 255
            list_colors.append([r,g,b])

        pcd = o3d.geometry.PointCloud()



        pcd.points = o3d.utility.Vector3dVector(list_points)
        if len(list_colors)!=0:
            pcd.colors = o3d.utility.Vector3dVector(list_colors)
        return pcd

    def read_to_colored_point_cloud(self):
        # 1. load data
        list_item = read_csv(self.model_file)
        list_points=[]
        list_colors=[]

        for item in list_item:
            x = float(item['x'])
            y = float(item['y'])
            z = float(item['z'])
            list_points.append([x,y,z])
            if len(item)<=4:
                continue
            r = float(item['r']) / 255
            g = float(item['g']) / 255
            b = float(item['b']) / 255
            list_colors.append([r,g,b])

        pcd = o3d.geometry.PointCloud()



        pcd.points = o3d.utility.Vector3dVector(list_points)
        if len(list_colors)!=0:
            pcd.colors = o3d.utility.Vector3dVector(list_colors)
        return pcd