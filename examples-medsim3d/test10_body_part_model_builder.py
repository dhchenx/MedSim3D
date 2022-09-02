from medsim3d.vhp.model_builder_color import *

ec_pg=ModelBuilderWithColor(
    polygon_file='datasets/thorax_polygon_area.pickle',
    dataset_folder='datasets/Female/thorax',
    use_color=True
)

ec_pg.build(body_part='thorax',
              save_edges_folder='datasets/Female/thorax_edges',
              save_detected_folder='datasets/Female/thorax_edges_detected',
              gender='Female',
                output_model_file="datasets/Female/thorax.csv"
            )