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
    traj = fm.electron_trajectory(energy = 3, si = 0, sf = 2.0, nrpts = 500, init_state = init_state)
    #s = traj[0,:]
    x = traj[1,:]
    z = traj[5,:]
    plt.plot(z,x)
    plt.show()
    
    
    
    
#plots_field_profiles()
calcs_trajectory()
    