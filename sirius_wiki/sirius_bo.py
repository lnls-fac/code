#!/usr/bin/python
# -*- coding: utf-8 -*-

from parameter import Parameter
#from definitions import ParameterDefinitions as Prms


''' PRIMITIVE PARAMETERS '''

bo_lattice_version                        = 'V901'
bo_lattice_type                           = 'FODO'
bo_lattice_circumference                  = 496.8 #[m]
bo_lattice_symmetry                       = 50

bo_ramp_cycling_frequency                 = 2.0   # [Hz]

bo_beam_injection_energy                  = 0.150 # [GeV]
bo_beam_injection_current                 = 2.0   #[mA]
bo_beam_extraction_energy                 = 3.0   # [GeV]
bo_beam_extraction_current                = 2.0   #[m]

bo_rf_harmonic_number                     = 828
bo_rf_injection_peak_voltage              = 1.1 #[MV]
bo_rf_extraction_peak_voltage             = 1.1 #[MV]

bo_magnet_dipole_number                         = 50
bo_magnet_dipole_deflection_angle               = 360.0/bo_magnet_dipole_number #[deg]
bo_magnet_dipole_hardedge_length                = 1.152 #[m]
bo_magnet_dipole_integrated_quadrupole_strength = -0.2484 #[1/m]
bo_magnet_dipole_integrated_sextupole_strength  = -2.2685*1.152 #[1/m²]

bo_optics_default_mode                    = 'M0'
bo_optics_tune_horizontal                 =  19.20433
bo_optics_tune_vertical                   =  7.31417
bo_optics_tune_synchrotron_injection      =  0.00966
bo_optics_tune_synchrotron_extraction     =  0.00442
bo_optics_chromaticity_horizontal         = +0.64073
bo_optics_chromaticity_vertical           = +0.54758
bo_optics_natural_chromaticity_horizontal = -35.43326
bo_optics_natural_chromaticity_vertical   = +12.28104
bo_optics_radiation_integral_i1 =  0.357376723856626 # [m]
bo_optics_radiation_integral_i2 =  0.632467570445733 # [1/m]
bo_optics_radiation_integral_i3 =  0.065161622362345 # [1/m^2]
bo_optics_radiation_integral_i4 = -0.138994900353256 # [1/m]
bo_optics_radiation_integral_i5 =  0.000202971145667 # [1/m]
bo_optics_radiation_integral_i6 =  0.008106555542826 # [1/m]



"""



    bo_optics_beam_size_horizontal_long_straight_section  = 7.009486798878925E+01 #[um]
    bo_optics_beam_size_horizontal_short_straight_section = 2.084762622184360E+01 #[um]
    bo_optics_beam_size_horizontal_dipole_bc              = 9.948943931676647E+00 #[um]
    bo_optics_beam_size_vertical_long_straight_section    = 3.214983743415169E+00 #[um]
    bo_optics_beam_size_vertical_short_straight_section   = 1.939167731203255E+00 #[um]
    bo_optics_beam_size_vertical_dipole_bc                = 3.996725872734588E+00 #[um]
    bo_optics_beam_divergence_horizontal_long_straight_section  = 3.915259575507898E+00 #[urad]
    bo_optics_beam_divergence_horizontal_short_straight_section = 1.316409860763686E+01 #[urad]
    bo_optics_beam_divergence_horizontal_dipole_bc              = 2.942299673538725E+01 #[urad]
    bo_optics_beam_divergence_vertical_long_straight_section    = 8.536265817057522E-01 #[urad]
    bo_optics_beam_divergence_vertical_short_straight_section   = 1.415244044631019E+00 #[urad]
    bo_optics_beam_divergence_vertical_dipole_bc                = 6.866611249310436E-01 #[urad]


    bo_extraction_vertical_damping_partition_number = 1.0

    bo_extraction_energy_loss_per_turn = optics.U0(bo_extraction_beam_energy, bo_extraction_radiation_integral_I2)
    bo_extraction_linear_momentum_compaction = optics.alpha1(bo_extraction_radiation_integral_I1,bo_circumference)
    bo_extraction_horizontal_damping_partition_number = optics.Jx(bo_extraction_radiation_integral_I2,bo_extraction_radiation_integral_I4)

    bo_extraction_longitudinal_damping_partition_number = optics.Js(bo_extraction_horizontal_damping_partition_number,bo_extraction_vertical_damping_partition_number)
    bo_extraction_natural_emittance = optics.natural_emittance(bo_extraction_beam_gamma_factor,bo_extraction_horizontal_damping_partition_number,bo_extraction_radiation_integral_I2,bo_extraction_radiation_integral_I5)
    bo_extraction_natural_energy_spread = optics.energy_spread(bo_extraction_beam_gamma_factor,bo_extraction_radiation_integral_I2,bo_extraction_radiation_integral_I3,bo_extraction_radiation_integral_I4)
    bo_extraction_horizontal_radiation_damping_time = optics.damping_time(bo_extraction_beam_energy,bo_extraction_radiation_integral_I2,bo_extraction_horizontal_damping_partition_number,bo_circumference)
    bo_extraction_vertical_radiation_damping_time = optics.damping_time(bo_extraction_beam_energy,bo_extraction_radiation_integral_I2,bo_extraction_vertical_damping_partition_number,bo_circumference)
    bo_extraction_longitudinal_radiation_damping_time = optics.damping_time(bo_extraction_beam_energy,bo_extraction_radiation_integral_I2,bo_extraction_longitudinal_damping_partition_number,bo_circumference)
    bo_extraction_rf_frequency = optics.rf_frequency(bo_extraction_revolution_frequency, bo_harmonic_number)
    bo_extraction_rf_wavelength = optics.rf_wavelength(bo_extraction_rf_frequency)
    bo_extraction_radiation_power = optics.radiation_power(bo_extraction_energy_loss_per_turn, bo_beam_current)
    bo_extraction_overvoltage = optics.overvoltage(bo_rf_cavity_peak_voltage, bo_extraction_energy_loss_per_turn)
    bo_extraction_synchronous_phase = optics.sync_phase(bo_extraction_overvoltage)
    bo_extraction_synchrotron_frequency = optics.frequency_from_tune(bo_extraction_revolution_frequency, bo_extraction_synchrotron_tune)
    bo_extraction_rf_energy_acceptance = optics.rf_energy_acceptance(bo_extraction_overvoltage, bo_extraction_beam_energy,bo_extraction_energy_loss_per_turn, bo_harmonic_number,bo_extraction_linear_momentum_compaction)
    bo_extraction_slip_factor = optics.slip_factor(bo_extraction_linear_momentum_compaction, bo_extraction_beam_gamma_factor)
    bo_extraction_natural_bunch_length = optics.bunch_length(bo_extraction_slip_factor,bo_extraction_natural_energy_spread,bo_extraction_synchrotron_frequency)
    bo_extraction_natural_bunch_duration = optics.bunch_duration(bo_extraction_natural_bunch_length, bo_extraction_beam_beta_factor)

    ''' dipoles '''

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


"""



parameter_list = [

  Parameter(name='BO lattice version', group='FAC', is_derived=False, value=bo_lattice_version, symbol='', units='', deps=[], obs=[], ),
  Parameter(name='BO lattice type', group='FAC', is_derived=False, value=bo_lattice_type, symbol='', units='', deps=[], obs=[], ),
  Parameter(name='BO lattice circumference', group='GIA', is_derived=False, value=bo_lattice_circumference, symbol=r'<math>C</math>', units='m', deps=[], obs=[], ),
  Parameter(name='BO lattice symmetry',      group='FAC', is_derived=False, value=bo_lattice_symmetry, symbol=r'<math>N_\text{SUPERCELLS}</math>', units='', deps=[], obs=[], ),

  Parameter(name='BO ramp cycling frequency',        group='FAC', is_derived=False, value=bo_ramp_cycling_frequency, symbol=r'<math>f_\text{cycle}</math>', units='Hz', deps=[], obs=[], ),

  Parameter(name='BO beam injection energy',            group='GIA', is_derived=False,   value=bo_beam_injection_energy, symbol=r'<math>E_\text{inj}</math>', units='GeV', obs=[], ),
  Parameter(name='BO beam injection current',           group='FAC', is_derived=False,   value=bo_beam_injection_current, symbol=r'<math>I_\text{inj}</math>', units='mA', obs=[], ),
  Parameter(name='BO beam injection gamma factor',      group='FAC', is_derived=True,    value='gamma("BO beam injection energy")', symbol=r'<math>\gamma_\text{inj}</math>', units='', obs=[r'<math>\gamma_\text{inj} \equiv \frac{E_\text{inj}}{E_0}</math>'], ),
  Parameter(name='BO beam injection beta factor',       group='FAC', is_derived=True,    value='beta("BO beam injection gamma factor")', symbol=r'<math>\beta_\text{inj}</math>', units='', obs=[r'<math>\beta_\text{inj} \equiv \sqrt{1 - \frac{1}{\gamma^2_\text{inj}}}</math>'], ),
  Parameter(name='BO beam injection velocity',          group='FAC', is_derived=True,    value='velocity("BO beam injection beta factor")', symbol=r'<math>v_\text{inj}</math>', units='m/s', obs=[r'<math>v_\text{inj} \equiv \beta_\text{inj} c</math>']),
  Parameter(name='BO beam injection magnetic rigidity', group='FAC', is_derived=True,    value='brho("BO beam injection energy", "BO beam injection beta factor")', symbol=r'<math>(B\rho)_\text{inj}</math>', units=unicode('T·m', encoding='utf-8'), deps=['BO beam energy'], obs=[r'<math>(B\rho) = \frac{p}{ec} = \frac{E}{ec^2}</math>'], ),
  Parameter(name='BO beam injection revolution period',    group='FAC', is_derived=True, value='revolution_period("BO lattice circumference", "BO beam injection velocity")', symbol=r'<math>T_\text{inj,rev}</math>', units=unicode('μs',encoding='utf-8'), obs=[r'<math>T_\text{inj,rev} \equiv \frac{C}{v_\text{inj}}</math>'], ),
  Parameter(name='BO beam injection revolution frequency', group='FAC', is_derived=True, value='1.0/"BO beam injection revolution period"', symbol=r'<math>f_\text{inj,rev}</math>', units='MHz', obs=[r'<math>f_\text{inj,rev} \equiv \frac{1}{T_\text{inj,rev}}</math>'], ),
  Parameter(name='BO beam injection electron number',      group='FAC', is_derived=True, value='number_of_electrons("BO beam injection current", "BO beam injection revolution period")', symbol=r'<math>N_\text{inj}</math>', units='', obs=[r'<math>N_\text{inj} \equiv \frac{I_\text{inj} T_\text{inj,rev}}{|e|}</math>'], ),

  Parameter(name='BO beam extraction energy',            group='GIA', is_derived=False,   value=bo_beam_extraction_energy, symbol=r'<math>E_\text{ext}</math>', units='GeV', obs=[], ),
  Parameter(name='BO beam extraction current',           group='FAC', is_derived=False,   value=bo_beam_extraction_current, symbol=r'<math>I_\text{ext}</math>', units='mA', obs=[], ),
  Parameter(name='BO beam extraction gamma factor',      group='FAC', is_derived=True,    value='gamma("BO beam extraction energy")', symbol=r'<math>\gamma_\text{ext}</math>', units='', obs=[r'<math>\gamma_\text{ext} \equiv \frac{E_\text{ext}}{E_0}</math>'], ),
  Parameter(name='BO beam extraction beta factor',       group='FAC', is_derived=True,    value='beta("BO beam extraction gamma factor")', symbol=r'<math>\beta_\text{ext}</math>', units='', obs=[r'<math>\beta_\text{ext} \equiv \sqrt{1 - \frac{1}{\gamma^2_\text{ext}}}</math>'], ),
  Parameter(name='BO beam extraction velocity',          group='FAC', is_derived=True,    value='velocity("BO beam extraction beta factor")', symbol=r'<math>v_\text{ext}</math>', units='m/s', obs=[r'<math>v_\text{ext} \equiv \beta_\text{ext} c</math>']),
  Parameter(name='BO beam extraction magnetic rigidity', group='FAC', is_derived=True,    value='brho("BO beam extraction energy", "BO beam extraction beta factor")', symbol=r'<math>(B\rho)_\text{ext}</math>', units=unicode('T·m', encoding='utf-8'), deps=['BO beam energy'], obs=[r'<math>(B\rho) = \frac{p}{ec} = \frac{E}{ec^2}</math>'], ),
  Parameter(name='BO beam extraction revolution period',    group='FAC', is_derived=True, value='revolution_period("BO lattice circumference", "BO beam extraction velocity")', symbol=r'<math>T_\text{ext,rev}</math>', units=unicode('μs',encoding='utf-8'), obs=[r'<math>T_\text{ext,rev} \equiv \frac{C}{v_\text{ext}}</math>'], ),
  Parameter(name='BO beam extraction revolution frequency', group='FAC', is_derived=True, value='1.0/"BO beam extraction revolution period"', symbol=r'<math>f_\text{ext,rev}</math>', units='MHz', obs=[r'<math>f_\text{ext,rev} \equiv \frac{1}{T_\text{ext,rev}}</math>'], ),
  Parameter(name='BO beam extraction electron number',      group='FAC', is_derived=True, value='number_of_electrons("BO beam extraction current", "BO beam extraction revolution period")', symbol=r'<math>N_\text{ext}</math>', units='', obs=[r'<math>N_\text{ext} \equiv \frac{I_\text{ext} T_\text{ext,rev}}{|e|}</math>'], ),

  Parameter(name='BO rf harmonic number',            group='FAC', is_derived=False, value=bo_rf_harmonic_number, symbol=r'<math>h</math>', units='', deps=[], obs=[], ),
  Parameter(name='BO rf injection frequency',        group='FAC', is_derived=True,  value='rf_frequency("BO beam injection revolution frequency","BO rf harmonic number")', symbol=r'<math>f_\text{inj,rf}</math>', units='MHz', obs=[r'<math>f_\text{inj,rf} \equiv h f_\text{inj,rev}</math>'], ),
  Parameter(name='BO rf injection peak voltage',     group='FAC', is_derived=False, value=bo_rf_injection_peak_voltage, symbol=r'<math>V_\text{inj,rf}</math>', units='MV', deps=[], obs=[], ),
  Parameter(name='BO rf extraction frequency',       group='FAC', is_derived=True,  value='rf_frequency("BO beam extraction revolution frequency","BO rf harmonic number")', symbol=r'<math>f_\text{ext,rf}</math>', units='MHz', obs=[r'<math>f_\text{ext,rf} \equiv h f_\text{ext,rev}</math>'], ),
  Parameter(name='BO rf extraction peak voltage',    group='FAC', is_derived=False, value=bo_rf_extraction_peak_voltage, symbol=r'<math>V_\text{inj,rf}</math>', units='MV', deps=[], obs=[], ),

  Parameter(name='BO magnet dipole number',                         group='FAC', is_derived=False, value=bo_magnet_dipole_number, symbol=r'<math>N_\text{dip}</math>', units='', deps=[], obs=[], ),
  Parameter(name='BO magnet dipole deflection angle',               group='FAC', is_derived=False, value=bo_magnet_dipole_deflection_angle, symbol=r'<math>\theta_\text{dip}</math>', units=unicode('°',encoding='utf-8'), deps=[], obs=[], ),
  Parameter(name='BO magnet dipole hardedge length',                group='FAC', is_derived=False, value=bo_magnet_dipole_hardedge_length, symbol=r'<math>L_\text{dip}</math>', units='m', deps=[], obs=[], ),
  Parameter(name='BO magnet dipole integrated quadrupole strength', group='FAC', is_derived=False, value=bo_magnet_dipole_integrated_quadrupole_strength, symbol=r'<math>(LK)_\text{dip}</math>', units='m<sup>-1</sup>', deps=[], obs=[],),
  Parameter(name='BO magnet dipole integrated sextupole strength',  group='FAC', is_derived=False, value=bo_magnet_dipole_integrated_sextupole_strength, symbol=r'<math>(LS)_\text{dip}</math>', units='m<sup>-2</sup>', deps=[], obs=[],),

  Parameter(name='BO magnet dipole hardedge bending radius',  group='FAC', is_derived=True, value='"BO magnet dipole hardedge length"/deg2rad("BO magnet dipole deflection angle")', symbol=r'<math>\rho</math>', units='m', obs=[r'<math>\rho = \frac{L_\text{dip}}{\theta_\text{dip}}</math>'], ),
  Parameter(name='BO magnet dipole hardedge sagitta',         group='FAC', is_derived=True, value='1000 * "BO magnet dipole hardedge bending radius" * (1.0 - cos(0.5*deg2rad("BO magnet dipole deflection angle")))', symbol=r'<math>S_\text{inj,sag}</math>', units='mm', obs=[r'<math>S_\text{sag} = \rho (1 - \cos \theta / 2)</math>'],),
  Parameter(name='BO magnet dipole hardedge quadrupole strength',   group='FAC', is_derived=True,  value='"BO magnet dipole integrated quadrupole strength"/"BO magnet dipole hardedge length"', symbol=r'<math>K_\text{dip}</math>', units='m<sup>-2</sup>', obs=[r'<math>K_\text{dip} \equiv \frac{(LK)_\text{dip}}{L_\text{dip}}</math>'],),
  Parameter(name='BO magnet dipole hardedge sextupole strength',    group='FAC', is_derived=True,  value='"BO magnet dipole integrated sextupole strength"/"BO magnet dipole hardedge length"', symbol=r'<math>S_\text{dip}</math>', units='m<sup>-3</sup>', obs=[r'<math>S_\text{dip} \equiv \frac{(LS)_\text{dip}}{L_\text{dip}}</math>'],),

  Parameter(name='BO magnet dipole hardedge magnetic field injection',  group='FAC', is_derived=True, value='"BO beam injection magnetic rigidity" / "BO magnet dipole hardedge bending radius"', symbol=r'<math>B_\text{inj}</math>', units='T', obs=[r'<math>B_\text{inj} = \frac{(B\rho)}{\rho}</math>'], ),
  Parameter(name='BO magnet dipole hardedge critical energy injection', group='FAC', is_derived=True, value='critical_energy("BO beam injection gamma factor", "BO magnet dipole hardedge bending radius")', symbol=r'<math>\epsilon_\text{c,inj}</math>', units='keV', obs=[r'<math>\epsilon_\text{c,inj} = \frac{3}{2} \hbar c \frac{\gamma_\text{inj}^3}{\rho}</math>'], ),
  Parameter(name='BO magnet dipole hardedge magnetic field extraction',  group='FAC', is_derived=True, value='"BO beam extraction magnetic rigidity" / "BO magnet dipole hardedge bending radius"', symbol=r'<math>B_\text{ext}</math>', units='T', obs=[r'<math>B_\text{ext} = \frac{(B\rho)}{\rho}</math>'], ),
  Parameter(name='BO magnet dipole hardedge critical energy extraction', group='FAC', is_derived=True, value='critical_energy("BO beam extraction gamma factor", "BO magnet dipole hardedge bending radius")', symbol=r'<math>\epsilon_\text{c,ext}</math>', units='keV', obs=[r'<math>\epsilon_\text{c,ext} = \frac{3}{2} \hbar c \frac{\gamma_\text{ext}^3}{\rho}</math>'], ),

  Parameter(name='BO optics default mode',  group='FAC', is_derived=False, value=bo_optics_default_mode, symbol='', units='', obs=[], ),
  Parameter(name='BO optics tune horizontal',  group='FAC', is_derived=False, value=bo_optics_tune_horizontal, symbol=r'<math>\nu_x</math>', units='', deps=['BO optics default mode'], obs=[], ),
  Parameter(name='BO optics tune vertical',  group='FAC', is_derived=False, value=bo_optics_tune_vertical, symbol=r'<math>\nu_y</math>', units='', deps=['BO optics default mode'], obs=[], ),
  Parameter(name='BO optics tune synchrotron injection',   group='FAC', is_derived=False, value=bo_optics_tune_synchrotron_injection, symbol=r'<math>\nu_\text{s, inj}</math>', units='', deps=['BO optics default mode'], obs=[], ),
  Parameter(name='BO optics tune synchrotron extraction',  group='FAC', is_derived=False, value=bo_optics_tune_synchrotron_extraction, symbol=r'<math>\nu_\text{s, ext}</math>', units='', deps=['BO optics default mode'], obs=[], ),
  Parameter(name='BO optics chromaticity horizontal',  group='FAC', is_derived=False, value=bo_optics_chromaticity_horizontal, symbol=r'<math>\xi_x</math>', units='', deps=['BO optics default mode'], obs=[], ),
  Parameter(name='BO optics chromaticity vertical',    group='FAC', is_derived=False, value=bo_optics_chromaticity_vertical,   symbol=r'<math>\xi_y</math>', units='', deps=['BO optics default mode'], obs=[], ),
  Parameter(name='BO optics natural chromaticity horizontal',  group='FAC', is_derived=False, value=bo_optics_natural_chromaticity_horizontal, symbol=r'<math>\xi_{0,x}</math>', units='', deps=['BO optics default mode'], obs=[], ),
  Parameter(name='BO optics natural chromaticity vertical',    group='FAC', is_derived=False, value=bo_optics_natural_chromaticity_vertical,   symbol=r'<math>\xi_{0,y}</math>', units='', deps=['BO optics default mode'], obs=[], ),

  Parameter(name='BO optics injection betatron frequency horizontal',  group='FAC', is_derived=True, value='frequency_from_tune("BO beam injection revolution frequency",  "BO optics tune horizontal")', symbol=r'<math>f_\text{x, inj}</math>', units='kHz', obs=[r'<math>f_\text{x, inj} \equiv f_\text{inj,rev} \text{frac}(\nu_x)</math>'], ),
  Parameter(name='BO optics extraction betatron frequency horizontal', group='FAC', is_derived=True, value='frequency_from_tune("BO beam extraction revolution frequency", "BO optics tune horizontal")', symbol=r'<math>f_\text{x, ext}</math>', units='kHz', obs=[r'<math>f_\text{x, ext} \equiv f_\text{inj,rev} \text{frac}(\nu_x)</math>'], ),
  Parameter(name='BO optics injection betatron frequency vertical',  group='FAC', is_derived=True, value='frequency_from_tune("BO beam injection revolution frequency",  "BO optics tune vertical")', symbol=r'<math>f_\text{y, inj}</math>', units='kHz', obs=[r'<math>f_\text{y, inj} \equiv f_\text{inj,rev} \text{frac}(\nu_y)</math>'], ),
  Parameter(name='BO optics extraction betatron frequency vertical', group='FAC', is_derived=True, value='frequency_from_tune("BO beam extraction revolution frequency", "BO optics tune vertical")', symbol=r'<math>f_\text{y, ext}</math>', units='kHz', obs=[r'<math>f_\text{y, ext} \equiv f_\text{inj,rev} \text{frac}(\nu_y)</math>'], ),

]
