from medsim3d.vhp.model_viewer import  *

gender="Male" # Male
ct_type="frozenCT" # frozenCT

mv=ModelViewer(model_csv_file=f'datasets/{gender}/{ct_type}.csv')

mv.convert_to_ply(save_ply_file=f'datasets/{gender}/{ct_type}.ply')

mv.show(ply_file=f'datasets/{gender}/{ct_type}.ply')