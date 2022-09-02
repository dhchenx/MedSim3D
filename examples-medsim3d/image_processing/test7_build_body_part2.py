from medsim3d.vhp.pipeline_bodypart import  *


ec_pg=ModelBuilderWithColor(
        polygon_file=None,
        dataset_folder= f"../datasets/Male/abdomen",
        use_color=True,
        include_id_in_csv=False
    )

ec_pg.build2(body_part="abdomen",
              save_edges_folder="datasets/Male/abdomen2_main_color",
              save_detected_folder="datasets/Male/abdomen2",
              gender="Male",
                output_model_file="datasets/Male/abdomen2.csv",
             algorithm=2
            )
'''
mv=ModelViewerColor(model_csv_file="datasets/Male/abdomen2.csv")
mv.convert_to_ply(save_ply_file="datasets/Male/abdomen2.ply")
mv.show(ply_file="datasets/Male/abdomen2.ply")
'''

