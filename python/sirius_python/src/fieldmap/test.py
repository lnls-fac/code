import math
import fieldmap
import numpy
from Tkinter import Tk
from tkFileDialog import askopenfilename
import matplotlib.pyplot as plt

def plots_field_profiles():
   
    ''' deletes all loaded fielmaps '''
    fieldmap.clear_all()
   
    ''' select file with fieldmap ''' 
    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    filename = askopenfilename(title = 'select file with fieldmap', filetypes=[('ascii files', '.txt')], initialdir = '/home/ximenes') # show an "Open" dialog box and return the path to the selected file
   
    ''' creates filemap object '''
    fm = fieldmap.Fieldmap(filename)
    
    ''' calcs transverse by profile '''
    posx = numpy.linspace(fm.xmin, fm.xmax, fm.nx)
    pos = numpy.zeros((3,len(posx)))
    pos[0,:] = posx
    field = fm.interpolate(pos)
    by_vs_x = field[1,:]
    
    ''' calcs longitudinal by profile '''
    posz = numpy.linspace(fm.zmin, fm.zmax, fm.nz)
    pos = numpy.zeros((3,len(posz)))
    pos[2,:] = posz
    field = fm.interpolate(pos)
    by_vs_z = field[1,:]
    
    ''' plots by vs x '''
    plt.subplot(2,1,0)
    plt.plot(1000*posx, by_vs_x)
    plt.xlabel('posx [mm]')
    plt.ylabel('By [T]')
    
    ''' plots by vs z '''
    plt.subplot(2,1,1)
    plt.plot(1000*posz, by_vs_z)
    plt.xlabel('posz [mm]')
    plt.ylabel('By [T]')
    
    plt.show()
    
   
def calcs_trajectory():
    
    ''' deletes all loaded fielmaps '''
    fieldmap.clear_all()
   
    ''' select file with fieldmap ''' 
    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    filename = askopenfilename(title = 'select file with fieldmap', filetypes=[('ascii files', '.txt')], initialdir = '/home/ximenes') # show an "Open" dialog box and return the path to the selected file
   
    ''' creates filemap object '''
    fm = fieldmap.Fieldmap(filename)
    
    ''' does runge-kutta integration with constant step size '''
    init_state = numpy.array([[0.],[0.],[0.],[0.],[0.],[1.0]])
    traj = fm.electron_trajectory(energy = 3, si = 0, sf = 2.0, nrpts = 5000, init_state = init_state)
    s     = traj[0,:]
    x     = traj[1,:]
    betax = traj[2,:]
    z     = traj[5,:]
    betaz = traj[6,:]
    
    ''' calcs final deflection angle '''
    angf  = abs(math.atan(betax[-1] / betaz[-1]))
    
    ''' compares with nominal deflection angle and calcs error '''
    nangle = 7.2 * (math.pi/180)
    dangle = 100 * (2*angf - nangle) / nangle
    print('final angle at s = {0:f}: {1:f}'.format(s[-1], angf * (180/math.pi)))
    print('angle error: {0:+6.3f}'.format(dangle))
    
    ''' plot trajectory in z-x plane '''
    plt.plot(z,x)
    plt.show()
    
    
    
    
#plots_field_profiles()
calcs_trajectory()
    