from medsim3d.vhp.downloader import VHPDownloader

vhp_downloader=VHPDownloader()

vhp_downloader.download_datasets_radiological_MRI(gender="Female",mri_type="mri",save_folder="datasets/female/mri")