import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from skimage.io import imshow, imread,imsave
from skimage.color import rgb2hsv, hsv2rgb
import cv2

body_part_root=f"../datasets/Male/abdomen"
file_name='a_vm1455.png'
image_path=body_part_root+"/"+file_name


red_girl = imread(image_path)
plt.figure(num=None, figsize=(8, 6), dpi=80)
imshow(red_girl)

# 37,86,115
red_filtered = (red_girl[:,:,0] > 37) & (red_girl[:,:,1] < 86) & (red_girl[:,:,2] < 115)
white_filter = (red_girl[:,:,0] > 37) & (red_girl[:,:,1] < 86) & (red_girl[:,:,2] < 115)

plt.figure(num=None, figsize=(8, 6), dpi=80)
red_girl_new = red_girl.copy()
red_girl_new[:, :, 0] = red_girl_new[:, :, 0] * red_filtered
red_girl_new[:, :, 1] = red_girl_new[:, :, 1] * red_filtered
red_girl_new[:, :, 2] = red_girl_new[:, :, 2] * red_filtered
imshow(red_girl_new)
imsave("test.jpg",red_girl_new)
plt.show()

# remove noise


lower_blue = np.array([100,150,0])
upper_blue = np.array([140,255,255])
lower_red = np.array([0,50,50]) #example value
upper_red = np.array([10,255,255]) #example value

img = cv2.imread("test.jpg")
img = cv2.resize(img, (900, 650), interpolation=cv2.INTER_CUBIC)

# convert BGR to HSV
imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
# create the Mask
mask = cv2.inRange(imgHSV, lower_red, upper_red)
mask = 255 - mask
res = cv2.bitwise_and(img, img, mask=mask)

cv2.imshow("mask", mask)
cv2.imshow("cam", img)
cv2.imshow("res", res)
cv2.waitKey()



