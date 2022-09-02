import numpy as np
import quickcsv
import os

class MatCreator:

    def __init__(self,point_csv_file:str):
        self.point_csv_file=point_csv_file

    def __int__(self):
        pass

    def create_by_points(self,list_points,save_mat_path,use_dict=False,MIN_VALUE=10000,key_name="instance",dim=64,size_scale=1.2,save_points_csv=""):

        # 64 x 64 x 64
        # read points and create world of 64x64x64
        points = []
        if not use_dict:
            for pt in list_points:
                points.append({
                    "x":str(pt[0]),
                    "y":str(pt[1]),
                    "z":str(pt[2])
                })
        else:
            points=list_points
        min_value = MIN_VALUE

        x_min_value=100000
        y_min_value=100000
        z_min_value=100000

        for p in points:
            if float(p["x"]) < x_min_value:
                x_min_value = float(p["x"])
            if float(p["y"]) < y_min_value:
                y_min_value = float(p["y"])
            if float(p["z"]) < z_min_value:
                z_min_value = float(p["z"])


        for idx, p in enumerate(points):
            if x_min_value<0:
                points[idx]["x"] = abs(x_min_value) + float(points[idx]['x'])
            if y_min_value<0:
                points[idx]["y"] = abs(y_min_value) + float(points[idx]['y'])
            if z_min_value<0:
                points[idx]["z"] = abs(z_min_value) + float(points[idx]['z'])

        x_min_value = 100000
        y_min_value = 100000
        z_min_value = 100000
        x_max_value = -100000
        y_max_value = -100000
        z_max_value = -100000

        for p in points:
            if float(p["x"]) < x_min_value:
                x_min_value = float(p["x"])
            if float(p["y"]) < y_min_value:
                y_min_value = float(p["y"])
            if float(p["z"]) < z_min_value:
                z_min_value = float(p["z"])

            if float(p["x"]) > x_max_value:
                x_max_value = float(p["x"])
            if float(p["y"]) > y_max_value:
                y_max_value = float(p["y"])
            if float(p["z"]) > z_max_value:
                z_max_value = float(p["z"])

        max_value = 0

        for p in points:
            if float(p["x"]) > max_value:
                max_value = float(p["x"])
            if float(p["y"]) > max_value:
                max_value = float(p["y"])
            if float(p["z"]) > max_value:
                max_value = float(p["z"])

        print(f"min: {min_value}, max: {max_value}")

        size = max_value * size_scale

        # d = int (dim * 1.0 / size)
        d=dim * 1.0 / size

        # create an empty matrix
        matrix = []
        for z in range(dim):
            list_x = []
            for x in range(dim):
                list_y = [0 for _ in range(dim)]
                list_x.append(list_y)
            matrix.append(list_x)

        print(np.asarray(matrix).shape)

        # fill 3D points with 1
        list_new_points=[]
        points_revised = []
        for idx, p in enumerate(points):
            x = int(d * float(p["x"]))
            y = int(d * float(p["y"]))
            z = int(d * float(p["z"]))
            # print(x,y,z)
            points_revised.append(p)
            list_new_points.append({
                "x":x,
                "y":y,
                "z":z
            })
            matrix[z][x][y] = 1

        if save_points_csv!="":
            quickcsv.write_csv(save_points_csv,list_new_points)

        # save mat file
        from scipy.io import loadmat, savemat
        x = {}
        x[key_name] = matrix
        savemat(save_mat_path, x)

    def create(self,save_mat_path,MIN_VALUE=10000,key_name="instance",dim=64,size_scale=1.2):

        # 64 x 64 x 64
        # read points and create world of 64x64x64
        points = quickcsv.read_csv(csv_path=self.point_csv_file)
        min_value = MIN_VALUE

        for p in points:
            if float(p["x"]) < min_value:
                min_value = float(p["x"])
            if float(p["y"]) < min_value:
                min_value = float(p["y"])
            if float(p["z"]) < min_value:
                min_value = float(p["z"])

        if min_value < 0:
            for idx, p in enumerate(points):
                points[idx]["x"] = abs(min_value) + float(points[idx]['x'])
                points[idx]["y"] = abs(min_value) + float(points[idx]['y'])
                points[idx]["z"] = abs(min_value) + float(points[idx]['z'])

        max_value = 0

        for p in points:
            if float(p["x"]) > max_value:
                max_value = float(p["x"])
            if float(p["y"]) > max_value:
                max_value = float(p["y"])
            if float(p["z"]) > max_value:
                max_value = float(p["z"])

        size = max_value * size_scale

        d = dim / size

        # create an empty matrix
        matrix = []
        for z in range(dim):
            list_x = []
            for x in range(dim):
                list_y = [0 for _ in range(dim)]
                list_x.append(list_y)
            matrix.append(list_x)

        print(np.asarray(matrix).shape)

        # fill 3D points with 1
        points_revised = []
        for idx, p in enumerate(points):
            x = int(d * float(p["x"]))
            y = int(d * float(p["y"]))
            z = int(d * float(p["z"]))
            # print(x,y,z)
            points_revised.append(p)
            matrix[z][x][y] = 1

        # save mat file
        from scipy.io import loadmat, savemat
        x = {}
        x[key_name] = matrix
        savemat(save_mat_path, x)