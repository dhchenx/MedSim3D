import open3d as o3d
from medsim3d.models.mat_converter import *

class Viewer3D:
    def __init__(self):
        pass

    def show_point_cloud(self,ply_file,uniform_color=None):
        # 3. read ply file
        pcd = o3d.io.read_point_cloud(ply_file)
        if uniform_color!=None:
            pcd.paint_uniform_color(uniform_color)

        # 4. visualize
        o3d.visualization.draw_geometries([pcd])

    def show_mat_file(self,mat_file,cube_len=64,threshold=0.5):
        v,f=MatConverter(mat_path=mat_file).read_mat_points(cube_len=cube_len,threshold=threshold)
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(v)
        o3d.visualization.draw_geometries([pcd])

    def show_triangle_mesh_by_vf(self,vertices,faces,N=5):

        vertices = o3d.utility.Vector3dVector(
            np.array(vertices))
        triangles = o3d.utility.Vector3iVector(
            np.array(faces))
        mesh_np = o3d.geometry.TriangleMesh(vertices, triangles)
        mesh_np.vertex_colors = o3d.utility.Vector3dVector(
            np.random.uniform(0, 1, size=(N, 3)))
        mesh_np.compute_vertex_normals()
        # print(np.asarray(mesh_np.triangle_normals))
        o3d.visualization.draw_geometries([mesh_np])

    def show_triangle_mesh(self,mat_file,cube_len=64,threshold=0.5,N=5):
        points,faces = MatConverter(mat_path=mat_file).read_mat_points(cube_len=cube_len, threshold=threshold)
        vertices = o3d.utility.Vector3dVector(
            np.array(points))
        triangles = o3d.utility.Vector3iVector(
            np.array(faces))
        mesh_np = o3d.geometry.TriangleMesh(vertices, triangles)
        mesh_np.vertex_colors = o3d.utility.Vector3dVector(
            np.random.uniform(0, 1, size=(N, 3)))
        mesh_np.compute_vertex_normals()
        # print(np.asarray(mesh_np.triangle_normals))
        o3d.visualization.draw_geometries([mesh_np])

    def show_object(self,obj_file,N=5):
        '''
        show .obj or .off files
        :param obj_file:
        :param N:
        :return:
        '''
        # obj_file2 = root_path + "/IEEEP2_63_R2_3DLOOK_3DLOOK_20200622.obj"

        textured_mesh = o3d.io.read_triangle_mesh(obj_file)

        textured_mesh.vertex_colors = o3d.utility.Vector3dVector(
            np.random.uniform(0, 1, size=(N, 3)))
        textured_mesh.compute_vertex_normals()

        o3d.visualization.draw_geometries([textured_mesh])