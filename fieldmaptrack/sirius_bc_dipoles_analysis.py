#!/usr/bin/python3 

from fieldmaptrack import beam
from fieldmaptrack import dipole_analysis
import numpy as np


config = dipole_analysis.Config()

config.config_label  = 'BC_model1_controlgap_8mm' #  identification label
config.fmap_filename = '/home/ximenes/fac_files/data/magnet_modelling/sirius/bc/fieldmaps/2014-09-05_Dipolo_Anel_BC_Modelo1_gap_lateral_8mm_-50_50mm_-2000_2000mm.txt' # parameter
config.fmap_extrapolation_flag = False #  does missing integral analysis with extrapolation functions
config.fmap_extrapolation_threshold_field_fraction = 0.3   #  for missing integrals analysis of fieldmap
config.fmap_extrapolation_exponents = [2,3,4,5,6,7,8,9,10] #  for extrapolating fieldmap
config.beam_energy  = 3.0    #  electron beam energy [GeV]
config.beam_current = 350    #  electron beam current [mA]
config.traj_length  = 800.0  #  total path length to track through RK
config.traj_nrpts   = 2001   #  number of points in RK 
config.traj_force_midplane_flag = True #  force trajectory on midplane (setting ry = py = 0)

perpendicular_grid = np.linspace(-5,5,11) #  grid of points on perpendicular line to ref trajectory
multipolar_monomials = [0,1,2,3,4,5,6]    #  monomials to include in the polynomial fit of multipoles

if __name__ == "__main__":
    
    print('DIPOLE ANALYSIS')
    print('===============')
         
    print('{0:<35s} {1}'.format('label:', config.config_label))
    
    config = dipole_analysis.raw_fieldmap_analysis(config)
    config = dipole_analysis.reference_trajectory(config)