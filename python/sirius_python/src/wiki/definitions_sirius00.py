#!/usr/bin/python

import optics


class ParameterDefinitions(object):

    # Storage ring parameters

    si_beam_energy            = 3.0       # [GeV]
    si_beam_gamma_factor      = optics.gamma(si_beam_energy)
    si_beam_beta_factor       = optics.beta(si_beam_gamma_factor)
    si_beam_velocity          = optics.velocity(si_beam_beta_factor)
    si_beam_magnetic_rigidity = optics.brho(si_beam_energy, si_beam_beta_factor)
    
    si_beam_current                      = 350.0 #[mA]
    si_lattice_version                   = 'V500' 
    si_lattice_circumference             = 518.396 #[m]
    si_lattice_symmetry                  = 10
    si_length_of_long_straight_sections  = 7.0 #[m]
    si_length_of_short_straight_sections = 6.0 #[m]
    si_harmonic_number                   = 864
    si_total_RF_voltage                  = 2.7 #[MV]
    
    si_revolution_period = optics.revolution_period(
        si_lattice_circumference, si_beam_velocity)

    si_revolution_frequency = optics.revolution_frequency(
        si_revolution_period)

    si_rf_frequency = optics.rf_frequency(
        si_revolution_frequency, si_harmonic_number)
    
    si_number_of_electrons = optics.number_of_electrons(
        si_beam_current, si_revolution_period)

    si_number_of_long_straight_sections  = si_lattice_symmetry
    si_number_of_short_straight_sections = si_lattice_symmetry
    si_number_of_B1_dipoles              = 4 * si_lattice_symmetry
    si_number_of_B2_dipoles              = 4 * si_lattice_symmetry
    si_number_of_B3_dipoles              = 4 * si_lattice_symmetry
    si_number_of_BC_dipoles              = 2 * si_lattice_symmetry
    
    si_hardedge_length_of_B1_dipoles =  0.828080 #[m] 
    si_hardedge_length_of_B2_dipoles =  1.228262 #[m]
    si_hardedge_length_of_B3_dipoles =  0.428011 #[m]
    si_hardedge_length_of_BC_dipoles =  0.125394 #[m]
    si_dipole_low_magnetic_field     =  0.583502298783241 #[T]
    si_dipole_high_magnetic_field    =  1.949975668803368 #[T]

    si_dipole_low_magnetic_field_bending_radius = optics.rho(
        si_beam_magnetic_rigidity, si_dipole_low_magnetic_field)

    si_dipole_high_magnetic_field_bending_radius = optics.rho(
        si_beam_magnetic_rigidity, si_dipole_high_magnetic_field)

    si_dipole_low_magnetic_field_critical_energy = optics.critical_energy(
        si_beam_gamma_factor, si_dipole_low_magnetic_field_bending_radius)

    si_dipole_high_magnetic_field_critical_energy = optics.critical_energy(
        si_beam_gamma_factor, si_dipole_high_magnetic_field_bending_radius)

    si_radiation_integral_I1_from_dipoles =  0.090315779996644     #[m]
    si_radiation_integral_I2_from_dipoles =  0.433104068989975     #[1/m]
    si_radiation_integral_I3_from_dipoles =  0.038257877157466     #[1/m^2]
    si_radiation_integral_I4_from_dipoles = -0.137100015107741     #[1/m]
    si_radiation_integral_I5_from_dipoles =  1.218542781664562e-05 #[1/m]
    si_radiation_integral_I6_from_dipoles =  0.019201555654789     #[1/m]
    si_radiation_integral_I1_from_IDs =  0.0 #[m]
    si_radiation_integral_I2_from_IDs =  0.0 #[1/m]
    si_radiation_integral_I3_from_IDs =  0.0 #[1/m^2]
    si_radiation_integral_I4_from_IDs =  0.0 #[1/m]
    si_radiation_integral_I5_from_IDs =  0.0 #[1/m]
    si_radiation_integral_I6_from_IDs =  0.0 #[1/m] 

    si_radiation_integral_I1 = (si_radiation_integral_I1_from_dipoles +
        si_radiation_integral_I1_from_IDs) #[m]

    si_radiation_integral_I2 = (si_radiation_integral_I2_from_dipoles +
        si_radiation_integral_I2_from_IDs) #[m]

    si_radiation_integral_I3 = (si_radiation_integral_I3_from_dipoles +
        si_radiation_integral_I3_from_IDs) #[m]

    si_radiation_integral_I4 = (si_radiation_integral_I4_from_dipoles +
        si_radiation_integral_I4_from_IDs) #[m]

    si_radiation_integral_I5 = (si_radiation_integral_I5_from_dipoles +
        si_radiation_integral_I5_from_IDs) #[m]

    si_radiation_integral_I6 = (si_radiation_integral_I6_from_dipoles +
        si_radiation_integral_I6_from_IDs) #[m]
    
    si_optics_mode = 'AC10.5'
    si_horizontal_betatron_tune = 46.179867828110417
    si_vertical_betatron_tune = 14.149994739104255
    si_synchrotron_tune = 0.004421565111775

    si_horizontal_natural_chromaticity = -113.1198708037573
    si_vertical_natural_chromaticity = -80.5026603600822
    si_horizontal_chromaticity = 0
    si_vertical_chromaticity = 0


    si_horizontal_betatron_frequency = optics.frequency_from_tune(
        si_revolution_frequency, si_horizontal_betatron_tune)

    si_vertical_betatron_frequency = optics.frequency_from_tune(
        si_revolution_frequency, si_vertical_betatron_tune)

    si_synchrotron_frequency = optics.frequency_from_tune(
        si_revolution_frequency, si_synchrotron_tune)
    
    si_energy_loss_per_turn_from_dipoles = optics.U0(
        si_beam_energy, si_radiation_integral_I2_from_dipoles)

    si_overvoltage_from_dipoles = optics.overvoltage(
        si_total_RF_voltage, si_energy_loss_per_turn_from_dipoles)

    si_synchronous_phase_from_dipoles = optics.sync_phase(
        si_overvoltage_from_dipoles)

    si_linear_momentum_compaction_from_dipoles = optics.alpha1(
        si_radiation_integral_I1_from_dipoles,
        si_lattice_circumference)

    si_rf_energy_acceptance_from_dipoles = optics.rf_energy_acceptance(
        si_overvoltage_from_dipoles, si_beam_energy,
        si_energy_loss_per_turn_from_dipoles, si_harmonic_number,
        si_linear_momentum_compaction_from_dipoles)

    si_horizontal_damping_partition_number_from_dipoles = optics.Jx(
        si_radiation_integral_I2_from_dipoles,
        si_radiation_integral_I4_from_dipoles)

    si_vertical_damping_partition_number_from_dipoles = 1.0

    si_longitudinal_damping_partition_number_from_dipoles = optics.Js(
        si_horizontal_damping_partition_number_from_dipoles,
        si_vertical_damping_partition_number_from_dipoles)

    si_natural_emittance_from_dipoles = optics.natural_emittance(
        si_beam_gamma_factor,
        si_horizontal_damping_partition_number_from_dipoles,
        si_radiation_integral_I2_from_dipoles,
        si_radiation_integral_I5_from_dipoles)

    si_natural_energy_spread_from_dipoles = optics.energy_spread(
        si_beam_gamma_factor,
        si_radiation_integral_I2_from_dipoles,
        si_radiation_integral_I3_from_dipoles,
        si_radiation_integral_I4_from_dipoles)

    si_energy_loss_per_turn_from_IDs = optics.U0(
        si_beam_energy, si_radiation_integral_I2_from_IDs)

    si_energy_loss_per_turn = optics.U0(
        si_beam_energy, si_radiation_integral_I2)

    si_overvoltage = optics.overvoltage(
        si_total_RF_voltage, si_energy_loss_per_turn)

    si_synchronous_phase = optics.sync_phase(
        si_overvoltage)

    si_linear_momentum_compaction = optics.alpha1(
        si_radiation_integral_I1,
        si_lattice_circumference)

    si_rf_energy_acceptance = optics.rf_energy_acceptance(
        si_overvoltage, si_beam_energy,
        si_energy_loss_per_turn, si_harmonic_number,
        si_linear_momentum_compaction) 

    si_horizontal_damping_partition_number = optics.Jx(
        si_radiation_integral_I2, si_radiation_integral_I4)

    si_vertical_damping_partition_number = 1.0

    si_longitudinal_damping_partition_number = optics.Js(
        si_horizontal_damping_partition_number,
        si_vertical_damping_partition_number)

    si_natural_emittance = optics.natural_emittance(
        si_beam_gamma_factor, si_horizontal_damping_partition_number,
        si_radiation_integral_I2, si_radiation_integral_I5)

    si_natural_energy_spread = optics.energy_spread(
        si_beam_gamma_factor, si_radiation_integral_I2,
        si_radiation_integral_I3, si_radiation_integral_I4)

    # Booster parameters
    
    bo_beam_current          = 2.0 # [mA]
    bo_lattice_version       = '' 
    bo_lattice_circumference = 496.8 # [m]
    bo_lattice_symmetry      = 10
    bo_harmonic_number       = 828
    bo_optics_mode = ''

    bo_number_of_dipoles = 50
    bo_number_of_QF_quadrupoles = 50
    bo_number_of_QD_quadrupoles = 25
    bo_number_of_SF_sextupoles = 25
    bo_number_of_SD_sextupoles = 10

    bo_hardedge_length_of_dipoles =  1.152 # [m]
    bo_hardedge_length_of_QF_quadrupoles = 0.3 # [m]
    bo_hardedge_length_of_QD_quadrupoles = 0.2 # [m]
    bo_hardedge_length_of_SF_sextupoles = 0.2 # [m]
    bo_hardedge_length_of_SD_sextupoles = 0.2 # [m]

    bo_maximum_integrated_sextupole = 20.0138457118891 # B''L/2 [T/m]

    bo_horizontal_betatron_tune = 19.204749345767866
    bo_vertical_betatron_tune   = 7.307442329080478
    bo_synchrotron_tune         = 0.004419249840938

    bo_horizontal_natural_chromaticity = -33.704073487683672
    bo_vertical_natural_chromaticity   = -13.950562838260794

    bo_cycling_frequency = 2.0 # [Hz]

    bo_injection_beam_energy        = 0.150 # [GeV]
    bo_injection_beam_gamma_factor  = optics.gamma(bo_injection_beam_energy)
    bo_injection_beam_beta_factor   = optics.beta(bo_injection_beam_gamma_factor)
    bo_injection_beam_velocity      = optics.velocity(bo_injection_beam_beta_factor)

    bo_injection_dipole_magnetic_field = 0.0546 # [T]
    bo_injection_QF_quadrupole_maximum_gradient = 1.0132009391643900 # [T/m]
    bo_injection_QD_quadrupole_maximum_absolute_gradient = 0.1250865356993070 # [T/m]

    bo_injection_beam_magnetic_rigidity = optics.brho(
        bo_injection_beam_energy,
        bo_injection_beam_beta_factor)

    bo_injection_dipole_bending_radius = optics.rho(
        bo_injection_beam_magnetic_rigidity, bo_injection_dipole_magnetic_field)

    bo_extraction_beam_energy       = 3.0; # [GeV]
    bo_extraction_beam_gamma_factor = optics.gamma(bo_extraction_beam_energy)
    bo_extraction_beam_beta_factor  = optics.beta(bo_extraction_beam_gamma_factor)
    bo_extraction_beam_velocity     = optics.velocity(bo_extraction_beam_beta_factor)

    bo_extraction_dipole_magnetic_field = 1.092 # [T]
    bo_extraction_QF_quadrupole_maximum_gradient = 20.2640187832877 # [T/m]
    bo_extraction_QD_quadrupole_maximum_absolute_gradient = 2.5017307139861400 # [T/m]

    bo_extraction_beam_magnetic_rigidity = optics.brho(
        bo_extraction_beam_energy,
        bo_extraction_beam_beta_factor)

    bo_extraction_dipole_bending_radius = optics.rho(
        bo_extraction_beam_magnetic_rigidity, bo_extraction_dipole_magnetic_field)

    bo_extraction_revolution_period = optics.revolution_period(
        bo_lattice_circumference, bo_extraction_beam_velocity)

    bo_extraction_revolution_frequency = optics.revolution_frequency(
        bo_extraction_revolution_period)
    
    bo_extraction_radiation_integral_I1 =  0.357376004142324 # [m]
    bo_extraction_radiation_integral_I2 =  0.632474441350948 # [1/m]
    bo_extraction_radiation_integral_I3 =  0.065162582244920 # [1/m^2]
    bo_extraction_radiation_integral_I4 = -0.139031150720390 # [1/m]
    bo_extraction_radiation_integral_I5 =  2.029704170935785e-04 # [1/m]
    bo_extraction_radiation_integral_I6 =  0.008112620479157 # [1/m]

    bo_extraction_energy_loss_per_turn_from_dipoles = optics.U0(
        bo_extraction_beam_energy, bo_extraction_radiation_integral_I2)

    bo_extraction_linear_momentum_compaction = optics.alpha1(
        bo_extraction_radiation_integral_I1,
        bo_lattice_circumference)
    
    bo_extraction_horizontal_damping_partition_number = optics.Jx(
        bo_extraction_radiation_integral_I2,
        bo_extraction_radiation_integral_I4)

    bo_extraction_vertical_damping_partition_number = 1.0

    bo_extraction_longitudinal_damping_partition_number = optics.Js(
        bo_extraction_horizontal_damping_partition_number,
        bo_extraction_vertical_damping_partition_number)

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

    bo_extraction_horizontal_damping_time = optics.damping_time(
        bo_extraction_beam_energy,
        bo_extraction_radiation_integral_I2,
        bo_extraction_horizontal_damping_partition_number,
        bo_lattice_circumference)

    bo_extraction_vertical_damping_time = optics.damping_time(
        bo_extraction_beam_energy,
        bo_extraction_radiation_integral_I2,
        bo_extraction_vertical_damping_partition_number,
        bo_lattice_circumference)

    bo_extraction_longitudinal_damping_time = optics.damping_time(
        bo_extraction_beam_energy,
        bo_extraction_radiation_integral_I2,
        bo_extraction_longitudinal_damping_partition_number,
        bo_lattice_circumference)

    bo_extraction_rf_frequency = optics.rf_frequency(
        bo_extraction_revolution_frequency, bo_harmonic_number)

    #bo_extraction_radiation_power_from_dipoles = optics.radiation_power_from_dipoles(
    #    bo_extraction_beam_energy,
    #    bo_extraction_dipole_bending_radius,
    #    bo_beam_current)
