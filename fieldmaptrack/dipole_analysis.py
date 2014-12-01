import matplotlib.pyplot as plt
import numpy as np
import fieldmaptrack
import math
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
        self.traj_center_sagitta_flag = True
        self.traj_force_midplane_flag = True
        self.traj_is_reference_traj = False
        self.multipoles_r0 = None
        self.model_segmentation = None
        self.model_multipoles_integral = None
                      
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
                        
def calc_reference_trajectory_good_field_region(config):  
    # calcs reference trajectory
    # ==========================
    # if it is the case, iterates the calculation of the trajectory
    # until its sagitta is centered in the good field region. This is
    # accomplished by changing the initial radial position of the trajectory
    # at the longitudinal center of the dipole.
    half_dipole_length = config.fmap.length / 2.0
    config.traj = fieldmaptrack.Trajectory(beam=config.beam, fieldmap=config.fmap)
    if config.traj_init_rx is not None:
        init_rx = config.traj_init_rx
    else:
        init_rx = 0.0
    init_ry, init_rz = 0.0, 0.0
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
        config.traj_sagitta = config.traj.calc_sagitta(half_dipole_length)
        
        if not config.traj_center_sagitta_flag:
            break
        new_init_rx = config.traj_sagitta / 2.0
        change_init_rx = new_init_rx - init_rx
        if abs(change_init_rx) < 0.001:
            break
        else:
            init_rx = new_init_rx
            
    return config
      
def calc_reference_trajectory(config):
    
    nominal_deflection = -abs(config.model_nominal_angle/2.0)
    deflection = 0.0;
    
    # search an upper energy for which deflection is lower than nominal
    energy1 = 1.005 * config.beam_energy
    while True:
        config.beam = fieldmaptrack.Beam(energy = energy1)
        config = calc_reference_trajectory_good_field_region(config)
        deflection1 = (180.0/math.pi)*math.atan(config.traj.px[-1]/config.traj.pz[-1])
        if deflection1 > nominal_deflection:
            break
        energy1 *= 1.005
    # search a lower energy for which deflection is higher than nominal
    energy2 = 0.995 * config.beam_energy
    while True:
        config.beam = fieldmaptrack.Beam(energy = energy2)
        config = calc_reference_trajectory_good_field_region(config)
        deflection2 = (180.0/math.pi)*math.atan(config.traj.px[-1]/config.traj.pz[-1])
        if deflection2 < nominal_deflection:
            break
        energy2 *= 0.995
    
    # does bisection
    iter = 0
    while True:
        energy = 0.5 * (energy1 + energy2)
        config.beam = fieldmaptrack.Beam(energy = energy)
        config = calc_reference_trajectory_good_field_region(config)
        deflection = (180.0/math.pi)*math.atan(config.traj.px[-1]/config.traj.pz[-1])
        if deflection > nominal_deflection:
            energy1 = energy
        else:
            energy2 = energy
        error = abs(100*(deflection - nominal_deflection)/nominal_deflection)
        if error < 0.001:
            break
        iter += 1
        if (iter > 20):
            raise Exception('max number of iterations while bisecting for correct deflection angle')
    
    energy = 0.5 * (energy1 + energy2)
    config.beam = fieldmaptrack.Beam(energy = energy)
    config.traj.bx = (config.beam_energy / energy) * config.traj.bx 
    config.traj.by = (config.beam_energy / energy) * config.traj.by
    config.traj.bz = (config.beam_energy / energy) * config.traj.bz
    return config
        
def trajectory_analysis(config):
    
    if config.traj_load_filename is not None:
        # loads trajectory from file
        half_dipole_length = config.fmap.length / 2.0
        config.beam = fieldmaptrack.Beam(energy = config.beam_energy)
        config.traj = fieldmaptrack.Trajectory(beam=config.beam, fieldmap=config.fmap)
        config.traj.load(config.traj_load_filename)
        config.traj_sagitta = calc_sagitta(half_dipole_length, config.traj)
    else:
        if config.traj_is_reference_traj:
            # rescale field so that nominal deflection is reached
            config = calc_reference_trajectory(config)
        else:
            # calcs trajectory centered in good-field-region
            config.beam = fieldmaptrack.Beam(energy = config.beam_energy)
            config = calc_reference_trajectory_good_field_region(config)     
       
    
    # prints basic information on the reference trajectory
    # ====================================================
    print('--- trajectory (rz > 0) ---')
    print(config.traj)
    print('{0:<35s} {1} mm'.format('sagitta:', config.traj_sagitta))
    
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
    config.multipoles.calc_multipoles_integrals_relative(config.multipoles.normal_multipoles_integral, 0, r0 = config.multipoles_r0)
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
        x,y = config.traj.rz, config.multipoles.normal_multipoles[n,:]
        ylabel, title, fname = config.multipoles.get_multipole_labels('normal',n)
        plt.plot(x,y)
        plt.grid(True)
        plt.xlabel('s [mm]'), plt.ylabel(ylabel)
        plt.title(title + ' along trajectory' + '\n' + '(' + config.config_label + ')')
        plt.gca().yaxis.get_major_formatter().set_powerlimits((-3,3))
        plt.savefig(config.config_label + '_fig{0:02d}_'.format(config.config_fig_number) + fname + '.pdf')
        plt.clf()
    
    # plots residual field 
    #config = plot_residual_field_in_curvilinear_system(config)
    config = plot_residual_field(config)
    return config

def model_analysis(config):
    
    # creates AT model
    config = create_AT_model(config, config.model_segmentation)
    
    # adds discrepancy of deflection angle as error in polynomb[0]
    l = np.array(config.model_segmentation) / 1000.0
    m = config.model_multipoles_integral.transpose() / (-config.beam.brho)
    mi = np.sum(m, axis=1)
    fmap_deflection    = mi[0]
    nominal_deflection = abs(config.model_nominal_angle/2)*(math.pi/180.0)
    error_polynomb = nominal_deflection - fmap_deflection
    
    # prints info on model
    print('--- model polynom_b (rz > 0) ---')
    fstr = '{0:<6.4f} {1:<+13.06e} '
    for i in range(m.shape[0]):
        fstr += '{'+str(i+2)+':<+13.6e} '
    for i in range(len(l)):
        val = [l[i]] + [m[0,i]] + list(m[:,i] / l[i])
        if i == len(l)-1:
            val[2] = error_polynomb
        else:
            val[2] = 0.0
        print(fstr.format(*val))
    val = [sum(l)] + [sum(m[0,:])] + [0.0] + list(mi[1:]) 
    print('---')
    print(fstr.format(*val))
    
    
     
    
    
    
    