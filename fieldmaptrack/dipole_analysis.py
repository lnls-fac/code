import matplotlib.pyplot as plt
import numpy as np
import fieldmaptrack.fieldmap as fieldmap
import fieldmaptrack.beam as beam
import fieldmaptrack.track as track

#from multiprocessing import Process

class Config:
    
    def __init__(self):
        
        self.config_label = None
        self.config_timestamp = None
        self.fmap_filename = None
        self.fmap_extrapolation_flag = False
        self.fmap_extrapolation_threshold_field_fraction = 0.3
        self.fmap_extrapolation_exponents = None
        self.traj_center_sagitta_flag = True
        self.traj_length = None 
        self.traj_nrpts = None 
        self.traj_force_midplane_flag = True
                                    
    
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
        
def raw_fieldmap_analysis(config):
        
    if config.fmap_extrapolation_flag and config.fmap_extrapolation_exponents is None:
        config.fmap_extrapolation_exponents = (2,3,4,5,6,7,8,9,10)

    # loads fieldmap from file
    # ========================
    config.fmap = fieldmap.FieldMap(config.fmap_filename)
    
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
      
def reference_trajectory(config):
    
    config.beam = beam.Beam(energy = config.beam_energy, current = config.beam_current)
    
    # Runge-Kutta trajectory calculation
    # ==================================
    config.traj = track.Trajectory(beam=config.beam, fieldmap=config.fmap)
    half_dipole_length = config.fmap.length / 2.0
    init_rx, init_ry, init_rz = 0.0, 0.0, 0.0
    init_px, init_py, init_pz = 0.0, 0.0, 1.0
    while True:
        config.traj.calc_trajectory(init_rx=init_rx, init_ry=init_ry, init_rz=init_rz,   
                                    init_px=init_px, init_py=init_py, init_pz=init_pz, 
                                    s_length       = config.traj_length, 
                                    s_nrpts        = config.traj_nrpts, 
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
    print('--- reference trajectory ---')
    print(config.traj)
    print('{0:<35s} {1} mm'.format('sagitta:', config.traj_sagitta))
    
#     monomials = [0,1,2,3,4,5,6,7]
#     grid = np.linspace(-5,5,21)
#     polynom_a, polynom_b = traj.calc_multipoles(perpendicular_grid, multipolar_monomials)
    
    return config
