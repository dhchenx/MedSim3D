import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('white')
sns.set_context('talk')

import pyNetLogo

netlogo = pyNetLogo.NetLogoLink(gui=True,thd=True,
                               #  netlogo_home='C:/Program Files/NetLogo 6.2.1'
                                )

netlogo.load_model('netlogo-models/MedSim3D-0.0.1a.nlogo3D')
netlogo.command('set scale 5')
netlogo.command('set sample-rate 37')
netlogo.command('set size-scale 1.2')
netlogo.command(f'load-obj-file-common "models/male.obj" true')
netlogo.command("create-vertices")
# netlogo.command("create-faces")