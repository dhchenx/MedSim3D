from medsim3d.vhp.pipeline_bodypart import  *

# A pipeline to build body parts in a simple way
pipeline_pelvis=PipelineBodyPart(
    gender="Female",
    body_part="pelvis",
    root_folder='../datasets/Female/test_pelvis'
)

pipeline_pelvis.run(force_download=False)