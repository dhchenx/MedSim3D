## MedSim3D: Medical Simulation Framework in the 3D environment

The `MedSim3D` framework provides a general programmable platform for 3D modeling and simulation in medical education.

### Installation

```
    pip install MedSim3D
```

### Dependencies

tqdm, requests, numpy, cv2, shapely, quick-csv, pillow, pandas, pyntcloud, sklearn, matplotlib, scipy, skimage

### Examples

Example 1: Download datasets from [the Visible Human Project](https://www.nlm.nih.gov/databases/download/vhp.html). 

```python
from medsim3d.vhp.downloader import VHPDownloader
vhp_downloader=VHPDownloader()
vhp_downloader.download_datasets(
    gender="Male", # Male or Female
    body_part="head", 
    # Options: abdomen, head, legs, pelvis, thighs, thorax
    save_folder="datasets/male/head")
```

Example 2: Build human body part 3D models from colored slices

```python
from medsim3d.vhp.pipeline_bodypart import  *
# A pipeline to build body parts in a simple way
pipeline_pelvis=PipelineBodyPart(
    gender="Female",
    body_part="pelvis", 
    # Options: abdomen, head, legs, pelvis, thighs, thorax
    root_folder='../datasets/Female'
)
pipeline_pelvis.run(force_download=True)
```

Example 3: Build human full-body 3D models from CT images

```python
from medsim3d.vhp.pipeline_human import *
pipeline_human=PipelineHuman(
    gender='Male',
    ct_type='frozenCT', # normalCT
    root_path='../datasets/Male'
)
pipeline_human.run(force_download=True)
```

### Screenshots

(1) Medical image processing using the VHP data sets

![MedSim3D image processing](https://dhchenx.github.io/projects/MedSim3D/medsim3d-image-processing.png)


(2) 3D agent-based modeling in NetLogo using VHP data sets

![MedSim3D agent-based 3D modeing](https://dhchenx.github.io/projects/MedSim3D/medsim3d-agent-based-modeling.png)

### Credits

- [The NLM Visible Human Project](https://www.nlm.nih.gov/research/visible/visible_human.html)
- [Open3D](http://www.open3d.org/)

### License

The `MedSim3D` toolkit is provided by [Donghua Chen](https://github.com/dhchenx) with MIT License.

