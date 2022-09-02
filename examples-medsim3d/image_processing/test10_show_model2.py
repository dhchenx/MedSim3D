from medsim3d.vhp.pipeline_bodypart import  *

gender = "Male"

body_parts = [
    "abdomen",
    "head", "legs", "pelvis", "thighs", "thorax"]
for body_part in body_parts:
    mv=ModelViewerColor(model_csv_file=f"datasets/{gender}/{body_part}2.csv")
    # mv.convert_to_ply(save_ply_file=f"datasets/{gender}/{body_part}2.ply")
    mv.show(ply_file=f"datasets/{gender}/{body_part}2.ply")