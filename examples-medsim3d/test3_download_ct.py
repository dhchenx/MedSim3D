from medsim3d.vhp.downloader import VHPDownloader

vhp_downloader=VHPDownloader()

vhp_downloader.download_datasets_radiological_CT(gender="Female",ct_type="normalCT",save_folder="datasets/female/normalCT")