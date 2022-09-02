import open3d as o3d
import numpy as np

class ObjReader:
    def __init__(self,model_file):
        self.model_file=model_file

    def read(self):
        textured_mesh = o3d.io.read_triangle_mesh(self.model_file)
        v=np.asarray(textured_mesh.vertices)
        f=np.asarray(textured_mesh.triangles)
        print(f"Number of vertices: {len(v)}, number of faces: {len(f)}")
        # print(np.asarray(textured_mesh.vertices))
        # print(np.asarray(textured_mesh.triangles))
        # o3d.visualization.draw_geometries([textured_mesh])
        return v,f