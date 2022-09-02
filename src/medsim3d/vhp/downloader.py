from tqdm import tqdm
import requests
import os

class VHPDownloader:

    def __init__(self):
        self.root_url="https://data.lhncbc.nlm.nih.gov/public/Visible-Human"

        # self.GenderItem="Male"
        # self.ResItem=['70mm','FullColor','PNG_format','radiological','INDEX','INDEX.Z','README']
        # PNG data
        self.MalePNGRangeDict={
            "abdomen":[1455,1997],
            "head":[1001,1377],
            "legs":[2265,2878],
            "pelvis":[1732,2028],
            "thighs":[1732,2411],
            "thorax":[1280,1688]
        }
        self.FemalePNGRangeDict={
            "abdomen": [1432, 1909],
            "head": [1001, 1285],
            "legs": [2200, 2730],
            "pelvis": [1703, 1953],
            "thighs": [1703, 2300],
            "thorax": [1262, 1488]
        }

        self.MalePNGPrefix="a_vm"
        self.FeMalePNGPrefix="avf"
        # PNG radiological data
        self.MaleRadioRangeDict={
            "frozenCT":[1006,2882],
            "mri":[1005,7625],
            "normalCT":[1012,2832],
            "scoutCT":[2001,2004],
        }
        self.FemaleRadioRangeDict = {
           # "frozenCT": [1006, 2882],
            "mri": [1014, 7584],
            "normalCT": [1001, 2734],
           # "scoutCT": [2001, 2004],
        }


    def get_all_male_body_parts(self):
        return list(self.MalePNGRangeDict.keys())

    def download_image(self,pic_url, save_path):

        if os.path.exists(save_path):
            return

        response = requests.get(pic_url, stream=True)

        if not response.ok:
            print(response)
            return

        with open(save_path, 'wb') as handle:
            if response.ok:
                for block in response.iter_content(1024):
                    if not block:
                        break
                    handle.write(block)

    def download_datasets_radiological_MRI(self, gender,  save_folder,mri_type="mri",):
        if not os.path.exists(save_folder):
            os.mkdir(save_folder)
        prefix="mvm"
        affix="f"
        current_range=self.MaleRadioRangeDict
        if gender=="Female":
            prefix="mvf"
            current_range=self.FemaleRadioRangeDict
        rr = current_range[mri_type]
        min_v = rr[0]
        max_v = rr[1]
        for idx in tqdm(range(min_v, max_v + 1)):
            if gender=="Male":
                url = f"{self.root_url}/{gender}-Images/PNG_format/radiological/{mri_type}/{prefix}{idx}{affix}.png"
                print(url)
                self.download_image(pic_url=url, save_path=f'{save_folder}/{prefix}{idx}{affix}.png')
            elif gender=="Female":
                cc=['1','p','t']
                for c in cc:
                    url1 = f"{self.root_url}/{gender}-Images/PNG_format/radiological/{mri_type}/{prefix}{idx}{c}.png"
                    print(url1)
                    self.download_image(pic_url=url1, save_path=f'{save_folder}/{prefix}{idx}{c}.png')

    def download_datasets_radiological_CT(self, gender, ct_type, save_folder):
        if not os.path.exists(save_folder):
            os.mkdir(save_folder)
        prefix="cvm"
        affix="f"
        current_range=self.MaleRadioRangeDict
        if gender=="Female":
            prefix="cvf"
            current_range=self.FemaleRadioRangeDict
        rr = current_range[ct_type]
        min_v = rr[0]
        max_v = rr[1]
        for idx in tqdm(range(min_v, max_v + 1)):
            if gender=="Male":
                url = f"{self.root_url}/{gender}-Images/PNG_format/radiological/{ct_type}/{prefix}{idx}{affix}.png"
                print(url)
                self.download_image(pic_url=url, save_path=f'{save_folder}/{prefix}{idx}{affix}.png')
            elif gender=="Female":
                url1 = f"{self.root_url}/{gender}-Images/PNG_format/radiological/{ct_type}/{prefix}{idx}{affix}.png"
                print(url1)
                self.download_image(pic_url=url1, save_path=f'{save_folder}/{prefix}{idx}{affix}.png')


    def download_datasets(self,gender,body_part,save_folder,download_female_parts=['a','b','c']):
        prefix=self.MalePNGPrefix
        if gender=="Female":
            prefix=self.FeMalePNGPrefix
        if not os.path.exists(save_folder):
            os.mkdir(save_folder)
        current_range=self.MalePNGRangeDict
        if gender=="Female":
            current_range=self.FemalePNGRangeDict
        rr=current_range[body_part]
        min_v=rr[0]
        max_v=rr[1]

        for idx in tqdm(range(min_v, max_v + 1)):
            if gender=="Male":
                url = f"{self.root_url}/{gender}-Images/PNG_format/{body_part}/{prefix}{idx}.png"
                print(url)
                self.download_image(pic_url=url, save_path=f'{save_folder}/{prefix}{idx}.png')
            elif gender=="Female":
                cc=download_female_parts
                for c in cc:
                    url1 = f"{self.root_url}/{gender}-Images/PNG_format/{body_part}/{prefix}{idx}{c}.png"
                    print(url1)
                    self.download_image(pic_url=url1, save_path=f'{save_folder}/{prefix}{idx}{c}.png')

        print("Finished!")
