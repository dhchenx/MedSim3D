'''
tester.py

Test the trained 3dgan models
'''

import torch
from torch import optim
from torch import nn
from collections import OrderedDict
from medsim3d.deeplearning.gan3d.utils import *
import os
from medsim3d.deeplearning.gan3d.model import net_G, net_D
# from lr_sh import  MultiStepLR

# added
import datetime
from tensorboardX import SummaryWriter
import matplotlib.pyplot as plt
import numpy as np

import visdom


# def test_gen(args):
#     test_z = []
#     test_num = 1000
#     for i in range(test_num):
#         z = generateZ(args, 1)
#         z = z.numpy()
#         test_z.append(z)

#     test_z = np.array(test_z)
#     print (test_z.shape)
# np.save("test_z", test_z)

def tester(args,params):
    print('Evaluation Mode...')

    # image_saved_path = '../images'
    # image_saved_path = params.images_dir
    image_saved_path = params.output_dir + '/' + args.model_name + '/' + args.logs + "/" + params.images_dir
    points_saved_path = params.output_dir + '/' + args.model_name + '/' + args.logs + "/" + params.points_dir
    if not os.path.exists(image_saved_path):
        os.makedirs(image_saved_path)

    if args.use_visdom:
        vis = visdom.Visdom()

    save_file_path = params.output_dir + '/' + args.model_name
    pretrained_file_path_G = save_file_path + '/' + args.logs + '/models/G.pth'
    pretrained_file_path_D = save_file_path + '/' + args.logs + '/models/D.pth'

    print(pretrained_file_path_G)

    D = net_D(args,params)
    G = net_G(args,params)

    if not torch.cuda.is_available():
        G.load_state_dict(torch.load(pretrained_file_path_G, map_location={'cuda:0': 'cpu'}))
        D.load_state_dict(torch.load(pretrained_file_path_D, map_location={'cuda:0': 'cpu'}))
    else:
        G.load_state_dict(torch.load(pretrained_file_path_G))
        D.load_state_dict(torch.load(pretrained_file_path_D, map_location={'cuda:0': 'cpu'}))

    print('visualizing model')

    # test generator
    # test_gen(args)
    G.to(params.device)
    D.to(params.device)
    G.eval()
    D.eval()

    # test_z = np.load("test_z.npy")
    # print (test_z.shape)
    # N = test_z.shape[0]

    N = params.testN

    for i in range(N):
        # z = test_z[i,:]
        # z = torch.FloatTensor(z)

        z = generateZ(args, 1,params)

        # print (z.size())
        fake = G(z)
        samples = fake.unsqueeze(dim=0).detach().cpu().numpy()
        # print (samples.shape)
        # print (fake)
        y_prob = D(fake)
        y_real = torch.ones_like(y_prob)
        # criterion = nn.BCELoss()
        # print (y_prob.item(), criterion(y_prob, y_real).item())

        # visualization
        if not args.use_visdom:
            SavePloat_Voxels(samples, image_saved_path, 'tester_' + str(i),params,points_dir=points_saved_path)  # norm_
        else:
            plotVoxelVisdom(samples[0, :], vis, "tester_" + str(i))
            SavePloat_Voxels(samples, image_saved_path, 'tester_' + str(i), params,points_dir=points_saved_path)  # norm_
