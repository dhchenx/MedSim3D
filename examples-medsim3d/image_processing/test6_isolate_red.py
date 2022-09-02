import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from skimage.io import imshow, imread,imsave
from skimage.color import rgb2hsv, hsv2rgb
import cv2
import os
from tqdm import tqdm

def isolate_image(image_path,save_path,save_main_color):
    red_girl = imread(image_path)
    red_girl = cv2.resize(red_girl, (1024, 608), interpolation=cv2.INTER_CUBIC)
    plt.figure(num=None, figsize=(8, 6), dpi=80)
    # imshow(red_girl)

    # 37,86,115
    red_filtered = (red_girl[:,:,0] > 37) & (red_girl[:,:,1] < 86) & (red_girl[:,:,2] < 115)
    plt.figure(num=None, figsize=(8, 6), dpi=80)
    red_girl_new = red_girl.copy()
    red_girl_new[:, :, 0] = red_girl_new[:, :, 0] * red_filtered
    red_girl_new[:, :, 1] = red_girl_new[:, :, 1] * red_filtered
    red_girl_new[:, :, 2] = red_girl_new[:, :, 2] * red_filtered
    # imshow(red_girl_new)
    imsave(save_main_color,red_girl_new)
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


if __name__=="__main__":
    body_part_root = f"../datasets/Male/abdomen"
    save_root="datasets/Male/abdomen"
    for file in tqdm(os.listdir(body_part_root)):
        img_path = f"{body_part_root}/{file}"
        print("img path: ", img_path)
        isolate_image(img_path,save_path=save_root+"/"+file,save_main_color=save_root+"_main_color/"+file)




