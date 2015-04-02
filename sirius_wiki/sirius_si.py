#!/usr/bin/python
# -*- coding: utf-8 -*-

from parameter import Parameter
from definitions import ParameterDefinitions as Prms


'''Storage ring parameters
   ======================='''

si_lattice_version                        = 'V03'
si_lattice_type                           = '5BA'
si_lattice_circumference                  = 518.396   #[m]
si_lattice_symmetry                       = 10
si_lattice_long_straight_section_length   = 7.0       #[m]
si_lattice_short_straight_section_length  = 6.0       #[m]

si_beam_energy                            = 3.0   # [GeV]
si_beam_current                           = 350.0 #[mA]

si_rf_harmonic_number                     = 864
si_rf_peak_voltage                        = 2.7       #[MV]

si_magnet_dipole_b1_deflection_angle         = 2.76654  #[deg]
si_magnet_dipole_b1_hardedge_length          = 0.828080 #[m]
si_magnet_dipole_b2_deflection_angle         = 4.10351  #[deg]
si_magnet_dipole_b2_hardedge_length          = 1.228262 #[m]
si_magnet_dipole_b3_deflection_angle         = 1.42995  #[deg]
si_magnet_dipole_b3_hardedge_length          = 0.428011 #[m]
si_magnet_dipole_bc_hardedge_length          = 0.125394 #[m]
si_magnet_dipole_bc_deflection_angle         = 1.40000  #[deg]

si_magnet_sextupole_sda_number = 20
si_magnet_sextupole_sda_hardedge_length = 0.15 #[m]
si_magnet_sextupole_sda_integrated_sextupolar_field_maximum = 360 #[T/m]
si_magnet_sextupole_sfa_number = 20
si_magnet_sextupole_sfa_hardedge_length = 0.15 #[m]
si_magnet_sextupole_sfa_integrated_sextupolar_field_maximum = 360 #[T/m]
si_magnet_sextupole_sdb_number = 20
si_magnet_sextupole_sdb_hardedge_length = 0.15 #[m]
si_magnet_sextupole_sdb_integrated_sextupolar_field_maximum = 360 #[T/m]
si_magnet_sextupole_sfb_number = 20
si_magnet_sextupole_sfb_hardedge_length = 0.15 #[m]
si_magnet_sextupole_sfb_integrated_sextupolar_field_maximum = 360 #[T/m]
si_magnet_sextupole_sd1_number = 20
si_magnet_sextupole_sd1_hardedge_length = 0.15 #[m]
si_magnet_sextupole_sd1_integrated_sextupolar_field_maximum = 360 #[T/m]
si_magnet_sextupole_sd2_number = 20
si_magnet_sextupole_sd2_hardedge_length = 0.15 #[m]
si_magnet_sextupole_sd2_integrated_sextupolar_field_maximum = 360 #[T/m]
si_magnet_sextupole_sd3_number = 20
si_magnet_sextupole_sd3_hardedge_length = 0.15 #[m]
si_magnet_sextupole_sd3_integrated_sextupolar_field_maximum = 360 #[T/m]
si_magnet_sextupole_sd4_number = 20
si_magnet_sextupole_sd4_hardedge_length = 0.15 #[m]
si_magnet_sextupole_sd4_integrated_sextupolar_field_maximum = 360 #[T/m]
si_magnet_sextupole_sd5_number = 20
si_magnet_sextupole_sd5_hardedge_length = 0.15 #[m]
si_magnet_sextupole_sd5_integrated_sextupolar_field_maximum = 360 #[T/m]
si_magnet_sextupole_sd6_number = 20
si_magnet_sextupole_sd6_hardedge_length = 0.15 #[m]
si_magnet_sextupole_sd6_integrated_sextupolar_field_maximum = 360 #[T/m]
si_magnet_sextupole_sf1_number = 20
si_magnet_sextupole_sf1_hardedge_length = 0.15 #[m]
si_magnet_sextupole_sf1_integrated_sextupolar_field_maximum = 360 #[T/m]
si_magnet_sextupole_sf2_number = 20
si_magnet_sextupole_sf2_hardedge_length = 0.15 #[m]
si_magnet_sextupole_sf2_integrated_sextupolar_field_maximum = 360 #[T/m]
si_magnet_sextupole_sf3_number = 20
si_magnet_sextupole_sf3_hardedge_length = 0.15 #[m]
si_magnet_sextupole_sf3_integrated_sextupolar_field_maximum = 360 #[T/m]
si_magnet_sextupole_sf4_number = 20
si_magnet_sextupole_sf4_hardedge_length = 0.15 #[m]
si_magnet_sextupole_sf4_integrated_sextupolar_field_maximum = 360 #[T/m]

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
si_optics_transverse_coupling = 1.0    # [%]
si_optics_damping_partition_number_vertical_dipole     = 1.0
si_optics_damping_partition_number_vertical          = 1.0

si_error_alignment_dipole     = 40  #[μm]
si_error_alignment_quadrupole = 40  #[μm]
si_error_alignment_sextupole  = 40  #[μm]
si_error_roll_dipole      = 0.2 #[mrad]
si_error_roll_quadrupole  = 0.2 #[mrad]
si_error_roll_sextupole   = 0.2 #[mrad]
si_error_excitation_dipole     = 0.05 #[%]
si_error_excitation_quadrupole = 0.05 #[%]
si_error_excitation_sextupole  = 0.05 #[%]
si_error_ripple_dipole        =  20   # [ppm]
si_error_ripple_quadrupole    =  20   # [ppm]
si_error_ripple_sextupole     =  20   # [ppm]
si_error_vibration_dipole     =  6    # [nm]
si_error_vibration_quadrupole =  6    # [nm]
si_error_vibration_sextupole  =  6    # [nm]

parameter_list = [
  Parameter(name='SI lattice version',       group='FAC', is_derived=False, value=si_lattice_version, symbol='', units='', deps=[], obs=[], ),
  Parameter(name='SI lattice type',          group='FAC', is_derived=False, value=si_lattice_type, symbol='', units='', deps=['SI lattice version'], obs=[], ),
  Parameter(name='SI lattice circumference', group='GIA', is_derived=False, value=si_lattice_circumference, symbol=r'<math>C</math>', units='m', deps=[], obs=[], ),
  Parameter(name='SI lattice symmetry',      group='FAC', is_derived=False, value=si_lattice_symmetry, symbol=r'<math>N_\text{SUPERCELLS}</math>', units='', deps=[], obs=[], ),
  Parameter(name='SI lattice long straight section number',  group='FAC', is_derived=True, value='"SI lattice symmetry"', symbol=r'<math>N_\text{lss}</math>', units='', deps=[], obs=[], ),
  Parameter(name='SI lattice short straight section number', group='FAC', is_derived=True, value='"SI lattice symmetry"', symbol=r'<math>N_\text{sss}</math>', units='', deps=[], obs=[], ),
  Parameter(name='SI lattice long straight section length',  group='FAC', is_derived=False, value=si_lattice_long_straight_section_length, symbol=r'<math>L_\text{lss}</math>', units='m', deps=[], obs=[], ),
  Parameter(name='SI lattice short straight section length', group='FAC', is_derived=False, value=si_lattice_short_straight_section_length, symbol=r'<math>L_\text{sss}</math>',  units='m', deps=[], obs=[], ),

  Parameter(name='SI beam energy',            group='GIA', is_derived=False, value=si_beam_energy, symbol=r'<math>E</math>', units='GeV', deps=[], obs=[], ),
  Parameter(name='SI beam current',           group='FAC', is_derived=False, value=si_beam_current, symbol=r'<math>I</math>', units='mA', deps=[], obs=[], ),
  Parameter(name='SI beam gamma factor',      group='FAC', is_derived=True, value='gamma("SI beam energy")', symbol=r'<math>\gamma</math>', units='', deps=[], obs=[r'<math>\gamma = \frac{E}{E_0}</math>'], ),
  Parameter(name='SI beam beta factor',       group='FAC', is_derived=True, value='beta("SI beam gamma factor")', symbol=r'<math>\beta</math>', units='', deps=[], obs=[r'<math>\beta \equiv \sqrt{1 - \frac{1}{\gamma^2}}</math>'], ),
  Parameter(name='SI beam velocity',          group='FAC', is_derived=True, value='velocity("SI beam beta factor")', symbol=r'<math>v</math>', units='m/s', deps=[], obs=[r'<math>v \equiv \beta c</math>'], ),
  Parameter(name='SI beam magnetic rigidity', group='FAC', is_derived=True, value='brho("SI beam energy", "SI beam beta factor")', symbol=r'<math>(B\rho)</math>', units=unicode('T·m', encoding='utf-8'), deps=[], obs=[r'<math>(B\rho) = \frac{p}{ec} = \frac{E}{ec^2}</math>'], ),
  Parameter(name='SI beam revolution period',    group='FAC', is_derived=True, value='revolution_period("SI lattice circumference", "SI beam velocity")', symbol=r'<math>T_\text{rev}</math>', units=unicode('μs',encoding='utf-8'), deps=[], obs=[r'<math>T_\text{rev} \equiv \frac{C}{v}</math>'], ),
  Parameter(name='SI beam revolution frequency', group='FAC', is_derived=True, value='1.0/"SI beam revolution period"', symbol=r'<math>f_\text{rev}</math>', units='MHz', deps=[], obs=[r'<math>f_\text{rev} \equiv \frac{1}{T_\text{rev}}</math>'], ),
  Parameter(name='SI beam electron number',      group='FAC', is_derived=True, value='number_of_electrons("SI beam current", "SI beam revolution period")', symbol=r'<math>N</math>', units='', deps=[], obs=[], ),

  Parameter(name='SI rf harmonic number', group='FAC', is_derived=False, value=si_rf_harmonic_number, symbol=r'<math>h</math>', units='', deps=[], obs=[], ),
  Parameter(name='SI rf frequency',       group='FAC', is_derived=True, value='rf_frequency("SI beam revolution frequency", "SI rf harmonic number")', symbol=r'<math>f_\text{rf}</math>', units='MHz', deps=[], obs=[], ),
  Parameter(name='SI rf peak voltage',    group='FAC', is_derived=False, value=si_rf_peak_voltage, symbol=r'<math>V_\text{rf}</math>', units='MV', deps=[], obs=[], ),

  Parameter(name='SI magnet dipole b1 number',                   group='FAC', is_derived=True, value='4*"SI lattice symmetry"', symbol=r'<math>N_\text{b1}</math>', units='', deps=[], obs=[], ),
  Parameter(name='SI magnet dipole b1 deflection angle',         group='FAC', is_derived=False, value=si_magnet_dipole_b1_deflection_angle, symbol=r'<math>\theta_\text{b1}</math>', units=unicode('°',encoding='utf-8'), deps=[], obs=[], ),
  Parameter(name='SI magnet dipole b1 hardedge length',          group='FAC', is_derived=False, value=si_magnet_dipole_b1_hardedge_length, symbol=r'<math>L_\text{b1}</math>', units='m', deps=[], obs=[], ),
  Parameter(name='SI magnet dipole b1 hardedge bending radius',  group='FAC', is_derived=True, value='"SI magnet dipole b1 hardedge length" / deg2rad("SI magnet dipole b1 deflection angle")', symbol=r'<math>\rho_\text{b1}</math>', units='m', deps=[], obs=[r'<math>\rho_\text{b1} = \frac{L_\text{b1}}{\theta_\text{b1}}</math>'], ),
  Parameter(name='SI magnet dipole b1 hardedge magnetic field',  group='FAC', is_derived=True, value='"SI beam magnetic rigidity" / "SI magnet dipole b1 hardedge bending radius"', symbol=r'<math>B_\text{b1}</math>', units='T', deps=[], obs=[r'<math>B_\text{b1} = \frac{(B\rho)}{\rho_\text{b1}}</math>'], ),
  Parameter(name='SI magnet dipole b1 hardedge critical energy', group='FAC', is_derived=True, value='critical_energy("SI beam gamma factor", "SI magnet dipole b1 hardedge bending radius")', symbol=r'<math>\epsilon_\text{c,b1}</math>', units='keV', deps=[], obs=[r'<math>\epsilon_\text{c,b1} = \frac{3}{2} \hbar c \frac{\gamma^3}{\rho_\text{b1}}</math>'], ),
  Parameter(name='SI magnet dipole b1 hardedge sagitta',         group='FAC', is_derived=True, value='1000*"SI magnet dipole b1 hardedge bending radius"*(1.0-cos(0.5*deg2rad("SI magnet dipole b1 deflection angle")))', symbol=r'<math>S_\text{sag, b1}</math>', units='mm', deps=[], obs=[r'<math>S_\text{sag, b1} = \rho_\text{b1} (1 - \cos \theta_\text{b1} / 2)</math>'],),
  Parameter(name='SI magnet dipole b2 number', group='FAC', is_derived=True, value='4*"SI lattice symmetry"', symbol=r'<math>N_\text{b2}</math>', units='', deps=[], obs=[], ),
  Parameter(name='SI magnet dipole b2 deflection angle', group='FAC', is_derived=False, value=si_magnet_dipole_b2_deflection_angle, symbol=r'<math>\theta_\text{b2}</math>', units=unicode('°',encoding='utf-8'), deps=[], obs=[], ),
  Parameter(name='SI magnet dipole b2 hardedge length', group='FAC', is_derived=False, value=si_magnet_dipole_b2_hardedge_length, symbol=r'<math>L_\text{b2}</math>', units='m', deps=[], obs=[], ),
  Parameter(name='SI magnet dipole b2 hardedge bending radius', group='FAC', is_derived=True, value='"SI magnet dipole b2 hardedge length" / deg2rad("SI magnet dipole b2 deflection angle")', symbol=r'<math>\rho_\text{b2}</math>', units='m', deps=[], obs=[r'<math>\rho_\text{b2} = \frac{L_\text{b2}}{\theta_\text{b2}}</math>'], ),
  Parameter(name='SI magnet dipole b2 hardedge magnetic field', group='FAC', is_derived=True, value='"SI beam magnetic rigidity" / "SI magnet dipole b2 hardedge bending radius"', symbol=r'<math>B_\text{b2}</math>', units='T', deps=[], obs=[r'<math>B_\text{b2} = \frac{(B\rho)}{\rho_\text{b2}}</math>'], ),
  Parameter(name='SI magnet dipole b2 hardedge critical energy', group='FAC', is_derived=True, value='critical_energy("SI beam gamma factor", "SI magnet dipole b2 hardedge bending radius")', symbol=r'<math>\epsilon_\text{c,b2}</math>', units='keV', deps=[], obs=[r'<math>\epsilon_\text{c,b2} = \frac{3}{2} \hbar c \frac{\gamma^3}{\rho_\text{b2}}</math>'], ),
  Parameter(name='SI magnet dipole b2 hardedge sagitta', group='FAC', is_derived=True, value='1000*"SI magnet dipole b2 hardedge bending radius" * (1.0-cos(0.5*deg2rad("SI magnet dipole b2 deflection angle")))', symbol=r'<math>S_\text{sag, b2}</math>', units='mm', deps=[], obs=[r'<math>S_\text{sag, b2} = \rho_\text{b2} (1 - \cos \theta_\text{b2} / 2)</math>'],),
  Parameter(name='SI magnet dipole b3 number', group='FAC', is_derived=True, value='4*"SI lattice symmetry"', symbol=r'<math>N_\text{b3}</math>', units='', deps=[], obs=[], ),
  Parameter(name='SI magnet dipole b3 deflection angle', group='FAC', is_derived=False, value=si_magnet_dipole_b3_deflection_angle, symbol=r'<math>\theta_\text{b3}</math>', units=unicode('°',encoding='utf-8'), deps=[], obs=[], ),
  Parameter(name='SI magnet dipole b3 hardedge length', group='FAC', is_derived=False, value=si_magnet_dipole_b3_hardedge_length, symbol=r'<math>L_\text{b3}</math>', units='m', deps=[], obs=[], ),
  Parameter(name='SI magnet dipole b3 hardedge bending radius', group='FAC', is_derived=True, value='"SI magnet dipole b3 hardedge length" / deg2rad("SI magnet dipole b3 deflection angle")', symbol=r'<math>\rho_\text{b3}</math>', units='m', deps=[], obs=[r'<math>\rho_\text{b3} = \frac{L_\text{b3}}{\theta_\text{b3}}</math>'], ),
  Parameter(name='SI magnet dipole b3 hardedge magnetic field', group='FAC', is_derived=True, value='"SI beam magnetic rigidity" / "SI magnet dipole b3 hardedge bending radius"', symbol=r'<math>B_\text{b3}</math>', units='T', deps=[], obs=[r'<math>B_\text{b3} = \frac{(B\rho)}{\rho_\text{b3}}</math>'], ),
  Parameter(name='SI magnet dipole b3 hardedge critical energy', group='FAC', is_derived=True, value='critical_energy("SI beam gamma factor", "SI magnet dipole b3 hardedge bending radius")', symbol=r'<math>\epsilon_\text{c,b3}</math>', units='keV', deps=[], obs=[r'<math>\epsilon_\text{c,b3} = \frac{3}{2} \hbar c \frac{\gamma^3}{\rho_\text{b3}}</math>'], ),
  Parameter(name='SI magnet dipole b3 hardedge sagitta', group='FAC', is_derived=True, value='1000*"SI magnet dipole b3 hardedge bending radius" * (1.0-cos(0.5*deg2rad("SI magnet dipole b3 deflection angle")))', symbol=r'<math>S_\text{sag, b3}</math>', units='mm', deps=[], obs=[r'<math>S_\text{sag, b3} = \rho_\text{b3} (1 - \cos \theta_\text{b3} / 2)</math>'],),
  Parameter(name='SI magnet dipole bc number', group='FAC', is_derived=True, value='2*"SI lattice symmetry"', symbol=r'<math>N_\text{bc}</math>', units='', deps=[], obs=[], ),

  Parameter(name='SI magnet dipole bc deflection angle', group='FAC', is_derived=False, value=si_magnet_dipole_bc_deflection_angle, symbol=r'<math>\theta_\text{bc}</math>', units=unicode('°',encoding='utf-8'), deps=[], obs=[], ),
  Parameter(name='SI magnet dipole bc hardedge length', group='FAC', is_derived=False, value=si_magnet_dipole_bc_hardedge_length, symbol=r'<math>L_\text{bc}</math>', units='m', deps=[], obs=[], ),
  Parameter(name='SI magnet dipole bc hardedge bending radius', group='FAC', is_derived=True, value='"SI magnet dipole bc hardedge length" / deg2rad("SI magnet dipole bc deflection angle")', symbol=r'<math>\rho_\text{bc}</math>', units='m', deps=[], ),
  Parameter(name='SI magnet dipole bc hardedge magnetic field', group='FAC', is_derived=True, value='"SI beam magnetic rigidity" / "SI magnet dipole bc hardedge bending radius"', symbol=r'<math>B_\text{bc}</math>', units='T', deps=[], ),
  Parameter(name='SI magnet dipole bc hardedge critical energy', group='FAC', is_derived=True, value='critical_energy("SI beam gamma factor", "SI magnet dipole bc hardedge bending radius")', symbol=r'<math>\epsilon_\text{c,bc}</math>', units='keV', deps=[], ),
  Parameter(name='SI magnet dipole bc hardedge sagitta', group='FAC', is_derived=True, value='1000 * "SI magnet dipole bc hardedge bending radius" * (1.0 - cos(0.5*deg2rad("SI magnet dipole bc deflection angle")))', symbol=r'<math>S_\text{sag, bc}</math>', units='mm', deps=[],),

  Parameter(name='SI magnet sextupole sda number', group='FAC', is_derived=False, value=si_magnet_sextupole_sda_number, symbol=r'<math>N_\text{sda}</math>', units='', deps=[], obs=[], ),
  Parameter(name='SI magnet sextupole sda hardedge length', group='FAC', is_derived=False, value=si_magnet_sextupole_sda_hardedge_length, symbol=r'<math>L_\text{sda}</math>', units='m', deps=[], obs=[], ),
  Parameter(name='SI magnet sextupole sda integrated sextupolar field maximum', group='FAC', is_derived=False, value=si_magnet_sextupole_sda_integrated_sextupolar_field_maximum, symbol=r"<math>(1/2)(B''L)_\text{max, sda}</math>", units='T.m<sup>-1</sup>', deps=[], obs=[r"<math>(1/2)(B''L)_\text{max, sda} \equiv \frac{1}{2} \int{ds\;\frac{\partial^2 B_y}{\partial x^2}}</math>"], ),
  Parameter(name='SI magnet sextupole sda hardedge sextupolar field maximum', group='FAC', is_derived=True, value='"SI magnet sextupole sda integrated sextupolar field maximum" / "SI magnet sextupole sda hardedge length"', symbol=r"<math>(1/2)B''_\text{max, sda}</math>", units='T.m<sup>-2</sup>', deps=[], ),
  Parameter(name='SI magnet sextupole sda hardedge strength maximum', group='FAC', is_derived=True, value='"SI magnet sextupole sda hardedge sextupolar field maximum" / "SI beam magnetic rigidity"', symbol=r"<math>S_\text{max, sda}</math>", units='m<sup>-3</sup>', deps=[], ),
  Parameter(name='SI magnet sextupole sfa number', group='FAC', is_derived=False, value=si_magnet_sextupole_sfa_number, symbol=r'<math>N_\text{sfa}</math>', units='', deps=[], obs=[], ),
  Parameter(name='SI magnet sextupole sfa hardedge length', group='FAC', is_derived=False, value=si_magnet_sextupole_sfa_hardedge_length, symbol=r'<math>L_\text{sfa}</math>', units='m', deps=[], obs=[], ),
  Parameter(name='SI magnet sextupole sfa integrated sextupolar field maximum', group='FAC', is_derived=False, value=si_magnet_sextupole_sfa_integrated_sextupolar_field_maximum, symbol=r"<math>(1/2)(B''L)_\text{max, sfa}</math>", units='T.m<sup>-1</sup>', deps=[], obs=[r"<math>(1/2)(B''L)_\text{max, sfa} \equiv \frac{1}{2} \int{ds\;\frac{\partial^2 B_y}{\partial x^2}}</math>"], ),
  Parameter(name='SI magnet sextupole sfa hardedge sextupolar field maximum', group='FAC', is_derived=True, value='"SI magnet sextupole sfa integrated sextupolar field maximum" / "SI magnet sextupole sfa hardedge length"', symbol=r"<math>(1/2)B''_\text{max, sfa}</math>", units='T.m<sup>-2</sup>', deps=[], ),
  Parameter(name='SI magnet sextupole sfa hardedge strength maximum', group='FAC', is_derived=True, value='"SI magnet sextupole sfa hardedge sextupolar field maximum" / "SI beam magnetic rigidity"', symbol=r"<math>S_\text{max, sfa}</math>", units='m<sup>-3</sup>', deps=[], ),
  Parameter(name='SI magnet sextupole sdb number', group='FAC', is_derived=False, value=si_magnet_sextupole_sdb_number, symbol=r'<math>N_\text{sdb}</math>', units='', deps=[], obs=[], ),
  Parameter(name='SI magnet sextupole sdb hardedge length', group='FAC', is_derived=False, value=si_magnet_sextupole_sdb_hardedge_length, symbol=r'<math>L_\text{sdb}</math>', units='m', deps=[], obs=[], ),
  Parameter(name='SI magnet sextupole sdb integrated sextupolar field maximum', group='FAC', is_derived=False, value=si_magnet_sextupole_sdb_integrated_sextupolar_field_maximum, symbol=r"<math>(1/2)(B''L)_\text{max, sdb}</math>", units='T.m<sup>-1</sup>', deps=[], obs=[r"<math>(1/2)(B''L)_\text{max, sdb} \equiv \frac{1}{2} \int{ds\;\frac{\partial^2 B_y}{\partial x^2}}</math>"], ),
  Parameter(name='SI magnet sextupole sdb hardedge sextupolar field maximum', group='FAC', is_derived=True, value='"SI magnet sextupole sdb integrated sextupolar field maximum" / "SI magnet sextupole sdb hardedge length"', symbol=r"<math>(1/2)B''_\text{max, sdb}</math>", units='T.m<sup>-2</sup>', deps=[], ),
  Parameter(name='SI magnet sextupole sdb hardedge strength maximum', group='FAC', is_derived=True, value='"SI magnet sextupole sdb hardedge sextupolar field maximum" / "SI beam magnetic rigidity"', symbol=r"<math>S_\text{max, sdb}</math>", units='m<sup>-3</sup>', deps=[], ),
  Parameter(name='SI magnet sextupole sfb number', group='FAC', is_derived=False, value=si_magnet_sextupole_sfb_number, symbol=r'<math>N_\text{sfb}</math>', units='', deps=[], obs=[], ),
  Parameter(name='SI magnet sextupole sfb hardedge length', group='FAC', is_derived=False, value=si_magnet_sextupole_sfb_hardedge_length, symbol=r'<math>L_\text{sfb}</math>', units='m', deps=[], obs=[], ),
  Parameter(name='SI magnet sextupole sfb integrated sextupolar field maximum', group='FAC', is_derived=False, value=si_magnet_sextupole_sfb_integrated_sextupolar_field_maximum, symbol=r"<math>(1/2)(B''L)_\text{max, sfb}</math>", units='T.m<sup>-1</sup>', deps=[], obs=[r"<math>(1/2)(B''L)_\text{max, sfb} \equiv \frac{1}{2} \int{ds\;\frac{\partial^2 B_y}{\partial x^2}}</math>"], ),
  Parameter(name='SI magnet sextupole sfb hardedge sextupolar field maximum', group='FAC', is_derived=True, value='"SI magnet sextupole sfb integrated sextupolar field maximum" / "SI magnet sextupole sfb hardedge length"', symbol=r"<math>(1/2)B''_\text{max, sfb}</math>", units='T.m<sup>-2</sup>', deps=[], ),
  Parameter(name='SI magnet sextupole sfb hardedge strength maximum', group='FAC', is_derived=True, value='"SI magnet sextupole sfb hardedge sextupolar field maximum" / "SI beam magnetic rigidity"', symbol=r"<math>S_\text{max, sfb}</math>", units='m<sup>-3</sup>', deps=[], ),
  Parameter(name='SI magnet sextupole sd1 number', group='FAC', is_derived=False, value=si_magnet_sextupole_sd1_number, symbol=r'<math>N_\text{sd1}</math>', units='', deps=[], obs=[], ),
  Parameter(name='SI magnet sextupole sd1 hardedge length', group='FAC', is_derived=False, value=si_magnet_sextupole_sd1_hardedge_length, symbol=r'<math>L_\text{sd1}</math>', units='m', deps=[], obs=[], ),
  Parameter(name='SI magnet sextupole sd1 integrated sextupolar field maximum', group='FAC', is_derived=False, value=si_magnet_sextupole_sd1_integrated_sextupolar_field_maximum, symbol=r"<math>(1/2)(B''L)_\text{max, sd1}</math>", units='T.m<sup>-1</sup>', deps=[], obs=[r"<math>(1/2)(B''L)_\text{max, sd1} \equiv \frac{1}{2} \int{ds\;\frac{\partial^2 B_y}{\partial x^2}}</math>"], ),
  Parameter(name='SI magnet sextupole sd1 hardedge sextupolar field maximum', group='FAC', is_derived=True, value='"SI magnet sextupole sd1 integrated sextupolar field maximum" / "SI magnet sextupole sd1 hardedge length"', symbol=r"<math>(1/2)B''_\text{max, sd1}</math>", units='T.m<sup>-2</sup>', deps=[], ),
  Parameter(name='SI magnet sextupole sd1 hardedge strength maximum', group='FAC', is_derived=True, value='"SI magnet sextupole sd1 hardedge sextupolar field maximum" / "SI beam magnetic rigidity"', symbol=r"<math>S_\text{max, sd1}</math>", units='m<sup>-3</sup>', deps=[], ),
  Parameter(name='SI magnet sextupole sd2 number', group='FAC', is_derived=False, value=si_magnet_sextupole_sd2_number, symbol=r'<math>N_\text{sd2}</math>', units='', deps=[], obs=[], ),
  Parameter(name='SI magnet sextupole sd2 hardedge length', group='FAC', is_derived=False, value=si_magnet_sextupole_sd2_hardedge_length, symbol=r'<math>L_\text{sd2}</math>', units='m', deps=[], obs=[], ),
  Parameter(name='SI magnet sextupole sd2 integrated sextupolar field maximum', group='FAC', is_derived=False, value=si_magnet_sextupole_sd2_integrated_sextupolar_field_maximum, symbol=r"<math>(1/2)(B''L)_\text{max, sd2}</math>", units='T.m<sup>-1</sup>', deps=[], obs=[r"<math>(1/2)(B''L)_\text{max, sd2} \equiv \frac{1}{2} \int{ds\;\frac{\partial^2 B_y}{\partial x^2}}</math>"], ),
  Parameter(name='SI magnet sextupole sd2 hardedge sextupolar field maximum', group='FAC', is_derived=True, value='"SI magnet sextupole sd2 integrated sextupolar field maximum" / "SI magnet sextupole sd2 hardedge length"', symbol=r"<math>(1/2)B''_\text{max, sd2}</math>", units='T.m<sup>-2</sup>', deps=[], ),
  Parameter(name='SI magnet sextupole sd2 hardedge strength maximum', group='FAC', is_derived=True, value='"SI magnet sextupole sd2 hardedge sextupolar field maximum" / "SI beam magnetic rigidity"', symbol=r"<math>S_\text{max, sd2}</math>", units='m<sup>-3</sup>', deps=[], ),
  Parameter(name='SI magnet sextupole sd3 number', group='FAC', is_derived=False, value=si_magnet_sextupole_sd3_number, symbol=r'<math>N_\text{sd3}</math>', units='', deps=[], obs=[], ),
  Parameter(name='SI magnet sextupole sd3 hardedge length', group='FAC', is_derived=False, value=si_magnet_sextupole_sd3_hardedge_length, symbol=r'<math>L_\text{sd3}</math>', units='m', deps=[], obs=[], ),
  Parameter(name='SI magnet sextupole sd3 integrated sextupolar field maximum', group='FAC', is_derived=False, value=si_magnet_sextupole_sd3_integrated_sextupolar_field_maximum, symbol=r"<math>(1/2)(B''L)_\text{max, sd3}</math>", units='T.m<sup>-1</sup>', deps=[], obs=[r"<math>(1/2)(B''L)_\text{max, sd3} \equiv \frac{1}{2} \int{ds\;\frac{\partial^2 B_y}{\partial x^2}}</math>"], ),
  Parameter(name='SI magnet sextupole sd3 hardedge sextupolar field maximum', group='FAC', is_derived=True, value='"SI magnet sextupole sd3 integrated sextupolar field maximum" / "SI magnet sextupole sd3 hardedge length"', symbol=r"<math>(1/2)B''_\text{max, sd3}</math>", units='T.m<sup>-2</sup>', deps=[], ),
  Parameter(name='SI magnet sextupole sd3 hardedge strength maximum', group='FAC', is_derived=True, value='"SI magnet sextupole sd3 hardedge sextupolar field maximum" / "SI beam magnetic rigidity"', symbol=r"<math>S_\text{max, sd3}</math>", units='m<sup>-3</sup>', deps=[], ),
  Parameter(name='SI magnet sextupole sd4 number', group='FAC', is_derived=False, value=si_magnet_sextupole_sd4_number, symbol=r'<math>N_\text{sd4}</math>', units='', deps=[], obs=[], ),
  Parameter(name='SI magnet sextupole sd4 hardedge length', group='FAC', is_derived=False, value=si_magnet_sextupole_sd4_hardedge_length, symbol=r'<math>L_\text{sd4}</math>', units='m', deps=[], obs=[], ),
  Parameter(name='SI magnet sextupole sd4 integrated sextupolar field maximum', group='FAC', is_derived=False, value=si_magnet_sextupole_sd4_integrated_sextupolar_field_maximum, symbol=r"<math>(1/2)(B''L)_\text{max, sd4}</math>", units='T.m<sup>-1</sup>', deps=[], obs=[r"<math>(1/2)(B''L)_\text{max, sd4} \equiv \frac{1}{2} \int{ds\;\frac{\partial^2 B_y}{\partial x^2}}</math>"], ),
  Parameter(name='SI magnet sextupole sd4 hardedge sextupolar field maximum', group='FAC', is_derived=True, value='"SI magnet sextupole sd4 integrated sextupolar field maximum" / "SI magnet sextupole sd4 hardedge length"', symbol=r"<math>(1/2)B''_\text{max, sd4}</math>", units='T.m<sup>-2</sup>', deps=[], ),
  Parameter(name='SI magnet sextupole sd4 hardedge strength maximum', group='FAC', is_derived=True, value='"SI magnet sextupole sd4 hardedge sextupolar field maximum" / "SI beam magnetic rigidity"', symbol=r"<math>S_\text{max, sd4}</math>", units='m<sup>-3</sup>', deps=[], ),
  Parameter(name='SI magnet sextupole sd5 number', group='FAC', is_derived=False, value=si_magnet_sextupole_sd5_number, symbol=r'<math>N_\text{sd5}</math>', units='', deps=[], obs=[], ),
  Parameter(name='SI magnet sextupole sd5 hardedge length', group='FAC', is_derived=False, value=si_magnet_sextupole_sd5_hardedge_length, symbol=r'<math>L_\text{sd5}</math>', units='m', deps=[], obs=[], ),
  Parameter(name='SI magnet sextupole sd5 integrated sextupolar field maximum', group='FAC', is_derived=False, value=si_magnet_sextupole_sd5_integrated_sextupolar_field_maximum, symbol=r"<math>(1/2)(B''L)_\text{max, sd5}</math>", units='T.m<sup>-1</sup>', deps=[], obs=[r"<math>(1/2)(B''L)_\text{max, sd5} \equiv \frac{1}{2} \int{ds\;\frac{\partial^2 B_y}{\partial x^2}}</math>"], ),
  Parameter(name='SI magnet sextupole sd5 hardedge sextupolar field maximum', group='FAC', is_derived=True, value='"SI magnet sextupole sd5 integrated sextupolar field maximum" / "SI magnet sextupole sd5 hardedge length"', symbol=r"<math>(1/2)B''_\text{max, sd5}</math>", units='T.m<sup>-2</sup>', deps=[], ),
  Parameter(name='SI magnet sextupole sd5 hardedge strength maximum', group='FAC', is_derived=True, value='"SI magnet sextupole sd5 hardedge sextupolar field maximum" / "SI beam magnetic rigidity"', symbol=r"<math>S_\text{max, sd5}</math>", units='m<sup>-3</sup>', deps=[], ),
  Parameter(name='SI magnet sextupole sd6 number', group='FAC', is_derived=False, value=si_magnet_sextupole_sd6_number, symbol=r'<math>N_\text{sd6}</math>', units='', deps=[], obs=[], ),
  Parameter(name='SI magnet sextupole sd6 hardedge length', group='FAC', is_derived=False, value=si_magnet_sextupole_sd6_hardedge_length, symbol=r'<math>L_\text{sd6}</math>', units='m', deps=[], obs=[], ),
  Parameter(name='SI magnet sextupole sd6 integrated sextupolar field maximum', group='FAC', is_derived=False, value=si_magnet_sextupole_sd6_integrated_sextupolar_field_maximum, symbol=r"<math>(1/2)(B''L)_\text{max, sd6}</math>", units='T.m<sup>-1</sup>', deps=[], obs=[r"<math>(1/2)(B''L)_\text{max, sd6} \equiv \frac{1}{2} \int{ds\;\frac{\partial^2 B_y}{\partial x^2}}</math>"], ),
  Parameter(name='SI magnet sextupole sd6 hardedge sextupolar field maximum', group='FAC', is_derived=True, value='"SI magnet sextupole sd6 integrated sextupolar field maximum" / "SI magnet sextupole sd6 hardedge length"', symbol=r"<math>(1/2)B''_\text{max, sd6}</math>", units='T.m<sup>-2</sup>', deps=[], ),
  Parameter(name='SI magnet sextupole sd6 hardedge strength maximum', group='FAC', is_derived=True, value='"SI magnet sextupole sd6 hardedge sextupolar field maximum" / "SI beam magnetic rigidity"', symbol=r"<math>S_\text{max, sd6}</math>", units='m<sup>-3</sup>', deps=[], ),
  Parameter(name='SI magnet sextupole sf1 number', group='FAC', is_derived=False, value=si_magnet_sextupole_sf1_number, symbol=r'<math>N_\text{sf1}</math>', units='', deps=[], obs=[], ),
  Parameter(name='SI magnet sextupole sf1 hardedge length', group='FAC', is_derived=False, value=si_magnet_sextupole_sf1_hardedge_length, symbol=r'<math>L_\text{sf1}</math>', units='m', deps=[], obs=[], ),
  Parameter(name='SI magnet sextupole sf1 integrated sextupolar field maximum', group='FAC', is_derived=False, value=si_magnet_sextupole_sf1_integrated_sextupolar_field_maximum, symbol=r"<math>(1/2)(B''L)_\text{max, sf1}</math>", units='T.m<sup>-1</sup>', deps=[], obs=[r"<math>(1/2)(B''L)_\text{max, sf1} \equiv \frac{1}{2} \int{ds\;\frac{\partial^2 B_y}{\partial x^2}}</math>"], ),
  Parameter(name='SI magnet sextupole sf1 hardedge sextupolar field maximum', group='FAC', is_derived=True, value='"SI magnet sextupole sf1 integrated sextupolar field maximum" / "SI magnet sextupole sf1 hardedge length"', symbol=r"<math>(1/2)B''_\text{max, sf1}</math>", units='T.m<sup>-2</sup>', deps=[], ),
  Parameter(name='SI magnet sextupole sf1 hardedge strength maximum', group='FAC', is_derived=True, value='"SI magnet sextupole sf1 hardedge sextupolar field maximum" / "SI beam magnetic rigidity"', symbol=r"<math>S_\text{max, sf1}</math>", units='m<sup>-3</sup>', deps=[], ),
  Parameter(name='SI magnet sextupole sf2 number', group='FAC', is_derived=False, value=si_magnet_sextupole_sf2_number, symbol=r'<math>N_\text{sf2}</math>', units='', deps=[], obs=[], ),
  Parameter(name='SI magnet sextupole sf2 hardedge length', group='FAC', is_derived=False, value=si_magnet_sextupole_sf2_hardedge_length, symbol=r'<math>L_\text{sf2}</math>', units='m', deps=[], obs=[], ),
  Parameter(name='SI magnet sextupole sf2 integrated sextupolar field maximum', group='FAC', is_derived=False, value=si_magnet_sextupole_sf2_integrated_sextupolar_field_maximum, symbol=r"<math>(1/2)(B''L)_\text{max, sf2}</math>", units='T.m<sup>-1</sup>', deps=[], obs=[r"<math>(1/2)(B''L)_\text{max, sf2} \equiv \frac{1}{2} \int{ds\;\frac{\partial^2 B_y}{\partial x^2}}</math>"], ),
  Parameter(name='SI magnet sextupole sf2 hardedge sextupolar field maximum', group='FAC', is_derived=True, value='"SI magnet sextupole sf2 integrated sextupolar field maximum" / "SI magnet sextupole sf2 hardedge length"', symbol=r"<math>(1/2)B''_\text{max, sf2}</math>", units='T.m<sup>-2</sup>', deps=[], ),
  Parameter(name='SI magnet sextupole sf2 hardedge strength maximum', group='FAC', is_derived=True, value='"SI magnet sextupole sf2 hardedge sextupolar field maximum" / "SI beam magnetic rigidity"', symbol=r"<math>S_\text{max, sf2}</math>", units='m<sup>-3</sup>', deps=[], ),
  Parameter(name='SI magnet sextupole sf3 number', group='FAC', is_derived=False, value=si_magnet_sextupole_sf3_number, symbol=r'<math>N_\text{sf3}</math>', units='', deps=[], obs=[], ),
  Parameter(name='SI magnet sextupole sf3 hardedge length', group='FAC', is_derived=False, value=si_magnet_sextupole_sf3_hardedge_length, symbol=r'<math>L_\text{sf3}</math>', units='m', deps=[], obs=[], ),
  Parameter(name='SI magnet sextupole sf3 integrated sextupolar field maximum', group='FAC', is_derived=False, value=si_magnet_sextupole_sf3_integrated_sextupolar_field_maximum, symbol=r"<math>(1/2)(B''L)_\text{max, sf3}</math>", units='T.m<sup>-1</sup>', deps=[], obs=[r"<math>(1/2)(B''L)_\text{max, sf3} \equiv \frac{1}{2} \int{ds\;\frac{\partial^2 B_y}{\partial x^2}}</math>"], ),
  Parameter(name='SI magnet sextupole sf3 hardedge sextupolar field maximum', group='FAC', is_derived=True, value='"SI magnet sextupole sf3 integrated sextupolar field maximum" / "SI magnet sextupole sf3 hardedge length"', symbol=r"<math>(1/2)B''_\text{max, sf3}</math>", units='T.m<sup>-2</sup>', deps=[], ),
  Parameter(name='SI magnet sextupole sf3 hardedge strength maximum', group='FAC', is_derived=True, value='"SI magnet sextupole sf3 hardedge sextupolar field maximum" / "SI beam magnetic rigidity"', symbol=r"<math>S_\text{max, sf3}</math>", units='m<sup>-3</sup>', deps=[], ),
  Parameter(name='SI magnet sextupole sf4 number', group='FAC', is_derived=False, value=si_magnet_sextupole_sf4_number, symbol=r'<math>N_\text{sf4}</math>', units='', deps=[], obs=[], ),
  Parameter(name='SI magnet sextupole sf4 hardedge length', group='FAC', is_derived=False, value=si_magnet_sextupole_sf4_hardedge_length, symbol=r'<math>L_\text{sf4}</math>', units='m', deps=[], obs=[], ),
  Parameter(name='SI magnet sextupole sf4 integrated sextupolar field maximum', group='FAC', is_derived=False, value=si_magnet_sextupole_sf4_integrated_sextupolar_field_maximum, symbol=r"<math>(1/2)(B''L)_\text{max, sf4}</math>", units='T.m<sup>-1</sup>', deps=[], obs=[r"<math>(1/2)(B''L)_\text{max, sf4} \equiv \frac{1}{2} \int{ds\;\frac{\partial^2 B_y}{\partial x^2}}</math>"], ),
  Parameter(name='SI magnet sextupole sf4 hardedge sextupolar field maximum', group='FAC', is_derived=True, value='"SI magnet sextupole sf4 integrated sextupolar field maximum" / "SI magnet sextupole sf4 hardedge length"', symbol=r"<math>(1/2)B''_\text{max, sf4}</math>", units='T.m<sup>-2</sup>', deps=[], ),
  Parameter(name='SI magnet sextupole sf4 hardedge strength maximum', group='FAC', is_derived=True, value='"SI magnet sextupole sf4 hardedge sextupolar field maximum" / "SI beam magnetic rigidity"', symbol=r"<math>S_\text{max, sf4}</math>", units='m<sup>-3</sup>', deps=[], ),

  Parameter(name='SI bpm number',        group='FAC', is_derived=False, value=si_bpm_number, symbol=r'<math>N_\text{bpm}</math>', units='', deps=[], obs=[]),
  Parameter(name='SI magnet chs number', group='FAC', is_derived=False, value=si_magnet_chs_number, symbol=r'<math>N_\text{chs}</math>', units='', deps=[], obs=[]),
  Parameter(name='SI magnet cvs number', group='FAC', is_derived=False, value=si_magnet_cvs_number, symbol=r'<math>N_\text{cvs}</math>', units='', deps=[], obs=[]),
  Parameter(name='SI magnet chf number', group='FAC', is_derived=False, value=si_magnet_chf_number, symbol=r'<math>N_\text{chf}</math>', units='', deps=[], obs=[]),
  Parameter(name='SI magnet cvf number', group='FAC', is_derived=False, value=si_magnet_cvf_number, symbol=r'<math>N_\text{cvf}</math>', units='', deps=[], obs=[]),
  Parameter(name='SI magnet qs number',  group='FAC', is_derived=False, value=si_magnet_qs_number,  symbol=r'<math>N_\text{qs}</math>',  units='', deps=[], obs=[]),
  Parameter(name='SI magnet chs maximum strength', group='FAC', is_derived=False, value=si_magnet_chs_maximum_strength, symbol=r'<math>\theta_\text{max,chs}</math>', units=unicode('μrad', encoding='utf-8'), deps=[], obs=[]),
  Parameter(name='SI magnet cvs maximum strength', group='FAC', is_derived=False, value=si_magnet_cvs_maximum_strength, symbol=r'<math>\theta_\text{max,cvs}</math>', units=unicode('μrad', encoding='utf-8'), deps=[], obs=[]),
  Parameter(name='SI magnet chf maximum strength', group='FAC', is_derived=False, value=si_magnet_chf_maximum_strength, symbol=r'<math>\theta_\text{max,chf}</math>', units=unicode('μrad', encoding='utf-8'), deps=[], obs=[]),
  Parameter(name='SI magnet cvf maximum strength', group='FAC', is_derived=False, value=si_magnet_cvf_maximum_strength, symbol=r'<math>\theta_\text{max,cvf}</math>', units=unicode('μrad', encoding='utf-8'), deps=[], obs=[]),
  Parameter(name='SI magnet qs maximum strength',  group='FAC', is_derived=False, value=si_magnet_qs_maximum_strength,  symbol=r'<math>\theta_\text{max,qs}</math>',  units='m<sup>-1</sup>', deps=[], obs=[]),

  Parameter(name='SI optics default mode', group='FAC', is_derived=False, value=si_optics_default_mode, symbol='', units='', deps=['SI lattice version'], obs=[], ),
  Parameter(name='SI optics tune horizontal', group='FAC', is_derived=False, value=si_optics_tune_horizontal, symbol=r'<math>\nu_x</math>', units='', deps=['SI optics default mode'], obs=[], ),
  Parameter(name='SI optics tune vertical',   group='FAC', is_derived=False, value=si_optics_tune_vertical,   symbol=r'<math>\nu_y</math>', units='', deps=['SI optics default mode'], obs=[], ),
  Parameter(name='SI optics tune synchrotron dipole', group='FAC', is_derived=False, value=si_optics_tune_synchrotron_dipole, symbol=r'<math>\nu_{s,\text{dip}}</math>', units='', deps=['SI optics default mode'], obs=[], ),
  Parameter(name='SI optics tune synchrotron',        group='FAC', is_derived=False, value=si_optics_tune_synchrotron, symbol=r'<math>\nu_{s}</math>', units='', deps=['SI optics default mode'], obs=[], ),
  Parameter(name='SI optics betatron frequency horizontal', group='FAC', is_derived=True, value='frequency_from_tune("SI beam revolution frequency", "SI optics tune horizontal")', symbol=r'<math>f_x</math>', units='kHz', deps=[], ),
  Parameter(name='SI optics betatron frequency vertical', group='FAC', is_derived=True, value='frequency_from_tune("SI beam revolution frequency", "SI optics tune vertical")', symbol=r'<math>f_y</math>', units='kHz', deps=[], ),
  Parameter(name='SI optics synchrotron frequency', group='FAC', is_derived=True, value='frequency_from_tune("SI beam revolution frequency", "SI optics tune synchrotron")', symbol=r'<math>f_{s}</math>', units='kHz', deps=[], ),
  Parameter(name='SI optics natural linear chromaticity horizontal', group='FAC', is_derived=False, value=si_optics_natural_chromaticity_horizontal, symbol=r'<math>\xi_{0, x}</math>', units='', deps=['SI optics default mode'], obs=[], ),
  Parameter(name='SI optics linear chromaticity horizontal', group='FAC', is_derived=False, value=si_optics_chromaticity_horizontal, symbol=r'<math>\xi_{x}</math>', units='', deps=['SI optics default mode'], obs=[], ),
  Parameter(name='SI optics natural linear chromaticity vertical', group='FAC', is_derived=False, value=si_optics_natural_chromaticity_vertical, symbol=r'<math>\xi_{0, y}</math>', units='', deps=['SI optics default mode'], obs=[], ),
  Parameter(name='SI optics linear chromaticity vertical', group='FAC', is_derived=False, value=si_optics_chromaticity_vertical, symbol=r'<math>\xi_{y}</math>', units='', deps=['SI optics default mode'], obs=[], ),
  Parameter(name='SI optics beam size horizontal long straight section',  group='FAC', is_derived=False, value=si_optics_beam_size_horizontal_long_straight_section,  symbol=r'<math>\sigma_\text{x, lss}</math>', units=unicode('μm',encoding='utf-8'), deps=['SI optics default mode'], obs=[r'<math>\sigma_\text{x, lss} = \sqrt{\epsilon_x \beta_{x, \text{lss}} + \left(\sigma_\delta \eta_{x, \text{lss}}\right)^2}</math>'], ),
  Parameter(name='SI optics beam size horizontal short straight section', group='FAC', is_derived=False, value=si_optics_beam_size_horizontal_short_straight_section, symbol=r'<math>\sigma_\text{x, sss}</math>', units=unicode('μm',encoding='utf-8'), deps=['SI optics default mode'], obs=[r'<math>\sigma_\text{x, sss} = \sqrt{\epsilon_x \beta_{x, \text{sss}} + \left(\sigma_\delta \eta_{x, \text{sss}}\right)^2}</math>'], ),
  Parameter(name='SI optics beam size horizontal dipole bc',              group='FAC', is_derived=False, value=si_optics_beam_size_horizontal_dipole_bc, symbol=r'<math>\sigma_\text{x, bc}</math>', units=unicode('μm',encoding='utf-8'), deps=['SI optics default mode'], obs=[r'<math>\sigma_\text{x, bc} = \sqrt{\epsilon_x \beta_{x, \text{bc}} + \left(\sigma_\delta \eta_{x, \text{bc}}\right)^2}</math>'], ),
  Parameter(name='SI optics beam size vertical long straight section',  group='FAC', is_derived=False, value=si_optics_beam_size_vertical_long_straight_section,  symbol=r'<math>\sigma_\text{y, lss}</math>', units=unicode('μm',encoding='utf-8'), deps=['SI optics default mode'], obs=[r'<math>\sigma_\text{y, lss} = \sqrt{\epsilon_y \beta_{y, \text{lss}} + \left(\sigma_\delta \eta_{y, \text{lss}}\right)^2}</math>'], ),
  Parameter(name='SI optics beam size vertical short straight section', group='FAC', is_derived=False, value=si_optics_beam_size_vertical_short_straight_section, symbol=r'<math>\sigma_\text{y, sss}</math>', units=unicode('μm',encoding='utf-8'), deps=['SI optics default mode'], obs=[r'<math>\sigma_\text{y, sss} = \sqrt{\epsilon_y \beta_{y, \text{sss}} + \left(\sigma_\delta \eta_{y, \text{sss}}\right)^2}</math>'], ),
  Parameter(name='SI optics beam size vertical dipole bc',              group='FAC', is_derived=False, value=si_optics_beam_size_vertical_dipole_bc, symbol=r'<math>\sigma_\text{y, bc}</math>', units=unicode('μm',encoding='utf-8'), deps=['SI optics default mode'], obs=[r'<math>\sigma_\text{y, bc} = \sqrt{\epsilon_y \beta_{y, \text{bc}} + \left(\sigma_\delta \eta_{y, \text{bc}}\right)^2}</math>'], ),
  Parameter(name='SI optics beam divergence horizontal long straight section',  group='FAC', is_derived=False, value=si_optics_beam_divergence_horizontal_long_straight_section,  symbol=r"<math>\sigma_\text{x', lss}</math>", units=unicode('μrad',encoding='utf-8'), deps=['SI optics default mode'], obs=[r"<math>\sigma_\text{x', lss} = \sqrt{\epsilon_x \gamma_{x, \text{lss}} + \left(\sigma_\delta \eta'_{x, \text{lss}}\right)^2}</math>"], ),
  Parameter(name='SI optics beam divergence horizontal short straight section', group='FAC', is_derived=False, value=si_optics_beam_divergence_horizontal_short_straight_section, symbol=r"<math>\sigma_\text{x', sss}</math>", units=unicode('μrad',encoding='utf-8'), deps=['SI optics default mode'], obs=[r"<math>\sigma_\text{x', sss} = \sqrt{\epsilon_x \gamma_{x, \text{sss}} + \left(\sigma_\delta \eta'_{x, \text{sss}}\right)^2}</math>"], ),
  Parameter(name='SI optics beam divergence horizontal dipole bc',              group='FAC', is_derived=False, value=si_optics_beam_divergence_horizontal_dipole_bc, symbol=r"<math>\sigma_\text{x', bc}</math>", units=unicode('μrad',encoding='utf-8'), deps=['SI optics default mode'], obs=[r"<math>\sigma_\text{x', bc} = \sqrt{\epsilon_x \gamma_{x, \text{bc}} + \left(\sigma_\delta \eta'_{x, \text{bc}}\right)^2}</math>"], ),
  Parameter(name='SI optics beam divergence vertical long straight section',  group='FAC', is_derived=False, value=si_optics_beam_divergence_vertical_long_straight_section,  symbol=r"<math>\sigma_\text{y', lss}</math>", units=unicode('μrad',encoding='utf-8'), deps=['SI optics default mode'], obs=[r"<math>\sigma_\text{y', lss} = \sqrt{\epsilon_y \gamma_{y, \text{lss}} + \left(\sigma_\delta \eta'_{y, \text{lss}}\right)^2}</math>"], ),
  Parameter(name='SI optics beam divergence vertical short straight section', group='FAC', is_derived=False, value=si_optics_beam_divergence_vertical_short_straight_section, symbol=r"<math>\sigma_\text{y', sss}</math>", units=unicode('μrad',encoding='utf-8'), deps=['SI optics default mode'], obs=[r"<math>\sigma_\text{y', sss} = \sqrt{\epsilon_y \gamma_{y, \text{sss}} + \left(\sigma_\delta \eta'_{y, \text{sss}}\right)^2}</math>"], ),
  Parameter(name='SI optics beam divergence vertical dipole bc',              group='FAC', is_derived=False, value=si_optics_beam_divergence_vertical_dipole_bc, symbol=r"<math>\sigma_\text{y', bc}</math>", units=unicode('μrad',encoding='utf-8'), deps=['SI optics default mode'], obs=[r"<math>\sigma_\text{y', bc} = \sqrt{\epsilon_y \gamma_{y, \text{bc}} + \left(\sigma_\delta \eta'_{y, \text{bc}}\right)^2}</math>"], ),
  Parameter(name='SI optics radiation integral i1 dipole', group='FAC', is_derived=False, value=si_optics_radiation_integral_i1_dipole, symbol=r'<math>I_\text{1,dip}</math>', units='m', deps=['SI beam magnetic rigidity', 'SI optics default mode'], obs=[r'<math>I_\text{1,dip} = \oint{\frac{\eta_x}{\rho_x}\,ds}</math>'], ),
  Parameter(name='SI optics radiation integral i2 dipole', group='FAC', is_derived=False, value=si_optics_radiation_integral_i2_dipole, symbol=r'<math>I_\text{2,dip}</math>', units='m<sup>-1</sup>', deps=['SI beam magnetic rigidity', 'SI optics default mode'], obs=[r'<math>I_\text{2,dip} = \oint{\frac{1}{\rho_x^2}\,ds}</math>'], ),
  Parameter(name='SI optics radiation integral i3 dipole', group='FAC', is_derived=False, value=si_optics_radiation_integral_i3_dipole, symbol=r'<math>I_\text{3,dip}</math>', units='m<sup>-2</sup>', deps=['SI beam magnetic rigidity', 'SI optics default mode'], obs=[r'<math>I_\text{3,dip} = \oint{\frac{1}{|\rho_x|^3}\,ds}</math>'], ),
  Parameter(name='SI optics radiation integral i4 dipole', group='FAC', is_derived=False, value=si_optics_radiation_integral_i4_dipole, symbol=r'<math>I_\text{4,dip}</math>', units='m<sup>-1</sup>', deps=['SI beam magnetic rigidity', 'SI optics default mode'], obs=[r'<math>I_\text{4,dip} = \frac{\eta_x(s_0) \tan \theta(s_0)}{\rho_x^2} + \oint{\frac{\eta_x}{\rho_x^3} \left(1 + 2 \rho_x^2 k\right)\,ds} + \frac{\eta_x(s_1) \tan \theta(s_1)}{\rho_x^2}</math>'], ),
  Parameter(name='SI optics radiation integral i5 dipole', group='FAC', is_derived=False, value=si_optics_radiation_integral_i5_dipole, symbol=r'<math>I_\text{5,dip}</math>', units='m<sup>-1</sup>', deps=['SI beam magnetic rigidity', 'SI optics default mode'], obs=[r'<math>I_\text{5,dip} = \oint{\frac{H_x}{|\rho_x|^3}\,ds}</math>', r"<math>H_x \equiv \gamma_x \eta_x^2 + 2 \alpha_x \eta_x \eta_x^' + \beta_x {\eta_x^'}^2</math>"], ),
  Parameter(name='SI optics radiation integral i6 dipole', group='FAC', is_derived=False, value=si_optics_radiation_integral_i6_dipole, symbol=r'<math>I_\text{6,dip}</math>', units='m<sup>-1</sup>', deps=['SI beam magnetic rigidity', 'SI optics default mode'], obs=[r'<math>I_\text{6,dip} = \oint{k^2 \eta_x^2\,ds}</math>'], ),
  Parameter(name='SI optics radiation integral i1 id', group='FAC', is_derived=False, value=si_optics_radiation_integral_i1_id, symbol=r'<math>I_\text{1,id}</math>', units='m', deps=['SI beam magnetic rigidity', 'SI optics default mode'], obs=[r'<math>I_\text{1,id} = \oint{\frac{\eta_x}{\rho_x}\,ds}</math>'], ),
  Parameter(name='SI optics radiation integral i2 id', group='FAC', is_derived=False, value=si_optics_radiation_integral_i2_id, symbol=r'<math>I_\text{2,id}</math>', units='m<sup>-1</sup>', deps=['SI beam magnetic rigidity', 'SI optics default mode'], obs=[r'<math>I_\text{2,id} = \oint{\frac{1}{\rho_x^2}\,ds}</math>'], ),
  Parameter(name='SI optics radiation integral i3 id', group='FAC', is_derived=False, value=si_optics_radiation_integral_i3_id, symbol=r'<math>I_\text{3,id}</math>', units='m<sup>-2</sup>', deps=['SI beam magnetic rigidity', 'SI optics default mode'], obs=[r'<math>I_\text{3,id} = \oint{\frac{1}{|\rho_x|^3}\,ds}</math>'], ),
  Parameter(name='SI optics radiation integral i4 id', group='FAC', is_derived=False, value=si_optics_radiation_integral_i4_id, symbol=r'<math>I_\text{4,id}</math>', units='m<sup>-1</sup>', deps=['SI beam magnetic rigidity', 'SI optics default mode'], obs=[r'<math>I_\text{4,id} = \frac{\eta_x(s_0) \tan \theta(s_0)}{\rho_x^2} + \oint{\frac{\eta_x}{\rho_x^3} \left(1 + 2 \rho_x^2 k\right)\,ds} + \frac{\eta_x(s_1) \tan \theta(s_1)}{\rho_x^2}</math>'], ),
  Parameter(name='SI optics radiation integral i5 id', group='FAC', is_derived=False, value=si_optics_radiation_integral_i5_id, symbol=r'<math>I_\text{5,id}</math>', units='m<sup>-1</sup>', deps=['SI beam magnetic rigidity', 'SI optics default mode'], obs=[r'<math>I_\text{5,id} = \oint{\frac{H_x}{|\rho_x|^3}\,ds}</math>', r"<math>H_x \equiv \gamma_x \eta_x^2 + 2 \alpha_x \eta_x \eta_x^' + \beta_x {\eta_x^'}^2</math>"], ),
  Parameter(name='SI optics radiation integral i6 id', group='FAC', is_derived=False, value=si_optics_radiation_integral_i6_id, symbol=r'<math>I_\text{6,id}</math>', units='m<sup>-1</sup>', deps=['SI beam magnetic rigidity', 'SI optics default mode'], obs=[r'<math>I_\text{6,id} = \oint{k^2 \eta_x^2\,ds}</math>'], ),
  Parameter(name='SI optics radiation integral i1', group='FAC', is_derived=True, value='("SI optics radiation integral i1 dipole" + "SI optics radiation integral i1 id")', symbol=r'<math>I_\text{1}</math>', units='m', deps=[], ),
  Parameter(name='SI optics radiation integral i2', group='FAC', is_derived=True, value='("SI optics radiation integral i2 dipole" + "SI optics radiation integral i2 id")', symbol=r'<math>I_\text{2}</math>', units='m<sup>-1</sup>', deps=[], ),
  Parameter(name='SI optics radiation integral i3', group='FAC', is_derived=True, value='("SI optics radiation integral i3 dipole" + "SI optics radiation integral i3 id")', symbol=r'<math>I_\text{3}</math>', units='m<sup>-2</sup>', deps=[], ),
  Parameter(name='SI optics radiation integral i4', group='FAC', is_derived=True, value='("SI optics radiation integral i4 dipole" + "SI optics radiation integral i4 id")', symbol=r'<math>I_\text{4}</math>', units='m<sup>-1</sup>', deps=[], ),
  Parameter(name='SI optics radiation integral i5', group='FAC', is_derived=True, value='("SI optics radiation integral i5 dipole" + "SI optics radiation integral i5 id")', symbol=r'<math>I_\text{5}</math>', units='m<sup>-1</sup>', deps=[], ),
  Parameter(name='SI optics radiation integral i6', group='FAC', is_derived=True, value='("SI optics radiation integral i6 dipole" + "SI optics radiation integral i6 id")', symbol=r'<math>I_\text{6}</math>', units='m<sup>-1</sup>', deps=[], ),
  Parameter(name='SI optics transverse coupling', group='FAC', is_derived=False, value=si_optics_transverse_coupling, symbol=r'<math>\kappa</math>', units='%', deps=['SI optics default mode'], obs=[], ),
  Parameter(name='SI optics damping partition number vertical dipole', group='FAC', is_derived=False, value=si_optics_damping_partition_number_vertical_dipole, symbol=r'<math>J_{\text{y, dip}}</math>', units='', deps=[], obs=['Vertical damping partition number is identically one for error-free machines for which vertical dispersion functions are zero everywhere.', r'<math>J_{\text{y, dip}} = 1 - \frac{I_\text{4y,dip}}{I_\text{2,dip}} \equiv 1</math>'], ),
  Parameter(name='SI optics damping partition number horizontal dipole', group='FAC', is_derived=True, value='Jx("SI optics radiation integral i2 dipole", "SI optics radiation integral i4 dipole")', symbol=r'<math>J_{\text{x, dip}}</math>', units='', deps=[], ),
  Parameter(name='SI optics damping partition number longitudinal dipole', group='FAC', is_derived=True, value='Js("SI optics damping partition number horizontal dipole", "SI optics damping partition number vertical dipole")', symbol=r'<math>J_{\text{s, dip}}</math>', units='', deps=[], ),
  Parameter(name='SI optics energy loss per turn dipole', group='FAC', is_derived=True, value='U0("SI beam energy", "SI optics radiation integral i2 dipole")', symbol=r'<math>U_\text{0,dip}</math>',   units='keV', deps=[], ),
  Parameter(name='SI optics radiation power dipole', group='FAC', is_derived=True, value='radiation_power("SI optics energy loss per turn dipole", "SI beam current")', symbol=r'<math>P_{\text{dip}}</math>', units='kW',    deps=[], ),
  Parameter(name='SI optics overvoltage dipole', group='FAC', is_derived=True, value='overvoltage("SI rf peak voltage", "SI optics energy loss per turn dipole")', symbol=r'<math>q_\text{dip}</math>', units='', deps=[], ),
  Parameter(name='SI optics synchronous phase dipole', group='FAC', is_derived=True, value='sync_phase("SI optics overvoltage dipole")', symbol=r'<math>\phi_0</math>', units=unicode('°',encoding='utf-8'), deps=[], ),
  Parameter(name='SI optics linear momentum compaction dipole', group='FAC', is_derived=True, value='alpha1("SI optics radiation integral i1 dipole", "SI lattice circumference")', symbol=r'<math>\alpha_\text{1,dip}</math>', units='', deps=[], ),
  Parameter(name='SI optics linear slip phase dipole', group='FAC', is_derived=True, value='slip_factor("SI optics linear momentum compaction dipole", "SI beam gamma factor")', symbol=r'<math>\eta_{1,\text{dip}}</math>', units='', deps=[], ),
  Parameter(name='SI optics rf energy acceptance dipole', group='FAC', is_derived=True, value='rf_energy_acceptance("SI optics overvoltage dipole", "SI beam energy", "SI optics energy loss per turn dipole", "SI rf harmonic number", "SI optics linear momentum compaction dipole")', symbol=r'<math>\epsilon_{\text{max},\text{dip}}</math>', units='%', deps=[], ),
  Parameter(name='SI optics natural emittance dipole', group='FAC', is_derived=True, value='natural_emittance("SI beam gamma factor", "SI optics damping partition number horizontal dipole", "SI optics radiation integral i2 dipole", "SI optics radiation integral i5 dipole")', symbol=r'<math>\epsilon_{0,\text{dip}}</math>', units=unicode('nm⋅rad',encoding='utf-8'), deps=[], ),
  Parameter(name='SI optics natural energy spread dipole', group='FAC', is_derived=True, value='energy_spread("SI beam gamma factor", "SI optics radiation integral i2 dipole", "SI optics radiation integral i3 dipole", "SI optics radiation integral i4 dipole")', symbol=r'<math>\sigma_{\delta,\text{dip}}</math>', units='%', deps=[], ),
  Parameter(name='SI optics natural bunch length dipole', group='FAC', is_derived=True, value='bunch_length("SI optics linear slip phase dipole", "SI optics natural energy spread dipole", "SI optics synchrotron frequency")', symbol=r'<math>\sigma_{\text{s, dip}}</math>', units='mm', deps=[], ),
  Parameter(name='SI optics natural bunch duration dipole', group='FAC', is_derived=True, value='bunch_duration("SI optics natural bunch length dipole", "SI beam beta factor")', symbol=r'<math>\sigma_{\text{t, dip}}</math>', units='ps', deps=[], ),
  Parameter(name='SI optics radiation damping time horizontal dipole', group='FAC', is_derived=True, value='damping_time("SI beam energy", "SI optics radiation integral i2 dipole", "SI optics damping partition number horizontal dipole", "SI lattice circumference")', symbol=r'<math>\alpha_{\text{x, dip}}</math>', units='ms', deps=[], ),
  Parameter(name='SI optics radiation damping time vertical dipole', group='FAC', is_derived=True, value='damping_time("SI beam energy", "SI optics radiation integral i2 dipole", "SI optics damping partition number vertical dipole", "SI lattice circumference")', symbol=r'<math>\alpha_{\text{y, dip}}</math>', units='ms', deps=[], ),
  Parameter(name='SI optics radiation damping time longitudinal dipole', group='FAC', is_derived=True, value='damping_time("SI beam energy", "SI optics radiation integral i2 dipole", "SI optics damping partition number longitudinal dipole", "SI lattice circumference")', symbol=r'<math>\alpha_{\text{s, dip}}</math>', units='ms', deps=[], ),
  Parameter(name='SI optics energy loss per turn id', group='FAC',is_derived=True, value='U0("SI beam energy", "SI optics radiation integral i2 id")', symbol=r'<math>U_\text{0,id}</math>', units='keV', deps=[], ),
  Parameter(name='SI optics damping partition number vertical', group='FAC', is_derived=False, value=si_optics_damping_partition_number_vertical, symbol=r'<math>J_{\text{y}}</math>', units='', deps=[], obs=['Vertical damping partition number is identically one for error-free machines for which vertical dispersion functions are zero everywhere.', r'<math>J_{\text{y}} = 1 - \frac{I_\text{4y,dip}}{I_\text{2}} \equiv 1</math>'], ),
  Parameter(name='SI optics damping partition number horizontal', group='FAC', is_derived=True, value='Jx("SI optics radiation integral i2", "SI optics radiation integral i4")', symbol=r'<math>J_{\text{x}}</math>', units='', deps=[], ),
  Parameter(name='SI optics damping partition number longitudinal', group='FAC', is_derived=True, value='Js("SI optics damping partition number horizontal", "SI optics damping partition number vertical")', symbol=r'<math>J_{\text{s}}</math>', units='', deps=[], ),
  Parameter(name='SI optics energy loss per turn', group='FAC', is_derived=True, value='U0("SI beam energy", "SI optics radiation integral i2")', symbol=r'<math>U_\text{0}</math>',   units='keV', deps=[], ),
  Parameter(name='SI optics radiation power', group='FAC', is_derived=True, value='radiation_power("SI optics energy loss per turn", "SI beam current")', symbol=r'<math>P</math>', units='kW',    deps=[], ),
  Parameter(name='SI optics overvoltage', group='FAC', is_derived=True, value='overvoltage("SI rf peak voltage", "SI optics energy loss per turn")', symbol=r'<math>q</math>', units='', deps=[], ),
  Parameter(name='SI optics synchronous phase', group='FAC', is_derived=True, value='sync_phase("SI optics overvoltage")', symbol=r'<math>\phi_0</math>', units=unicode('°',encoding='utf-8'), deps=[], ),
  Parameter(name='SI optics linear momentum compaction', group='FAC', is_derived=True, value='alpha1("SI optics radiation integral i1", "SI lattice circumference")', symbol=r'<math>\alpha_\text{1}</math>', units='', deps=[], ),
  Parameter(name='SI optics linear slip phase', group='FAC', is_derived=True, value='slip_factor("SI optics linear momentum compaction", "SI beam gamma factor")', symbol=r'<math>\eta_{1}</math>', units='', deps=[], ),
  Parameter(name='SI optics rf energy acceptance', group='FAC', is_derived=True, value='rf_energy_acceptance("SI optics overvoltage", "SI beam energy", "SI optics energy loss per turn", "SI rf harmonic number", "SI optics linear momentum compaction")', symbol=r'<math>\epsilon_{\text{max}}</math>', units='%', deps=[], ),
  Parameter(name='SI optics natural emittance', group='FAC', is_derived=True, value='natural_emittance("SI beam gamma factor", "SI optics damping partition number horizontal", "SI optics radiation integral i2", "SI optics radiation integral i5")', symbol=r'<math>\epsilon_{0}</math>', units=unicode('nm⋅rad',encoding='utf-8'), deps=[], ),
  Parameter(name='SI optics natural energy spread', group='FAC', is_derived=True, value='energy_spread("SI beam gamma factor", "SI optics radiation integral i2", "SI optics radiation integral i3", "SI optics radiation integral i4")', symbol=r'<math>\sigma_{\delta,\text{dip}}</math>', units='%', deps=[], ),
  Parameter(name='SI optics natural bunch length', group='FAC', is_derived=True, value='bunch_length("SI optics linear slip phase", "SI optics natural energy spread", "SI optics synchrotron frequency")', symbol=r'<math>\sigma_{\text{s, dip}}</math>', units='mm', deps=[], ),
  Parameter(name='SI optics natural bunch duration', group='FAC', is_derived=True, value='bunch_duration("SI optics natural bunch length", "SI beam beta factor")', symbol=r'<math>\sigma_{\text{t, dip}}</math>', units='ps', deps=[], ),
  Parameter(name='SI optics radiation damping time horizontal', group='FAC', is_derived=True, value='damping_time("SI beam energy", "SI optics radiation integral i2", "SI optics damping partition number horizontal", "SI lattice circumference")', symbol=r'<math>\alpha_{\text{x, dip}}</math>', units='ms', deps=[], ),
  Parameter(name='SI optics radiation damping time vertical', group='FAC', is_derived=True, value='damping_time("SI beam energy", "SI optics radiation integral i2", "SI optics damping partition number vertical", "SI lattice circumference")', symbol=r'<math>\alpha_{\text{y, dip}}</math>', units='ms', deps=[], ),
  Parameter(name='SI optics radiation damping time longitudinal', group='FAC', is_derived=True, value='damping_time("SI beam energy", "SI optics radiation integral i2", "SI optics damping partition number longitudinal", "SI lattice circumference")', symbol=r'<math>\alpha_{\text{s, dip}}</math>', units='ms', deps=[], ),

  Parameter(name='SI error alignment dipole', group='FAC', is_derived=False, value=si_error_alignment_dipole, symbol=r'<math>E_{xy,\text{dip}}</math>', units=unicode('μm', encoding='utf-8'), deps=[], obs=[r'Random transverse position error (standard deviation) for <math>x</math> and <math>y</math>.', unicode('Simulations assume Gaussian distribution truncated at ±2σ.', encoding='utf-8')], ),
  Parameter(name='SI error alignment quadrupole', group='FAC', is_derived=False, value=si_error_alignment_quadrupole, symbol=r'<math>E_{xy,\text{quad}}</math>', units=unicode('μm', encoding='utf-8'), deps=[], obs=[r'Random transverse position error (standard deviation) for <math>x</math> and <math>y</math>.', unicode('Simulations assume Gaussian distribution truncated at ±2σ.', encoding='utf-8')], ),
  Parameter(name='SI error alignment sextupole', group='FAC', is_derived=False, value=si_error_alignment_sextupole, symbol=r'<math>E_{xy,\text{sext}}</math>', units=unicode('μm', encoding='utf-8'), deps=[], obs=[r'Random transverse position error (standard deviation) for <math>x</math> and <math>y</math>.', unicode('Simulations assume Gaussian distribution truncated at ±2σ.', encoding='utf-8')], ),
  Parameter(name='SI error roll dipole', group='FAC', is_derived=False, value=si_error_roll_dipole, symbol=r'<math>E_{\theta,\text{dip}}</math>', units='mrad', deps=[], obs=[r'Random rotation error (standard deviation) around longitudinal axis.', unicode('Simulations assume Gaussian distribution truncated at ±2σ.', encoding='utf-8')], ),
  Parameter(name='SI error roll quadrupole', group='FAC', is_derived=False, value=si_error_roll_quadrupole, symbol=r'<math>E_{\theta,\text{quad}}</math>', units='mrad', deps=[], obs=[r'Random rotation error (standard deviation) around longitudinal axis.', unicode('Simulations assume Gaussian distribution truncated at ±2σ.', encoding='utf-8')], ),
  Parameter(name='SI error roll sextupole', group='FAC', is_derived=False, value=si_error_roll_sextupole, symbol=r'<math>E_{\theta,\text{sext}}</math>', units='mrad', deps=[], obs=[r'Random rotation error (standard deviation) around longitudinal axis.', unicode('Simulations assume Gaussian distribution truncated at ±2σ.', encoding='utf-8')], ),
  Parameter(name='SI error excitation dipole', group='FAC', is_derived=False, value=si_error_excitation_dipole, symbol=r'<math>E_{\text{exc,dip}}</math>', units='%', deps=[], obs=[r'Static or low frequency random excitation error (standard deviation).', unicode('Simulations assume Gaussian distribution truncated at ±2σ.', encoding='utf-8')], ),
  Parameter(name='SI error excitation quadrupole', group='FAC', is_derived=False, value=si_error_excitation_quadrupole, symbol=r'<math>E_{\text{exc,quad}}</math>', units='%', deps=[], obs=[r'Static or low frequency random excitation error (standard deviation).', unicode('Simulations assume Gaussian distribution truncated at ±2σ.', encoding='utf-8')], ),
  Parameter(name='SI error excitation sextupole', group='FAC', is_derived=False, value=si_error_excitation_sextupole, symbol=r'<math>E_{\text{exc,sext}}</math>', units='%', deps=[], obs=[r'Static or low frequency random excitation error (standard deviation).', unicode('Simulations assume Gaussian distribution truncated at ±2σ.', encoding='utf-8')], ),
  Parameter(name='SI error ripple dipole',     group='FAC', is_derived=False, value=si_error_ripple_dipole, symbol=r'<math>E_\text{ripp, dip}</math>', units='ppm', deps=[], obs=[], ),
  Parameter(name='SI error ripple quadrupole', group='FAC', is_derived=False, value=si_error_ripple_quadrupole, symbol=r'<math>E_\text{ripp, quad}</math>', units='ppm', deps=[], obs=[], ),
  Parameter(name='SI error ripple sextupole',  group='FAC', is_derived=False, value=si_error_ripple_sextupole, symbol=r'<math>E_\text{ripp, sext}</math>', units='ppm', deps=[], obs=[], ),
  Parameter(name='SI error vibration dipole', group='FAC', is_derived=False, value=si_error_vibration_dipole, symbol=r'<math>E_\text{vib, dip}</math>', units='nm', deps=[], obs=[], ),
  Parameter(name='SI error vibration quadrupole', group='FAC', is_derived=False, value=si_error_vibration_quadrupole, symbol=r'<math>E_\text{vib, quad}</math>', units='nm', deps=[], obs=[], ),
  Parameter(name='SI error vibration sextupole', group='FAC', is_derived=False, value=si_error_vibration_sextupole, symbol=r'<math>E_\text{vib, sext}</math>', units='nm', deps=[], obs=[], ),
]
