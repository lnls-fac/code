import matplotlib.pyplot as plt
import numpy as np
import fieldmaptrack

#from multiprocessing import Process

class Config:
    
    def __init__(self):
        
        self.config_label = None
        self.config_timestamp = None
        self.fmap_filename = None
        self.fmap_extrapolation_flag = False
        self.fmap_extrapolation_threshold_field_fraction = 0.3
        self.fmap_extrapolation_exponents = None
        self.traj_rk_s_step = None
        self.traj_rk_length = None 
        self.traj_rk_nrpts = None
        self.traj_rk_min_rz = None
        self.traj_center_sagitta_flag = True
        self.traj_force_midplane_flag = True
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

def calc_sagitta(half_dipole_length, trajectory):
    
    rx = trajectory.rx
    rz = trajectory.rz
    
    if rz[-1] < half_dipole_length:
        raise DipoleAnalysisException('trajectory path does not exit dipole')
    
    i = 0
    while (rz[i] < half_dipole_length):
        i += 1
    sagitta = rx[0] - rx[i]
    return sagitta
              
def trajectory_analysis(config):
    
    config.beam = fieldmaptrack.Beam(energy = config.beam_energy, current = config.beam_current)
    
    # calcs reference trajectory
    # ==========================
    # if it is the case, iterates the calculation of the trajectory
    # until its sagitta is centered in the good field region. This is
    # accomplished by changing the initial radial position of the trajectory
    # at the longitudinal center of the dipole.
    config.traj = fieldmaptrack.Trajectory(beam=config.beam, fieldmap=config.fmap)
    half_dipole_length = config.fmap.length / 2.0
    init_rx, init_ry, init_rz = 0.0, 0.0, 0.0
    init_px, init_py, init_pz = 0.0, 0.0, 1.0
    rk_min_rz = config.fmap.rz[-1]
    while True:
        config.traj.calc_trajectory(init_rx=init_rx, init_ry=init_ry, init_rz=init_rz,   
                                    init_px=init_px, init_py=init_py, init_pz=init_pz, 
                                    s_step         = config.traj_rk_s_step,
                                    s_length       = config.traj_rk_length, 
                                    s_nrpts        = config.traj_rk_nrpts, 
                                    min_rz         = rk_min_rz,
                                    force_midplane = config.traj_force_midplane_flag) 
        config.traj_sagitta = calc_sagitta(half_dipole_length, config.traj)
        if not config.traj_center_sagitta_flag:
            break
        new_init_rx = config.traj_sagitta / 2.0
        change_init_rx = new_init_rx - init_rx
        if abs(change_init_rx) < 0.001:
            break
        else:
            init_rx = new_init_rx
    
    
    # prints basic information on the reference trajectory
    # ====================================================
    print('--- trajectory ---')
    print(config.traj)
    print('{0:<35s} {1} mm'.format('sagitta:', config.traj_sagitta))
    
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
    config.multipoles.calc_multipoles()
    config.multipoles.calc_multipoles_integrals()
    config.multipoles.calc_multipoles_integrals_normalized(config.multipoles.polynom_b, 0, r0 = config.multipoles_r0)
    
    # prints basic information on multipoles
    # ======================================
    print('--- multipoles on trajectory ---')
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