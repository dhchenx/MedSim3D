import os
import pickle

import quickcsv
import scipy.ndimage as nd
import scipy.io as io
import matplotlib
import open3d as o3d
import skimage.measure as sk
from pathlib import Path
import numpy as np

class MatConverter:

    def __init__(self,mat_path):
        self.mat_path=mat_path

    def getVoxelFromMat(self,path, cube_len=64):
        if cube_len == 32:
            voxels = io.loadmat(path)['instance'] # 30x30x30
            voxels = np.pad(voxels, (1, 1), 'constant', constant_values=(0, 0))
        elif cube_len==16:
            voxels = io.loadmat(path)['instance']  # 30x30x30
            voxels = np.pad(voxels, (1, 1), 'constant', constant_values=(0, 0))
            voxels = nd.zoom(voxels, (0.5,0.5, 0.5), mode='constant', order=0)
        elif cube_len==64:
            voxels = io.loadmat(path)['instance']  # 30x30x30
            voxels = np.pad(voxels, (1, 1), 'constant', constant_values=(0, 0))
            voxels = nd.zoom(voxels, (2,2,2), mode='constant', order=0)
        else:
            # voxels = np.load(path)
            # voxels = io.loadmat(path)['instance'] # 64x64x64
            # voxels = np.pad(voxels, (2, 2), 'constant', constant_values=(0, 0))
            # print (voxels.shape)
            d=round(cube_len/32,2)
            voxels = io.loadmat(path)['instance'] # 30x30x30
            voxels = np.pad(voxels, (1, 1), 'constant', constant_values=(0, 0))
            voxels = nd.zoom(voxels, (d,d,d), mode='constant', order=0)
            # print ('here')
        # print (voxels.shape)
        return voxels


    def getVFByMarchingCubes(self,voxels, threshold=0.5):
        v, f, norm,val = sk.marching_cubes(voxels, level=threshold)
        return v, f

    def read_mat_file(self,mat_path,points_file,cube_len=64,threshold=0.5):

        voxels=self.getVoxelFromMat(path=mat_path,cube_len=cube_len)
        v,f=self.getVFByMarchingCubes(voxels,threshold=threshold)

        list_points=[]
        # print("point: ")
        for vv in v:
            list_points.append({
                "x":vv[0],
                "y":vv[1],
                "z":vv[2]
            })
        # print("face: ")
        # for ff in f:
        #    print(ff)

        quickcsv.write_csv(points_file,list_points)
        return v,f

    def read_mat_points(self,cube_len=64,threshold=0.5):

        voxels=self.getVoxelFromMat(path=self.mat_path,cube_len=cube_len)
        v,f=self.getVFByMarchingCubes(voxels,threshold=threshold)

        return v,f

    def save_point_cloud(self,csv_file,pointcloud_file):
        # 1. load data
        list_item = quickcsv.read_csv(csv_file)
        list_points = []

        for item in list_item:
            x = float(item['x'])
            y = float(item['y'])
            z = float(item['z'])

            list_points.append([x, y, z])
        pcd = o3d.geometry.PointCloud()

        pcd.points = o3d.utility.Vector3dVector(list_points)

        o3d.io.write_point_cloud(pointcloud_file, pcd, write_ascii=True)

    def create_triangle_mesh(self,points,faces):
        N = 5
        vertices = o3d.utility.Vector3dVector(
            np.array(points))
        triangles = o3d.utility.Vector3iVector(
            np.array(faces))
        mesh_np = o3d.geometry.TriangleMesh(vertices, triangles)
        mesh_np.vertex_colors = o3d.utility.Vector3dVector(
            np.random.uniform(0, 1, size=(N, 3)))
        mesh_np.compute_vertex_normals()
        print(np.asarray(mesh_np.triangle_normals))
        print("Displaying mesh made using numpy ...")
        o3d.visualization.draw_geometries([mesh_np])

    def to_mesh_obj(self):
        points,faces=self.read_mat_points()
        N = 5
        vertices = o3d.utility.Vector3dVector(
            np.array(points))
        triangles = o3d.utility.Vector3iVector(
            np.array(faces))
        mesh_np = o3d.geometry.TriangleMesh(vertices, triangles)
        # mesh_np.vertex_colors = o3d.utility.Vector3dVector(np.random.uniform(0, 1, size=(N, 3)))
        # mesh_np.compute_vertex_normals()
        return mesh_np

    def to_mesh_obj_by_computing_vertice_mormals(self):
        points,faces=self.read_mat_points()
        N = 5
        vertices = o3d.utility.Vector3dVector(
            np.array(points))
        triangles = o3d.utility.Vector3iVector(
            np.array(faces))
        mesh_np = o3d.geometry.TriangleMesh(vertices, triangles)
        mesh_np.vertex_colors = o3d.utility.Vector3dVector(
            np.random.uniform(0, 1, size=(N, 3)))
        mesh_np.compute_vertex_normals()
        return mesh_np

    def show_point_cloud(self,pointcloud_file):
        # 3. read ply file
        pcd = o3d.io.read_point_cloud(pointcloud_file)
        # pcd.paint_uniform_color([0.5, 0.5, 0.5])

        # 4. visualize
        o3d.visualization.draw_geometries([pcd])

    def convert(self,output_csv_file,output_ply_file,output_v_file,output_f_file,cube_len=64,threshold=0.5):
        v,f=self.read_mat_file(mat_path=self.mat_path,points_file=output_csv_file,cube_len=cube_len,threshold=0.5)
        self.save_point_cloud(csv_file=output_csv_file,pointcloud_file=output_ply_file)
        # self.show_pointCloud(output_ply_file)
        # create_triangle_mesh(v,f)
        pickle.dump(v,open(output_v_file,"wb"))
        pickle.dump(f, open(output_f_file, "wb"))
        return v,f

    def show(self,ply_file):
        self.show_point_cloud(ply_file)

    def show_triangle_mesh(self,v_file,f_file):
        v=pickle.load(open(v_file,"rb"))
        f=pickle.load(open(f_file,"rb"))
        self.create_triangle_mesh(v,f)
