import os
import random
from tqdm import tqdm
from medsim3d.vhp.pipeline_bodypart import  *
import math
# (39, 54, 107, 255)
base_color=[39,54,107]
def color_similarity(base_col_val,oth_col_val):
    return math.sqrt(sum((base_col_val[i]-oth_col_val[i])**2 for i in range(3)))
import quickcsv
from quickcsv.file import *
list_all=[]
for f in tqdm(os.listdir("datasets/Male/abdomen_points")):
    points_file="datasets/Male/abdomen_points"+"/"+f
    list_r=quickcsv.read_csv(points_file)
    list_new_r=random.choices(list_r,k=10000)
    list_new_r1=[]
    for p in list_new_r:
        r=int(p['r'])
        g=int(p['g'])
        b=int(p['b'])
        diff=color_similarity(base_color,[r,g,b])
        if diff<50:
            continue
        list_new_r1.append(p)
    list_all+=list_new_r1

quickcsv.write_csv("datasets/Male/abdomen.csv",list_all)

mv=ModelViewerColor(model_csv_file="datasets/Male/abdomen.csv")
mv.convert_to_ply(save_ply_file="datasets/Male/abdomen.ply")
mv.show(ply_file="datasets/Male/abdomen.ply")


