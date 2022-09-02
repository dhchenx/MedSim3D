import os
from medsim3d.vhp.downloader import *
from medsim3d.vhp.image_point_picker import *
from medsim3d.vhp.edge_converter_within_polygon import *
from medsim3d.vhp.model_builder_color import *
from medsim3d.vhp.model_viewer_color import *

# step 0: parameter settings
gender='Female'
body_part='pelvis'
root_folder="../datasets/"

# folder variables
gender_folder=f"{root_folder}/{gender}"
dataset_folder=f"{root_folder}/{gender}/{body_part}"
polygon_file=f'{root_folder}/{gender}/{body_part}_polygon_area.pickle'
save_edges_folder=f"{root_folder}/{gender}/{body_part}_edges"
save_detected_folder=f"{root_folder}/{gender}/{body_part}_edges_detected"
output_model_file=f"{root_folder}/{gender}/{body_part}.csv"
output_ply_file=f"{root_folder}/{gender}/{body_part}.ply"

if not os.path.exists(gender_folder):
    os.mkdir(gender_folder)
if not os.path.exists(dataset_folder):
    os.mkdir(dataset_folder)

# step 1: download body part data
if not os.path.exists(dataset_folder):
    vhp_downloader=VHPDownloader()
    vhp_downloader.download_datasets(gender=gender,body_part=body_part,save_folder=dataset_folder,download_female_parts=['a'])

# step 3: pick valid points within given polygon area from the slices
ipp=ImagePointPicker()
first_image_file=os.listdir(dataset_folder)[0]
img_path = dataset_folder+"/"+first_image_file
if not os.path.exists(polygon_file):
    print("Please pick polygon's point sets by double-click and close after finish!")
    ipp.start_to_pick(img_path=img_path,save_points_file=polygon_file)
else:
    print("Polygon file already exists, using the existing one!")

# Step 4: identify valid points of the body part from the images
'''
ec_pg=EdgeConverterWithInPolygon(
    polygon_file=polygon_file,
    dataset_folder=dataset_folder)

ec_pg.convert(body_part=body_part,
              save_edges_folder=save_edges_folder,
              save_detected_folder=save_detected_folder,
              gender=gender)
'''

# Step 5: Start to build 3D models and output a point csv file
ec_pg=ModelBuilderWithColor(
    polygon_file=polygon_file,
    dataset_folder=dataset_folder,
    use_color=True
)

ec_pg.build(body_part=body_part,
              save_edges_folder=save_edges_folder,
              save_detected_folder=save_detected_folder,
              gender=gender,
                output_model_file=output_model_file
            )


# Step 6: Convert the point csv file into PLY file and show the PLY file
mv=ModelViewerColor(model_csv_file=output_model_file)
mv.convert_to_ply(save_ply_file=output_ply_file)
mv.show(ply_file=output_ply_file)

