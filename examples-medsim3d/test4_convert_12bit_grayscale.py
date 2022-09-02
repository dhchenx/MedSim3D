from medsim3d.vhp.radiological_data_converter import *

rdc=RadiologicalDataConverter(dataset_folder="datasets/Female/normalCT")
rdc.convert(save_folder="datasets/Female/normalCT_converted")