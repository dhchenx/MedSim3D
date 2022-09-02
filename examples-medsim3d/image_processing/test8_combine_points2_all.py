import os
import random
from tqdm import tqdm
from medsim3d.vhp.pipeline_bodypart import  *
import math
# (39, 54, 107, 255)
base_color=[39,54,107]
base_color_green=[55, 170, 20]
def color_similarity(base_col_val,oth_col_val):
    return math.sqrt(sum((base_col_val[i]-oth_col_val[i])**2 for i in range(3)))
import quickcsv
from quickcsv.file import *

gender = "Male"

body_parts = [
    "head",
    "abdomen",
    "legs", "pelvis", "thighs", "thorax"]

dict_stat={}


for body_part in body_parts:
    list_all=[]
    all_c=0
    for f in tqdm(os.listdir(f"datasets/{gender}/{body_part}2_points")):
        points_file=f"datasets/{gender}/{body_part}2_points"+"/"+f
        list_r=quickcsv.read_csv(points_file)
        c=len(list_r)
        list_new_r=random.choices(list_r,k=10000)
        list_new_r1=[]
        # list_new_r = quickcsv.read_csv(points_file)
        for p in list_new_r:
            r=int(p['r'])
            g=int(p['g'])
            b=int(p['b'])
            diff=color_similarity(base_color,[r,g,b])
            if diff<50:
                continue
            diff1=color_similarity(base_color_green,[r,g,b])
            if diff1< 100:
                continue
            list_new_r1.append(p)
        all_c+=c
        list_all+=list_new_r1
    dict_stat[body_part]=all_c
    quickcsv.write_csv(f"datasets/{gender}/{body_part}2.csv",list_all)
    print("count = ",all_c)
    #mv=ModelViewerColor(model_csv_file=f"datasets/{gender}/{body_part}2.csv")
    #mv.convert_to_ply(save_ply_file=f"datasets/{gender}/{body_part}2.ply")
    #mv.show(ply_file=f"datasets/{gender}/{body_part}2.ply")

print("body part\tNo. points")
for k in dict_stat:
    print(f"{k}\t{dict_stat[k]}")


