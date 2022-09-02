'''
params.py

Managers of all hyper-parameters

'''

import torch

class GAN3DParameters:
    def __init__(self,
                 batch_size=32,
                 epochs=20,
        soft_label = False,

    adv_weight = 0,
    d_thresh = 0.8,
    z_dim = 200,
    z_dis = "norm",
    model_save_step = 1,
    g_lr = 0.0025,
    d_lr = 0.00001,
    beta = (0.5, 0.999),
    cube_len = 32,
    leak_value = 0.2,
    bias = False,
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu'),
    data_dir = '../datasets/',
    model_dir = 'Male/',  # change it to train on other data models
    output_dir = '../outputs',
                 middle_dir="30/",
                 images_dir="../test_outputs",
                 points_dir="../test_points",
                 testN=8
                 ):
        self.epochs = epochs
        self.batch_size = batch_size
        self.soft_label = soft_label
        self.adv_weight = adv_weight
        self.d_thresh = d_thresh
        self.z_dim = z_dim
        self.z_dis = z_dis
        self.model_save_step = model_save_step
        self.g_lr =g_lr
        self.d_lr =d_lr
        self.beta =beta
        self.cube_len = cube_len
        self.leak_value =leak_value
        self.bias = bias
        self.device = device
        self.data_dir = data_dir
        self.model_dir = model_dir  # change it to train on other data models
        self.output_dir = output_dir
        self.images_dir =images_dir
        self.middle_dir=middle_dir
        self.points_dir=points_dir
        self.testN=testN

    def print_params(self):
        l = 16
        print(l * '*' + 'hyper-parameters' + l * '*')

        print('epochs =', self.epochs)
        print('batch_size =', self.batch_size)
        print('soft_labels =', self.soft_label)
        print('adv_weight =', self.adv_weight)
        print('d_thresh =', self.d_thresh)
        print('z_dim =', self.z_dim)
        print('z_dis =', self.z_dis)
        print('model_images_save_step =', self.model_save_step)
        print('data =', self.model_dir)
        print('device =', self.device)
        print('g_lr =', self.g_lr)
        print('d_lr =', self.d_lr)
        print('cube_len =', self.cube_len)
        print('leak_value =', self.leak_value)
        print('bias =', self.bias)

        print(l * '*' + 'hyper-parameters' + l * '*')
