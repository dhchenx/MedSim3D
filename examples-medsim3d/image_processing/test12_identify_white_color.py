import cv2
import numpy as np
from skimage.io import imshow, imread,imsave

body_part_root=f"../datasets/Male/abdomen"
file_name='a_vm1455.png'
image_path=body_part_root+"/"+file_name

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

while(1):

    image = imread(image_path)
    image = cv2.resize(image, (512, 304), interpolation=cv2.INTER_CUBIC)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # define range of white color in HSV
    # change it according to your need !
    # selected pix's color:  (184, 166, 109)
    r1=color_dict_HSV["white"][0]
    r2=color_dict_HSV["white"][1]
    lower_white = np.array(r1, dtype=np.uint8)
    upper_white = np.array(r2, dtype=np.uint8)

    # Threshold the HSV image to get only white colors
    mask = cv2.inRange(hsv, lower_white, upper_white)
    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(image,image, mask= mask)

    cv2.imshow('frame',image)
    cv2.imshow('mask',mask)
    cv2.imshow('res',res)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()