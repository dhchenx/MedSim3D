from medsim3d.vhp.model_viewer_color import  *

gender="Female" # Male
body_part="thorax" # frozenCT

mv=ModelViewerColor(model_csv_file=f'datasets/{gender}/{body_part}.csv')

mv.convert_to_ply(save_ply_file=f'datasets/{gender}/{body_part}.ply')

mv.show(ply_file=f'datasets/{gender}/{body_part}.ply')

