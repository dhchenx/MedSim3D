# https://ieee-dataport.org/open-access/dataset-ieee-ic-3dbp-comparative-analysis-anthropometric-methods
from quickcsv import *

class IEEE_IC_3DBP_Dataset:
    def __init__(self,dataset_folder):
        self.dataset_folder=dataset_folder

    def get_subject_info(self,category,subject):
        list_basic_info=read_csv(csv_path=self.dataset_folder+"/"+ category+"/basic_info.csv" )
        for item in list_basic_info:
            if item['Subject']==subject:
                return item
        return None

    def get_subject_measurement(self,category, subject,repetition_no):
        list_basic_info = read_csv(csv_path=self.dataset_folder + "/" + category + f"/measurement{repetition_no}.csv")
        for item in list_basic_info:
            if item['Subject'] == subject:
                return item
        return None

    def get_subject_3d_object(self,category,subject,repetition_no):
        model_file = self.dataset_folder+"/" +category+"/"+ f"models/{subject}_R{repetition_no}_{category}_20200622.obj"
        return model_file