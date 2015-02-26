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

    # calcs multipoles around reference trajectory
    # ============================================
    config.multipoles = fieldmaptrack.Multipoles(trajectory=config.traj,
                                         perpendicular_grid=config.multipoles_perpendicular_grid,
                                         normal_field_fitting_monomials=config.multipoles_normal_field_fitting_monomials,
                                         skew_field_fitting_monomials=config.multipoles_skew_field_fitting_monomials)
    config.multipoles.calc_multipoles(is_ref_trajectory_flag = False)
    config.multipoles.calc_multipoles_integrals()
    config.multipoles.calc_multipoles_integrals_relative(config.multipoles.normal_multipoles_integral, main_monomial = 0, r0 = config.multipoles_r0, is_skew = False)

    # saves multipoles to file
    config.multipoles.save('multipoles.txt')

    # prints basic information on multipoles
    # ======================================
    print('--- multipoles on reference trajectory (rz > 0) ---')
    print(config.multipoles)

    # plots normal multipoles
    config = plot_normal_multipoles(config)
    # plots skew multipoles
    config = plot_skew_multipoles(config)

    # plots residual normal field
    config = plot_residual_normal_field(config)
    # plots residual skew field
    config = plot_residual_skew_field(config)

    return config
