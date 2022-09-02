import os
from medsim3d.vhp.downloader import *
from medsim3d.vhp.image_point_picker import *
from medsim3d.vhp.edge_converter_within_polygon import *
from medsim3d.vhp.model_builder_color import *
from medsim3d.vhp.model_viewer_color import *

class PipelineBodyPart:

    def __init__(self,gender,body_part,root_folder,use_point_id=True):
        # step 0: parameter settings
        self.gender=gender
        self.body_part=body_part
        self.root_folder=root_folder
        self.use_point_id=use_point_id
        # folder variables
        # self.gender_folder = f"{root_folder}/{gender}"
        self.dataset_folder = f"{root_folder}/{body_part}"
        self.polygon_file = f'{root_folder}/{body_part}_polygon_area.pickle'
        self.save_edges_folder = f"{root_folder}/{body_part}_edges"
        self.save_detected_folder = f"{root_folder}/{body_part}_edges_detected"
        self.output_model_file = f"{root_folder}/{body_part}.csv"
        self.output_ply_file = f"{root_folder}/{body_part}.ply"

    def show_model(self):
        mv = ModelViewerColor(model_csv_file=self.output_model_file)
        mv.convert_to_ply(save_ply_file=self.output_ply_file)
        mv.show(ply_file=self.output_ply_file)

    def run(self,force_download=False):
        # if not os.path.exists(self.gender_folder):
        #     os.mkdir(self.gender_folder)
        if not os.path.exists(self.dataset_folder):
            os.mkdir(self.dataset_folder)

        # step 1: download body part data
        if force_download:
            vhp_downloader=VHPDownloader()
            vhp_downloader.download_datasets(gender=self.gender,body_part=self.body_part,save_folder=self.dataset_folder,download_female_parts=['a'])
        else:
            if not os.path.exists(self.dataset_folder):
                vhp_downloader = VHPDownloader()
                vhp_downloader.download_datasets(gender=self.gender, body_part=self.body_part,
                                                 save_folder=self.dataset_folder, download_female_parts=['a'])

        # step 3: pick valid points within given polygon area from the slices
        ipp=ImagePointPicker()
        first_image_file=os.listdir(self.dataset_folder)[0]
        img_path = self.dataset_folder+"/"+first_image_file
        if not os.path.exists(self.polygon_file):
            print("Please pick polygon's point sets by double-click and close after finish!")
            ipp.start_to_pick(img_path=img_path,save_points_file=self.polygon_file)
        else:
            print("Polygon file already exists, using the existing one!")

        # Step 4: identify valid points of the body part from the images
        '''
        ec_pg=EdgeConverterWithInPolygon(
            polygon_file=self.polygon_file,
            dataset_folder=self.dataset_folder)

        ec_pg.convert(body_part=self.body_part,
                      save_edges_folder=self.save_edges_folder,
                      save_detected_folder=self.save_detected_folder,
                      gender=self.gender)
        '''

        # Step 5: Start to build 3D models and output a point csv file
        ec_pg=ModelBuilderWithColor(
            polygon_file=self.polygon_file,
            dataset_folder=self.dataset_folder,
            use_color=True,
            include_id_in_csv=self.use_point_id
        )

        ec_pg.build(body_part=self.body_part,
                      save_edges_folder=self.save_edges_folder,
                      save_detected_folder=self.save_detected_folder,
                      gender=self.gender,
                        output_model_file=self.output_model_file
                    )

        # Step 6: Convert the point csv file into PLY file and show the PLY file
        mv=ModelViewerColor(model_csv_file=self.output_model_file)
        mv.convert_to_ply(save_ply_file=self.output_ply_file)
        mv.show(ply_file=self.output_ply_file)

