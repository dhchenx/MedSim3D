import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('white')
sns.set_context('talk')

import pyNetLogo

netlogo = pyNetLogo.NetLogoLink(gui=True,thd=True,netlogo_home='C:/Program Files/NetLogo 6.2.1')

netlogo.load_model('netlogo-models/MedSim3D-0.0.1a.nlogo3D')
netlogo.command('setup')