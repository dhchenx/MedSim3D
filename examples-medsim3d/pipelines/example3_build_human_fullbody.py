from medsim3d.vhp.downloader import VHPDownloader
from medsim3d.vhp.radiological_data_converter import *
from medsim3d.vhp.model_builder import  *
from medsim3d.vhp.model_viewer import  *

# Step 0: configuration
gender="Female" # Male
ct_type="normalCT" # frozenCT
root_path=f"../../visible_human/datasets/{gender}-Images/PNG_format/radiological"

# folder variables
dataset_folder=f"{root_path}/{ct_type}"
converted_folder=f"{root_path}/{ct_type}_converted"
edges_folder=f"{root_path}/{ct_type}_edges"
detected_folder=f"{root_path}/{ct_type}_detected"
csv_model_file=f"../datasets/{gender}/{ct_type}.csv"
ply_model_file=f"../datasets/{gender}/{ct_type}.ply"

# Step 1: download dataset
if not os.path.exists(dataset_folder):
    vhp_downloader=VHPDownloader()
    vhp_downloader.download_datasets_radiological_CT(gender=gender,ct_type=ct_type,save_folder=dataset_folder)

# Step 2: Convert original images into 12 bit grayscale image so as to see clearly
rdc=RadiologicalDataConverter(dataset_folder=dataset_folder)
rdc.convert(save_folder=converted_folder)

# Step 3: Build the model
mb=ModelBuilder()
mb.build(
    gender=gender,
    ct_type=ct_type,
    converted_folder=converted_folder,
    edge_folder=edges_folder,
    detected_folder=detected_folder,
    output_model_path=csv_model_file
)

# Step 4: Show model
mv=ModelViewer(model_csv_file=csv_model_file)

mv.convert_to_ply(save_ply_file=ply_model_file)

mv.show(ply_file=ply_model_file)
