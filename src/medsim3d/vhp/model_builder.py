import cv2
from tqdm import tqdm
import numpy as np
from quickcsv import *
import os
import math
import cv2

class ModelBuilder:

    def __init__(self,):
        self.MaleRadioRangeDict = {
            "frozenCT": [1006, 2882],
            "mri": [1005, 7625],
            "normalCT": [1012, 2832],
            "scoutCT": [2001, 2004],
        }
        self.FemaleRadioRangeDict = {
            # "frozenCT": [1006, 2882],
            "mri": [1014, 7584],
            "normalCT": [1001, 2734],
            # "scoutCT": [2001, 2004],
        }

    def show_edges(self,img_path, t=120):
        image = cv2.imread(img_path, 0)
        edges = cv2.Canny(image, t, 3*t)

        cv2.imshow("canny", edges)

        cv2.waitKey(0)
        cv2.destroyAllWindows()


    def save_edges(self,img_path, save_path, t=120):
        image = cv2.imread(img_path, 0)
        edges = cv2.Canny(image, t, 3 * t)

        cv2.imwrite(save_path,edges)

    def get_edges(self,img_path,  t=120):
        image = cv2.imread(img_path, 0)
        edges = cv2.Canny(image, t, 3 * t)

        return edges



    def dist(self,x1,y1,x2,y2):
        return math.sqrt((x1-x2)*(x1-x2)+(y1-y2)*(y1-y2))

    def detect_colored_points_removed_for_female(self,idx, img_path, save_path, z, count):

        # img_path='datasets/Male-Images/PNG_format/radiological/fronzenCT_converted/cvm1635f.png'

        # img_path=r'datasets\Male-Images\PNG_format\radiological\fronzenCT_detected\cvm1269f.png'

        img = cv2.imread(img_path)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)  # 色彩空间转换为hsv，分离.

        # 色相（H）是色彩的基本属性，就是平常所说的颜色名称，如红色、黄色等。
        # 饱和度（S）是指色彩的纯度，越高色彩越纯，低则逐渐变灰，取0-100%的数值。
        # 明度（V），取0-100%。
        # OpenCV中H,S,V范围是0-180,0-255,0-255
        low = np.array([0, 0, 0])
        high = np.array([180, 255, 46])

        dst = cv2.inRange(src=hsv, lowerb=low, upperb=high)  # HSV高低阈值，提取图像部分区域

        # 寻找白色的像素点坐标。
        # 白色像素值是255，所以np.where(dst==255)
        xy = np.column_stack(np.where(dst == 0))
        # print(xy)

        # center point
        c_x = 256
        c_y = 256

        '''
        横向：y
        竖向：x

        '''

        # 在原图的红色数字上用 金黄色 描点填充。
        list_points = []
        for c in xy:

            y = c[0]
            x = c[1]

            if (idx >= 1001 and idx <= 1209 and self.dist(x, y, c_x, c_y) <= 250) or (
                    idx > 1209 and self.dist(x, y, c_x, c_y) <= 250 and y < 380):
                # print(c, dist(c_x, c_y, x, y))
                # 注意颜色值是(b,g,r)，不是(r,g,b)
                # 坐标:c[1]是x,c[0]是y
                cv2.circle(img=img, center=(int(c[1]), int(c[0])), radius=1, color=(0, 0, 255), thickness=1)
                if count % 1 == 0:
                    if (idx >= 1001 and idx <= 1209):  # 头部
                        model = {
                            "id": idx,
                            "x": round((x - 255) / 10 * 0.6, 4),
                            "y": round((y - 255) / 10 * 0.6 - 2, 4),
                            "z": round((z - 3.5 * 512 / 2) / 10, 4)
                        }
                    elif idx >= 2116:
                        model = {
                            "id": idx,
                            "x": round((x - 255) / 10 * 0.75, 4),
                            "y": round((y - 255) / 10 * 0.75, 4),
                            "z": round((z - 3.5 * 512 / 2) / 10, 4)
                        }
                    else:
                        model = {
                            "id": idx,
                            "x": (x - 255) / 10,
                            "y": (y - 255) / 10,
                            "z": round((z - 3.5 * 512 / 2) / 10, 4)
                        }
                    list_points.append(model)

        cv2.imwrite(save_path, img)
        return list_points

    def detect_colored_points_removed_for_man(self,idx,img_path,save_path,z,count):

        # img_path='datasets/Male-Images/PNG_format/radiological/fronzenCT_converted/cvm1635f.png'

        # img_path=r'datasets\Male-Images\PNG_format\radiological\fronzenCT_detected\cvm1269f.png'

        img = cv2.imread(img_path)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        low = np.array([0, 0, 0])
        high = np.array([180, 255, 46])

        dst = cv2.inRange(src=hsv, lowerb=low, upperb=high)

        xy = np.column_stack(np.where(dst == 0))
        # print(xy)

        # center point
        c_x=256
        c_y=256

        list_points=[]
        for c in xy:

            y=c[0]
            x=c[1]


            if   (idx >= 1012 and idx <= 1019 and  self.dist(x, y, c_x, c_y) <= 100 ) or\
                    (idx > 1019 and idx <= 1059 and  self.dist(x, y, c_x, c_y) <= 200 ) or \
                    (idx >= 1060 and idx <= 1236 and self.dist(x, y, c_x, c_y) <= 256) or \
                     ((idx > 1236 and idx < 2558) and self.dist(x, y, c_x, c_y) <= 250 and y<400 ) \
                    or (idx >= 2558 and idx<=2877 and self.dist(x, y, c_x, c_y) <= 250 and y < 350):

                if idx >= 2157 and idx <= 2382 :
                    if y < 180:
                        continue

                # print(c, dist(c_x, c_y, x, y))
                # 注意颜色值是(b,g,r)，不是(r,g,b)
                # 坐标:c[1]是x,c[0]是y
                cv2.circle(img=img, center=(int(c[1]), int(c[0])), radius=1, color=(0, 0, 255), thickness=1)


                if count % 1 == 0:
                    if (idx >= 1012 and idx <= 1236): # 头部
                        model = {
                            "id": idx,
                            "x": round((x-255) / 10 * 0.6,4),
                            "y": round((y-255)/10 * 0.6 - 5,4) ,
                            "z": round((z - 3.5*512/2)/10,4)
                        }
                    elif idx>=2659:
                        model = {
                            "id": idx,
                            "x": (x - 255) / 10,
                            "y": (y - 255) / 10 + 4,
                            "z": round((z - 3.5 * 512 / 2) / 10, 4)
                        }
                    else:
                        model = {
                            "id": idx,
                            "x": (x - 255) / 10 ,
                            "y":(y - 255) / 10 ,
                            "z": round((z - 3.5 * 512 / 2) / 10, 4)
                        }

                    list_points.append(model)

        cv2.imwrite(save_path, img)
        return list_points

    def build(self,converted_folder,edge_folder,detected_folder,output_model_path,body_rate=3.5,t=100,gender='Male',ct_type='normalCT',
              start_v=-1, end_v=-1,save_csv=True
              ):
        # img_path = 'datasets/Male-Images/PNG_format/radiological/mri_converted/mvm11501.png'
        # show_edges(img_path=img_path)

        prefix = "cvm"
        affix = "f"
        current_range = self.MaleRadioRangeDict
        if gender == "Female":
            prefix = "cvf"
            current_range = self.FemaleRadioRangeDict
        rr = current_range[ct_type]
        min_v = rr[0]
        max_v = rr[1]
        if start_v!=-1:
            min_v=start_v
        if end_v!=-1:
            max_v=end_v

        d=body_rate*512*1.0/(rr[1]-rr[0])
        count=0
        list_all_points=[]

        for id in tqdm(range(min_v, max_v + 1)):
            # print(id)
            count += 1
            img_path = f'{converted_folder}/{prefix}{id}{affix}.png'
            if not os.path.exists(img_path):
                continue
            if gender=="Male":
                if id<=1011:
                    continue
            save_path = f'{edge_folder}/{prefix}{id}{affix}.png'
            self.save_edges(img_path=img_path,save_path=save_path,t=t)
            save_path_detect = f'{detected_folder}/{prefix}{id}{affix}.png'

            current_z=round((count+1)*d,4)
            list_points=[]
            if gender=="Male":
                list_points=self.detect_colored_points_removed_for_man(img_path=save_path,save_path=save_path_detect,idx=id,z=current_z,count=count)
            elif gender=="Female":
                list_points = self.detect_colored_points_removed_for_female(img_path=save_path, save_path=save_path_detect,
                                                                         idx=id, z=current_z, count=count)

            list_all_points+=list_points

        if save_csv:
            write_csv(output_model_path,list_all_points)

        return list_all_points
