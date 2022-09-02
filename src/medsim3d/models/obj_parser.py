# https://all3dp.com/1/obj-file-format-3d-printing-cad/
import open3d as o3d
import numpy as np
from medsim3d.models.off_writer import OFFWriter
from medsim3d.models.viewer3d import Viewer3D

class ObjRawParser:

    def __init__(self,model_file):
        self.vertices = []
        self.faces = []
        self.faces_vn = []
        self.faces_vt = []
        self.vts = []
        self.vns = []
        self.mtllibs = []
        self.model_file=model_file

    def parse(self,to_triangle_mesh=False,split=' '):
        # obj_file="models/male.obj"

        with open(self.model_file,'r') as fobj:
            for line in fobj:
                line=line.strip()
                if line=="":
                    continue
                if line.startswith("#"):
                    line = fobj.readline().strip()
                    continue
                ls=line.split(split)
                # print(ls)
                if ls[0]=="mtllib":
                    self.mtllibs.append(ls[1])
                if ls[0]=="v" and len(ls)==4: # vertices
                    vertice=[float(v) for v in ls[1:]]
                    self.vertices.append(vertice)
                if ls[0]=="f": # faces
                    if not to_triangle_mesh:
                        list_f=[]
                        list_fvt=[]
                        list_fvn=[]
                        for v in ls[1:]:
                            if '/' in v:
                                vv=v.split("/")
                                f=vv[0]
                                fvt=vv[1]
                                fvn=vv[2]
                                list_f.append(int(f))

                                list_fvt.append(fvt)
                                list_fvn.append(fvn)
                            else:
                                list_f.append(int(v))
                        self.faces.append(list_f)
                        if len(list_fvt) != 0:
                            self.faces_vt.append(list_fvt)
                            self.faces_vn.append(list_fvn)
                    else:
                        # convert polygon to triangles
                        list_triangles=self.tripoly(ls[1:])
                        for triangle in list_triangles:
                            ll=[triangle[0],triangle[1],triangle[2]]
                            list_f = []
                            list_fvt = []
                            list_fvn = []
                            for v in ll:
                                if '/' in v:
                                    vv = v.split("/")
                                    f = vv[0]
                                    fvt = vv[1]
                                    fvn = vv[2]
                                    list_f.append(int(f))
                                    list_fvt.append(int(fvt))
                                    list_fvn.append(int(fvn))
                                else:
                                    list_f.append(int(v))
                            self.faces.append(list_f)
                            if len(list_fvt) != 0:
                                self.faces_vt.append(list_fvt)
                                self.faces_vn.append(list_fvn)

                if ls[0]=="vn":
                    vn=[float(v) for v in ls[1:]]
                    self.vns.append(vn)
                if ls[0] == "vt":
                    vt = [float(v) for v in ls[1:]]
                    self.vts.append(vt)

        print(f"Vertices: {len(self.vertices)}, Faces: {len(self.faces)}, Vertices Normal: {len(self.vns)}, Vertices Texture: {len(self.vts)}")
        print(f"Faces VN: {len(self.faces_vn)}, Faces VT: {len(self.faces_vt)}")

    def save_to_pointcloud(self,ply_file):
        pcd = o3d.geometry.PointCloud()

        pcd.points = o3d.utility.Vector3dVector(self.vertices)

        o3d.io.write_point_cloud(ply_file, pcd, write_ascii=True)

    def tripoly(self,poly):
        return [(poly[0], b, c) for b, c in zip(poly[1:], poly[2:])]

    def save_to_off(self,save_off_file):
        OFFWriter(model_file=save_off_file,vertices=self.vertices,faces=self.faces).write()

    def save_to_triangle_mesh(self,mesh_file,N=5,show=False):
        vertices = o3d.utility.Vector3dVector(
            np.array(self.vertices))
        triangles = o3d.utility.Vector3iVector(
            np.array(self.faces))
        mesh_np = o3d.geometry.TriangleMesh(vertices, triangles)
        mesh_np.vertex_colors = o3d.utility.Vector3dVector(
            np.random.uniform(0, 1, size=(N, 3)))
        mesh_np.compute_vertex_normals()
        # print(np.asarray(mesh_np.triangle_normals))
        # print("Displaying mesh made using numpy ...")
        o3d.io.write_triangle_mesh(filename=mesh_file,mesh=mesh_np,write_ascii=True)
        if show:
            o3d.visualization.draw_geometries([mesh_np])


