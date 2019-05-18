# -*- coding: utf-8 -*-
"""
Created on Mon May 06 17:24:08 2019

@author: petrahulsman
"""

import scipy.io as spio
import numpy as np
import matplotlib.pyplot as plt

folder = 'C:\\Users\\Sanne de Smet\\Documents\\Master_Watermanagement\\Q4\\Fieldwork\\Data\\2019_05_13_ADCP\\Sontek\\Monday afternoon\\'
mat = spio.loadmat(folder+'20051002153808.mat',squeeze_me=True)

Velocity    = mat['WaterTrack']['Velocity'][()]                             # velocity for each of the 4 beams
Vprofile    = Velocity[:,0,:]                                               # average velocity profile
Vmean       = mat['Summary']['Mean_Vel'][()][:,0] # = nanmean(Vprofile,1)   # average velocity averaged over the depth
Depth       = mat['Summary']['Depth'][()]         # = BottomTrack.VB_Depth  # vertical beam (VB) depth for each vertical sample (using only the echo sounder which is only used to measure the depth at 1Mhz frequency to reach greater depths)
Cells       = (mat['Summary']['Cells'][()]).astype('int')                   # number of cells for each vertical beam
Discharge   = mat['Summary']['Total_Q'][()]                                 # discharge
Track       = mat['Summary']['Track'][()]        							# track location for each sample in X/Y coordinates
Distance    = np.sum(abs(Track),1)    #this is probably not be correct and it depends how Track is measured. Please check this!
Depth_BT    = mat['BottomTrack']['BT_Depth'][()]						    # bottom track (BT) depth using 4 beams at 3MHz frequency (smaller depth range, higher resolution). The depth is estimated assuming the river bed does not move and using boat movement information.
DepthBeam   = mat['BottomTrack']['BT_Beam_Depth'][()]                       # total water depth for each beam


vbeam=118 #choose the location of a vertical sample
Cellsize = Depth[vbeam]/Cells[vbeam]
#Here, the vertical cell depth is assumed to be constant and calculated:
#cellsize = total_depth/nr_of_cells
#This depends with the chosen settings, so please check this!


fig=plt.figure(2, figsize=(8,5))
plt.subplots_adjust(hspace=0.3, wspace=0.5)
ax=plt.subplot2grid((2,5), (0,0),colspan=4)
plt.imshow(Vprofile,vmin=0,vmax=0.3)
plt.plot([vbeam,vbeam],[Cells[vbeam],0],'--r')
plt.colorbar()
plt.title('Velocity profile [m/s]')

ax=plt.subplot2grid((2,3), (1,2),colspan=1)
Depth_profile = -np.cumsum(np.ones((Cells[vbeam],1)))*Cellsize
plt.plot(Vprofile[0:Cells[vbeam],vbeam],Depth_profile)
plt.xlabel('Velocity [m/s]')
plt.ylabel('Depth [m]')
plt.title('Velocity profile at red dashed line')

ax=plt.subplot2grid((2,3), (1,0),colspan=2)
plt.plot(Distance,-Depth)
plt.plot([Distance[vbeam],Distance[vbeam]],[-Depth[vbeam],0],'--r')
plt.title('Depth profile')
plt.ylabel('Depth [m]')
plt.xlabel('Distance [m]')
plt.ylim([-2,0])

