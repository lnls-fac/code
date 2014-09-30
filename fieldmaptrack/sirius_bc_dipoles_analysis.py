#!/usr/bin/env python3 

import fieldmaptrack as fmaptrack
import fieldmaptrack.dipole_analysis as analysis
import numpy as np

config = analysis.Config()

config.config_label  = 'bc_model1_controlgap_8mm' #  identification label
config.fmap_filename = '/home/ximenes/fac_files/data/magnet_modelling/sirius/bc/fieldmaps/2014-09-05_Dipolo_Anel_BC_Modelo1_gap_lateral_8mm_-50_50mm_-2000_2000mm.txt' # parameter
config.fmap_extrapolation_flag = False #  does missing integral analysis with extrapolation functions
#config.fmap_extrapolation_threshold_field_fraction = 0.3   #  for missing integrals analysis of fieldmap
#config.fmap_extrapolation_exponents = (2,3,4,5,6,7,8,9,10) #  for extrapolating fieldmap
config.beam_energy     = 3.0    #  electron beam energy [GeV]
config.beam_current    = 350    #  electron beam current [mA]
config.traj_rk_s_step  = 1.0    #  step in s for the 4th-order RK integration
#config.traj_rk_length  = 800.0  #  total path length to track through RK
#config.traj_rk_nrpts   = 2001   #  number of points in RK 
config.traj_force_midplane_flag = True #  force trajectory on midplane (setting ry = py = 0)

config.multipoles_perpendicular_grid = np.linspace(-10,10,31) #  grid of points on perpendicular line to ref trajectory
config.multipoles_fitting_monomials  = (0,1,2,3,4,5,6,7,8,9,10)    #  monomials to include in the polynomial fit of multipoles
config.multipoles_r0 = 11.7 # [mm]

if __name__ == "__main__":
    
    print('DIPOLE ANALYSIS')
    print('===============')
         
    print('{0:<35s} {1}'.format('label:', config.config_label))
    
    config = analysis.raw_fieldmap_analysis(config)
    config = analysis.trajectory_analysis(config)
    config = analysis.multipoles_analysis(config)
