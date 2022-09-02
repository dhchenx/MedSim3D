from medsim3d.deeplearning.gan3d.gan3d_core import GAN3D
from medsim3d.deeplearning.gan3d.gan3d_parameters import GAN3DParameters

if __name__ == '__main__':
    # 1. define 3DGAN parameters, especially for data_dir, model_dir and output_dir
    gan3d_params=GAN3DParameters(
        epochs=500,
        data_dir="datasets/",
        model_dir="Male/",
        output_dir="outputs",
        middle_dir="30/"
    )
    # 2. Construct the 3DGAN model and train
    gan3d = GAN3D(

        logs_folder="test2",
        model_name="dcgan",
        use_visdom=True,
        params=gan3d_params
    )

    # 3. start the server: python -m visdom.server

    # 4. start to train
    gan3d.start()

