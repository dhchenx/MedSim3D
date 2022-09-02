import cv2
from tqdm import tqdm
import numpy as np
import os
import math

import cv2
import numpy as np

class EdgeConverter:
    def __init__(self,dataset_folder):
        self.dataset_folder=dataset_folder

    def show_edges(sef,img_path, t=120):
        image = cv2.imread(img_path, 0)
        edges = cv2.Canny(image, t, 3 * t)

        cv2.imshow("canny", edges)

        cv2.waitKey(0)
        cv2.destroyAllWindows()


    def save_edges(self,img_path, save_path, t=120):
        image = cv2.imread(img_path, 0)
        edges = cv2.Canny(image, t, 3 * t)

        cv2.imwrite(save_path, edges)


    def get_edges(self,img_path, t=120):
        image = cv2.imread(img_path, 0)
        edges = cv2.Canny(image, t, 3 * t)

        return edges




    def dist(self,x1, y1, x2, y2):
        return math.sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2))


    def detect_colored_points_removed(self,idx, img_path, save_path):

        img = cv2.imread(img_path)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        low = np.array([0, 0, 0])
        high = np.array([180, 255, 46])

        dst = cv2.inRange(src=hsv, lowerb=low, upperb=high)

        xy = np.column_stack(np.where(dst == 0))

        # center point
        c_x = 256
        c_y = 256

        for c in xy:

            y = c[0]
            x = c[1]

            if (idx >= 1014 and idx <= 1236) or (
                    (idx < 1014 or (idx > 1236 and idx <= 2558)) and self.dist(x, y, c_x, c_y) <= 250 and y < 400) \
                    or (idx > 2558 and self.dist(x, y, c_x, c_y) <= 250 and y < 350):
                cv2.circle(img=img, center=(int(c[1]), int(c[0])), radius=1, color=(0, 0, 255), thickness=1)

        cv2.imwrite(save_path, img)

    def convert(self,save_edge_folder,save_detected_folder,t=100):
        # img_path = 'datasets/Male-Images/PNG_format/radiological/mri_converted/mvm11501.png'
        # show_edges(img_path=img_path)
        if  not os.path.exists(save_edge_folder):
            os.mkdir(save_edge_folder)
        if not os.path.exists(save_detected_folder):
            os.mkdir(save_detected_folder)
        for file in tqdm(os.listdir(self.dataset_folder)):
            filename,ext=os.path.splitext(file)
            idx=int(filename.replace("cvf","").replace("cvm","").replace("f",""))
            img_path=self.dataset_folder+"/"+file
            # filename,ext=os.path.splitext(file)
            save_edge_path=save_edge_folder+"/"+file
            self.save_edges(img_path=img_path, save_path=save_edge_path, t=t)
            save_detected_path = save_detected_folder + "/" + file
            self.detect_colored_points_removed(idx=idx, img_path=save_edge_path, save_path=save_detected_path)


