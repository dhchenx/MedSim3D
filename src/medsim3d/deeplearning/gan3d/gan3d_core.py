'''
main.py

Welcome, this is the entrance to 3dgan
'''

import argparse
from medsim3d.deeplearning.gan3d.trainer import trainer
import torch

from medsim3d.deeplearning.gan3d.tester import tester
from medsim3d.deeplearning.gan3d.gan3d_parameters import GAN3DParameters




class GAN3D:
    def __init__(self,
                 logs_folder="first_test",
                 model_name="dcgan",
                 local_test=False,
                 test=False,
                 use_visdom=True,
                 params:GAN3DParameters=None
                 ):
        # add arguments
        self.parser = argparse.ArgumentParser()

        # loggings parameters
        self.parser.add_argument('--logs', type=str, default=logs_folder, help='logs by tensorboardX')
        self.parser.add_argument('--local_test', type=self.str2bool, default=local_test, help='local test verbose')
        self.parser.add_argument('--model_name', type=str, default=model_name, help='model name for saving')
        self.parser.add_argument('--test', type=self.str2bool, default=test, help='call tester.py')
        self.parser.add_argument('--use_visdom', type=self.str2bool, default=use_visdom, help='visualization by visdom')
        self.args = self.parser.parse_args()
        self.params=params
        # list params
        if self.params==None:
            self.params=GAN3DParameters()

        self.params.print_params()

    def str2bool(self,v):
        if v.lower() in ('yes', 'true', 't', 'y', '1'):
            return True
        elif v.lower() in ('no', 'false', 'f', 'n', '0'):
            return False
        else:
            raise argparse.ArgumentTypeError('Boolean value expected.')

    def start(self):
        # run program
        if not self.args.test:
            trainer(self.args, self.params)
        else:
            tester(self.args,self.params)

