import cv2
import pickle

import quickcsv
from PIL import Image

class ImagePointPicker:
    def __init__(self):
        pass



    def start_to_pick_color(self,img_path,save_points_file,save_colors_file):
        list_points = []
        list_colors=[]
        # stores mouse position in global variables ix(for x coordinate) and iy(for y coordinate)
        # on double click inside the image
        def select_point(event, x, y, flags, param):
            global ix, iy
            if event == cv2.EVENT_LBUTTONDBLCLK:  # captures left button double-click
                ix, iy = x, y
                list_points.append([ix, iy])
                print(ix, iy)


                im = Image.open(img_path)  # Can be many different formats.
                pix = im.load()
                print("selected pix's color: ",pix[x, y])
                list_colors.append(pix[x,y])

                # img_path = "../datasets/Female-Images/PNG_format/thorax_analysis/edges/avf1405a.png"

        img = cv2.imread(img_path)
        cv2.namedWindow('image')
        # bind select_point function to a window that will capture the mouse click
        cv2.setMouseCallback('image', select_point)
        cv2.imshow('image', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        # save point list
        lps=[]
        for p in list_points:
            lps.append({
                "x":p[0],
                "y":p[1]
            })
        lcs=[]
        for c in list_colors:
            lcs.append({
                 "r":c[0],
                "g":c[1],
                "b":c[2]
            })
        if save_points_file != None:
            quickcsv.write_csv(save_points_file.replace(".pickle",".csv"),lps)
            quickcsv.write_csv(save_colors_file, lcs)
            pickle.dump(list_points, open(save_points_file, 'wb'))

    def start_to_pick(self,img_path,save_points_file):
        list_points = []

        # stores mouse position in global variables ix(for x coordinate) and iy(for y coordinate)
        # on double click inside the image
        def select_point(event, x, y, flags, param):
            global ix, iy
            if event == cv2.EVENT_LBUTTONDBLCLK:  # captures left button double-click
                ix, iy = x, y
                list_points.append([ix, iy])
                print(ix, iy)

        # img_path = "../datasets/Female-Images/PNG_format/thorax_analysis/edges/avf1405a.png"

        img = cv2.imread(img_path)
        cv2.namedWindow('image')
        # bind select_point function to a window that will capture the mouse click
        cv2.setMouseCallback('image', select_point)
        cv2.imshow('image', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        if save_points_file!=None:
            pickle.dump(list_points, open(save_points_file, 'wb'))

