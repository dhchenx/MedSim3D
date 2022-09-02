import cv2
from tqdm import tqdm
import numpy as np
import os

from shapely.geometry import Point, Polygon
import pickle

class EdgeConverterWithInPolygon:
    def __init__(self,polygon_file,dataset_folder):
        list_points=pickle.load(open(polygon_file,'rb'))
        self.coords = []
        for item in list_points:
            print(item)
            self.coords.append((item[0], item[1]))
        self.dataset_folder=dataset_folder
        self.MalePNGRangeDict = {
            "abdomen": [1455, 1997],
            "head": [1001, 1377],
            "legs": [2265, 2878],
            "pelvis": [1732, 2028],
            "thighs": [1732, 2411],
            "thorax": [1280, 1688]
        }
        self.FemalePNGRangeDict={
            "abdomen": [1432, 1909],
            "head": [1001, 1285],
            "legs": [2200, 2730],
            "pelvis": [1703, 1953],
            "thighs": [1703, 2300],
            "thorax": [1262, 1488]
        }

        self.MalePNGPrefix = "a_vm"
        self.FeMalePNGPrefix = "avf"

    def is_in_area(self,x,y):

        # Create Point objects
        p1 = Point(x, y)

        # Create a square
        # coords = [(24.89, 60.06), (24.75, 60.06), (24.75, 60.30), (24.89, 60.30)]
        poly = Polygon(self.coords)

        # PIP test with 'within'
        return p1.within(poly) # True

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

    def detect_colored_points(self,img_path,save_path):
        # img_path = 'test.png'

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

        # 在原图的红色数字上用 金黄色 描点填充。
        for c in xy:
            x=c[1]
            y=c[0]
            if self.is_in_area(x,y):
            # print(c)
            # 注意颜色值是(b,g,r)，不是(r,g,b)
            # 坐标:c[1]是x,c[0]是y
                cv2.circle(img=img, center=(int(c[1]), int(c[0])), radius=1, color=(0, 0, 255), thickness=1)

        cv2.imwrite(save_path,img)


    def convert(self,body_part,save_edges_folder,save_detected_folder,gender='Male',t=80):
        # img_path = 'datasets/Male-Images/PNG_format/radiological/mri_converted/mvm11501.png'
        # show_edges(img_path=img_path)
        prefix = self.MalePNGPrefix
        affix=""
        if gender == "Female":
            prefix = self.FeMalePNGPrefix
            affix="a"
        if not os.path.exists(save_edges_folder):
            os.mkdir(save_edges_folder)
        if not os.path.exists(save_detected_folder):
            os.mkdir(save_detected_folder)
        current_range = self.MalePNGRangeDict
        if gender == "Female":
            current_range = self.FemalePNGRangeDict
        rr = current_range[body_part]
        min_v = rr[0]
        max_v = rr[1]

        for idx in tqdm(range(min_v, max_v + 1)):
            print(idx)
            img_path = f'{self.dataset_folder}/{prefix}{idx}{affix}.png'
            if not os.path.exists(img_path):
                continue
            save_path = f'{save_edges_folder}/{prefix}{idx}{affix}.png'
            self.save_edges(img_path=img_path, save_path=save_path, t=t)
            save_path_detect =  f'{save_detected_folder}/{prefix}{idx}{affix}.png'
            self.detect_colored_points(img_path=save_path, save_path=save_path_detect)
