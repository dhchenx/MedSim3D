import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from skimage.io import imshow, imread,imsave
from skimage.color import rgb2hsv, hsv2rgb
import cv2
import os
from tqdm import tqdm

def isolate_image(image_path,save_path=None,save_main_color=None):
    red_girl = imread(image_path)

    red_girl = cv2.resize(red_girl, (1024, 608), interpolation=cv2.INTER_CUBIC)
    height, width, channels = red_girl.shape
    red_girl[int(0.8*height): height, 0: width ] = (0, 0, 0)
    # plt.figure(num=None, figsize=(8, 6), dpi=80)
    # imshow(red_girl)

    # 37,86,115
    red_filtered = (red_girl[:,:,0] > 37) & (red_girl[:,:,1] < 86) & (red_girl[:,:,2] < 115)
    # selected color: (184, 166, 109)
    white_filtered_min = (red_girl[:, :, 0] > 170) & (red_girl[:, :, 1] > 140) & (red_girl[:, :, 2] > 80)
    white_filtered_max = (red_girl[:, :, 0] < 200) & (red_girl[:, :, 1] < 200) & (red_girl[:, :, 2] < 130)
    white_filtered=white_filtered_min & white_filtered_max
    # selected pix's color:  (139, 116, 83)
    white_filtered2_min = (red_girl[:, :, 0] > 130 ) & (red_girl[:, :, 1] > 110) & (red_girl[:, :, 2] > 80)
    white_filtered2_max = (red_girl[:, :, 0] <140) & (red_girl[:, :, 1] < 120) & (red_girl[:, :, 2] < 90)
    white_filtered2=white_filtered2_min & white_filtered2_max
    red_filtered=red_filtered  | white_filtered | white_filtered2
    plt.figure(num=None, figsize=(8, 6), dpi=80)
    red_girl_new = red_girl.copy()
    red_girl_new[:, :, 0] = red_girl_new[:, :, 0] * red_filtered
    red_girl_new[:, :, 1] = red_girl_new[:, :, 1] * red_filtered
    red_girl_new[:, :, 2] = red_girl_new[:, :, 2] * red_filtered
    imshow(red_girl_new)
    imsave("test3.jpg",red_girl_new)
    plt.show()

    # remove noise
    lower_yellow = np.array([22, 93, 0])
    upper_yellow = np.array([45, 255, 255])

    lower_blue = np.array([100,150,0])
    upper_blue = np.array([140,255,255])
    lower_red = np.array([0,50,50]) #example value
    upper_red = np.array([10,255,255]) #example value

    img = cv2.imread("test3.jpg")
    img = cv2.resize(img, (1024, 608), interpolation=cv2.INTER_CUBIC)

    # convert BGR to HSV
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # create the Mask
    mask1 = cv2.inRange(imgHSV, lower_yellow, upper_yellow)
    mask2=cv2.inRange(imgHSV, lower_red, upper_red)
    mask=cv2.bitwise_or(mask1,mask2)
    mask = 255 - mask
    res = cv2.bitwise_and(img, img, mask=mask)
    mask1 = cv2.bitwise_not(mask)
    cv2.imshow("mask", mask)

    # cv2.imshow("cam", img)
    cv2.imshow("res", res)
    cv2.waitKey()
    # cv2.imwrite(save_path,mask1)


if __name__=="__main__":
    body_part_root = f"../datasets/Male/abdomen"
    file_name = 'a_vm1455.png'
    image_path = body_part_root + "/" + file_name
    isolate_image(image_path=image_path)