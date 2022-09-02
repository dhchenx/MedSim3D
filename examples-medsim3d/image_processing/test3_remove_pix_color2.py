
import cv2
import numpy as np

body_part_root=f"../datasets/Male/abdomen"
file_name='a_vm1455.png'
image_path=body_part_root+"/"+file_name


lower_blue = np.array([100,150,0])
upper_blue = np.array([140,255,255])


img = cv2.imread(image_path)
img = cv2.resize(img, (900, 650), interpolation=cv2.INTER_CUBIC)

# convert BGR to HSV
imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
# create the Mask
mask = cv2.inRange(imgHSV, lower_blue, upper_blue)
mask = 255 - mask
res = cv2.bitwise_and(img, img, mask=mask)

cv2.imshow("mask", mask)
cv2.imshow("cam", img)
cv2.imshow("res", res)
cv2.waitKey()

