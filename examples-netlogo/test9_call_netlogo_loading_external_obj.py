import os.path

from medsim3d.datasets.ieee_ic_3dbp import IEEE_IC_3DBP_Dataset
from medsim3d.models.viewer3d import Viewer3D

human_body_datasets=IEEE_IC_3DBP_Dataset(dataset_folder='../examples-med3dsim/datasets/human_body_shapes')

subject='IEEEP2_01' # scale 0.05; size-scale 1.2 sample-rate 1 offset-y -50
category='3DLOOK_3DLOOK'
'''
basic_info=human_body_datasets.get_subject_info(category=f'{category}',subject=f'{subject}')
print(basic_info)
measurement1=human_body_datasets.get_subject_measurement(category=category,subject=subject,repetition_no=1)
print(measurement1)
measurement2=human_body_datasets.get_subject_measurement(category=category,subject=subject,repetition_no=2)
print(measurement2)
'''
obj_file=human_body_datasets.get_subject_3d_object(category=category,subject=subject,repetition_no=1)
print(obj_file)
# Viewer3D().show_object(obj_file=obj_file)

from medsim3d.netlogo.simulator3d import *

sim3d=NetLogo3DSim(netlogo_model_name="MedSim3D-0.0.1a1.nlogo3d")

abs_path = os.path.abspath(obj_file)
abs_path = abs_path.replace("\\", "/")
print("abs path: ",abs_path)

config_model=sim3d.predict_3dworld_size(model_path=abs_path)

sim3d.run_model(model_path=abs_path,
                scale=config_model["scale"],
                size_scale=config_model["size-scale"],
                sample_rate=config_model["sample-rate"],
                offset_x=config_model["offset-x"],
                offset_y=config_model["offset-y"],
                offset_z=config_model["offset-z"],
                )

