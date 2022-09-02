from medsim3d.vhp.model_builder import  *

mb=ModelBuilder()

gender="Female"

root_path=f"../visible_human/datasets/{gender}-Images/PNG_format/radiological"
'''
# 1. show the frozen CT of male
mb.build(
    gender="Male",
    ct_type="frozenCT",
    converted_folder=root_path+"/fronzenCT_converted",
    edge_folder=root_path+"/fronzenCT_edges",
    detected_folder=root_path+"/fronzenCT_detected",
    output_model_path="datasets/Male/frozenCT.csv"
)
'''
'''
# 2. show the normal CT of male
mb.build(
    gender="Male",
    ct_type="normalCT",
    converted_folder=root_path+"/normalCT_converted",
    edge_folder=root_path+"/normalCT_edges",
    detected_folder=root_path+"/normalCT_detected",
    output_model_path="datasets/Male/normalCT.csv"
)
'''

# 3. show the normal CT of female
mb.build(
    gender="Female",
    ct_type="normalCT",
    converted_folder=root_path+"/normalCT_converted",
    edge_folder=root_path+"/normalCT_edges",
    detected_folder=root_path+"/normalCT_detected",
    output_model_path="datasets/Female/normalCT.csv"
)