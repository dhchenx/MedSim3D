import os

from medsim3d.vhp.downloader import VHPDownloader
from medsim3d.vhp.radiological_data_converter import *
from medsim3d.vhp.model_builder import  *
from medsim3d.vhp.model_viewer import  *

class PipelineHuman:

    def __init__(self,gender,ct_type,root_path):
        # Step 0: configuration
        self.gender = gender  # Male
        self.ct_type = ct_type  # frozenCT
        self.root_path = root_path

        # folder variables
        self.dataset_folder = f"{root_path}/{ct_type}"
        self.converted_folder = f"{root_path}/{ct_type}_converted"
        self.edges_folder = f"{root_path}/{ct_type}_edges"
        self.detected_folder = f"{root_path}/{ct_type}_detected"
        self.csv_model_file = f"{root_path}/{ct_type}.csv"
        self.ply_model_file = f"{root_path}/{ct_type}.ply"

    def show_model(self,ply_model_file=None):
        # Step 4: Show model
        mv = ModelViewer(model_csv_file=self.csv_model_file)
        if ply_model_file==None:
            mv.convert_to_ply(save_ply_file=self.ply_model_file)
        else:
            self.ply_model_file=ply_model_file

        mv.show(ply_file=self.ply_model_file)

    def run(self,force_download=False):
        if not os.path.exists(self.converted_folder):
            os.mkdir(self.converted_folder)
        if not os.path.exists(self.edges_folder):
            os.mkdir(self.edges_folder)
        if not os.path.exists(self.detected_folder):
            os.mkdir(self.detected_folder)

        # Step 1: download dataset
        if force_download:
            vhp_downloader = VHPDownloader()
            vhp_downloader.download_datasets_radiological_CT(gender=self.gender, ct_type=self.ct_type,
                                                             save_folder=self.dataset_folder)
        else:
            if not os.path.exists(self.dataset_folder):
                vhp_downloader=VHPDownloader()
                vhp_downloader.download_datasets_radiological_CT(gender=self.gender,ct_type=self.ct_type,save_folder=self.dataset_folder)

        # Step 2: Convert original images into 12 bit grayscale image so as to see clearly
        rdc=RadiologicalDataConverter(dataset_folder=self.dataset_folder)
        rdc.convert(save_folder=self.converted_folder)

        # Step 3: Build the model
        mb=ModelBuilder()
        mb.build(
            gender=self.gender,
            ct_type=self.ct_type,
            converted_folder=self.converted_folder,
            edge_folder=self.edges_folder,
            detected_folder=self.detected_folder,
            output_model_path=self.csv_model_file
        )

        # Step 4: Show model
        mv=ModelViewer(model_csv_file=self.csv_model_file)

        mv.convert_to_ply(save_ply_file=self.ply_model_file)

        mv.show(ply_file=self.ply_model_file)
