import pyNetLogo
import os

import quickcsv

from medsim3d.models.mat_converter import MatConverter
from medsim3d.models.obj_reader import ObjReader
from medsim3d.models.off_reader import OFFReader
from medsim3d.models.ply_parser import PLYParser

class NetLogo3DSim:
    def __init__(self,netlogo_model_name):
        self.netlogo_model_name=netlogo_model_name

    def run_model_male(self):
        self.netlogo = pyNetLogo.NetLogoLink(gui=True,thd=True,
                                       #  netlogo_home='C:/Program Files/NetLogo 6.2.1'
                                        )
        current_path = os.path.dirname(__file__)
        current_path=current_path.replace("\\","/")
        print("Current path: ",current_path)
        self.netlogo.load_model(current_path+'/app/MedSim3D-0.0.1a.nlogo3D')
        model_path=current_path+"/app/models/male.obj"
        self.netlogo.command('set scale 5')
        self.netlogo.command('set sample-rate 37')
        self.netlogo.command('set size-scale 1.2')
        self.netlogo.command(f'load-obj-file-common "{model_path}" true')
        self.netlogo.command("create-vertices")
        self.netlogo.command('user-message "The model loading is finished!"')
        # netlogo.command("create-faces")

    def get_default_libs_path(self):
        current_path = os.path.dirname(__file__)
        current_path = current_path.replace("\\", "/")
        return current_path

    def predict_3dworld_size(self,model_path:str,MAX_WORLD_SIZE=100,MAX_LOADED_POINTS=40000):
        vertices=[]
        faces=[]
        if model_path.endswith(".obj"):
            vertices, faces = ObjReader(model_file=model_path).read()
        if model_path.endswith(".off"):
            vertices,faces = OFFReader(model_file=model_path).read()
        if model_path.endswith(".ply"):
            vertices,faces = PLYParser(model_file=model_path).parse()
        if model_path.endswith(".csv"):
            list_vertices=quickcsv.read_csv(model_path)
            for vertice in list_vertices:
                x=float(vertice['x'])
                y=float(vertice['y'])
                z=float(vertice['z'])
                vertices.append([x,y,z])
        if model_path.endswith(".mat"):
            vertices,faces=MatConverter(mat_path=model_path).read_mat_points()
        list_x=[]
        list_y=[]
        list_z=[]
        for vertice in vertices:
            x=vertice[0]
            y=vertice[1]
            z=vertice[2]
            list_x.append(x)
            list_y.append(y)
            list_z.append(z)
        min_x=min(list_x)
        max_x=max(list_x)
        min_y=min(list_y)
        max_y=max(list_y)
        min_z=min(list_z)
        max_z=max(list_z)

        if min_x>0:
            min_x=0
        if max_x<0:
            max_x=0

        if min_y > 0:
            min_y = 0
        if max_y < 0:
            max_y = 0

        if min_z > 0:
            min_z = 0
        if max_z < 0:
            max_z = 0

        min_x=round(min_x,0)+1
        max_x=round(max_x,0)+1
        min_y = round(min_y, 0) + 1
        max_y = round(max_y, 0) + 1
        min_z = round(min_z, 0) + 1
        max_z = round(max_z, 0) + 1

        range_x=max_x-min_x
        range_y=max_y-min_y
        range_z=max_z-min_z
        max_size=MAX_WORLD_SIZE
        range_max=-1
        if range_x> range_max:
            range_max=range_x
        if range_y>range_max:
            range_max=range_y
        if range_z > range_max:
            range_max=range_z

        scale = max_size * 1.0 / range_max

        avg_x=int(scale*(max_x+min_x)/2)
        avg_y = int(scale * (max_y+min_y) / 2)
        avg_z = int(scale * (max_z+min_z) / 2)

        print("Actual world: ")
        print(f"World Size of X: [{min_x},{max_x}]")
        print(f"World Size of X: [{min_y},{max_y}]")
        print(f"World Size of X: [{min_z},{max_z}]")

        print("Resized world: ")
        print(f"World Size of X: [{round(min_x*scale-avg_x,0) },{round(max_x* scale-avg_x,0)}]")
        print(f"World Size of X: [{round(min_y* scale-avg_y,0)},{round(max_y* scale-avg_y,0)}]")
        print(f"World Size of X: [{round(min_z* scale-avg_z,0)},{round(max_z* scale-avg_z,0)}]")
        print("Predicted parameter values: ")
        print(f"scale = {round(scale,2)}")
        print(f"offset-x = {-avg_x}")
        print(f"offset-y = {-avg_y}")
        print(f"offset-z = {-avg_z}")

        max_points=MAX_LOADED_POINTS
        sample_rate=1
        if len(vertices)>max_points:
            sample_rate= int(len(vertices) * 1.0 / max_points)

        return {
            "scale":round(scale,2),
            "offset-x":-avg_x,
            "offset-y":-avg_y,
            "offset-z":-avg_z,
            "sample-rate": sample_rate,
            "size-scale":1.2,
            "world-min-x":int(round(min_x*scale-avg_x,0)),
            "world-max-x": int(round(max_x * scale * 1.2 - avg_x, 0)),
            "world-min-y": int(round(min_y * scale * 1.2 - avg_y, 0)),
            "world-max-y": int(round(max_y * scale * 1.2 - avg_y, 0)),
            "world-min-z": int(round(min_z* scale * 1.2 - avg_z, 0)),
            "world-max-z": int(round(max_z * scale * 1.2 - avg_z, 0)),
        }

    def run_model(self,model_path,scale=5,sample_rate=1,size_scale=1.2,auto_world_resize=False,offset_x=0,offset_y=0,offset_z=0,
                  world_min_x=-20,world_max_x=20, world_min_y=-20,world_max_y=20, world_min_z=-20,world_max_z=20
                  ):
        self.netlogo = pyNetLogo.NetLogoLink(gui=True,thd=True,
                                       #  netlogo_home='C:/Program Files/NetLogo 6.2.1'
                                        )
        current_path = os.path.dirname(__file__)
        current_path = current_path.replace("\\", "/")
        print("Current path: ",current_path)
        self.netlogo.load_model(current_path+f'/app/{self.netlogo_model_name}')
        # model_path=current_path+"/app/models/male.obj"
        self.netlogo.command(f'set scale {scale}')
        self.netlogo.command(f"set current-model-path \"{model_path}\"")
        self.netlogo.command(f"set input-selected-path \"{model_path}\"")
        self.netlogo.command(f'set offset-x {offset_x}')
        self.netlogo.command(f'set offset-y {offset_y}')
        self.netlogo.command(f'set offset-z {offset_z}')
        if not auto_world_resize:
            self.netlogo.command(f'set world-min-x {world_min_x}')
            self.netlogo.command(f'set world-max-x {world_max_x}')
            self.netlogo.command(f'set world-min-y {world_min_y}')
            self.netlogo.command(f'set world-max-y {world_max_y}')
            self.netlogo.command(f'set world-min-z {world_min_z}')
            self.netlogo.command(f'set world-max-z {world_max_z}')

        self.netlogo.command(f'set sample-rate {sample_rate}')
        self.netlogo.command(f'set size-scale {size_scale}')
        # netlogo.command(f'load-obj-file')
        # netlogo.command("create-vertices")
        # netlogo.command('user-message "The model loading is finished!"')
        # netlogo.command("create-faces")
    def close(self):
        if self.netlogo!=None:
            self.netlogo.kill_workspace()