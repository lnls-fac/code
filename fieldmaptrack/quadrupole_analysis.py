import matplotlib.pyplot as plt
import numpy as np
import fieldmaptrack
import math
from fieldmaptrack.track import Trajectory
from fieldmaptrack.common_analysis import *

class Config:
    
    def __init__(self):
        
        self.config_label = None
        self.config_timestamp = None
        self.fmap_filename = None
        self.fmap_extrapolation_flag = False
        self.fmap_extrapolation_threshold_field_fraction = 0.3
        self.fmap_extrapolation_exponents = None
        self.model_hardedge_length = None
        self.traj_rk_s_step = None
        self.traj_rk_length = None 
        self.traj_rk_nrpts = None
        self.traj_rk_min_rz = None
        self.traj_save = True
        self.traj_load_filename = None
        self.traj_init_rx = None
        self.multipoles_r0 = None
    
def multipoles_analysis(config):
    
    if config.multipoles_perpendicular_grid is None:
        config.multipoles_perpendicular_grid = (-5,-4,-3,-2,-1,0,1,2,3,4,5)
    if config.multipoles_fitting_monomials is None:
        config.multipoles_fitting_monomials = (0,1,2,3,4,5,6)
    
    # calcs multipoles around reference trajectory
    # ============================================
    config.multipoles = fieldmaptrack.Multipoles(trajectory=config.traj, 
                                         perpendicular_grid=config.multipoles_perpendicular_grid,
                                         fitting_monomials=config.multipoles_fitting_monomials)
    config.multipoles.calc_multipoles(is_ref_trajectory_flag = False)
    config.multipoles.calc_multipoles_integrals()
    config.multipoles.calc_multipoles_integrals_relative(config.multipoles.polynom_b_integral, main_monomial = 1, r0 = config.multipoles_r0)
    config.multipoles.calc_hardedge_polynomials(config.model_hardedge_length)
        
         
    # saves multipoles to file
    config.multipoles.save('multipoles.txt')
    
    # prints basic information on multipoles
    # ======================================
    print('--- multipoles on reference trajectory (rz > 0) ---')
    print(config.multipoles)
    
    # plots normal multipoles
    for n in range(len(config.multipoles_fitting_monomials)):  
        try:
             config.config_fig_number += 1
        except:
            config.config_fig_number = 1
        x,y = config.traj.rz, config.multipoles.polynom_b[n,:]
        ylabel, title, fname = config.multipoles.get_multipole_labels('normal',n)
        plt.plot(x,y)
        plt.grid(True)
        plt.xlabel('s [mm]'), plt.ylabel(ylabel)
        plt.title(title + ' along trajectory' + '\n' + '(' + config.config_label + ')')
        plt.gca().yaxis.get_major_formatter().set_powerlimits((-3,3))
        plt.savefig(config.config_label + '_fig{0:02d}_'.format(config.config_fig_number) + fname + '.pdf')
        plt.clf()
    
    # plots residual field 
    config = plot_residual_field(config)
    
    return config