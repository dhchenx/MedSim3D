from medsim3d.vhp.pipeline_bodypart import  *

mv=ModelViewerColor(model_csv_file="datasets/Male/abdomen2.csv")
mv.convert_to_ply(save_ply_file="datasets/Male/abdomen2.ply")
mv.show(ply_file="datasets/Male/abdomen2.ply")