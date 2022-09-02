import scipy
from PIL import Image
import numpy as np
from sklearn.externals._pilutil import imresize
import cv2
import matplotlib.image as mat_img
from tqdm import tqdm
import os

class RadiologicalDataConverter:
    def __init__(self,dataset_folder):
        self.dataset_folder=dataset_folder

    def matrix2uint8(self,matrix):
      '''
    matrix must be a numpy array NXN
    Returns uint8 version
      '''
      m_min= np.min(matrix)
      m_max= np.max(matrix)
      matrix = matrix-m_min
      return(np.array(np.rint( (matrix-m_min)/float(m_max-m_min) * 255.0),dtype=np.uint8))
      #np.rint, Round elements of the array to the nearest integer.

    def preprocess(self,img, crop=True, resize=True, dsize=(224, 224)):
      if img.dtype == np.uint8:
        img = img / 255.0

      if crop:
        short_edge = min(img.shape[:2])
        yy = int((img.shape[0] - short_edge) / 2)
        xx = int((img.shape[1] - short_edge) / 2)
        crop_img = img[yy: yy + short_edge, xx: xx + short_edge]
      else:
        crop_img = img

      if resize:
        norm_img = imresize(crop_img, dsize)
      else:
        norm_img = crop_img

      return (norm_img).astype(np.float32)

    def deprocess(self,img):
      return np.clip(img * 255, 0, 255).astype(np.uint8)

    def convert(self,save_folder):
        if  not os.path.exists(save_folder):
            os.mkdir(save_folder)
        for file in tqdm(os.listdir(self.dataset_folder)):
            img_path=self.dataset_folder+"/"+file
            # filename,ext=os.path.splitext(file)
            save_path=save_folder+"/"+file
            if os.path.exists(img_path) and not os.path.exists(save_path):
                print(img_path)
                try:
                    img = mat_img.imread(img_path)

                    img = self.matrix2uint8(self.preprocess(img=img, crop=False, resize=False))

                    status = cv2.imwrite(save_path, img)
                    print(save_path,status)
                except Exception as err:
                    print(err)
                print()
        print("Finished!")
