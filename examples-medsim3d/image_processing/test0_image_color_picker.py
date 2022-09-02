from medsim3d.vhp.image_point_picker import *

body_part_root=f"../datasets/Male/abdomen"
file_name='a_vm1455.png'
image_path=body_part_root+"/"+file_name

ipp=ImagePointPicker()
ipp.start_to_pick(img_path=image_path,save_points_file="selected_points.pickle")

