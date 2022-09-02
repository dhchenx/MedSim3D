import open3d as o3d
print("Testing IO for meshes ...")
mesh = o3d.io.read_triangle_mesh("datasets/ply/male.ply")
print(mesh)
o3d.io.write_triangle_mesh("datasets/ply/male-ascii.ply", mesh,write_ascii=True)