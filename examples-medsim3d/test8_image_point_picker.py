from medsim3d.vhp.image_point_picker import *

ipp=ImagePointPicker()
img_path = "../visible_human/datasets/Female-Images/PNG_format/thorax_analysis/edges/avf1405a.png"
ipp.start_to_pick(img_path=img_path,save_points_file='datasets/thorax_polygon_area.pickle')

