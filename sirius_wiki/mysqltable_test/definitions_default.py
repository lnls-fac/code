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
   
    '''Storage ring parameters
       ======================='''

    si_lattice_version                        = 'V03' 
    si_lattice_type                           = '5BA'
    si_lattice_circumference                  = 518.396   #[m]
    si_lattice_symmetry                       = 10
    si_lattice_long_straight_section_number   = si_lattice_symmetry
    si_lattice_short_straight_section_number  = si_lattice_symmetry
    si_lattice_long_straight_section_length   = 7.0       #[m]
    si_lattice_short_straight_section_length  = 6.0       #[m]

    si_beam_energy                            = 3.0   # [GeV]
    si_beam_gamma_factor                      = optics.gamma(si_beam_energy)
    si_beam_beta_factor                       = optics.beta(si_beam_gamma_factor)
    si_beam_velocity                          = optics.velocity(si_beam_beta_factor)
    si_beam_magnetic_rigidity                 = optics.brho(si_beam_energy, si_beam_beta_factor)
    si_beam_current                           = 350.0 #[mA]
    si_beam_revolution_period                 = optics.revolution_period(si_lattice_circumference, si_beam_velocity)
    si_beam_revolution_frequency              = optics.revolution_frequency(si_beam_revolution_period)
    si_beam_electron_number                   = optics.number_of_electrons(si_beam_current, si_beam_revolution_period)
           
    si_rf_harmonic_number                     = 864
    si_rf_frequency                           = optics.rf_frequency(si_beam_revolution_frequency, si_rf_harmonic_number)
    si_rf_peak_voltage                        = 2.7       #[MV]

    si_magnet_dipole_b1_number                   = 4 * si_lattice_symmetry
    si_magnet_dipole_b1_deflection_angle         = 2.76654  #[deg]
    si_magnet_dipole_b1_hardedge_length          = 0.828080 #[m] 
    si_magnet_dipole_b1_hardedge_bending_radius  = si_magnet_dipole_b1_hardedge_length / math.radians(si_magnet_dipole_b1_deflection_angle)
    si_magnet_dipole_b1_hardedge_magnetic_field  = si_beam_magnetic_rigidity / si_magnet_dipole_b1_hardedge_bending_radius
    si_magnet_dipole_b1_hardedge_sagitta         = 1000 * si_magnet_dipole_b1_hardedge_bending_radius * (1.0 - math.cos(0.5*math.radians(si_magnet_dipole_b1_deflection_angle))) #[mm]
    si_magnet_dipole_b1_hardedge_critical_energy = optics.critical_energy(si_beam_gamma_factor, si_magnet_dipole_b1_hardedge_bending_radius)

    si_magnet_dipole_b2_number                   = 4 * si_lattice_symmetry
    si_magnet_dipole_b2_deflection_angle         = 4.10351  #[deg]    
    si_magnet_dipole_b2_hardedge_length          = 1.228262 #[m]
    si_magnet_dipole_b2_hardedge_bending_radius  = si_magnet_dipole_b2_hardedge_length / math.radians(si_magnet_dipole_b2_deflection_angle)
    si_magnet_dipole_b2_hardedge_magnetic_field  = si_beam_magnetic_rigidity / si_magnet_dipole_b2_hardedge_bending_radius    
    si_magnet_dipole_b2_hardedge_sagitta         = 1000 * si_magnet_dipole_b2_hardedge_bending_radius * (1.0 - math.cos(0.5*math.radians(si_magnet_dipole_b2_deflection_angle))) #[mm]
    si_magnet_dipole_b2_hardedge_critical_energy = optics.critical_energy(si_beam_gamma_factor, si_magnet_dipole_b2_hardedge_bending_radius)

    si_magnet_dipole_b3_number                   = 4 * si_lattice_symmetry
    si_magnet_dipole_b3_deflection_angle         = 1.42995  #[deg]
    si_magnet_dipole_b3_hardedge_length          = 0.428011 #[m]
    si_magnet_dipole_b3_hardedge_bending_radius  = si_magnet_dipole_b3_hardedge_length / math.radians(si_magnet_dipole_b3_deflection_angle)
    si_magnet_dipole_b3_hardedge_magnetic_field  = si_beam_magnetic_rigidity / si_magnet_dipole_b3_hardedge_bending_radius
    si_magnet_dipole_b3_hardedge_sagitta         = 1000 * si_magnet_dipole_b3_hardedge_bending_radius * (1.0 - math.cos(0.5*math.radians(si_magnet_dipole_b3_deflection_angle))) #[mm]
    si_magnet_dipole_b3_hardedge_critical_energy = optics.critical_energy(si_beam_gamma_factor, si_magnet_dipole_b3_hardedge_bending_radius)

    si_magnet_dipole_bc_number                   = 4 * si_lattice_symmetry
    si_magnet_dipole_bc_hardedge_length          = 0.125394 #[m]
    si_magnet_dipole_bc_deflection_angle         = 1.40000  #[deg]
    si_magnet_dipole_bc_hardedge_bending_radius  = si_magnet_dipole_bc_hardedge_length / math.radians(si_magnet_dipole_bc_deflection_angle)
    si_magnet_dipole_bc_hardedge_magnetic_field  = si_beam_magnetic_rigidity / si_magnet_dipole_bc_hardedge_bending_radius
    si_magnet_dipole_bc_hardedge_sagitta         = 1000 * si_magnet_dipole_bc_hardedge_bending_radius * (1.0 - math.cos(0.5*math.radians(si_magnet_dipole_bc_deflection_angle))) #[mm]
    si_magnet_dipole_bc_hardedge_critical_energy = optics.critical_energy(si_beam_gamma_factor, si_magnet_dipole_bc_hardedge_bending_radius)    

    ''' correction system '''
    si_bpm_number = 180
    si_magnet_chs_number = 160
    si_magnet_cvs_number = 120
    si_magnet_chf_number = 80
    si_magnet_cvf_number = 80
    si_magnet_qs_number  = 80
    si_magnet_chs_maximum_strength = 250   #[urad]
    si_magnet_cvs_maximum_strength = 250   #[urad]
    si_magnet_chf_maximum_strength = 25    #[urad]
    si_magnet_cvf_maximum_strength = 25    #[urad]
    si_magnet_qs_maximum_strength  = 0.003 # [1/m]

    si_optics_default_mode = 'C02'
    si_optics_tune_horizontal                 =  4.813860814231471E+01
    si_optics_tune_vertical                   =  1.320733867979753E+01
    si_optics_tune_synchrotron                =  4.364436028401864E-03
    si_optics_tune_synchrotron_dipole         =  4.364436028401864E-03
    si_optics_betatron_frequency_horizontal   = optics.frequency_from_tune(si_beam_revolution_frequency, si_optics_tune_horizontal)
    si_optics_betatron_frequency_vertical     = optics.frequency_from_tune(si_beam_revolution_frequency, si_optics_tune_vertical)
    si_optics_synchrotron_frequency           = optics.frequency_from_tune(si_beam_revolution_frequency, si_optics_tune_synchrotron)
  
    si_optics_chromaticity_horizontal         = -4.330757974457811E-03
    si_optics_natural_chromaticity_horizontal = -1.252309601795787E+02
    si_optics_chromaticity_vertical           = -6.926578421939666E-01
    si_optics_natural_chromaticity_vertical   = -8.022172846011699E+01
    si_optics_beam_size_horizontal_long_straight_section  = 7.009486798878925E+01 #[um]
    si_optics_beam_size_horizontal_short_straight_section = 2.084762622184360E+01 #[um]
    si_optics_beam_size_horizontal_dipole_bc              = 9.948943931676647E+00 #[um]
    si_optics_beam_size_vertical_long_straight_section    = 3.214983743415169E+00 #[um]
    si_optics_beam_size_vertical_short_straight_section   = 1.939167731203255E+00 #[um]
    si_optics_beam_size_vertical_dipole_bc                = 3.996725872734588E+00 #[um]
    si_optics_beam_divergence_horizontal_long_straight_section  = 3.915259575507898E+00 #[urad]
    si_optics_beam_divergence_horizontal_short_straight_section = 1.316409860763686E+01 #[urad]
    si_optics_beam_divergence_horizontal_dipole_bc              = 2.942299673538725E+01 #[urad]
    si_optics_beam_divergence_vertical_long_straight_section    = 8.536265817057522E-01 #[urad]
    si_optics_beam_divergence_vertical_short_straight_section   = 1.415244044631019E+00 #[urad]
    si_optics_beam_divergence_vertical_dipole_bc                = 6.866611249310436E-01 #[urad]

    ''' DIPOLES ONLY '''
    si_optics_radiation_integral_i1_dipole = +8.799905562300937E-02 #[m]
    si_optics_radiation_integral_i2_dipole = +4.331040689899748E-01 #[1/m]
    si_optics_radiation_integral_i3_dipole = +3.825787715746642E-02 #[1/m^2]
    si_optics_radiation_integral_i4_dipole = -1.331248659312025E-01 #[1/m]
    si_optics_radiation_integral_i5_dipole = +1.176581653611004E-05 #[1/m]
    si_optics_radiation_integral_i6_dipole = +1.800079309293100E-02 #[1/m]
    ''' IDs '''
    si_optics_radiation_integral_i1_id = 0.0 #[m]
    si_optics_radiation_integral_i2_id = 0.0 #[1/m]
    si_optics_radiation_integral_i3_id = 0.0 #[1/m^2]
    si_optics_radiation_integral_i4_id = 0.0 #[1/m]
    si_optics_radiation_integral_i5_id = 0.0 #[1/m]
    si_optics_radiation_integral_i6_id = 0.0 #[1/m]
    ''' DIPOLES and IDs '''
    si_optics_radiation_integral_i1 = (si_optics_radiation_integral_i1_dipole + si_optics_radiation_integral_i1_id) #[m]
    si_optics_radiation_integral_i2 = (si_optics_radiation_integral_i2_dipole + si_optics_radiation_integral_i2_id) #[m]
    si_optics_radiation_integral_i3 = (si_optics_radiation_integral_i3_dipole + si_optics_radiation_integral_i3_id) #[m]
    si_optics_radiation_integral_i4 = (si_optics_radiation_integral_i4_dipole + si_optics_radiation_integral_i4_id) #[m]
    si_optics_radiation_integral_i5 = (si_optics_radiation_integral_i5_dipole + si_optics_radiation_integral_i5_id) #[m]
    si_optics_radiation_integral_i6 = (si_optics_radiation_integral_i6_dipole + si_optics_radiation_integral_i6_id) #[m]
     

    si_optics_transverse_coupling = 1.0    # [%]

    si_optics_damping_partition_number_vertical_dipole     = 1.0
    si_optics_damping_partition_number_horizontal_dipole   = optics.Jx(si_optics_radiation_integral_i2_dipole, si_optics_radiation_integral_i4_dipole)
    si_optics_damping_partition_number_longitudinal_dipole = optics.Js(si_optics_damping_partition_number_horizontal_dipole, si_optics_damping_partition_number_vertical_dipole)
    si_optics_energy_loss_per_turn_dipole                  = optics.U0(si_beam_energy, si_optics_radiation_integral_i2_dipole)
    si_optics_radiation_power_dipole                       = optics.radiation_power(si_optics_energy_loss_per_turn_dipole, si_beam_current)
    si_optics_overvoltage_dipole                           = optics.overvoltage(si_rf_peak_voltage, si_optics_energy_loss_per_turn_dipole)
    si_optics_synchronous_phase_dipole                     = optics.sync_phase(si_optics_overvoltage_dipole)
    si_optics_linear_momentum_compaction_dipole            = optics.alpha1(si_optics_radiation_integral_i1_dipole, si_lattice_circumference)
    si_optics_linear_slip_phase_dipole                     = optics.slip_factor(si_optics_linear_momentum_compaction_dipole, si_beam_gamma_factor)
    si_optics_rf_energy_acceptance_dipole                  = optics.rf_energy_acceptance(si_optics_overvoltage_dipole, si_beam_energy, si_optics_energy_loss_per_turn_dipole, si_rf_harmonic_number, si_optics_linear_momentum_compaction_dipole)
    si_optics_natural_emittance_dipole                     = optics.natural_emittance(si_beam_gamma_factor, si_optics_damping_partition_number_horizontal_dipole, si_optics_radiation_integral_i2_dipole, si_optics_radiation_integral_i5_dipole)
    si_optics_natural_energy_spread_dipole                 = optics.energy_spread(si_beam_gamma_factor, si_optics_radiation_integral_i2_dipole, si_optics_radiation_integral_i3_dipole, si_optics_radiation_integral_i4_dipole)
    si_optics_natural_bunch_length_dipole                  = optics.bunch_length(si_optics_linear_slip_phase_dipole, si_optics_natural_energy_spread_dipole, si_optics_synchrotron_frequency)
    si_optics_natural_bunch_duration_dipole                = optics.bunch_duration(si_optics_natural_bunch_length_dipole, si_beam_beta_factor)    
    si_optics_radiation_damping_time_horizontal_dipole     = optics.damping_time(si_beam_energy, si_optics_radiation_integral_i2_dipole, si_optics_damping_partition_number_horizontal_dipole, si_lattice_circumference)                                                                        
    si_optics_radiation_damping_time_vertical_dipole       = optics.damping_time(si_beam_energy, si_optics_radiation_integral_i2_dipole, si_optics_damping_partition_number_vertical_dipole, si_lattice_circumference)                                                                        
    si_optics_radiation_damping_time_longitudinal_dipole   = optics.damping_time(si_beam_energy, si_optics_radiation_integral_i2_dipole, si_optics_damping_partition_number_longitudinal_dipole, si_lattice_circumference)                                                                        

    
    
    si_optics_damping_partition_number_vertical          = 1.0
    si_optics_damping_partition_number_horizontal        = optics.Jx(si_optics_radiation_integral_i2, si_optics_radiation_integral_i4)
    si_optics_damping_partition_number_longitudinal        = optics.Js(si_optics_damping_partition_number_horizontal, si_optics_damping_partition_number_vertical)
    si_optics_energy_loss_per_turn_id     = optics.U0(si_beam_energy, si_optics_radiation_integral_i2_id)
    si_optics_energy_loss_per_turn        = optics.U0(si_beam_energy, si_optics_radiation_integral_i2)
    si_optics_radiation_power             = optics.radiation_power(si_optics_energy_loss_per_turn, si_beam_current)
    si_optics_overvoltage                 = optics.overvoltage(si_rf_peak_voltage, si_optics_energy_loss_per_turn)
    si_optics_synchronous_phase           = optics.sync_phase(si_optics_overvoltage)
    si_optics_linear_momentum_compaction        = optics.alpha1(si_optics_radiation_integral_i1, si_lattice_circumference)
    si_optics_linear_slip_phase                 = optics.slip_factor(si_optics_linear_momentum_compaction, si_beam_gamma_factor)       
    si_optics_rf_energy_acceptance              = optics.rf_energy_acceptance(si_optics_overvoltage, si_beam_energy, si_optics_energy_loss_per_turn, si_rf_harmonic_number, si_optics_linear_momentum_compaction) 
    si_optics_natural_emittance                            = optics.natural_emittance(si_beam_gamma_factor, si_optics_damping_partition_number_horizontal, si_optics_radiation_integral_i2, si_optics_radiation_integral_i5)
    si_optics_natural_energy_spread              = optics.energy_spread(si_beam_gamma_factor, si_optics_radiation_integral_i2, si_optics_radiation_integral_i3, si_optics_radiation_integral_i4)
    si_optics_natural_bunch_length = optics.bunch_length(si_optics_linear_slip_phase, si_optics_natural_energy_spread, si_optics_synchrotron_frequency)
    si_optics_natural_bunch_duration                     = optics.bunch_duration(si_optics_natural_bunch_length, si_beam_beta_factor)
    si_optics_radiation_damping_time_horizontal          = optics.damping_time(si_beam_energy, si_optics_radiation_integral_i2, si_optics_damping_partition_number_horizontal, si_lattice_circumference) 
    si_optics_radiation_damping_time_vertical            = optics.damping_time(si_beam_energy, si_optics_radiation_integral_i2, si_optics_damping_partition_number_vertical, si_lattice_circumference)
    si_optics_radiation_damping_time_longitudinal        = optics.damping_time(si_beam_energy, si_optics_radiation_integral_i2, si_optics_damping_partition_number_longitudinal, si_lattice_circumference)

 
    si_errors_alignment_dipole     = 40  #[μm]
    si_errors_alignment_quadrupole = 40  #[μm]
    si_errors_alignment_sextupole  = 40  #[μm]
    si_errors_roll_dipole      = 0.2 #[mrad]
    si_errors_roll_quadrupole  = 0.2 #[mrad]
    si_errors_roll_sextupole   = 0.2 #[mrad]
    si_errors_excitation_dipole     = 0.05 #[%]
    si_errors_excitation_quadrupole = 0.05 #[%]
    si_errors_excitation_sextupole  = 0.05 #[%]
    ''' high frequency error tolerances '''
    si_errors_ripple_dipole        =  20   # [ppm]
    si_errors_ripple_quadrupole    =  20   # [ppm]    
    si_errors_ripple_sextupole     =  20   # [ppm]
    si_errors_vibration_dipole     =  6    # [nm]
    si_errors_vibration_quadrupole =  6    # [nm]
    si_errors_vibration_sextupole  =  6    # [nm]
    
    ''' insertion devices '''
    si_magnet_id_ivu19_name              = 'IVU19'
    si_magnet_id_ivu19_type              = 'IVU'
    si_magnet_id_ivu19_period            = 19.0   # [mm]
    si_magnet_id_ivu19_number_of_periods = 105
    si_magnet_id_ivu19_length            = 200.0  # [cm]
    si_magnet_id_ivu19_minimum_gap       = 4.5    # [mm]
    si_magnet_id_ivu19_maximum_horizontal_field = 0.0    # [T]
    si_magnet_id_ivu19_maximum_vertical_field   = 1.28   # [T]

    si_magnet_id_ivu25_name              = 'IVU25'
    si_magnet_id_ivu25_type              = 'IVU'
    si_magnet_id_ivu25_period            = 25.0   # [mm]
    si_magnet_id_ivu25_number_of_periods = 80
    si_magnet_id_ivu25_length            = 200.0  # [cm]
    si_magnet_id_ivu25_minimum_gap       = 8.0    # [mm]
    si_magnet_id_ivu25_maximum_horizontal_field = 0.0    # [T]
    si_magnet_id_ivu25_maximum_vertical_field   = 0.94   # [T]

    si_magnet_id_epu80_name              = 'EPU80'
    si_magnet_id_epu80_type              = 'EPU'
    si_magnet_id_epu80_period            = 80.0   # [mm]
    si_magnet_id_epu80_number_of_periods = 38
    si_magnet_id_epu80_length            = 270.0  # [cm]
    si_magnet_id_epu80_minimum_gap       = 16.0   # [mm]
    si_magnet_id_epu80_maximum_horizontal_field = 0.0    # [T]
    si_magnet_id_epu80_maximum_vertical_field   = 0.90   # [T]

    si_magnet_id_scw4t_name              = 'SCW4T'
    si_magnet_id_scw4t_type              = 'SCW'
    si_magnet_id_scw4t_period            = 60.0   # [mm]
    si_magnet_id_scw4t_number_of_periods = 16
    si_magnet_id_scw4t_length            = 100.0  # [cm]
    si_magnet_id_scw4t_minimum_gap       = 22.0   # [mm]
    si_magnet_id_scw4t_maximum_horizontal_field = 0.0    # [T]
    si_magnet_id_scw4t_maximum_vertical_field   = 4.00   # [T]

 
    ''' multipole errors for dipoles '''
    si_reference_position_for_multipole_contribution_for_dipoles = 11.7 # [mm]
    si_systematic_normal_6_pole_error_tolerance_for_dipoles  = -9.0e-5
    si_systematic_normal_8_pole_error_tolerance_for_dipoles  =  3.0e-5
    si_systematic_normal_10_pole_error_tolerance_for_dipoles =  1.0e-4
    si_systematic_normal_12_pole_error_tolerance_for_dipoles = -8.0e-5
    si_systematic_normal_14_pole_error_tolerance_for_dipoles =  6.0e-5
    si_random_normal_6_pole_error_tolerance_for_dipoles      =  4.0e-5
    si_random_normal_8_pole_error_tolerance_for_dipoles      =  4.0e-5
    si_random_normal_10_pole_error_tolerance_for_dipoles     =  4.0e-5
    si_random_normal_12_pole_error_tolerance_for_dipoles     =  4.0e-5
    si_random_normal_14_pole_error_tolerance_for_dipoles     =  4.0e-5
    si_random_normal_16_pole_error_tolerance_for_dipoles     =  4.0e-5
    si_random_normal_18_pole_error_tolerance_for_dipoles     =  4.0e-5
    si_random_skew_6_pole_error_tolerance_for_dipoles        =  1.0e-5
    si_random_skew_8_pole_error_tolerance_for_dipoles        =  1.0e-5
    si_random_skew_10_pole_error_tolerance_for_dipoles       =  1.0e-5
    si_random_skew_12_pole_error_tolerance_for_dipoles       =  1.0e-5
    si_random_skew_14_pole_error_tolerance_for_dipoles       =  1.0e-5
    si_random_skew_16_pole_error_tolerance_for_dipoles       =  1.0e-5
    si_random_skew_18_pole_error_tolerance_for_dipoles       =  1.0e-5
    
    ''' multipole errors for quadrupoles '''
    si_reference_position_for_multipole_contribution_for_quadrupoles = 11.7 # [mm]
    si_systematic_normal_8_pole_error_tolerance_for_quadrupoles  =  1.0e-5
    si_systematic_normal_12_pole_error_tolerance_for_quadrupoles = -3.0e-5
    si_systematic_normal_20_pole_error_tolerance_for_quadrupoles =  8.0e-5    
    si_random_normal_6_pole_error_tolerance_for_quadrupoles      =  4.0e-5
    si_random_normal_8_pole_error_tolerance_for_quadrupoles      =  4.0e-5
    si_random_normal_10_pole_error_tolerance_for_quadrupoles     =  4.0e-5
    si_random_normal_12_pole_error_tolerance_for_quadrupoles     =  4.0e-5
    si_random_normal_14_pole_error_tolerance_for_quadrupoles     =  4.0e-5
    si_random_normal_16_pole_error_tolerance_for_quadrupoles     =  4.0e-5
    si_random_normal_18_pole_error_tolerance_for_quadrupoles     =  4.0e-5
    si_random_normal_20_pole_error_tolerance_for_quadrupoles     =  4.0e-5
    si_random_skew_6_pole_error_tolerance_for_quadrupoles        =  1.0e-5
    si_random_skew_8_pole_error_tolerance_for_quadrupoles        =  1.0e-5
    si_random_skew_10_pole_error_tolerance_for_quadrupoles       =  1.0e-5
    si_random_skew_12_pole_error_tolerance_for_quadrupoles       =  1.0e-5
    si_random_skew_14_pole_error_tolerance_for_quadrupoles       =  1.0e-5
    si_random_skew_16_pole_error_tolerance_for_quadrupoles       =  1.0e-5
    si_random_skew_18_pole_error_tolerance_for_quadrupoles       =  1.0e-5
    si_random_skew_20_pole_error_tolerance_for_quadrupoles       =  1.0e-5
    
    ''' multipole errors for sextupoles '''
    si_reference_position_for_multipole_contribution_for_sextupoles = 11.7 # [mm]
    si_systematic_normal_18_pole_error_tolerance_for_sextupoles =  4.0e-6
    si_systematic_normal_30_pole_error_tolerance_for_sextupoles = -1.0e-7    
    si_random_normal_8_pole_error_tolerance_for_sextupoles      =  4.0e-5
    si_random_normal_10_pole_error_tolerance_for_sextupoles     =  4.0e-5
    si_random_normal_12_pole_error_tolerance_for_sextupoles     =  4.0e-5
    si_random_normal_14_pole_error_tolerance_for_sextupoles     =  4.0e-5
    si_random_normal_16_pole_error_tolerance_for_sextupoles     =  4.0e-5
    si_random_normal_18_pole_error_tolerance_for_sextupoles     =  4.0e-5
    si_random_normal_20_pole_error_tolerance_for_sextupoles     =  4.0e-5
    si_random_normal_22_pole_error_tolerance_for_sextupoles     =  4.0e-5
    si_random_normal_30_pole_error_tolerance_for_sextupoles     =  4.0e-5
    si_random_skew_8_pole_error_tolerance_for_sextupoles        =  1.0e-5
    si_random_skew_10_pole_error_tolerance_for_sextupoles       =  1.0e-5
    si_random_skew_12_pole_error_tolerance_for_sextupoles       =  1.0e-5
    si_random_skew_14_pole_error_tolerance_for_sextupoles       =  1.0e-5
    si_random_skew_16_pole_error_tolerance_for_sextupoles       =  1.0e-5
    si_random_skew_18_pole_error_tolerance_for_sextupoles       =  1.0e-5
    si_random_skew_20_pole_error_tolerance_for_sextupoles       =  1.0e-5
    si_random_skew_22_pole_error_tolerance_for_sextupoles       =  1.0e-5
    si_random_skew_30_pole_error_tolerance_for_sextupoles       =  1.0e-5

    



     

   
    si_magnet_id_ivu19_maximum_horizontal_deflection_parameter = optics.id_deflection_parameter(si_magnet_id_ivu19_maximum_vertical_field, si_magnet_id_ivu19_period)
    si_magnet_id_ivu19_maximum_vertical_deflection_parameter   = optics.id_deflection_parameter(si_magnet_id_ivu19_maximum_horizontal_field, si_magnet_id_ivu19_period)  
    si_magnet_id_ivu19_maximum_power     = optics.id_mean_power(si_beam_energy, si_beam_current, si_magnet_id_ivu19_period, si_magnet_id_ivu19_number_of_periods, si_magnet_id_ivu19_maximum_horizontal_deflection_parameter)
    
   
    si_magnet_id_ivu25_maximum_horizontal_deflection_parameter = optics.id_deflection_parameter(si_magnet_id_ivu25_maximum_vertical_field, si_magnet_id_ivu25_period)
    si_magnet_id_ivu25_maximum_vertical_deflection_parameter   = optics.id_deflection_parameter(si_magnet_id_ivu25_maximum_horizontal_field, si_magnet_id_ivu25_period)  
    si_magnet_id_ivu25_maximum_power     = optics.id_mean_power(si_beam_energy, si_beam_current, si_magnet_id_ivu25_period, si_magnet_id_ivu25_number_of_periods, si_magnet_id_ivu25_maximum_horizontal_deflection_parameter)
    
  


    si_magnet_id_epu80_maximum_horizontal_deflection_parameter = optics.id_deflection_parameter(si_magnet_id_epu80_maximum_vertical_field, si_magnet_id_epu80_period)
    si_magnet_id_epu80_maximum_vertical_deflection_parameter   = optics.id_deflection_parameter(si_magnet_id_epu80_maximum_horizontal_field, si_magnet_id_epu80_period)  
    si_magnet_id_epu80_maximum_power     = optics.id_mean_power(si_beam_energy, si_beam_current, si_magnet_id_epu80_period, si_magnet_id_epu80_number_of_periods, si_magnet_id_epu80_maximum_horizontal_deflection_parameter)
  
   
    si_magnet_id_scw4t_maximum_horizontal_deflection_parameter = optics.id_deflection_parameter(si_magnet_id_scw4t_maximum_vertical_field, si_magnet_id_scw4t_period)
    si_magnet_id_scw4t_maximum_vertical_deflection_parameter   = optics.id_deflection_parameter(si_magnet_id_scw4t_maximum_horizontal_field, si_magnet_id_scw4t_period)  
    si_magnet_id_scw4t_maximum_power     = optics.id_mean_power(si_beam_energy, si_beam_current, si_magnet_id_scw4t_period, si_magnet_id_scw4t_number_of_periods, si_magnet_id_scw4t_maximum_horizontal_deflection_parameter)
    
  
    

    '''Booster parameters
       =================='''
    
    bo_beam_current           = 2.0 # [mA]
    bo_lattice_version        = 'V900' 
    bo_circumference          = 496.8 # [m]
    bo_lattice_symmetry       = 10
    bo_harmonic_number        = 828
    bo_optics_mode            = 'M0'
    bo_rf_cavity_peak_voltage = 0.95 # [MV]
    bo_cycling_frequency      = 2.0 # [Hz]

    bo_dipole_deflection_angle    = 7.2 # [°]
    bo_hardedge_length_of_dipoles = 1.152 # [m]
    bo_dipole_bending_radius      = bo_hardedge_length_of_dipoles / math.radians(bo_dipole_deflection_angle)


    '''injection'''
    bo_injection_beam_energy        = 0.150 # [GeV]
    bo_injection_beam_gamma_factor  = optics.gamma(bo_injection_beam_energy)
    bo_injection_beam_beta_factor   = optics.beta(bo_injection_beam_gamma_factor)
    bo_injection_beam_velocity      = optics.velocity(bo_injection_beam_beta_factor)
    bo_injection_beam_magnetic_rigidity = optics.brho(
        bo_injection_beam_energy,
        bo_injection_beam_beta_factor)
    bo_injection_dipole_magnetic_field = bo_injection_beam_magnetic_rigidity / bo_dipole_bending_radius
    bo_injection_synchrotron_tune                        = 0.009655851289284

    '''extraction'''
    bo_extraction_beam_energy       = 3.0; # [GeV]
    bo_extraction_beam_gamma_factor = optics.gamma(bo_extraction_beam_energy)
    bo_extraction_beam_beta_factor  = optics.beta(bo_extraction_beam_gamma_factor)
    bo_extraction_beam_velocity     = optics.velocity(bo_extraction_beam_beta_factor)
    bo_extraction_beam_magnetic_rigidity = optics.brho(
        bo_extraction_beam_energy,
        bo_extraction_beam_beta_factor)
    bo_extraction_synchrotron_tune  = 0.004419254284301

    bo_extraction_dipole_magnetic_field = bo_extraction_beam_magnetic_rigidity / bo_dipole_bending_radius
    bo_extraction_revolution_period = optics.revolution_period(bo_circumference, bo_extraction_beam_velocity)
    bo_extraction_revolution_frequency = optics.revolution_frequency(bo_extraction_revolution_period)
    bo_extraction_radiation_integral_I1 =  0.357375949836236 # [m]
    bo_extraction_radiation_integral_I2 =  0.632474441350948 # [1/m]
    bo_extraction_radiation_integral_I3 =  0.065162582244920 # [1/m^2]
    bo_extraction_radiation_integral_I4 = -0.139031129276436 # [1/m]
    bo_extraction_radiation_integral_I5 =  0.000202970389114 # [1/m]
    bo_extraction_radiation_integral_I6 =  0.008112617986838 # [1/m]
    bo_extraction_energy_loss_per_turn = optics.U0(
        bo_extraction_beam_energy, bo_extraction_radiation_integral_I2)
    bo_extraction_linear_momentum_compaction = optics.alpha1(bo_extraction_radiation_integral_I1,bo_circumference)
    bo_extraction_horizontal_damping_partition_number = optics.Jx(bo_extraction_radiation_integral_I2,bo_extraction_radiation_integral_I4)
    bo_extraction_vertical_damping_partition_number = 1.0
    bo_extraction_longitudinal_damping_partition_number = optics.Js(bo_extraction_horizontal_damping_partition_number,bo_extraction_vertical_damping_partition_number)
    bo_extraction_natural_emittance = optics.natural_emittance(
        bo_extraction_beam_gamma_factor,
        bo_extraction_horizontal_damping_partition_number,
        bo_extraction_radiation_integral_I2,
        bo_extraction_radiation_integral_I5)
    bo_extraction_natural_energy_spread = optics.energy_spread(
        bo_extraction_beam_gamma_factor,
        bo_extraction_radiation_integral_I2,
        bo_extraction_radiation_integral_I3,
        bo_extraction_radiation_integral_I4)
    bo_extraction_horizontal_radiation_damping_time = optics.damping_time(
        bo_extraction_beam_energy,
        bo_extraction_radiation_integral_I2,
        bo_extraction_horizontal_damping_partition_number,
        bo_circumference)
    bo_extraction_vertical_radiation_damping_time = optics.damping_time(
        bo_extraction_beam_energy,
        bo_extraction_radiation_integral_I2,
        bo_extraction_vertical_damping_partition_number,
        bo_circumference)
    bo_extraction_longitudinal_radiation_damping_time = optics.damping_time(
        bo_extraction_beam_energy,
        bo_extraction_radiation_integral_I2,
        bo_extraction_longitudinal_damping_partition_number,
        bo_circumference)
    bo_extraction_rf_frequency = optics.rf_frequency(bo_extraction_revolution_frequency, bo_harmonic_number)
    bo_extraction_rf_wavelength = optics.rf_wavelength(bo_extraction_rf_frequency)
    bo_extraction_radiation_power = optics.radiation_power(bo_extraction_energy_loss_per_turn, bo_beam_current)
    bo_extraction_overvoltage = optics.overvoltage(bo_rf_cavity_peak_voltage, bo_extraction_energy_loss_per_turn)
    bo_extraction_synchronous_phase = optics.sync_phase(bo_extraction_overvoltage)
    bo_extraction_synchrotron_frequency = optics.frequency_from_tune(bo_extraction_revolution_frequency, bo_extraction_synchrotron_tune)
    bo_extraction_rf_energy_acceptance = optics.rf_energy_acceptance(
        bo_extraction_overvoltage, bo_extraction_beam_energy,
        bo_extraction_energy_loss_per_turn, bo_harmonic_number,
        bo_extraction_linear_momentum_compaction)
    bo_extraction_slip_factor = optics.slip_factor(bo_extraction_linear_momentum_compaction, bo_extraction_beam_gamma_factor)
    bo_extraction_natural_bunch_length = optics.bunch_length(
        bo_extraction_slip_factor,
        bo_extraction_natural_energy_spread,
        bo_extraction_synchrotron_frequency)
    bo_extraction_natural_bunch_duration = optics.bunch_duration(bo_extraction_natural_bunch_length, bo_extraction_beam_beta_factor)

    ''' dipoles '''
    bo_number_of_dipoles           = 50
    bo_hardedge_sagitta_of_dipoles = 1000 * bo_dipole_bending_radius * (1.0 - math.cos(0.5*math.radians(bo_dipole_deflection_angle))) #[mm]
    bo_dipole_quadrupole_integrated_strength = -0.247428712258696 # [1/m^1] (derived from model6 fieldmap analysis)
    bo_dipole_sextupole_integrated_strength  = -2.578215176201312 # [1/m^2] (derived from model6 fieldmap analysis)
    bo_dipole_quadrupole_strength = bo_dipole_quadrupole_integrated_strength / (bo_hardedge_length_of_dipoles) # [1/m^2]
    bo_dipole_sextupole_strength  = bo_dipole_sextupole_integrated_strength  / (bo_hardedge_length_of_dipoles) # [1/m^3]
    bo_injection_dipole_integrated_field = bo_injection_beam_magnetic_rigidity * (math.pi/180.0) * bo_dipole_deflection_angle # [T.m]
    bo_injection_dipole_quadrupole_integrated_gradient = - bo_dipole_quadrupole_integrated_strength * bo_injection_beam_magnetic_rigidity # [T]
    bo_injection_dipole_sextupole_integrated_gradient  = - bo_dipole_sextupole_integrated_strength * bo_injection_beam_magnetic_rigidity  # [T/m]
    bo_injection_dipole_quadrupole_gradient = bo_injection_dipole_quadrupole_integrated_gradient / bo_hardedge_length_of_dipoles # [T/m]
    bo_injection_dipole_sextupole_gradient  = bo_injection_dipole_sextupole_integrated_gradient / bo_hardedge_length_of_dipoles # [T/m^2]
    bo_extraction_dipole_integrated_field = bo_extraction_beam_magnetic_rigidity * (math.pi/180.0) * bo_dipole_deflection_angle # [T.m]    
    bo_extraction_dipole_quadrupole_integrated_gradient = - bo_dipole_quadrupole_integrated_strength * bo_extraction_beam_magnetic_rigidity # [T]
    bo_extraction_dipole_sextupole_integrated_gradient  = - bo_dipole_sextupole_integrated_strength * bo_extraction_beam_magnetic_rigidity  # [T/m]
    bo_extraction_dipole_quadrupole_gradient = bo_extraction_dipole_quadrupole_integrated_gradient / bo_hardedge_length_of_dipoles # [T/m]
    bo_extraction_dipole_sextupole_gradient  = bo_extraction_dipole_sextupole_integrated_gradient / bo_hardedge_length_of_dipoles # [T/m^2]

    bo_dipoles_alignment_error_tolerance    = 100 # [μm]
    bo_dipoles_rotation_error_tolerance     = 0.5 # [mrad]
    bo_dipoles_excitation_error_tolerance   = 0.1 # [%]
    bo_reference_position_for_multipole_contribution_for_dipoles = 17.5 # [mm]
    
    bo_systematic_normal_8_pole_error_tolerance_for_dipoles  =  4.0e-4 # segmented model of the dipole shows much
    bo_systematic_normal_10_pole_error_tolerance_for_dipoles = -3.6e-4 # lower multipole errors. Nevertheless these values are
    bo_systematic_normal_12_pole_error_tolerance_for_dipoles =  2.7e-4 # kept as spec for real measurements.
    bo_systematic_normal_14_pole_error_tolerance_for_dipoles = -1.3e-4 #
    bo_random_normal_6_pole_error_tolerance_for_dipoles      =  5.5e-4
    bo_random_normal_8_pole_error_tolerance_for_dipoles      =  4.0e-4
    bo_random_normal_10_pole_error_tolerance_for_dipoles     =  4.0e-4
    bo_random_normal_12_pole_error_tolerance_for_dipoles     =  4.0e-4
    bo_random_normal_14_pole_error_tolerance_for_dipoles     =  4.0e-4
    bo_random_normal_16_pole_error_tolerance_for_dipoles     =  4.0e-4
    bo_random_normal_18_pole_error_tolerance_for_dipoles     =  4.0e-4
    bo_random_skew_6_pole_error_tolerance_for_dipoles        =  1.0e-4
    bo_random_skew_8_pole_error_tolerance_for_dipoles        =  1.0e-4
    bo_random_skew_10_pole_error_tolerance_for_dipoles       =  1.0e-4
    bo_random_skew_12_pole_error_tolerance_for_dipoles       =  1.0e-4
    bo_random_skew_14_pole_error_tolerance_for_dipoles       =  1.0e-4
    bo_random_skew_16_pole_error_tolerance_for_dipoles       =  1.0e-4
    bo_random_skew_18_pole_error_tolerance_for_dipoles       =  1.0e-4

    ''' quadrupoles '''
    bo_number_of_QF_quadrupoles = 50
    bo_number_of_QD_quadrupoles = 25
    bo_hardedge_length_of_short_quadrupoles = 0.2 # [m]
    bo_hardedge_length_of_long_quadrupoles  = 0.2 # [m]
    bo_hardedge_length_of_QF_quadrupoles = bo_hardedge_length_of_long_quadrupoles # [m]
    bo_hardedge_length_of_QD_quadrupoles = bo_hardedge_length_of_short_quadrupoles # [m]
    
    bo_QF_quadrupole_maximum_strength                     = 2.025 # [1/m^2] 
    bo_injection_QF_quadrupole_maximum_gradient           = bo_QF_quadrupole_maximum_strength *  bo_injection_beam_magnetic_rigidity # [T/m]
    bo_extraction_QF_quadrupole_maximum_gradient          = bo_QF_quadrupole_maximum_strength *  bo_extraction_beam_magnetic_rigidity # [T/m]

    bo_QD_quadrupole_maximum_strength                     = 0.250 # [1/m^2] 
    bo_injection_QD_quadrupole_maximum_gradient           = bo_QD_quadrupole_maximum_strength *  bo_injection_beam_magnetic_rigidity # [T/m]
    bo_extraction_QD_quadrupole_maximum_gradient          = bo_QD_quadrupole_maximum_strength *  bo_extraction_beam_magnetic_rigidity # [T/m]

    #bo_injection_QF_quadrupole_maximum_gradient           = 1.0132009391643900 # [T/m]
    #bo_extraction_QF_quadrupole_maximum_gradient          = 20.2640187832877   # [T/m]
    #bo_injection_QD_quadrupole_maximum_absolute_gradient  = 0.1250865356993070 # [T/m]    
    #bo_extraction_QD_quadrupole_maximum_absolute_gradient = 2.5017307139861400 # [T/m]

    bo_quadrupoles_alignment_error_tolerance  = 100 # [μm]    
    bo_quadrupoles_rotation_error_tolerance   = 0.5 # [mrad]
    bo_quadrupoles_excitation_error_tolerance = 0.2 # [%]
    
    bo_reference_position_for_multipole_contribution_for_quadrupoles = 17.5 # [mm]
    bo_systematic_normal_12_pole_error_tolerance_for_quadrupoles = -1.00e-3
    bo_systematic_normal_20_pole_error_tolerance_for_quadrupoles = +1.10e-3
    bo_systematic_normal_28_pole_error_tolerance_for_quadrupoles = +0.08e-3
    bo_random_normal_6_pole_error_tolerance_for_quadrupoles  = 7.0e-4
    bo_random_normal_8_pole_error_tolerance_for_quadrupoles  = 4.0e-4
    bo_random_normal_10_pole_error_tolerance_for_quadrupoles = 4.0e-4
    bo_random_normal_12_pole_error_tolerance_for_quadrupoles = 4.0e-4
    bo_random_normal_14_pole_error_tolerance_for_quadrupoles = 4.0e-4
    bo_random_normal_16_pole_error_tolerance_for_quadrupoles = 4.0e-4
    bo_random_normal_18_pole_error_tolerance_for_quadrupoles = 4.0e-4
    bo_random_normal_20_pole_error_tolerance_for_quadrupoles = 4.0e-4
    bo_random_skew_6_pole_error_tolerance_for_quadrupoles    =10.0e-4
    bo_random_skew_8_pole_error_tolerance_for_quadrupoles    = 5.0e-4
    bo_random_skew_10_pole_error_tolerance_for_quadrupoles   = 1.0e-4
    bo_random_skew_12_pole_error_tolerance_for_quadrupoles   = 1.0e-4
    bo_random_skew_14_pole_error_tolerance_for_quadrupoles   = 1.0e-4
    bo_random_skew_16_pole_error_tolerance_for_quadrupoles   = 1.0e-4
    bo_random_skew_18_pole_error_tolerance_for_quadrupoles   = 1.0e-4
    bo_random_skew_20_pole_error_tolerance_for_quadrupoles   = 1.0e-4

    '''sextupoles'''
    bo_number_of_SF_sextupoles = 25
    bo_number_of_SD_sextupoles = 10
    bo_hardedge_length_of_SF_sextupoles = 0.2 # [m]
    bo_hardedge_length_of_SD_sextupoles = 0.2 # [m]


    bo_SF_sextupole_maximum_strength                     = 10.000 # [1/m^3] 
    bo_injection_SF_sextupole_maximum_gradient           = bo_SF_sextupole_maximum_strength *  bo_injection_beam_magnetic_rigidity # [T/m^2]
    bo_extraction_SF_sextupole_maximum_gradient          = bo_SF_sextupole_maximum_strength *  bo_extraction_beam_magnetic_rigidity # [T/m^2]

    bo_SD_sextupole_maximum_strength                    = 10.000 # [1/m^3] 
    bo_injection_SD_sextupole_maximum_gradient          = bo_SD_sextupole_maximum_strength *  bo_injection_beam_magnetic_rigidity # [T/m^2]
    bo_extraction_SD_sextupole_maximum_gradient         = bo_SD_sextupole_maximum_strength *  bo_extraction_beam_magnetic_rigidity # [T/m^2]

    bo_sextupoles_alignment_error_tolerance = 100 # [μm]
    bo_sextupoles_rotation_error_tolerance = 0.5 # [mrad]
    bo_sextupoles_excitation_error_tolerance = 0.2 # [%]
    bo_reference_position_for_multipole_contribution_for_sextupoles = 17.5 # [mm]
    bo_systematic_normal_18_pole_error_tolerance_for_sextupoles = -2.4e-2
    bo_systematic_normal_30_pole_error_tolerance_for_sextupoles = -1.7e-2
    bo_random_normal_8_pole_error_tolerance_for_sextupoles  = 4.0e-4
    bo_random_normal_10_pole_error_tolerance_for_sextupoles = 4.0e-4
    bo_random_normal_12_pole_error_tolerance_for_sextupoles = 4.0e-4
    bo_random_normal_14_pole_error_tolerance_for_sextupoles = 4.0e-4
    bo_random_normal_16_pole_error_tolerance_for_sextupoles = 4.0e-4
    bo_random_normal_18_pole_error_tolerance_for_sextupoles = 4.0e-5
    bo_random_normal_20_pole_error_tolerance_for_sextupoles = 4.0e-5
    bo_random_skew_8_pole_error_tolerance_for_sextupoles    = 1.0e-4
    bo_random_skew_10_pole_error_tolerance_for_sextupoles   = 1.0e-4
    bo_random_skew_12_pole_error_tolerance_for_sextupoles   = 1.0e-4
    bo_random_skew_14_pole_error_tolerance_for_sextupoles   = 1.0e-4
    bo_random_skew_16_pole_error_tolerance_for_sextupoles   = 1.0e-4
    bo_random_skew_18_pole_error_tolerance_for_sextupoles   = 1.0e-4
    bo_random_skew_20_pole_error_tolerance_for_sextupoles   = 1.0e-4

    '''bpms'''
    bo_beam_position_monitors_alignment_error_tolerance = 500 # [um]
        
    '''orbit correction system'''
    bo_number_of_beam_position_monitors = 50
    bo_number_of_horizontal_dipole_correctors = 25
    bo_number_of_vertical_dipole_correctors = 25
    bo_horizontal_dipole_corrector_maximum_strength = 0.35 # [mrad]
    bo_vertical_dipole_corrector_maximum_strength = 0.35 # [mrad]

    '''optics'''
    bo_horizontal_betatron_tune = 19.20475
    bo_vertical_betatron_tune   = 7.30744
    bo_horizontal_natural_chromaticity = -35.447586554937516
    bo_vertical_natural_chromaticity   =  12.502204960185281


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
    tb_beam_gamma_factor      = optics.gamma(1.0e-3*tb_beam_energy)
    tb_beam_beta_factor       = optics.beta(tb_beam_gamma_factor)
    tb_beam_velocity          = optics.velocity(tb_beam_beta_factor)
    tb_beam_magnetic_rigidity = optics.brho(1.0e-3*tb_beam_energy, tb_beam_beta_factor)

    tb_total_length = 21.2475 # [m]
    tb_number_of_dipoles = 4
    tb_number_of_quadrupoles = 13
    tb_number_of_septa = 1
    tb_maximum_quadrupole_gradient = 10.0 # [T/m]

    tb_arc_length_of_dipole = 0.300 # [m]
    tb_arc_length_of_septum = 0.5000 # [m]

    tb_dipole_deflection_angle = 15.0 # [°]
    tb_septum_deflection_angle = 21.75 # [°]

    tb_dipole_bending_radius = tb_arc_length_of_dipole / math.radians(tb_dipole_deflection_angle)
    tb_septum_bending_radius = tb_arc_length_of_septum / math.radians(tb_septum_deflection_angle)

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
    ts_beam_gamma_factor      = optics.gamma(ts_beam_energy)
    ts_beam_beta_factor       = optics.beta(ts_beam_gamma_factor)
    ts_beam_velocity          = optics.velocity(ts_beam_beta_factor)
    ts_beam_magnetic_rigidity = optics.brho(ts_beam_energy, ts_beam_beta_factor)

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

    ts_dipole_bending_radius = ts_hardedge_length_of_dipoles / math.radians(ts_dipole_deflection_angle)
    ts_extraction_septum_bending_radius = ts_hardedge_length_of_extraction_septum / math.radians(ts_extraction_septum_deflection_angle)
    ts_thick_injection_septum_bending_radius = ts_hardedge_length_of_thick_injection_septum / math.radians(ts_thick_injection_septum_deflection_angle)
    ts_thin_injection_septum_bending_radius = ts_hardedge_length_of_thin_injection_septum / math.radians(ts_thin_injection_septum_deflection_angle)

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



