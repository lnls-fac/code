import matplotlib.pyplot as plt
import numpy as np
import fieldmaptrack
import math
from fieldmaptrack.track import Trajectory

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
                      
def raw_fieldmap_analysis(config):
        
    if config.fmap_extrapolation_flag and config.fmap_extrapolation_exponents is None:
        config.fmap_extrapolation_exponents = (2,3,4,5,6,7,8,9,10)

    # loads fieldmap from file
    # ========================
    config.fmap = fieldmaptrack.FieldMap(config.fmap_filename)
    
    # plots basic data
    # ================
    
    # -- longitudinal profile at (x,y) = (0,0)
    try:
        config.config_fig_number += 1
    except:
        config.config_fig_number = 1
    x,y = config.fmap.rz, config.fmap.by[config.fmap.ry_zero][config.fmap.rx_zero,:]
    plt.plot(x,y)
    plt.grid(True)
    plt.xlabel('rz [mm]'), plt.ylabel('by [mm]')
    plt.title(config.config_label + '\n' + 'Longitudinal profile of vertical field')
    plt.savefig(config.config_label + '_fig{0:02d}_'.format(config.config_fig_number) + 'by-vs-rz.pdf')
    plt.clf()
    
    # -- transversal profile at (y,z) = (0,0)
    try:
        config.config_fig_number += 1
    except:
        config.config_fig_number = 1
    x, y = config.fmap.rx, config.fmap.by[config.fmap.ry_zero][:,config.fmap.rz_zero]
    plt.plot(x,y)
    plt.grid(True)
    plt.xlabel('rx [mm]'), plt.ylabel('by [T]')
    plt.title(config.config_label + '\n' + 'Transverse profile of vertical field')
    plt.savefig(config.config_label + '_fig{0:02d}_'.format(config.config_fig_number) +  'by-vs-rx.pdf')
    plt.clf()
    
    
    # calculates missing integrals
    # ============================
    if config.fmap_extrapolation_flag:
        config.fmap.field_extrapolation_analysis(threshold_field_fraction = config.fmap_extrapolation_threshold_field_fraction, 
                                        polyfit_exponents = config.fmap_extrapolation_exponents)

    # prints basic raw information on the fieldmap
    # ============================================
    print('--- fieldmap ---')
    print(config.fmap)
    
    return config    

def calc_reference_trajectory(config):
    
    config.traj = Trajectory(beam=config.beam, fieldmap=config.fmap)
    max_z  = config.fmap.rz_max
    s_step = max_z / (config.traj_rk_nrpts - 1.0)
    config.traj.s_step = s_step
    config.traj.s  = np.array([s_step * i for i in range(config.traj_rk_nrpts)])
    config.traj.rx = np.array([0 for i in range(config.traj_rk_nrpts)])
    config.traj.ry = np.array([0 for i in range(config.traj_rk_nrpts)])
    config.traj.rz = np.array([s_step * i for i in range(config.traj_rk_nrpts)])
    config.traj.px = np.array([0 for i in range(config.traj_rk_nrpts)])
    config.traj.py = np.array([0 for i in range(config.traj_rk_nrpts)])
    config.traj.pz = np.array([1.0 for i in range(config.traj_rk_nrpts)])
    config.traj.s  = np.array(config.traj.rz)
    config.traj.bx = np.array([0 for i in range(config.traj_rk_nrpts)]) 
    config.traj.by = np.array([0 for i in range(config.traj_rk_nrpts)])
    config.traj.bz = np.array([0 for i in range(config.traj_rk_nrpts)])
    return config
        
def trajectory_analysis(config):
    
    if config.traj_load_filename is not None:
        # loads trajectory from file
        config.beam = fieldmaptrack.Beam(energy = config.beam_energy)
        config.traj = fieldmaptrack.Trajectory(beam=config.beam, fieldmap=config.fmap)
        config.traj.load(config.traj_load_filename)
    else:
        # calcs trajectory centered in good-field-region
        config.beam = fieldmaptrack.Beam(energy = config.beam_energy)
        config = calc_reference_trajectory(config)     
       
    
    # prints basic information on the reference trajectory
    # ====================================================
    print('--- trajectory (rz > 0) ---')
    print(config.traj)
    
    # saves trajectory in file
    config.traj.save(filename='trajectory.txt')
        
    # saves field on trajectory in file
    config.traj.save_field(filename='field_on_trajectory.txt')
    
    return config

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
    
    return config