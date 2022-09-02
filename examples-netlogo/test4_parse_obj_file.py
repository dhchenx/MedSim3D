from medsim3d.models.obj_parser import ObjRawParser
from medsim3d.models.viewer3d import Viewer3D

if __name__=="__main__":
    obj_parser=ObjRawParser(model_file="models/male.obj")
    obj_parser.parse(to_triangle_mesh=True)

    # Example 1:
    # obj_parser.save_to_pointcloud(ply_file='outputs/male-pointcloud.ply')
    # Viewer3D().show_point_cloud(ply_file='outputs/male-pointcloud.ply')

    # Example 2:
    obj_parser.save_to_off(save_off_file='outputs/male.off')
    Viewer3D().show_object(obj_file="outputs/male.off")

    # Example 3:
    # obj_parser.save_to_triangle_mesh(mesh_file='outputs/male-mesh.ply',show=True)

    # Example 4:
    # print(obj_parser.vertices[:5])
    # print(obj_parser.faces[:5])
    # Viewer3D().show_triangle_mesh_by_vf(vertices=obj_parser.vertices, faces=obj_parser.faces)

