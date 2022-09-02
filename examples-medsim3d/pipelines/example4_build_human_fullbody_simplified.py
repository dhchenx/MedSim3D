from medsim3d.vhp.pipeline_human import *

pipeline_human=PipelineHuman(
    gender='Male',
    ct_type='frozenCT',
    root_path='../datasets/Male/test_frozen'
)

pipeline_human.run(force_download=False)

