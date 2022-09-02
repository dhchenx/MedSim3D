from medsim3d.vhp.edge_converter_within_polygon import *

ec_pg=EdgeConverterWithInPolygon(
    polygon_file='datasets/thorax_polygon_area.pickle',
    dataset_folder='datasets/Female/thorax')

ec_pg.convert(body_part='thorax',
              save_edges_folder='datasets/Female/thorax_edges',
              save_detected_folder='datasets/Female/thorax_edges_detected',
              gender='Female')