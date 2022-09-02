from medsim3d.datasets.ieee_ic_3dbp import IEEE_IC_3DBP_Dataset
from medsim3d.models.viewer3d import Viewer3D

human_body_datasets=IEEE_IC_3DBP_Dataset(dataset_folder='datasets/human_body_shapes')

subject='IEEEP2_01'
category='3DLOOK_3DLOOK'

basic_info=human_body_datasets.get_subject_info(category=f'{category}',subject=f'{subject}')
print(basic_info)
measurement1=human_body_datasets.get_subject_measurement(category=category,subject=subject,repetition_no=1)
print(measurement1)
measurement2=human_body_datasets.get_subject_measurement(category=category,subject=subject,repetition_no=2)
print(measurement2)

obj_file=human_body_datasets.get_subject_3d_object(category=category,subject=subject,repetition_no=1)
print(obj_file)
Viewer3D().show_object(obj_file=obj_file)

