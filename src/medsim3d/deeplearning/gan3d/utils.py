
'''
utils.py

Some utility functions

'''
import quickcsv
import scipy.ndimage as nd
import scipy.io as io
import matplotlib


# if params.device.type != 'cpu':
#    matplotlib.use('Agg')

import matplotlib.pyplot as plt
import skimage.measure as sk
from mpl_toolkits import mplot3d
import matplotlib.gridspec as gridspec
import numpy as np
from torch.utils import data
from torch.autograd import Variable
import torch
import os
import pickle

def getVoxelFromMat(path, cube_len=64):
    if cube_len == 32:
        voxels = io.loadmat(path)['instance'] # 30x30x30
        voxels = np.pad(voxels, (1, 1), 'constant', constant_values=(0, 0))
    elif cube_len==64:
        voxels = io.loadmat(path)['instance']  # 62x62x62
        voxels = np.pad(voxels, (1, 1), 'constant', constant_values=(0, 0))
        voxels = nd.zoom(voxels, (2, 2, 2), mode='constant', order=0)
    else:
        # voxels = np.load(path) 
        # voxels = io.loadmat(path)['instance'] # 64x64x64
        # voxels = np.pad(voxels, (2, 2), 'constant', constant_values=(0, 0))
        # print (voxels.shape)
        voxels = io.loadmat(path)['instance'] # 30x30x30
        voxels = np.pad(voxels, (1, 1), 'constant', constant_values=(0, 0))
        voxels = nd.zoom(voxels, (2, 2, 2), mode='constant', order=0)
        # print ('here')
    # print (voxels.shape)
    return voxels


def getVFByMarchingCubes(voxels, threshold=0.5):
    v, f, norm,val = sk.marching_cubes(voxels, level=threshold)
    return v, f


def plotVoxelVisdom(voxels, visdom, title):
    v, f = getVFByMarchingCubes(voxels)
    visdom.mesh(X=v, Y=f, opts=dict(opacity=0.5, title=title))


def SavePloat_Voxels(voxels, path, iteration,params,points_dir=""):
    voxels = voxels[:8].__ge__(0.5)
    fig = plt.figure(figsize=(32, 16))
    gs = gridspec.GridSpec(2, 4)
    gs.update(wspace=0.05, hspace=0.05)
    list_points=[]

    if not os.path.exists(params.points_dir):
        os.mkdir(params.points_dir)
    count = 0
    for i, sample in enumerate(voxels):
        x, y, z = sample.nonzero()
        for idx,xx in enumerate(x):
            yy=y[idx]
            zz=z[idx]
            list_points.append({
                "id":count,
                "x":xx,
                "y":yy,
                "z":zz
            })
            count+=1
        ax = plt.subplot(gs[i], projection='3d')
        ax.scatter(x, y, z, zdir='z', c='red')
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        # ax.set_aspect('equal')
    # print (path + '/{}.png'.format(str(iteration).zfill(3)))
    plt.savefig(path + '/{}.png'.format(str(iteration).zfill(3)), bbox_inches='tight')
    plt.close()

    if len(list_points)!=0 and os.path.exists(points_dir):
        quickcsv.write_csv(points_dir+'/{}.csv'.format(str(iteration).zfill(3)),list_rows=list_points)


class ShapeNetDataset(data.Dataset):

    def __init__(self, root, args,  train_or_val="train",params=None):
        
        
        self.root = root
        self.listdir = os.listdir(self.root)
        # print (self.listdir)  
        # print (len(self.listdir)) # 10668

        data_size = len(self.listdir)
#        self.listdir = self.listdir[0:int(data_size*0.7)]
        self.listdir = self.listdir[0:int(data_size)]
        
        print ('data_size =', len(self.listdir)) # train: 10668-1000=9668
        self.args = args
        self.params=params

    def __getitem__(self, index):
        with open(self.root + self.listdir[index], "rb") as f:
            volume = np.asarray(getVoxelFromMat(f, self.params.cube_len), dtype=np.float32)
            # print (volume.shape)
        return torch.FloatTensor(volume)

    def __len__(self):
        return len(self.listdir)


def generateZ(args, batch,params):

    if params.z_dis == "norm":
        Z = torch.Tensor(batch, params.z_dim).normal_(0, 0.33).to(params.device)
    elif params.z_dis == "uni":
        Z = torch.randn(batch, params.z_dim).to(params.device).to(params.device)
    else:
        print("z_dist is not normal or uniform")

    return Z

if __name__=="__main__":
    mat_path=r"D:\UIBE科研\国自科青年\NetLogo\论文2\medical-education-project\visible_human\deep_learning\gans\3dgan\simple-pytorch-3dgan-master\volumetric_data\chair\30\train\chair_000000643_6.mat"

    voxels=getVoxelFromMat(path=mat_path,cube_len=64)
    v,f=getVFByMarchingCubes(voxels)
    print(v)
    list_points=[]
    for vv in v:
        list_points.append({
            "x":vv[0],
            "y":vv[1],
            "z":vv[2]
        })
    quickcsv.write_csv("mat_points.csv",list_points)

    print(f)


    '''
    from scipy.io import loadmat

    annots = loadmat(mat_path)
    print(annots)

    con_list = [[element for element in upperElement] for upperElement in annots['instance']]

    print(con_list)

    import pandas as pd

    # zip provides us with both the x and y in a tuple.
    newData = list(zip(con_list[0], con_list[1]))
    columns = ['obj_contour_x', 'obj_contour_y']
    df = pd.DataFrame(newData, columns=columns)
    print(df.head(20))
    '''





