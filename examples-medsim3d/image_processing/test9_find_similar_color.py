import numpy as np
from skimage import io
from skimage.color import rgb2lab, deltaE_cie76
import math

def get_pct_color(img_rgb, rgb_color, threshold=10):
    img_lab = rgb2lab(img_rgb)
    rgb_color_3d = np.uint8(np.asarray([[rgb_color]]))
    rgb_color_lab = rgb2lab(rgb_color_3d)
    delta = deltaE_cie76(rgb_color_lab, img_lab)
    x_positions, y_positions = np.where(delta < threshold)
    nb_pixel = img_rgb.shape[0] * img_rgb.shape[1]
    pct_color = len(x_positions) / nb_pixel
    return pct_color

img_rgb = io.imread('https://i.stack.imgur.com/npnrv.png')
green = [0, 160, 0]
s=get_pct_color(img_rgb, green, 10)
print("s=",s)

base=[35,103,239]
test_color=[153,0,0]
test_color1=[0,128,255]

def color_similarity(base_col_val,oth_col_val):
    return math.sqrt(sum((base_col_val[i]-oth_col_val[i])**2 for i in range(3)))

print(color_similarity(base,test_color))
print(color_similarity(base,test_color1))