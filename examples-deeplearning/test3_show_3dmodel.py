from medsim3d.netlogo.simulator3d import *

model_file='outputs/dcgan/test1/test_points/tester_0.csv'

sim3d=NetLogo3DSim(netlogo_model_name="MedSim3D-0.0.1a2.nlogo3d")

abs_path=os.path.abspath(model_file)
abs_path = abs_path.replace("\\", "/")

config_model=sim3d.predict_3dworld_size(model_path=abs_path)

print(config_model)

sim3d.run_model(model_path=abs_path,
                scale=config_model["scale"],
                size_scale=config_model["size-scale"],
                sample_rate=config_model["sample-rate"],
                offset_x=config_model["offset-x"],
                offset_y=config_model["offset-y"],
                offset_z=config_model["offset-z"],
                world_min_x=config_model["world-min-x"],
                world_max_x=config_model["world-max-x"],
                world_min_y=config_model["world-min-y"],
                world_max_y=config_model["world-max-y"],
                world_min_z=config_model["world-min-z"],
                world_max_z=config_model["world-max-z"],
                auto_world_resize=True
                )
