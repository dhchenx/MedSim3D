from medsim3d.vhp.pipeline_bodypart import  *

gender = "Female"

body_parts = [
    "abdomen",
    "head", "legs", "pelvis", "thighs", "thorax"]

for body_part in body_parts:
    print("body part: ",body_part)
    ec_pg=ModelBuilderWithColor(
            polygon_file=None,
            dataset_folder= f"../datasets/{gender}/{body_part}",
            use_color=True,
            include_id_in_csv=False
        )

    ec_pg.build2(body_part=body_part,
                  save_edges_folder=f"datasets/{gender}/{body_part}2_main_color",
                  save_detected_folder=f"datasets/{gender}/{body_part}2",
                  gender=gender,
                    output_model_file=f"datasets/{gender}/{body_part}2.csv",
                 algorithm=2,
                 replace=True
                )
'''
mv=ModelViewerColor(model_csv_file="datasets/Male/abdomen2.csv")
mv.convert_to_ply(save_ply_file="datasets/Male/abdomen2.ply")
mv.show(ply_file="datasets/Male/abdomen2.ply")
'''

