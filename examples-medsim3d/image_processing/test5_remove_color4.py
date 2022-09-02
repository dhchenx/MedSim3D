import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from skimage.io import imshow, imread,imsave
from skimage.color import rgb2hsv, hsv2rgb
import cv2

blue_lower=np.array([100,150,0],np.uint8)
blue_upper=np.array([140,255,255],np.uint8)
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



