import numpy as np
from PIL import Image
# import matplotlib.pyplot as plt
from skimage.io import imshow, imread,imsave
from skimage.color import rgb2hsv, hsv2rgb
import cv2
import os
from tqdm import tqdm
import pickle
from medsim3d.vhp.edge_converter import *

def isolate_image(image_path,save_path):
    red_girl = imread(image_path)
    red_girl = cv2.resize(red_girl, (1024, 608), interpolation=cv2.INTER_CUBIC)
    # plt.figure(num=None, figsize=(8, 6), dpi=80)
    # imshow(red_girl)

    # 37,86,115
    red_filtered = (red_girl[:,:,0] > 37) & (red_girl[:,:,1] < 86) & (red_girl[:,:,2] < 115)
    # plt.figure(num=None, figsize=(8, 6), dpi=80)
    red_girl_new = red_girl.copy()
    red_girl_new[:, :, 0] = red_girl_new[:, :, 0] * red_filtered
    red_girl_new[:, :, 1] = red_girl_new[:, :, 1] * red_filtered
    red_girl_new[:, :, 2] = red_girl_new[:, :, 2] * red_filtered
    # imshow(red_girl_new)
    # imsave(save_main_color,red_girl_new)
    # plt.show()

    # remove noise

    lower_blue = np.array([100,150,0])
    upper_blue = np.array([140,255,255])
    lower_red = np.array([0,50,50]) #example value
    upper_red = np.array([10,255,255]) #example value

    img = cv2.imread("test.jpg")
    img = cv2.resize(img, (1024, 608), interpolation=cv2.INTER_CUBIC)

    # convert BGR to HSV
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # create the Mask
    mask = cv2.inRange(imgHSV, lower_red, upper_red)
    mask = 255 - mask
    res = cv2.bitwise_and(img, img, mask=mask)
    mask1 = cv2.bitwise_not(mask)
    # cv2.imshow("mask", mask)
    # cv2.imshow("cam", img)
    # cv2.imshow("res", res)
    # cv2.waitKey()
    cv2.imwrite(save_path,mask1)

def isolate_image2(image_path, save_path=None, save_main_color=None,width=1024,height=608):
    red_girl = imread(image_path)
    red_girl = cv2.resize(red_girl, (width, height), interpolation=cv2.INTER_CUBIC)
    height, width, channels = red_girl.shape
    red_girl[int(0.8 * height): height, 0: width] = (0, 0, 0)
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
    # plt.figure(num=None, figsize=(8, 6), dpi=80)
    red_girl_new = red_girl.copy()
    red_girl_new[:, :, 0] = red_girl_new[:, :, 0] * red_filtered
    red_girl_new[:, :, 1] = red_girl_new[:, :, 1] * red_filtered
    red_girl_new[:, :, 2] = red_girl_new[:, :, 2] * red_filtered
    # imshow(red_girl_new)
    if save_main_color!=None:
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

def detect_edges(img_path, save_path, t=100):
    image = cv2.imread(img_path, 0)
    edges = cv2.Canny(image, t, 3 * t)

    cv2.imwrite(save_path,edges)

from shapely.geometry import Point, Polygon
def is_in_area(coords,x,y):
    if coords==None:
        return True

    # Create Point objects
    p1 = Point(x, y)

    # Create a square
    # coords = [(24.89, 60.06), (24.75, 60.06), (24.75, 60.30), (24.89, 60.30)]
    poly = Polygon(coords)

    # PIP test with 'within'
    return p1.within(poly) # True

def detect_edges_with_polygon(img_path, save_path, t=50):
    global coords
    img = cv2.imread(img_path, 0)
    edges = cv2.Canny(img, t, 3 * t)
    cv2.imwrite(save_path, edges)

    img = cv2.imread(save_path)

    height, width, channels = img.shape

    low = np.array([0, 0, 0])
    high = np.array([180, 255, 46])
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)  # ?????????????????????hsv?????????.
    # color_edges= cv2.cvtColor(edges,cv2.COLOR_GRAY2RGB)
    # hsv=cv2.cvtColor(color_edges,cv2.COLOR_BGR2HSV)

    dst = cv2.inRange(src=hsv, lowerb=low, upperb=high)  # HSV???????????????????????????????????????

    # ?????????????????????????????????
    # ??????????????????255?????????np.where(dst==255)
    xy = np.column_stack(np.where(dst == 0))
    blank_image = np.zeros((height, width, 3), np.uint8)
    for c in xy:
        if is_in_area(coords,c[1], c[0]):
            cv2.circle(img=blank_image, center=(int(c[1]), int(c[0])), radius=1, color=(0, 0, 255), thickness=1)

    cv2.imwrite(save_path,blank_image)

coords = None

def load_polygon_file(polygon_file):
    coords = []
    list_points = pickle.load(open(polygon_file, 'rb'))
    for item in list_points:
        coords.append((item[0], item[1]))
    return coords


import time
import random

if __name__=="__main__":
    gender = "Female"

    body_parts=["abdomen", "head", "legs", "pelvis", "thighs", "thorax"]
    for body_part in body_parts:
        # body_part = "abdomen"
        body_part_root = f"../datasets/{gender}/{body_part}"
        list_body_part_time_cost=[]
        list_files=random.choices(os.listdir(body_part_root),k=10)
        for file_name in tqdm(list_files[:10]):
            # file_name = 'a_vm1455.png'
            time_cost = {}
            coords = load_polygon_file(f'datasets/areas/{gender}/{body_part}_polygon_area.pickle')

            image_path = body_part_root + "/" + file_name
            start=time.time()
            # Using Canny algorithm (86)
            detect_edges(img_path=image_path,save_path='datasets/evaluate/canny_'+file_name)
            time1=time.time()
            # Using Canny algorithm with polygons
            detect_edges_with_polygon(img_path=image_path, save_path='datasets/evaluate/canny2_' + file_name)
            time2=time.time()
            # Using single-color isolate algorithm
            isolate_image(image_path=image_path,save_path='datasets/evaluate/iso_'+file_name)
            time3=time.time()
            # Using multi-color isolate algorithm
            isolate_image2(image_path=image_path, save_main_color='datasets/evaluate/iso2c_' + file_name, save_path='datasets/evaluate/iso2_' + file_name)
            time4=time.time()
            time_cost["canny"]=time1-start
            time_cost["canny_polygon"]=time2-time1
            time_cost["isolate1"]=time3-time2
            time_cost["isolate2"]=time4-time3
            print("Method\tTime cost")
            for k in time_cost:
                print(f"{k}\t{round(time_cost[k],4)}")
            list_body_part_time_cost.append(time_cost)
            print()

        pickle.dump(list_body_part_time_cost,open(f"datasets/evaluate_results/{gender}_{body_part}.pickle","wb"))



