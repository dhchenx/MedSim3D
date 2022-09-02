import os
# https://modelnet.cs.princeton.edu/
# http://3dvision.princeton.edu/projects/2014/3DShapeNets/ModelNet10.zip
# http://modelnet.cs.princeton.edu/ModelNet40.zip

class ModelNetDataset:
    def __init__(self,dataset_folder):
        self.dataset_folder=dataset_folder

    def get_categories(self):
        list_cat=[]
        for file in os.listdir(self.dataset_folder):
            if os.path.isdir(os.path.join(self.dataset_folder,file)):
                list_cat.append(file)
        return list_cat

    def get_object_files_by_category(self,category, split='all'):
        folder= self.dataset_folder+"/" +category +f"/{split}"
        list_object_files=[]
        if not split=='all':
            for file in os.listdir(folder):
                if not file.endswith(".off"):
                    continue
                list_object_files.append(folder+"/"+file)
        else:
            for file in os.listdir(self.dataset_folder+"/" +category +"/train"):
                if not file.endswith(".off"):
                    continue
                list_object_files.append(folder+"/"+file)
            for file in os.listdir(self.dataset_folder+"/" +category +"/test"):
                if not file.endswith(".off"):
                    continue
                list_object_files.append(folder+"/"+file)

        return list_object_files