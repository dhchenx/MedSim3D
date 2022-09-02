from medsim3d.vhp.edge_converter import *

ec=EdgeConverter(dataset_folder="datasets/Female/normalCT_converted")
ec.convert(save_edge_folder="datasets/Female/normalCT_edges",save_detected_folder="datasets/Female/normalCT_edges_detected")