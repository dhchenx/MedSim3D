from medsim3d.vhp.downloader import VHPDownloader

vhp_downloader=VHPDownloader()

vhp_downloader.download_datasets(gender="Female",body_part="abdomen",save_folder="datasets/female/abdomen")