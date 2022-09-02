import os

from medsim3d.vhp.image_point_picker import ImagePointPicker

body_part_root=f"../datasets/Male/abdomen"
'''
for file in os.listdir(body_part_root):
    img_path=f"{body_part_root}/{file}"
    print("img path: ",img_path)
'''
file_name='a_vm1455.png'
image_path=body_part_root+"/"+file_name

ipp=ImagePointPicker()
ipp.start_to_pick_color(img_path=image_path,save_points_file="selected_points.pickle",save_colors_file="selected_colors.csv")