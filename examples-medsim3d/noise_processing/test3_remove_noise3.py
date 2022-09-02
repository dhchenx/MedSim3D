import cv2
import numpy as np
# https://stackoverflow.com/questions/30369031/remove-spurious-small-islands-of-noise-in-an-image-python-opencv
root_path="datasets/evaluate1"

image_path=root_path+"/"+"iso2_a_vm1455.png"

img = cv2.imread(image_path)

cv2.imshow('Original', img)

img_bw = 255*(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) > 5).astype('uint8')

se1 = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
se2 = cv2.getStructuringElement(cv2.MORPH_RECT, (2,2))
mask = cv2.morphologyEx(img_bw, cv2.MORPH_CLOSE, se1)
mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, se2)

mask = np.dstack([mask, mask, mask]) / 255
out = img * mask

cv2.imshow('Output', out)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.imwrite('output1.png', out)