# -*- coding: utf-8 -*-

'''
Date: 2014-10-15

Current Lattice Versions (see http://10.0.21.132/FAC:Sirius_lattice_versions):

SI: V03.C02
BO: V901.M0
TS: V300
TB: V200

'''

import optics
import math

class ParameterDefinitions(object):

    '''Booster to storage ring transport line parameters'''

    ts_beam_energy            = 3.0 # [GeV]
    ts_beam_gamma_factor      = gamma(ts_beam_energy)
    ts_beam_beta_factor       = beta(ts_beam_gamma_factor)
    ts_beam_velocity          = velocity(ts_beam_beta_factor)
    ts_beam_magnetic_rigidity = brho(ts_beam_energy, ts_beam_beta_factor)

    ts_total_length = 27.88 # [m]
    ts_number_of_dipoles = 2
    ts_number_of_quadrupoles = 8
    ts_maximum_quadrupole_gradient = 25.0 # [T/m]

    ts_hardedge_length_of_dipoles = bo_hardedge_length_of_dipoles # [m]
    ts_hardedge_length_of_extraction_septum = 0.85 # [m]
    ts_hardedge_length_of_thick_injection_septum = 1.100 # [m]
    ts_hardedge_length_of_thin_injection_septum = 1.400 # [m]

    ts_dipole_deflection_angle = bo_dipole_deflection_angle # [°]
    ts_extraction_septum_deflection_angle = -3.60 # [°]
    ts_thick_injection_septum_deflection_angle = 6.2 # [°]
    ts_thin_injection_septum_deflection_angle = 4.73 # [°]

    ts_dipole_bending_radius = ts_hardedge_length_of_dipoles / deg2rad(ts_dipole_deflection_angle)
    ts_extraction_septum_bending_radius = ts_hardedge_length_of_extraction_septum / deg2rad(ts_extraction_septum_deflection_angle)
    ts_thick_injection_septum_bending_radius = ts_hardedge_length_of_thick_injection_septum / deg2rad(ts_thick_injection_septum_deflection_angle)
    ts_thin_injection_septum_bending_radius = ts_hardedge_length_of_thin_injection_septum / deg2rad(ts_thin_injection_septum_deflection_angle)

    ts_dipole_magnetic_field = ts_beam_magnetic_rigidity / ts_dipole_bending_radius
    ts_extraction_septum_magnetic_field = ts_beam_magnetic_rigidity / ts_extraction_septum_bending_radius
    ts_thick_injection_septum_magnetic_field = ts_beam_magnetic_rigidity / ts_thick_injection_septum_bending_radius
    ts_thin_injection_septum_magnetic_field = ts_beam_magnetic_rigidity / ts_thin_injection_septum_bending_radius

    ts_dipole_sagitta = 18.1 # [mm]
    ts_extraction_septum_sagitta = 6.7 # [mm]
    ts_thick_injection_septum_sagitta = 14.9 # [mm]
    ts_thin_injection_septum_sagitta = 14.4 # [mm]

    ts_number_of_dipoles = 2
    ts_number_of_extraction_septa = 2
    ts_number_of_thick_injection_septa = 1
    ts_number_of_thin_injection_septa = 1

    '''correction system'''
    ts_number_of_beam_position_monitors = 5
    ts_number_of_horizontal_dipole_correctors = 3
    ts_number_of_vertical_dipole_correctors = 5
    ts_horizontal_dipole_corrector_maximum_strength = 0.35 # [mrad]
    ts_vertical_dipole_corrector_maximum_strength = 0.35 # [mrad]

    ts_hardedge_length_of_QA1_quadrupoles = bo_hardedge_length_of_short_quadrupoles # [m]
    ts_hardedge_length_of_QA2_quadrupoles = bo_hardedge_length_of_short_quadrupoles # [m]
    ts_hardedge_length_of_QB1_quadrupoles = bo_hardedge_length_of_short_quadrupoles # [m]
    ts_hardedge_length_of_QB2_quadrupoles = bo_hardedge_length_of_short_quadrupoles # [m]
    ts_hardedge_length_of_QC1_quadrupoles = bo_hardedge_length_of_short_quadrupoles # [m]
    ts_hardedge_length_of_QC2_quadrupoles = bo_hardedge_length_of_short_quadrupoles # [m]
    ts_hardedge_length_of_QC3_quadrupoles = bo_hardedge_length_of_short_quadrupoles # [m]
    ts_hardedge_length_of_QC4_quadrupoles = bo_hardedge_length_of_short_quadrupoles # [m]

    ts_QA1_quadrupole_strength =  0.85 # [1/m^2]
    ts_QA2_quadrupole_strength =  1.01 # [1/m^2]
    ts_QB1_quadrupole_strength = -0.32 # [1/m^2]
    ts_QB2_quadrupole_strength =  2.19 # [1/m^2]
    ts_QC1_quadrupole_strength = -1.88 # [1/m^2]
    ts_QC2_quadrupole_strength =  1.80 # [1/m^2]
    ts_QC3_quadrupole_strength =  1.80 # [1/m^2]
    ts_QC4_quadrupole_strength = -1.32 # [1/m^2]

    ts_QA1_quadrupole_gradient = ts_beam_magnetic_rigidity * ts_QA1_quadrupole_strength
    ts_QA2_quadrupole_gradient = ts_beam_magnetic_rigidity * ts_QA2_quadrupole_strength
    ts_QB1_quadrupole_gradient = ts_beam_magnetic_rigidity * ts_QB1_quadrupole_strength
    ts_QB2_quadrupole_gradient = ts_beam_magnetic_rigidity * ts_QB2_quadrupole_strength
    ts_QC1_quadrupole_gradient = ts_beam_magnetic_rigidity * ts_QC1_quadrupole_strength
    ts_QC2_quadrupole_gradient = ts_beam_magnetic_rigidity * ts_QC2_quadrupole_strength
    ts_QC3_quadrupole_gradient = ts_beam_magnetic_rigidity * ts_QC3_quadrupole_strength
    ts_QC4_quadrupole_gradient = ts_beam_magnetic_rigidity * ts_QC4_quadrupole_strength

    """
