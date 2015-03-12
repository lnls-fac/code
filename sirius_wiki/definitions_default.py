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

    """
    ''' Linac parameters
        ================ '''

    li_multi_bunch_beam_energy = 150.0 # [MeV]
    li_multi_bunch_rf_frequency = 3.0 # [GHz]
    li_multi_bunch_maximum_normalized_emittance = 50.0 # [π·mm·mrad]
    li_multi_bunch_maximum_rms_energy_spread = 0.5 # [%]
    li_multi_bunch_maximum_pulse_to_pulse_energy_variation = 0.25 # [%]
    li_multi_bunch_maximum_pulse_to_pulse_jitter = 100.0 # [ps]
    li_multi_bunch_minimum_pulse_charge = 3.0 # [nC]
    li_multi_bunch_minimum_pulse_duration = 150.0 # [ns]
    li_multi_bunch_maximum_pulse_duration = 300.0 # [ns]
    li_multi_bunch_repetition_rate = 2.0 # [Hz]

    li_single_bunch_beam_energy = 150.0 # [MeV]
    li_single_bunch_rf_frequency = 3.0 # [GHz]
    li_single_bunch_maximum_normalized_emittance = 50.0 # [π·mm·mrad]
    li_single_bunch_maximum_rms_energy_spread = 0.5 # [%]
    li_single_bunch_maximum_pulse_to_pulse_energy_variation = 0.25 # [%]
    li_single_bunch_maximum_pulse_to_pulse_jitter = 100.0 # [ps]
    li_single_bunch_minimum_pulse_charge = 1.0 # [nC]
    li_single_bunch_maximum_pulse_duration = 1.0 # [ns]
    li_single_bunch_repetition_rate = 2.0 # [Hz]

    '''Linac to booster transport line parameters'''

    tb_beam_energy            = 150.0 # [MeV]
    tb_beam_gamma_factor      = gamma(1.0e-3*tb_beam_energy)
    tb_beam_beta_factor       = beta(tb_beam_gamma_factor)
    tb_beam_velocity          = velocity(tb_beam_beta_factor)
    tb_beam_magnetic_rigidity = brho(1.0e-3*tb_beam_energy, tb_beam_beta_factor)

    tb_total_length = 21.2475 # [m]
    tb_number_of_dipoles = 4
    tb_number_of_quadrupoles = 13
    tb_number_of_septa = 1
    tb_maximum_quadrupole_gradient = 10.0 # [T/m]

    tb_arc_length_of_dipole = 0.300 # [m]
    tb_arc_length_of_septum = 0.5000 # [m]

    tb_dipole_deflection_angle = 15.0 # [°]
    tb_septum_deflection_angle = 21.75 # [°]

    tb_dipole_bending_radius = tb_arc_length_of_dipole / deg2rad(tb_dipole_deflection_angle)
    tb_septum_bending_radius = tb_arc_length_of_septum / deg2rad(tb_septum_deflection_angle)

    tb_dipole_magnetic_field = tb_beam_magnetic_rigidity / tb_dipole_bending_radius
    tb_septum_magnetic_field = tb_beam_magnetic_rigidity / tb_septum_bending_radius

    tb_dipole_sagitta = 9.8 # [mm]
    tb_septum_sagitta = 23.7 # [mm]


    tb_hardedge_length_of_QA1_quadrupoles = 0.05 # [m]
    tb_hardedge_length_of_QA2_quadrupoles = 0.10 # [m]
    tb_hardedge_length_of_QA3_quadrupoles = 0.10 # [m]
    tb_hardedge_length_of_QB1_quadrupoles = 0.10 # [m]
    tb_hardedge_length_of_QB2_quadrupoles = 0.10 # [m]
    tb_hardedge_length_of_QC1_quadrupoles = 0.10 # [m]
    tb_hardedge_length_of_QC2_quadrupoles = 0.10 # [m]
    tb_hardedge_length_of_QC3_quadrupoles = 0.10 # [m]
    tb_hardedge_length_of_QD1_quadrupoles = 0.10 # [m]
    tb_hardedge_length_of_QD2_quadrupoles = 0.10 # [m]
    tb_hardedge_length_of_QE1_quadrupoles = 0.10 # [m]
    tb_hardedge_length_of_QE2_quadrupoles = 0.10 # [m]

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
