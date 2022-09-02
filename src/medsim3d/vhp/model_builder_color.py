import quickcsv
from shapely.geometry import Point, Polygon
import pickle
from quickcsv import *
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from skimage.io import imshow, imread,imsave
import cv2
import os
from tqdm import tqdm
import skimage
from skimage import morphology
class ModelBuilderWithColor:
    def __init__(self,polygon_file,dataset_folder,use_color=True,include_id_in_csv=True):

        self.coords = None
        if polygon_file!=None:
            self.coords=[]
            list_points = pickle.load(open(polygon_file, 'rb'))
            for item in list_points:
                print(item)
                self.coords.append((item[0], item[1]))

        self.include_id_in_csv=include_id_in_csv

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
        self.use_color=use_color

        self.MalePNGPrefix = "a_vm"
        self.FeMalePNGPrefix = "avf"

    def is_in_area(self,x,y):
        if self.coords==None:
            return True

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
        try:
            cv2.imwrite(save_path,edges)
        except Exception as err:
            print(err)
            pass

    def get_edges(self,img_path,  t=120):
        image = cv2.imread(img_path, 0)
        edges = cv2.Canny(image, t, 3 * t)

        return edges

    def detect_colored_points(self,idx,img_path,save_path,z,original_img_path=None,detect_black=False,z_scale=1.0,resize=False):
        # img_path = 'test.png'
        if original_img_path!=None:
            try:
                im = Image.open(original_img_path)  # Can be many different formats.
                if resize:
                    width, height = im.size
                    im = im.resize((int(width / 2), int(height / 2)))
                original_img = im.load()
            except Exception as err:
                print("error: ")
                print(err)
                original_img=None
        else:
            original_img=None
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
        if detect_black:
            xy = np.column_stack(np.where(dst == 0))
        else:
            xy = np.column_stack(np.where(dst == 0))
        # print(xy)

        color_dict_HSV = {'black': [[180, 255, 30], [0, 0, 0]],
                          'white': [[180, 18, 255], [0, 0, 231]],
                          'red1': [[180, 255, 255], [159, 50, 70]],
                          'red2': [[9, 255, 255], [0, 50, 70]],
                          'green': [[89, 255, 255], [36, 50, 70]],
                          'blue': [[128, 255, 255], [90, 50, 70]],
                          'yellow': [[35, 255, 255], [25, 50, 70]],
                          'purple': [[158, 255, 255], [129, 50, 70]],
                          'orange': [[24, 255, 255], [10, 50, 70]],
                          'gray': [[180, 18, 230], [0, 0, 40]]}

        # 在原图的红色数字上用 金黄色 描点填充。
        list_useful_points=[]
        for c in xy:
            x=c[1]
            y=c[0]
            model=None
            if self.is_in_area(x,y):
            # print(c)
            # 注意颜色值是(b,g,r)，不是(r,g,b)
            # 坐标:c[1]是x,c[0]是y
                if self.coords!=None:
                    cv2.circle(img=img, center=(int(c[1]), int(c[0])), radius=1, color=(0, 0, 255), thickness=1)
                if original_img_path==None:
                    if self.include_id_in_csv:
                        model = {
                            "id": idx,
                            "x": round(x * 0.33, 2),
                            "y": round(y * 0.33, 2),
                            "z": round(z*z_scale,2)

                        }
                    else:
                        model = {

                            "x": round(x * 0.33, 2),
                            "y": round(y * 0.33, 2),
                            "z": round(z* z_scale,2)

                        }
                else:
                    pix_color=original_img[x,y]
                    r=pix_color[0]
                    g=pix_color[1]
                    b=pix_color[2]
                    if r<10 and g<10 and b< 10:
                        continue
                    min_blue=color_dict_HSV["blue"][0]
                    max_blue=color_dict_HSV["blue"][1]
                    if r>=min_blue[0] and r<=max_blue[0] and g>=min_blue[1] and g<=max_blue[1] and b>=min_blue[2] and b<=max_blue[2]:
                        continue
                    min_green = color_dict_HSV["green"][0]
                    max_green = color_dict_HSV["green"][1]
                    if r>=min_green[0] and r<=max_green[0] and g>=min_green[1] and g<=max_green[1] and b>=min_green[2] and b<=max_green[2]:
                        continue
                    if self.include_id_in_csv:
                        model = {
                            "id": idx,
                            "x": round(x * 0.33,2),
                            "y": round(y * 0.33,2),
                            "z": round(z*z_scale,2),
                            "r":pix_color[0],
                            "g": pix_color[1],
                            "b": pix_color[2],
                        }
                    else:
                        model = {

                            "x": round(x * 0.33, 2),
                            "y": round(y * 0.33, 2),
                            "z": round(z*z_scale,2),
                            "r": pix_color[0],
                            "g": pix_color[1],
                            "b": pix_color[2],
                        }
                # print("color = ",)
                if model!=None:
                    list_useful_points.append(model)
        if save_path!=None:
            cv2.imwrite(save_path,img)
        return list_useful_points

    def isolate_image(self,image_path, save_path, save_main_color,width=2048,height=1216):
        red_girl = imread(image_path)
        red_girl = cv2.resize(red_girl, (width, height), interpolation=cv2.INTER_CUBIC)
        plt.figure(num=None, figsize=(8, 6), dpi=80)
        # imshow(red_girl)

        # 37,86,115
        red_filtered = (red_girl[:, :, 0] > 37) & (red_girl[:, :, 1] < 86) & (red_girl[:, :, 2] < 115)
        plt.figure(num=None, figsize=(8, 6), dpi=80)
        red_girl_new = red_girl.copy()
        red_girl_new[:, :, 0] = red_girl_new[:, :, 0] * red_filtered
        red_girl_new[:, :, 1] = red_girl_new[:, :, 1] * red_filtered
        red_girl_new[:, :, 2] = red_girl_new[:, :, 2] * red_filtered
        # imshow(red_girl_new)
        imsave(save_main_color, red_girl_new)
        # plt.show()

        # remove noise

        lower_blue = np.array([100, 150, 0])
        upper_blue = np.array([140, 255, 255])
        lower_red = np.array([0, 50, 50])  # example value
        upper_red = np.array([10, 255, 255])  # example value

        img = cv2.imread(save_main_color)
        img = cv2.resize(img, (width, height), interpolation=cv2.INTER_CUBIC)

        # convert BGR to HSV
        imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        # create the Mask
        mask = cv2.inRange(imgHSV, lower_red, upper_red)
        mask = 255 - mask
        res = cv2.bitwise_and(img, img, mask=mask)

        # cv2.imshow("mask", mask)
        # cv2.imshow("cam", img)
        # cv2.imshow("res", res)
        # cv2.waitKey()
        cv2.imwrite(save_path, mask)

    def isolate_image2(self,image_path, save_path=None, save_main_color=None,width=2048,height=1216):
        red_girl = imread(image_path)

        red_girl = cv2.resize(red_girl, (width, height), interpolation=cv2.INTER_CUBIC)
        height, width, channels = red_girl.shape
        red_girl[int(0.8 * height): height, 0: width] = (0, 0, 0)
        red_girl[0: height, 0:int( 0.08* width)] = (0, 0, 0)
        # plt.figure(num=None, figsize=(8, 6), dpi=80)
        # imshow(red_girl)

        # 37,86,115
        red_filtered = (red_girl[:, :, 0] > 37) & (red_girl[:, :, 1] < 86) & (red_girl[:, :, 2] < 115)
        # selected color: (184, 166, 109)
        white_filtered_min = (red_girl[:, :, 0] > 170) & (red_girl[:, :, 1] > 140) & (red_girl[:, :, 2] > 80)
        white_filtered_max = (red_girl[:, :, 0] < 200) & (red_girl[:, :, 1] < 200) & (red_girl[:, :, 2] < 130)
        white_filtered = white_filtered_min & white_filtered_max
        # selected pix's color:  (139, 116, 83)
        white_filtered2_min = (red_girl[:, :, 0] > 130) & (red_girl[:, :, 1] > 110) & (red_girl[:, :, 2] > 80)
        white_filtered2_max = (red_girl[:, :, 0] < 140) & (red_girl[:, :, 1] < 120) & (red_girl[:, :, 2] < 90)
        white_filtered2 = white_filtered2_min & white_filtered2_max
        red_filtered = red_filtered | white_filtered | white_filtered2
        plt.figure(num=None, figsize=(8, 6), dpi=80)
        red_girl_new = red_girl.copy()
        red_girl_new[:, :, 0] = red_girl_new[:, :, 0] * red_filtered
        red_girl_new[:, :, 1] = red_girl_new[:, :, 1] * red_filtered
        red_girl_new[:, :, 2] = red_girl_new[:, :, 2] * red_filtered
        # imshow(red_girl_new)
        imsave(save_main_color, red_girl_new)
        # plt.show()

        # remove noise
        lower_yellow = np.array([22, 93, 0])
        upper_yellow = np.array([45, 255, 255])

        lower_blue = np.array([100, 150, 0])
        upper_blue = np.array([140, 255, 255])
        lower_red = np.array([0, 50, 50])  # example value
        upper_red = np.array([10, 255, 255])  # example value

        img = cv2.imread(save_main_color)
        img = cv2.resize(img, (width, height), interpolation=cv2.INTER_CUBIC)

        # convert BGR to HSV
        imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        # create the Mask
        mask1 = cv2.inRange(imgHSV, lower_yellow, upper_yellow)
        mask2 = cv2.inRange(imgHSV, lower_red, upper_red)
        mask = cv2.bitwise_or(mask1, mask2)
        mask = 255 - mask
        res = cv2.bitwise_and(img, img, mask=mask)
        mask1 = cv2.bitwise_not(mask)
        # cv2.imshow("mask", mask)

        # cv2.imshow("cam", img)
        # cv2.imshow("res", res)
        # cv2.waitKey()
        cv2.imwrite(save_path,mask1)

    def remove_noise2(self,image_path,save_path, min_size=2, connectivity=2, thresold=0.1):
        # read the image, grayscale it, binarize it, then remove small pixel clusters
        im1 = plt.imread(image_path)
        im = skimage.color.gray2rgb(im1)
        grayscale = skimage.color.rgb2gray(im)

        binarized = np.where(grayscale > thresold, 1, 0)
        processed = morphology.remove_small_objects(binarized.astype(bool), min_size=min_size,
                                                    connectivity=connectivity).astype(int)

        # black out pixels
        mask_x, mask_y = np.where(processed == 0)
        im[mask_x, mask_y, :3] = 0

        # plot the result
        # plt.figure(figsize=(10, 10))
        # plt.imshow(im)

        plt.imsave(save_path, im)

    def build2(self,gender,body_part,save_edges_folder,save_detected_folder,output_model_file,replace=False,t=100,start_v=-1,end_v=-1,save_csv=True,algorithm=1):
        # img_path = 'datasets/Male-Images/PNG_format/radiological/mri_converted/mvm11501.png'
        # show_edges(img_path=img_path)

        prefix = self.MalePNGPrefix
        affix = ""
        if gender == "Female":
            prefix = self.FeMalePNGPrefix
            affix = "a"
        if not os.path.exists(save_edges_folder):
            os.mkdir(save_edges_folder)
        if not os.path.exists(save_detected_folder):
            os.mkdir(save_detected_folder)
        if not os.path.exists(save_detected_folder+f"_points"):
            os.mkdir(save_detected_folder+f"_points")
        current_range = self.MalePNGRangeDict
        if gender == "Female":
            current_range = self.FemalePNGRangeDict
        rr = current_range[body_part]
        min_v = rr[0]
        max_v = rr[1]

        if start_v!=-1:
            min_v=start_v
        if end_v!=-1:
            max_v=end_v

        # width=2048
        # height=1216 # 0.33mm
        # current_z=0 # 1mm
        # size_x=width*0.33
        # size_y=height*0.33
        d_z=0
        list_all_points=[]
        for idx in tqdm(range(min_v, max_v + 1)):
            print(idx)
            img_path = f'{self.dataset_folder}/{prefix}{idx}{affix}.png'
            save_path = f'{save_edges_folder}/{prefix}{idx}{affix}.png'
            save_path_detect = f'{save_detected_folder}/{prefix}{idx}{affix}.png'

            if not os.path.exists(img_path):
                continue

            if not os.path.exists(save_path_detect) or replace==True :
                if algorithm==1:
                    self.isolate_image(image_path=img_path,save_path=save_path_detect,save_main_color=save_path,width=1024,height=608)
                elif algorithm==2:

                    self.isolate_image2(image_path=img_path, save_path=save_path_detect, save_main_color=save_path,
                                       width=1024, height=608)
                    # remove noise
                    print("removing noise...")
                    self.remove_noise2(image_path=save_path_detect,save_path=save_path_detect)
                else:
                    raise Exception("not found algorithm")
            if not self.use_color:
                img_path=None
            list_useful_points=self.detect_colored_points(idx=idx,img_path=save_path_detect, detect_black=True,z_scale=0.33,
                                                          save_path=None,z=d_z,original_img_path=img_path,resize=True)
            print("Identified points: ",len(list_useful_points))
            d_z+=1
            # list_all_points+=list_useful_points
            if len(list_useful_points)!=0:
                quickcsv.write_csv(save_detected_folder+f"_points/{prefix}{idx}{affix}.csv",list_useful_points)
        #if save_csv:
        #    write_csv(output_model_file, list_all_points)
        return list_all_points

    def build(self,gender,body_part,save_edges_folder,save_detected_folder,output_model_file,t=100,start_v=-1,end_v=-1,save_csv=True):
        # img_path = 'datasets/Male-Images/PNG_format/radiological/mri_converted/mvm11501.png'
        # show_edges(img_path=img_path)

        prefix = self.MalePNGPrefix
        affix = ""
        if gender == "Female":
            prefix = self.FeMalePNGPrefix
            affix = "a"
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

        if start_v!=-1:
            min_v=start_v
        if end_v!=-1:
            max_v=end_v

        width=2048
        height=1216 # 0.33mm
        current_z=0 # 1mm
        size_x=width*0.33
        size_y=height*0.33
        d_z=0
        list_all_points=[]
        for idx in tqdm(range(min_v, max_v + 1)):
            print(idx)
            img_path = f'{self.dataset_folder}/{prefix}{idx}{affix}.png'
            save_path = f'{save_edges_folder}/{prefix}{idx}{affix}.png'
            save_path_detect = f'{save_detected_folder}/{prefix}{idx}{affix}.png'

            if not os.path.exists(img_path):
                continue

            if not os.path.exists(save_path):
                self.save_edges(img_path=img_path, save_path=save_path, t=t)
            if not self.use_color:
                img_path=None
            list_useful_points=self.detect_colored_points(idx=idx,img_path=save_path, save_path=save_path_detect,z=d_z,original_img_path=img_path)
            d_z+=1
            list_all_points+=list_useful_points
        if save_csv:
            write_csv(output_model_file, list_all_points)
        return list_all_points
