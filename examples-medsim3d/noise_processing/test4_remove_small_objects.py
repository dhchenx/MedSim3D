import matplotlib.pyplot as plt
from skimage import morphology
import numpy as np
import skimage

root_path="datasets/evaluate1"

image_path=root_path+"/"+"iso2_a_vm1455.png"

# read the image, grayscale it, binarize it, then remove small pixel clusters
im1 = plt.imread(image_path)
im=skimage.color.gray2rgb(im1)
grayscale = skimage.color.rgb2gray(im)

binarized = np.where(grayscale>0.1, 1, 0)
processed = morphology.remove_small_objects(binarized.astype(bool), min_size=4, connectivity=2).astype(int)

# black out pixels
mask_x, mask_y = np.where(processed == 0)
im[mask_x, mask_y, :3] = 0

# plot the result
plt.figure(figsize=(10,10))
plt.imshow(im)

plt.imsave("output2.png",im)

# plt.show()