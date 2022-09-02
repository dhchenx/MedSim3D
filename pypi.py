from quick_pypi.deploy import *

auto_deploy(
    cwd=os.path.dirname(os.path.realpath(__file__)),
    name="MedSim3D",
    long_name="Medical Simulation 3D",
    description="Medical Simulation Framework in the 3D Environment",
    long_description="An agent-based simulation framework for medical education in the 3D environment",
    src_root="src",
    dists_root=f"dists",
    pypi_token='D:/GitHub/pypi_upload_token.txt',
    test=False,
    version="0.0.1a3",
    project_url="http://github.com/dhchenx/MedSim3D",
    author_name="Donghua Chen",
    author_email="douglaschan@126.com",
    requires="tqdm;requests;quick-csv;numpy;cv2;pillow;pandas;matplotlib;scipy;skimage;sklearn;shapely;pyntcloud", # use ; for multiple requires
    license='MIT',
    license_filename='LICENSE',
    keywords="medical education, simulation, agent-based modeling, 3D",
    github_username="dhchenx",
    readme_path="README.md",
    topic="Scientific/Engineering :: Medical Science Apps.",
    intended_audience="Healthcare Industry",
    exclude="recursive-exclude src *.csv *.obj *.off *.ply *.nlogo3d *.nlogo",
   # only_build=True
   # console_scripts=""
)

