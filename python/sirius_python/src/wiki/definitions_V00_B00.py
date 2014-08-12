'''
Lattice/Mode V00_B00
====================
Date: 2014-08-12
New naming convention
This lattice/optics mode corresponds to the previous V500_AC10.5
'''

import optics

class ParameterDefinitions(object):

    '''Storage ring parameters'''

    sr_beam_energy            = 3.0       # [GeV]
    sr_beam_gamma_factor      = optics.gamma(sr_beam_energy)
    sr_beam_beta_factor       = optics.beta(sr_beam_gamma_factor)
    sr_beam_velocity          = optics.velocity(sr_beam_beta_factor)
    sr_beam_magnetic_rigidity = optics.brho(sr_beam_energy, sr_beam_beta_factor)
    
    sr_beam_current                      = 350.0 #[mA]
    sr_lattice_version                   = 'V00' 
    sr_lattice_circumference             = 518.396 #[m]
    sr_lattice_symmetry                  = 10
    sr_length_of_long_straight_sections  = 7.0 #[m]
    sr_length_of_short_straight_sections = 6.0 #[m]
    sr_harmonic_number                   = 864
    sr_total_RF_voltage                  = 2.7 #[MV]
    
    sr_revolution_period = optics.revolution_period(
        sr_lattice_circumference, sr_beam_velocity)

    sr_revolution_frequency = optics.revolution_frequency(
        sr_revolution_period)

    sr_rf_frequency = optics.rf_frequency(
        sr_revolution_frequency, sr_harmonic_number)
    
    sr_number_of_electrons = optics.number_of_electrons(
        sr_beam_current, sr_revolution_period)

    sr_number_of_long_straight_sections  = sr_lattice_symmetry
    sr_number_of_short_straight_sections = sr_lattice_symmetry
    sr_number_of_B1_dipoles              = 4 * sr_lattice_symmetry
    sr_number_of_B2_dipoles              = 4 * sr_lattice_symmetry
    sr_number_of_B3_dipoles              = 4 * sr_lattice_symmetry
    sr_number_of_BC_dipoles              = 2 * sr_lattice_symmetry
    
    sr_hardedge_length_of_B1_dipoles =  0.828080 #[m] 
    sr_hardedge_length_of_B2_dipoles =  1.228262 #[m]
    sr_hardedge_length_of_B3_dipoles =  0.428011 #[m]
    sr_hardedge_length_of_BC_dipoles =  0.125394 #[m]
    sr_dipole_low_magnetic_field     =  0.583502298783241 #[T]
    sr_dipole_high_magnetic_field    =  1.949975668803368 #[T]

    sr_dipole_low_magnetic_field_bending_radius = optics.rho(
        sr_beam_magnetic_rigidity, sr_dipole_low_magnetic_field)

    sr_dipole_high_magnetic_field_bending_radius = optics.rho(
        sr_beam_magnetic_rigidity, sr_dipole_high_magnetic_field)

    sr_dipole_low_magnetic_field_critical_energy = optics.critical_energy(
        sr_beam_gamma_factor, sr_dipole_low_magnetic_field_bending_radius)

    sr_dipole_high_magnetic_field_critical_energy = optics.critical_energy(
        sr_beam_gamma_factor, sr_dipole_high_magnetic_field_bending_radius)

    sr_radiation_integral_I1_from_dipoles =  0.090315779996644     #[m]
    sr_radiation_integral_I2_from_dipoles =  0.433104068989975     #[1/m]
    sr_radiation_integral_I3_from_dipoles =  0.038257877157466     #[1/m^2]
    sr_radiation_integral_I4_from_dipoles = -0.137100015107741     #[1/m]
    sr_radiation_integral_I5_from_dipoles =  1.218542781664562e-05 #[1/m]
    sr_radiation_integral_I6_from_dipoles =  0.019201555654789     #[1/m]
    sr_radiation_integral_I1_from_IDs =  0.0 #[m]
    sr_radiation_integral_I2_from_IDs =  0.0 #[1/m]
    sr_radiation_integral_I3_from_IDs =  0.0 #[1/m^2]
    sr_radiation_integral_I4_from_IDs =  0.0 #[1/m]
    sr_radiation_integral_I5_from_IDs =  0.0 #[1/m]
    sr_radiation_integral_I6_from_IDs =  0.0 #[1/m] 

    sr_radiation_integral_I1 = (sr_radiation_integral_I1_from_dipoles +
        sr_radiation_integral_I1_from_IDs) #[m]

    sr_radiation_integral_I2 = (sr_radiation_integral_I2_from_dipoles +
        sr_radiation_integral_I2_from_IDs) #[m]

    sr_radiation_integral_I3 = (sr_radiation_integral_I3_from_dipoles +
        sr_radiation_integral_I3_from_IDs) #[m]

    sr_radiation_integral_I4 = (sr_radiation_integral_I4_from_dipoles +
        sr_radiation_integral_I4_from_IDs) #[m]

    sr_radiation_integral_I5 = (sr_radiation_integral_I5_from_dipoles +
        sr_radiation_integral_I5_from_IDs) #[m]

    sr_radiation_integral_I6 = (sr_radiation_integral_I6_from_dipoles +
        sr_radiation_integral_I6_from_IDs) #[m]
    
    sr_optics_mode = 'B00'
    sr_horizontal_betatron_tune = 46.179867828110417
    sr_vertical_betatron_tune = 14.149994739104255
    sr_synchrotron_tune = 0.004421565111775

    sr_horizontal_natural_chromaticity = -113.1198708037573
    sr_vertical_natural_chromaticity = -80.5026603600822
    sr_horizontal_chromaticity = 0
    sr_vertical_chromaticity = 0


    sr_horizontal_betatron_frequency = optics.frequency_from_tune(
        sr_revolution_frequency, sr_horizontal_betatron_tune)

    sr_vertical_betatron_frequency = optics.frequency_from_tune(
        sr_revolution_frequency, sr_vertical_betatron_tune)

    sr_synchrotron_frequency = optics.frequency_from_tune(
        sr_revolution_frequency, sr_synchrotron_tune)
    
    sr_energy_loss_per_turn_from_dipoles = optics.U0(
        sr_beam_energy, sr_radiation_integral_I2_from_dipoles)

    sr_overvoltage_from_dipoles = optics.overvoltage(
        sr_total_RF_voltage, sr_energy_loss_per_turn_from_dipoles)

    sr_synchronous_phase_from_dipoles = optics.sync_phase(
        sr_overvoltage_from_dipoles)

    sr_linear_momentum_compaction_from_dipoles = optics.alpha1(
        sr_radiation_integral_I1_from_dipoles,
        sr_lattice_circumference)

    sr_rf_energy_acceptance_from_dipoles = optics.rf_energy_acceptance(
        sr_overvoltage_from_dipoles, sr_beam_energy,
        sr_energy_loss_per_turn_from_dipoles, sr_harmonic_number,
        sr_linear_momentum_compaction_from_dipoles)

    sr_horizontal_damping_partition_number_from_dipoles = optics.Jx(
        sr_radiation_integral_I2_from_dipoles,
        sr_radiation_integral_I4_from_dipoles)

    sr_vertical_damping_partition_number_from_dipoles = 1.0

    sr_longitudinal_damping_partition_number_from_dipoles = optics.Js(
        sr_horizontal_damping_partition_number_from_dipoles,
        sr_vertical_damping_partition_number_from_dipoles)

    sr_natural_emittance_from_dipoles = optics.natural_emittance(
        sr_beam_gamma_factor,
        sr_horizontal_damping_partition_number_from_dipoles,
        sr_radiation_integral_I2_from_dipoles,
        sr_radiation_integral_I5_from_dipoles)

    sr_natural_energy_spread_from_dipoles = optics.energy_spread(
        sr_beam_gamma_factor,
        sr_radiation_integral_I2_from_dipoles,
        sr_radiation_integral_I3_from_dipoles,
        sr_radiation_integral_I4_from_dipoles)

    sr_energy_loss_per_turn_from_IDs = optics.U0(
        sr_beam_energy, sr_radiation_integral_I2_from_IDs)

    sr_energy_loss_per_turn = optics.U0(
        sr_beam_energy, sr_radiation_integral_I2)

    sr_overvoltage = optics.overvoltage(
        sr_total_RF_voltage, sr_energy_loss_per_turn)

    sr_synchronous_phase = optics.sync_phase(
        sr_overvoltage)

    sr_linear_momentum_compaction = optics.alpha1(
        sr_radiation_integral_I1,
        sr_lattice_circumference)

    sr_rf_energy_acceptance = optics.rf_energy_acceptance(
        sr_overvoltage, sr_beam_energy,
        sr_energy_loss_per_turn, sr_harmonic_number,
        sr_linear_momentum_compaction) 

    sr_horizontal_damping_partition_number = optics.Jx(
        sr_radiation_integral_I2, sr_radiation_integral_I4)

    sr_vertical_damping_partition_number = 1.0

    sr_longitudinal_damping_partition_number = optics.Js(
        sr_horizontal_damping_partition_number,
        sr_vertical_damping_partition_number)

    sr_natural_emittance = optics.natural_emittance(
        sr_beam_gamma_factor, sr_horizontal_damping_partition_number,
        sr_radiation_integral_I2, sr_radiation_integral_I5)

    sr_natural_energy_spread = optics.energy_spread(
        sr_beam_gamma_factor, sr_radiation_integral_I2,
        sr_radiation_integral_I3, sr_radiation_integral_I4)

    '''Booster parameters'''
    
    bo_beam_current          = 2.0 # [mA]
    bo_lattice_version       = '' 
    bo_circumference         = 496.8 # [m]
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
        bo_circumference, bo_extraction_beam_velocity)

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
        bo_circumference)
    
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
        bo_circumference)

    bo_extraction_vertical_damping_time = optics.damping_time(
        bo_extraction_beam_energy,
        bo_extraction_radiation_integral_I2,
        bo_extraction_vertical_damping_partition_number,
        bo_circumference)

    bo_extraction_longitudinal_damping_time = optics.damping_time(
        bo_extraction_beam_energy,
        bo_extraction_radiation_integral_I2,
        bo_extraction_longitudinal_damping_partition_number,
        bo_circumference)

    bo_extraction_rf_frequency = optics.rf_frequency(
        bo_extraction_revolution_frequency, bo_harmonic_number)

    bo_extraction_radiation_power_from_dipoles = optics.radiation_power_from_dipoles(
        bo_extraction_energy_loss_per_turn_from_dipoles, bo_beam_current)
