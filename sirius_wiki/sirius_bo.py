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
bo_magnet_dipole_hardedge_length                = 1.152 #[m]
bo_magnet_dipole_integrated_quadrupole_strength = -0.2484 #[1/m]
bo_magnet_dipole_integrated_sextupole_strength  = -2.2685*1.152 #[1/m²]

bo_magnet_quadrupole_qf_number = 50
bo_magnet_quadrupole_qd_number = 25
bo_magnet_quadrupole_short_hardedge_length = 0.2 # [m]
bo_magnet_quadrupole_long_hardedge_length  = 0.2 # [m]
bo_magnet_quadrupole_qf_hardedge_length = bo_magnet_quadrupole_long_hardedge_length # [m]
bo_magnet_quadrupole_qd_hardedge_length = bo_magnet_quadrupole_short_hardedge_length # [m]

bo_magnet_sextupole_sf_number = 25
bo_magnet_sextupole_sd_number = 10
bo_magnet_sextupole_sf_hardedge_length = 0.2 # [m]
bo_magnet_sextupole_sd_hardedge_length = 0.2 # [m]
bo_magnet_sextupole_sf_maximum_strength = 10.000 # [1/m^3]
bo_magnet_sextupole_sd_maximum_strength = 10.000 # [1/m^3]
bo_magnet_quadrupole_qf_maximum_strength = 2.025 # [1/m^2]
bo_magnet_quadrupole_qd_maximum_strength = 0.250 # [1/m^2]

bo_bpm_number = 50
bo_magnet_ch_number = 25
bo_magnet_cv_number = 25
bo_magnet_ch_maximum_normalized_integrated_field = 0.35 # [mrad]
bo_magnet_cv_maximum_normalized_integrated_field = 0.35 # [mrad]

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

bo_error_alignment_bpm = 500 # [um]
bo_error_alignment_dipole = 100 # [μm]

bo_error_rotation_dipole = 0.5 # [mrad]

bo_error_excitation_dipole = 0.1 # [%]

bo_optics_extraction_damping_partition_number_vertical = 1.0

bo_error_alignment_quadrupole  = 100 # [μm]
bo_error_rotation_quadrupole   = 0.5 # [mrad]
bo_error_excitation_quadrupole = 0.2 # [%]

bo_error_alignment_sextupole = 100 # [μm]
bo_error_rotation_sextupole = 0.5 # [mrad]
bo_error_excitation_sextupole = 0.2 # [%]

bo_error_multipole_dipole_reference_position = 17.5 # [mm]

bo_error_multipole_dipole_systematic_normal_8_pole  =  4.0e-4 # segmented model of the dipole shows much
bo_error_multipole_dipole_systematic_normal_10_pole = -3.6e-4 # lower multipole errors. Nevertheless these values are
bo_error_multipole_dipole_systematic_normal_12_pole =  2.7e-4 # kept as spec for real measurements.
bo_error_multipole_dipole_systematic_normal_14_pole = -1.3e-4

bo_error_multipole_dipole_random_normal_6_pole      =  5.5e-4
bo_error_multipole_dipole_random_normal_8_pole      =  4.0e-4
bo_error_multipole_dipole_random_normal_10_pole     =  4.0e-4
bo_error_multipole_dipole_random_normal_12_pole     =  4.0e-4
bo_error_multipole_dipole_random_normal_14_pole     =  4.0e-4
bo_error_multipole_dipole_random_normal_16_pole     =  4.0e-4
bo_error_multipole_dipole_random_normal_18_pole     =  4.0e-4

bo_error_multipole_dipole_random_skew_6_pole        =  1.0e-4
bo_error_multipole_dipole_random_skew_8_pole        =  1.0e-4
bo_error_multipole_dipole_random_skew_10_pole       =  1.0e-4
bo_error_multipole_dipole_random_skew_12_pole       =  1.0e-4
bo_error_multipole_dipole_random_skew_14_pole       =  1.0e-4
bo_error_multipole_dipole_random_skew_16_pole       =  1.0e-4
bo_error_multipole_dipole_random_skew_18_pole       =  1.0e-4

bo_error_multipole_quadrupole_reference_position = 17.5 # [mm]

bo_error_multipole_quadrupole_systematic_normal_12_pole = -1.00e-3
bo_error_multipole_quadrupole_systematic_normal_20_pole = +1.10e-3
bo_error_multipole_quadrupole_systematic_normal_28_pole = +0.08e-3

bo_error_multipole_quadrupole_random_normal_6_pole  = 7.0e-4
bo_error_multipole_quadrupole_random_normal_8_pole  = 4.0e-4

bo_error_multipole_quadrupole_random_normal_10_pole = 4.0e-4
bo_error_multipole_quadrupole_random_normal_12_pole = 4.0e-4
bo_error_multipole_quadrupole_random_normal_14_pole = 4.0e-4
bo_error_multipole_quadrupole_random_normal_16_pole = 4.0e-4
bo_error_multipole_quadrupole_random_normal_18_pole = 4.0e-4
bo_error_multipole_quadrupole_random_normal_20_pole = 4.0e-4

bo_error_multipole_quadrupole_random_skew_6_pole    =10.0e-4
bo_error_multipole_quadrupole_random_skew_8_pole    = 5.0e-4
bo_error_multipole_quadrupole_random_skew_10_pole   = 1.0e-4
bo_error_multipole_quadrupole_random_skew_12_pole   = 1.0e-4
bo_error_multipole_quadrupole_random_skew_14_pole   = 1.0e-4
bo_error_multipole_quadrupole_random_skew_16_pole   = 1.0e-4
bo_error_multipole_quadrupole_random_skew_18_pole   = 1.0e-4
bo_error_multipole_quadrupole_random_skew_20_pole   = 1.0e-4

bo_error_multipole_sextupole_reference_position = 17.5 # [mm]

bo_error_multipole_sextupole_systematic_normal_18_pole = -2.4e-2
bo_error_multipole_sextupole_systematic_normal_30_pole = -1.7e-2

bo_error_multipole_sextupole_random_normal_8_pole  = 4.0e-4
bo_error_multipole_sextupole_random_normal_10_pole = 4.0e-4
bo_error_multipole_sextupole_random_normal_12_pole = 4.0e-4
bo_error_multipole_sextupole_random_normal_14_pole = 4.0e-4
bo_error_multipole_sextupole_random_normal_16_pole = 4.0e-4
bo_error_multipole_sextupole_random_normal_18_pole = 4.0e-5
bo_error_multipole_sextupole_random_normal_20_pole = 4.0e-5

bo_error_multipole_sextupole_random_skew_8_pole    = 1.0e-4
bo_error_multipole_sextupole_random_skew_10_pole   = 1.0e-4
bo_error_multipole_sextupole_random_skew_12_pole   = 1.0e-4
bo_error_multipole_sextupole_random_skew_14_pole   = 1.0e-4
bo_error_multipole_sextupole_random_skew_16_pole   = 1.0e-4
bo_error_multipole_sextupole_random_skew_18_pole   = 1.0e-4
bo_error_multipole_sextupole_random_skew_20_pole   = 1.0e-4

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
    Parameter(name='BO rf extraction wavelength', group='FAC', is_derived=True, value='rf_wavelength("BO rf extraction frequency")', symbol=r'<math>\lambda_\text{RF}</math>', units=u'm', deps=[], obs=[r'<math>\lambda_\text{RF} = \frac{c}{f_\text{RF}}</math>'], ),

    Parameter(name='BO magnet dipole number',                         group='FAC', is_derived=False, value=bo_magnet_dipole_number, symbol=r'<math>N_\text{dip}</math>', units='', deps=[], obs=[], ),
    Parameter(name='BO magnet dipole deflection angle',               group='FAC', is_derived=True, value='360.0/"BO magnet dipole number"', symbol=r'<math>\theta_\text{dip}</math>', units=unicode('°',encoding='utf-8'), deps=[], obs=[], ),
    Parameter(name='BO magnet dipole hardedge length',                group='FAC', is_derived=False, value=bo_magnet_dipole_hardedge_length, symbol=r'<math>L_\text{dip}</math>', units='m', deps=[], obs=[], ),
    Parameter(name='BO magnet dipole extraction integrated field', group='FAC', is_derived=True, value='"BO beam extraction magnetic rigidity" * deg2rad("BO magnet dipole deflection angle")', symbol=r'(BL)_{ext}', units='T.m', deps=[], obs=[], ),
    Parameter(name='BO magnet dipole integrated quadrupole strength', group='FAC', is_derived=False, value=bo_magnet_dipole_integrated_quadrupole_strength, symbol=r'<math>(LK)_\text{dip}</math>', units='m<sup>-1</sup>', deps=[], obs=[],),
    Parameter(name='BO magnet dipole integrated sextupole strength',  group='FAC', is_derived=False, value=bo_magnet_dipole_integrated_sextupole_strength, symbol=r'<math>(LS)_\text{dip}</math>', units='m<sup>-2</sup>', deps=[], obs=[],),

    Parameter(name='BO magnet dipole hardedge bending radius',  group='FAC', is_derived=True, value='"BO magnet dipole hardedge length"/deg2rad("BO magnet dipole deflection angle")', symbol=r'<math>\rho</math>', units='m', obs=[r'<math>\rho = \frac{L_\text{dip}}{\theta_\text{dip}}</math>'], ),
    Parameter(name='BO magnet dipole hardedge sagitta',         group='FAC', is_derived=True, value='1000 * "BO magnet dipole hardedge bending radius" * (1.0 - cos(0.5*deg2rad("BO magnet dipole deflection angle")))', symbol=r'<math>S_\text{inj,sag}</math>', units='mm', obs=[r'<math>S_\text{sag} = \rho (1 - \cos \theta / 2)</math>'],),
    Parameter(name='BO magnet dipole hardedge quadrupole strength',   group='FAC', is_derived=True,  value='"BO magnet dipole integrated quadrupole strength"/"BO magnet dipole hardedge length"', symbol=r'<math>K_\text{dip}</math>', units='m<sup>-2</sup>', obs=[r'<math>K_\text{dip} \equiv \frac{(LK)_\text{dip}}{L_\text{dip}}</math>'],),
    Parameter(name='BO magnet dipole hardedge sextupole strength',    group='FAC', is_derived=True,  value='"BO magnet dipole integrated sextupole strength"/"BO magnet dipole hardedge length"', symbol=r'<math>S_\text{dip}</math>', units='m<sup>-3</sup>', obs=[r'<math>S_\text{dip} \equiv \frac{(LS)_\text{dip}}{L_\text{dip}}</math>'],),

    Parameter(name='BO magnet dipole injection integrated field', group='FAC', is_derived=True, value='"BO beam injection magnetic rigidity"*deg2rad("BO magnet dipole deflection angle")', symbol=r'(BL)_{inj}', units='T.m', deps=[], obs=[], ),
    Parameter(name='BO magnet dipole injection hardedge magnetic field',  group='FAC', is_derived=True, value='"BO beam injection magnetic rigidity" / "BO magnet dipole hardedge bending radius"', symbol=r'<math>B_\text{inj}</math>', units='T', obs=[r'<math>B_\text{inj} = \frac{(B\rho)}{\rho}</math>'], ),
    Parameter(name='BO magnet dipole injection hardedge critical energy', group='FAC', is_derived=True, value='critical_energy("BO beam injection gamma factor", "BO magnet dipole hardedge bending radius")', symbol=r'<math>\epsilon_\text{c,inj}</math>', units='keV', obs=[r'<math>\epsilon_\text{c,inj} = \frac{3}{2} \hbar c \frac{\gamma_\text{inj}^3}{\rho}</math>'], ),
    Parameter(name='BO magnet dipole extraction integrated field', group='FAC', is_derived=True, value='"BO beam extraction magnetic rigidity"*deg2rad("BO magnet dipole deflection angle")', symbol=r'(BL)_{ext}', units='T.m', deps=[], obs=[], ),
    Parameter(name='BO magnet dipole extraction hardedge magnetic field',  group='FAC', is_derived=True, value='"BO beam extraction magnetic rigidity" / "BO magnet dipole hardedge bending radius"', symbol=r'<math>B_\text{ext}</math>', units='T', obs=[r'<math>B_\text{ext} = \frac{(B\rho)}{\rho}</math>'], ),
    Parameter(name='BO magnet dipole extraction hardedge critical energy', group='FAC', is_derived=True, value='critical_energy("BO beam extraction gamma factor", "BO magnet dipole hardedge bending radius")', symbol=r'<math>\epsilon_\text{c,ext}</math>', units='keV', obs=[r'<math>\epsilon_\text{c,ext} = \frac{3}{2} \hbar c \frac{\gamma_\text{ext}^3}{\rho}</math>'], ),

    Parameter(name='BO magnet dipole extraction quadrupole integrated gradient', group='FAC', is_derived=True, value='-1*"BO magnet dipole integrated quadrupole strength"*"BO beam extraction magnetic rigidity"', symbol=r'', units='T', deps=[], obs=[], ),
    Parameter(name='BO magnet dipole extraction quadrupole gradient', group='FAC', is_derived=True, value='"BO magnet dipole extraction quadrupole integrated gradient"/"BO magnet dipole hardedge length"', symbol=r'', units='T/m', deps=[], obs=[], ),
    Parameter(name='BO magnet dipole extraction sextupole integrated gradient', group='FAC', is_derived=True, value='-1*"BO magnet dipole integrated sextupole strength"*"BO beam extraction magnetic rigidity"', symbol=r'', units='T', deps=[], obs=[], ),
    Parameter(name='BO magnet dipole extraction sextupole gradient', group='FAC', is_derived=True, value='"BO magnet dipole extraction sextupole integrated gradient"/"BO magnet dipole hardedge length"', symbol=r'', units='T/m', deps=[], obs=[], ),

    Parameter(name='BO magnet dipole injection quadrupole integrated gradient', group='FAC', is_derived=True, value='-1*"BO magnet dipole integrated quadrupole strength"*"BO beam injection magnetic rigidity"', symbol=r'', units='T', deps=[], obs=[], ),
    Parameter(name='BO magnet dipole injection sextupole integrated gradient', group='FAC', is_derived=True, value='-1*"BO magnet dipole integrated sextupole strength"*"BO beam injection magnetic rigidity"', symbol=r'', units='T', deps=[], obs=[], ),
    Parameter(name='BO magnet dipole injection quadrupole gradient', group='FAC', is_derived=True, value='"BO magnet dipole injection quadrupole integrated gradient"/"BO magnet dipole hardedge length"', symbol=r'', units='T', deps=[], obs=[], ),
    Parameter(name='BO magnet dipole injection sextupole gradient', group='FAC', is_derived=True, value='"BO magnet dipole injection sextupole integrated gradient"/"BO magnet dipole hardedge length"', symbol=r'', units='T', deps=[], obs=[], ),

    Parameter(name='BO magnet quadrupole qf number', group='FAC', is_derived=False, value=bo_magnet_quadrupole_qf_number, symbol=r'<math>N_\text{QF}</math>', units='', deps=[], obs=[], ),
    Parameter(name='BO magnet quadrupole qf hardedge length', group='FAC', is_derived=False, value=bo_magnet_quadrupole_qf_hardedge_length, symbol=r'<math>L_\text{QF}</math>', units='m', deps='', obs=[], ),
    Parameter(name='BO magnet quadrupole qd number', group='FAC', is_derived=False, value=bo_magnet_quadrupole_qd_number, symbol=r'<math>N_\text{QD}</math>', units='', deps=[], obs=[], ),
    Parameter(name='BO magnet quadrupole qd hardedge length', group='FAC', is_derived=False, value=bo_magnet_quadrupole_qd_hardedge_length, symbol=r'<math>L_\text{QD}</math>', units='m', deps='', obs=[], ),

    Parameter(name='BO magnet sextupole sf number', group='FAC', is_derived=False, value=bo_magnet_sextupole_sf_number, symbol=r'<math>N_\text{SF}</math>', units='', deps=[], obs=[], ),
    Parameter(name='BO magnet sextupole sf hardedge length', group='FAC', is_derived=False, value=bo_magnet_sextupole_sf_hardedge_length, symbol=r'<math>L_\text{SF}</math>', units='m', deps='', obs=[], ),
    Parameter(name='BO magnet sextupole sd number', group='FAC', is_derived=False, value=bo_magnet_sextupole_sd_number, symbol=r'<math>N_\text{SD}</math>', units='', deps=[], obs=['Bipolar.'], ),
    Parameter(name='BO magnet sextupole sd hardedge length', group='FAC', is_derived=False, value=bo_magnet_sextupole_sd_hardedge_length, symbol=r'<math>L_\text{SD}</math>', units='m', deps='', obs=[], ),

    Parameter(name='BO magnet sextupole sf maximum strength', group='FAC', is_derived=False, value=bo_magnet_sextupole_sf_maximum_strength, symbol=r"<math>\frac{1}{2} S_\text{QF,max}</math>", units=unicode('m<sup>-3</sup>', encoding='utf-8'), deps=[], obs=[], ),
    Parameter(name='BO magnet sextupole injection sf maximum gradient', group='FAC', is_derived=True, value='"BO magnet sextupole sf maximum strength"*"BO beam injection magnetic rigidity"', symbol=r"<math>\frac{1}{2} B''_\text{SF,max,inj}</math>", units=unicode('T·m<sup>-2</sup>', encoding='utf-8'), deps=[], obs=[], ),
    Parameter(name='BO magnet sextupole extraction sf maximum gradient', group='FAC', is_derived=True, value='"BO magnet sextupole sf maximum strength"*"BO beam extraction magnetic rigidity"', symbol=r"<math>\frac{1}{2} B''_\text{SF,max,ext}</math>", units=unicode('T·m<sup>-2</sup>', encoding='utf-8'), deps=[], obs=[],  ),
    Parameter(name='BO magnet sextupole sd maximum strength', group='FAC', is_derived=False, value=bo_magnet_sextupole_sd_maximum_strength, symbol=r"<math>\frac{1}{2} S_\text{SD,max}</math>", units=unicode('m<sup>-3</sup>', encoding='utf-8'), deps=[], obs=[], ),
    Parameter(name='BO magnet sextupole injection sd maximum gradient', group='FAC', is_derived=True, value='"BO magnet sextupole sd maximum strength"*"BO beam injection magnetic rigidity"', symbol=r"<math>\frac{1}{2} B''_\text{SD,max,inj}</math>", units=unicode('T·m<sup>-2</sup>', encoding='utf-8'), deps=[], obs=['Bipolar.'], ),
    Parameter(name='BO magnet sextupole extraction sd maximum gradient', group='FAC', is_derived=True, value='"BO magnet sextupole sd maximum strength"*"BO beam extraction magnetic rigidity"', symbol=r"<math>\frac{1}{2} B'_\text{SD,max,ext}</math>", units=unicode('T·m<sup>-2</sup>', encoding='utf-8'), deps=[], obs=['Bipolar.'], ),

    Parameter(name='BO magnet quadrupole qf maximum strength', group='FAC', is_derived=False, value=bo_magnet_quadrupole_qf_maximum_strength, symbol=r"<math>K_\text{QF,max}</math>", units=unicode('m<sup>-2</sup>', encoding='utf-8'), deps=[], obs=[], ),
    Parameter(name='BO magnet quadrupole injection qf maximum gradient', group='FAC', is_derived=True, value='"BO magnet quadrupole qf maximum strength"*"BO beam injection magnetic rigidity"', symbol=r"<math>B'_\text{QF,max,inj}</math>", units=unicode('T·m<sup>-1</sup>', encoding='utf-8'), deps=[], obs=[], ),
    Parameter(name='BO magnet quadrupole extraction qf maximum gradient', group='FAC', is_derived=True, value='"BO magnet quadrupole qf maximum strength"*"BO beam extraction magnetic rigidity"', symbol=r"<math>B'_\text{QF,max,ext}</math>", units=unicode('T·m<sup>-1</sup>', encoding='utf-8'), deps=[], obs=[], ),
    Parameter(name='BO magnet quadrupole qd maximum strength', group='FAC', is_derived=False, value=bo_magnet_quadrupole_qd_maximum_strength, symbol=r"<math>K_\text{QD,max}</math>", units=unicode('m<sup>-2</sup>', encoding='utf-8'), deps=[], obs=[], ),
    Parameter(name='BO magnet quadrupole injection qd maximum gradient', group='FAC', is_derived=True, value='"BO magnet quadrupole qd maximum strength"*"BO beam injection magnetic rigidity"', symbol=r"<math>B'_\text{QD,max,inj}</math>", units=unicode('T·m<sup>-1</sup>', encoding='utf-8'), deps=[], obs=['Bipolar.'], ),
    Parameter(name='BO magnet quadrupole extraction qd maximum gradient', group='FAC', is_derived=True, value='"BO magnet quadrupole qd maximum strength"*"BO beam extraction magnetic rigidity"', symbol=r"<math>B'_\text{QD,max,ext}</math>", units=unicode('T·m<sup>-1</sup>', encoding='utf-8'), deps=[], obs=['Bipolar.'], ),

    Parameter(name='BO magnet ch number', group='FAC', is_derived=False, value=bo_magnet_ch_number, symbol=r'<math>N_\text{CH}</math>', units='', deps=[], obs=[], ),
    Parameter(name='BO magnet cv number', group='FAC', is_derived=False, value=bo_magnet_cv_number, symbol=r'<math>N_\text{CV}</math>', units='', deps=[], obs=[], ),
    Parameter(name='BO magnet ch maximum normalized integrated field', group='FAC', is_derived=False, value=bo_magnet_ch_maximum_normalized_integrated_field, symbol=r'<math>\theta_\text{CH,max}</math>', units='mrad', deps=[], obs=[], ),
    Parameter(name='BO magnet cv maximum normalized integrated field', group='FAC', is_derived=False, value=bo_magnet_cv_maximum_normalized_integrated_field, symbol=r'<math>\theta_\text{CV,max}</math>', units='mrad', deps=[], obs=[], ),

    Parameter(name='BO bpm number', group='FAC', is_derived=False, value=bo_bpm_number, symbol=r'<math>N_\text{BPM}</math>', units='', deps=[], obs=[], ),

    Parameter(name='BO optics extraction radiation integral i1', group='FAC', is_derived=False, value=bo_optics_radiation_integral_i1, symbol=r'<math>I_\text{1}</math>', units='m', deps=['BO beam extraction magnetic rigidity', 'BO lattice version', 'BO optics default mode'], obs=[r'<math>I_\text{1} = \oint{\frac{\eta_x}{\rho_x}\,ds}</math>'], ),
    Parameter(name='BO optics extraction radiation integral i2', group='FAC', is_derived=False, value=bo_optics_radiation_integral_i2, symbol=r'<math>I_\text{2}</math>', units='1/m', deps=['BO beam extraction magnetic rigidity', 'BO lattice version'], obs=[r'<math>I_\text{2} = \oint{\frac{1}{\rho_x^2}\,ds}</math>'], ),
    Parameter(name='BO optics extraction radiation integral i3', group='FAC', is_derived=False, value=bo_optics_radiation_integral_i3, symbol=r'<math>I_\text{3}</math>', units='1/m^2', deps=['BO beam extraction magnetic rigidity', 'BO lattice version'], obs=[r'<math>I_\text{3} = \oint{\frac{1}{|\rho_x|^3}\,ds}</math>'], ),
    Parameter(name='BO optics extraction radiation integral i4', group='FAC', is_derived=False, value=bo_optics_radiation_integral_i4, symbol=r'<math>I_\text{4}</math>', units='1/m', deps=['BO beam extraction magnetic rigidity', 'BO lattice version'], obs=[r'<math>I_\text{4} = \frac{\eta_x(s_0) \tan \theta(s_0)}{\rho_x^2} + \oint{\frac{\eta_x}{\rho_x^3} \left(1 + 2 \rho_x^2 k\right)\,ds} + \frac{\eta_x(s_1) \tan \theta(s_1)}{\rho_x^2}</math>'], ),
    Parameter(name='BO optics extraction radiation integral i5', group='FAC', is_derived=False, value=bo_optics_radiation_integral_i5, symbol=r'<math>I_\text{5}</math>', units='1/m', deps=['BO beam extraction magnetic rigidity', 'BO lattice version', 'BO optics default mode'], obs=[r'<math>I_\text{5} = \oint{\frac{H_x}{|\rho_x|^3}\,ds}</math>', r"<math>H_x \equiv \gamma_x \eta_x^2 + 2 \alpha_x \eta_x \eta_x^' + \beta_x {\eta_x^'}^2</math>"], ),
    Parameter(name='BO optics extraction radiation integral i6', group='FAC', is_derived=False, value=bo_optics_radiation_integral_i6, symbol=r'<math>I_\text{6}</math>', units='1/m', deps=['BO beam extraction magnetic rigidity', 'BO lattice version', 'BO optics default mode'], obs=[r'<math>I_\text{6} = \oint{k^2 \eta_x^2\,ds}</math>'], ),

    Parameter(name='BO optics default mode',  group='FAC', is_derived=False, value=bo_optics_default_mode, symbol='', units='', obs=[], ),
    Parameter(name='BO optics tune horizontal',  group='FAC', is_derived=False, value=bo_optics_tune_horizontal, symbol=r'<math>\nu_x</math>', units='', deps=['BO optics default mode'], obs=[], ),
    Parameter(name='BO optics tune vertical',  group='FAC', is_derived=False, value=bo_optics_tune_vertical, symbol=r'<math>\nu_y</math>', units='', deps=['BO optics default mode'], obs=[], ),
    Parameter(name='BO optics injection tune synchrotron',   group='FAC', is_derived=False, value=bo_optics_tune_synchrotron_injection, symbol=r'<math>\nu_\text{s, inj}</math>', units='', deps=['BO optics default mode'], obs=[], ),
    Parameter(name='BO optics extraction tune synchrotron',  group='FAC', is_derived=False, value=bo_optics_tune_synchrotron_extraction, symbol=r'<math>\nu_\text{s, ext}</math>', units='', deps=['BO optics default mode'], obs=[], ),
    Parameter(name='BO optics chromaticity horizontal',  group='FAC', is_derived=False, value=bo_optics_chromaticity_horizontal, symbol=r'<math>\xi_x</math>', units='', deps=['BO optics default mode'], obs=[], ),
    Parameter(name='BO optics chromaticity vertical',    group='FAC', is_derived=False, value=bo_optics_chromaticity_vertical,   symbol=r'<math>\xi_y</math>', units='', deps=['BO optics default mode'], obs=[], ),
    Parameter(name='BO optics natural chromaticity horizontal',  group='FAC', is_derived=False, value=bo_optics_natural_chromaticity_horizontal, symbol=r'<math>\xi_{0,x}</math>', units='', deps=['BO optics default mode'], obs=[], ),
    Parameter(name='BO optics natural chromaticity vertical',    group='FAC', is_derived=False, value=bo_optics_natural_chromaticity_vertical,   symbol=r'<math>\xi_{0,y}</math>', units='', deps=['BO optics default mode'], obs=[], ),
    Parameter(name='BO optics extraction energy loss per turn', group='FAC', is_derived=True, value='U0("BO beam extraction energy", "BO optics extraction radiation integral i2")', symbol=r'<math>U_0</math>', units='keV', deps=[], obs=[r'<math>U_0 = \oint{P_\gamma dt} = \frac{C_\gamma}{2\pi} E^4_0 I_2</math>'], ),

    Parameter(name='BO optics injection betatron frequency horizontal',  group='FAC', is_derived=True, value='frequency_from_tune("BO beam injection revolution frequency",  "BO optics tune horizontal")', symbol=r'<math>f_\text{x, inj}</math>', units='kHz', obs=[r'<math>f_\text{x, inj} \equiv f_\text{inj,rev} \text{frac}(\nu_x)</math>'], ),
    Parameter(name='BO optics extraction betatron frequency horizontal', group='FAC', is_derived=True, value='frequency_from_tune("BO beam extraction revolution frequency", "BO optics tune horizontal")', symbol=r'<math>f_\text{x, ext}</math>', units='kHz', obs=[r'<math>f_\text{x, ext} \equiv f_\text{inj,rev} \text{frac}(\nu_x)</math>'], ),
    Parameter(name='BO optics injection betatron frequency vertical',  group='FAC', is_derived=True, value='frequency_from_tune("BO beam injection revolution frequency",  "BO optics tune vertical")', symbol=r'<math>f_\text{y, inj}</math>', units='kHz', obs=[r'<math>f_\text{y, inj} \equiv f_\text{inj,rev} \text{frac}(\nu_y)</math>'], ),
    Parameter(name='BO optics extraction betatron frequency vertical', group='FAC', is_derived=True, value='frequency_from_tune("BO beam extraction revolution frequency", "BO optics tune vertical")', symbol=r'<math>f_\text{y, ext}</math>', units='kHz', obs=[r'<math>f_\text{y, ext} \equiv f_\text{inj,rev} \text{frac}(\nu_y)</math>'], ),

    Parameter(name='BO optics extraction linear momentum compaction', group='FAC', is_derived=True, value='alpha1("BO optics extraction radiation integral i1", "BO lattice circumference")', symbol=r'<math>\alpha_\text{1}</math>', units='', deps=[], obs=[r'<math>\alpha_\text{1} = \frac{I_\text{1}}{C}</math>'], ),
    Parameter(name='BO optics extraction damping partition number horizontal', group='FAC', is_derived=True, value='Jx("BO optics extraction radiation integral i2", "BO optics extraction radiation integral i4")', symbol=r'<math>J_x</math>', units='', deps=[], obs=[r'<math>J_x = 1 - \frac{I_\text{4}}{I_\text{2}}</math>'], ),
    Parameter(name='BO optics extraction damping partition number vertical', group='FAC', is_derived=False, value=bo_optics_extraction_damping_partition_number_vertical, symbol=r'<math>J_y</math>', units='', deps=[], obs=['Vertical damping partition number is identically one for error-free machines for which vertical dispersion functions are zero everywhere.', r'<math>J_y = 1 - \frac{I_{4,y}}{I_\text{2}} \equiv 1</math>'], ),
    Parameter(name='BO optics extraction damping partition number longitudinal', group='FAC', is_derived=True, value='Js("BO optics extraction damping partition number horizontal", "BO optics extraction damping partition number vertical")', symbol=r'<math>J_s</math>', units='', deps=[], obs=["Its value is derived from Robinson's sum rule.", r'<math>J_s = 4 - J_x - J_y</math>'], ),
    Parameter(name='BO optics extraction natural emittance', group='FAC', is_derived=True, value='natural_emittance("BO beam extraction gamma factor", "BO optics extraction damping partition number horizontal", "BO optics extraction radiation integral i2", "BO optics extraction radiation integral i5")', symbol=r'<math>\epsilon_0</math>', units=unicode('nm⋅rad',encoding='utf-8'), deps=[], obs=[r'<math>\epsilon_0 = C_\text{q} \frac{\gamma^2}{J_x} \frac{I_\text{5}}{I_\text{2}}</math>'], ),
    Parameter(name='BO optics extraction natural energy spread', group='FAC', is_derived=True, value='energy_spread("BO beam extraction gamma factor", "BO optics extraction radiation integral i2", "BO optics extraction radiation integral i3", "BO optics extraction radiation integral i4")', symbol=r'<math>\sigma_\delta</math>', units='%', deps=[], obs=[r'<math>\sigma_\delta = \sqrt{C_\text{q} \gamma^2 \frac{I_\text{3}}{2 I_\text{2} + I_\text{4}}}</math>'], ),
    Parameter(name='BO optics extraction radiation damping time horizontal', group='FAC', is_derived=True, value='damping_time("BO beam extraction energy", "BO optics extraction radiation integral i2", "BO optics extraction damping partition number horizontal", "BO lattice circumference")', symbol=r'<math>\tau_x</math>', units='ms', deps=[], obs=[r'<math>\tau_x = \frac{3(m_e c^2)^3}{r_e c} \frac{C}{E_0^3 I_2 J_x}</math>'], ),
    Parameter(name='BO optics extraction radiation damping time longitudinal', group='FAC', is_derived=True, value='damping_time("BO beam extraction energy", "BO optics extraction radiation integral i2", "BO optics extraction damping partition number longitudinal", "BO lattice circumference")', symbol=r'<math>\tau_s</math>', units='ms', deps=[], obs=[r'<math>\tau_s = \frac{3(m_e c^2)^3}{r_e c} \frac{C}{E_0^3 I_2 J_s}</math>'], ),
    Parameter(name='BO optics extraction radiation damping time vertical', group='FAC', is_derived=True, value='damping_time("BO beam extraction energy", "BO optics extraction radiation integral i2", "BO optics extraction damping partition number vertical", "BO lattice circumference")', symbol=r'<math>\tau_y</math>', units='ms', deps=[], obs=[r'<math>\tau_y = \frac{3(m_e c^2)^3}{r_e c} \frac{C}{E_0^3 I_2 J_y}</math>'], ),

    Parameter(name='BO optics extraction radiation power', group='FAC', is_derived=True, value='radiation_power("BO optics extraction energy loss per turn", "BO beam extraction current")', symbol=r'<math>P</math>', units='kW', deps=[], obs=[r'<math>P = U_0 I</math>'], ),
    Parameter(name='BO optics extraction overvoltage', group='FAC', is_derived=True, value='overvoltage("BO rf extraction peak voltage", "BO optics extraction energy loss per turn")', symbol=r'<math>q</math>', units='', deps=[], obs=[r'<math>q = \frac{eV_\text{RF}}{U_0}</math>'], ),
    Parameter(name='BO optics extraction synchronous phase', group='FAC', is_derived=True, value='sync_phase("BO optics extraction overvoltage")', symbol=r'<math>\phi_0</math>', units=unicode('°',encoding='utf-8'), deps=[], obs=[r'<math>\phi_0 = \pi - \arcsin\left(\frac{1}{q}\right)</math>'], ),
    Parameter(name='BO optics extraction synchrotron frequency', group='FAC', is_derived=True, value='frequency_from_tune("BO beam extraction revolution frequency", "BO optics extraction tune synchrotron")', symbol=r'<math>f_s</math>', units='kHz', deps=[], obs=[r'<math>f_s = f_\text{rev} \left( \nu_s - \lfloor \nu_s\rfloor \right)</math>'], ),
    Parameter(name='BO optics extraction rf energy acceptance', group='FAC', is_derived=True, value='rf_energy_acceptance("BO optics extraction overvoltage", "BO beam extraction energy", "BO optics extraction energy loss per turn", "BO rf harmonic number","BO optics extraction linear momentum compaction")', symbol=r'<math>\epsilon_\text{max}</math>', units='%', deps=[], obs=[r'<math>\epsilon_\text{max} = \sqrt{\frac{1}{\pi h \alpha_x} \frac{U_0}{E} F(q)}</math>', r'<math>F(q) = 2 \left( \sqrt{q^2 - 1} - \cos^{-1} (1/q) \right)</math>'], ),
    Parameter(name='BO optics extraction slip factor', group='FAC', is_derived=True, value='slip_factor("BO optics extraction linear momentum compaction", "BO beam extraction gamma factor")', symbol=r'<math>\eta</math>', units='', deps=[], obs=[r'<math>\eta = \alpha_1 - \frac{1}{\gamma^2}</math>'], ),
    Parameter(name='BO optics extraction natural bunch length', group='FAC', is_derived=True, value='bunch_length("BO optics extraction slip factor", "BO optics extraction natural energy spread", "BO optics extraction synchrotron frequency")', symbol=r'<math>\sigma_s</math>', units='mm', deps=[], obs=[r'<math>\sigma_s = \frac{c |\eta|}{2 \pi f_s} \sigma_\delta</math>'], ),
    Parameter(name='BO optics extraction natural bunch duration', group='FAC', is_derived=True, value='bunch_duration("BO optics extraction natural bunch length", "BO beam extraction beta factor")', symbol=r'<math>\sigma_\tau</math>', units='ps', deps=[], obs=[r'<math>\sigma_\tau = \frac{\sigma_s}{\beta c}</math>'], ),

    Parameter(name='BO error alignment dipole', group='FAC', is_derived=False, value=bo_error_alignment_dipole, symbol=r'<math>E_{xy,\text{dip}}</math>', units=unicode('μm', encoding='utf-8'), deps=[], obs=[r'Random transverse position error (standard deviation) for <math>x</math> and <math>y</math>.', unicode('Simulations assume Gaussian distribution truncated at ±2σ.', encoding='utf-8')]),
    Parameter(name='BO error rotation dipole', group='FAC', is_derived=False, value=bo_error_rotation_dipole, symbol=r'<math>E_{\theta,\text{dip}}</math>', units='mrad', deps=[], obs=[r'Random rotation error (standard deviation) around longitudinal axis.', unicode('Simulations assume Gaussian distribution truncated at ±2σ.', encoding='utf-8')]),
    Parameter(name='BO error excitation dipole', group='FAC', is_derived=False, value=bo_error_excitation_dipole, symbol=r'<math>E_{\text{exc,dip}}</math>', units='%', deps=[], obs=[r'Static or low frequency random excitation error (standard deviation).', unicode('Simulations assume Gaussian distribution truncated at ±2σ.', encoding='utf-8')]),

    Parameter(name='BO error alignment quadrupole', group='FAC', is_derived=False, value=bo_error_alignment_quadrupole, symbol=r'<math>E_{xy,\text{QUAD}}</math>', units=unicode('μm', encoding='utf-8'), deps=[], obs=[r'Random transverse position error (standard deviation) for <math>x</math> and <math>y</math>.', unicode('Simulations assume Gaussian distribution truncated at ±2σ.', encoding='utf-8')], ),
    Parameter(name='BO error rotation quadrupole', group='FAC', is_derived=False, value=bo_error_rotation_quadrupole, symbol=r'<math>E_{\theta,\text{QUAD}}</math>', units='mrad', deps=[], obs=[r'Random rotation error (standard deviation) around longitudinal axis.', unicode('Simulations assume Gaussian distribution truncated at ±2σ.', encoding='utf-8')], ),
    Parameter(name='BO error excitation quadrupole', group='FAC', is_derived=False, value=bo_error_excitation_quadrupole, symbol=r'<math>E_{\text{exc,QUAD}}</math>', units='%', deps=[], obs=[r'Static or low frequency random excitation error (standard deviation).', unicode('Simulations assume Gaussian distribution truncated at ±2σ.', encoding='utf-8')], ),

    Parameter(name='BO error alignment sextupole', group='FAC', is_derived=False, value=bo_error_alignment_sextupole, symbol=r'<math>E_{xy,\text{SEXT}}</math>', units=unicode('μm', encoding='utf-8'), deps=[], obs=[r'Random transverse position error (standard deviation) for <math>x</math> and <math>y</math>.', unicode('Simulations assume Gaussian distribution truncated at ±2σ.', encoding='utf-8')], ),
    Parameter(name='BO error rotation sextupole', group='FAC', is_derived=False, value=bo_error_rotation_sextupole, symbol=r'<math>E_{\theta,\text{SEXT}}</math>', units='mrad', deps=[], obs=[r'Random rotation error (standard deviation) around longitudinal axis.', unicode('Simulations assume Gaussian distribution truncated at ±2σ.', encoding='utf-8')], ),
    Parameter(name='BO error excitation sextupole', group='FAC', is_derived=False,value=bo_error_excitation_sextupole, symbol=r'<math>E_{\text{exc,SEXT}}</math>',units='%', deps=[], obs=[r'Static or low frequency random excitation error (standard deviation).', unicode('Simulations assume Gaussian distribution truncated at ±2σ.', encoding='utf-8')], ),

    Parameter(name='BO error alignment bpm', group='FAC', is_derived=False, value=bo_error_alignment_bpm, symbol=r'<math>E_{xy,\text{BPM}}</math>', units=unicode('μm', encoding='utf-8'), deps=[], obs=[r'Random transverse position error (standard deviation) for <math>x</math> and <math>y</math>.', unicode('Simulations assume Gaussian distribution truncated at ±2σ.', encoding='utf-8')]),

    Parameter(name='BO error multipole dipole reference position', group='FAC', is_derived=False, value=bo_error_multipole_dipole_reference_position, symbol=r'<math>r_{0,\text{dip}}</math>', units='mm', deps=[], obs=[], ),

    Parameter(name='BO error multipole dipole systematic normal 8-pole', group='FAC', is_derived=False, value=bo_error_multipole_dipole_systematic_normal_8_pole, symbol=r'<math>M_{B_3/B_0,dip}^{\text{sys,normal}}</math>', units='', deps=['BO error multipole dipole reference position'], obs=[r'Relative value, calculated at <math>r_0</math>.', 'From approved model1 of 2013-05-07'], ),
    Parameter(name='BO error multipole dipole systematic normal 10-pole', group='FAC', is_derived=False, value=bo_error_multipole_dipole_systematic_normal_10_pole, symbol=r'<math>M_{B_4/B_0,dip}^{\text{sys,normal}}</math>', units='', deps=['BO error multipole dipole reference position'],  obs=[r'Relative value, calculated at <math>r_0</math>.', 'From approved model1 of 2013-05-07'], ),
    Parameter(name='BO error multipole dipole systematic normal 12-pole', group='FAC', is_derived=False, value=bo_error_multipole_dipole_systematic_normal_12_pole, symbol=r'<math>M_{B_5/B_0,dip}^{\text{sys,normal}}</math>', units='', deps=['BO error multipole dipole reference position'], obs=[r'Relative value, calculated at <math>r_0</math>.', 'From approved model1 of 2013-05-07'], ),
    Parameter(name='BO error multipole dipole systematic normal 14-pole', group='FAC', is_derived=False, value=bo_error_multipole_dipole_systematic_normal_14_pole, symbol=r'<math>M_{B_6/B_0,dip}^{\text{sys,normal}}</math>', units='', deps=['BO error multipole dipole reference position'], obs=[r'Relative value, calculated at <math>r_0</math>.', 'From approved model1 of 2013-05-07'], ),

    Parameter(name='BO error multipole dipole random normal 6-pole', group='FAC', is_derived=False, value=bo_error_multipole_dipole_random_normal_6_pole, symbol=r'<math>M_{B_2/B_0,dip}^{\text{rnd,normal}}</math>', units='', deps=['BO error multipole dipole reference position'], obs=[r'Relative value, calculated at <math>r_0</math>.', unicode('Simulations assume Gaussian distribution truncated at ±2σ.', encoding='utf-8'), 'From approved model1 of 2013-05-07'], ),
    Parameter(name='BO error multipole dipole random normal 8-pole', group='FAC', is_derived=False, value=bo_error_multipole_dipole_random_normal_8_pole, symbol=r'<math>M_{B_3/B_0,dip}^{\text{rnd,normal}}</math>', units='', deps=['BO error multipole dipole reference position'], obs=[r'Relative value, calculated at <math>r_0</math>.', unicode('Simulations assume Gaussian distribution truncated at ±2σ.', encoding='utf-8'), 'From approved model1 of 2013-05-07'], ),
    Parameter(name='BO error multipole dipole random normal 10-pole', group='FAC', is_derived=False, value=bo_error_multipole_dipole_random_normal_10_pole, symbol=r'<math>M_{B_4/B_0,dip}^{\text{rnd,normal}}</math>', units='', deps=['BO error multipole dipole reference position'], obs=[r'Relative value, calculated at <math>r_0</math>.', unicode('Simulations assume Gaussian distribution truncated at ±2σ.', encoding='utf-8'), 'From approved model1 of 2013-05-07'], ),
    Parameter(name='BO error multipole dipole random normal 12-pole', group='FAC', is_derived=False, value=bo_error_multipole_dipole_random_normal_12_pole, symbol=r'<math>M_{B_5/B_0,dip}^{\text{rnd,normal}}</math>', units='', deps=['BO error multipole dipole reference position'], obs=[r'Relative value, calculated at <math>r_0</math>.', unicode('Simulations assume Gaussian distribution truncated at ±2σ.', encoding='utf-8'), 'From approved model1 of 2013-05-07'], ),
    Parameter(name='BO error multipole dipole random normal 14-pole', group='FAC', is_derived=False, value=bo_error_multipole_dipole_random_normal_14_pole, symbol=r'<math>M_{B_6/B_0,dip}^{\text{rnd,normal}}</math>', units='', deps=['BO error multipole dipole reference position'], obs=[r'Relative value, calculated at <math>r_0</math>.', unicode('Simulations assume Gaussian distribution truncated at ±2σ.', encoding='utf-8'), 'From approved model1 of 2013-05-07'], ),
    Parameter(name='BO error multipole dipole random normal 16-pole', group='FAC', is_derived=False, value=bo_error_multipole_dipole_random_normal_16_pole, symbol=r'<math>M_{B_7/B_0,dip}^{\text{rnd,normal}}</math>', units='', deps=['BO error multipole dipole reference position'], obs=[r'Relative value, calculated at <math>r_0</math>.', unicode('Simulations assume Gaussian distribution truncated at ±2σ.', encoding='utf-8'), 'From approved model1 of 2013-05-07'], ),
    Parameter(name='BO error multipole dipole random normal 18-pole', group='FAC', is_derived=False, value=bo_error_multipole_dipole_random_normal_18_pole, symbol=r'<math>M_{B_8/B_0,dip}^{\text{rnd,normal}}</math>', units='', deps=['BO error multipole dipole reference position'], obs=[r'Relative value, calculated at <math>r_0</math>.', unicode('Simulations assume Gaussian distribution truncated at ±2σ.', encoding='utf-8'), 'From approved model1 of 2013-05-07'], ),

    Parameter(name='BO error multipole dipole random skew 6-pole', group='FAC', is_derived=False, value=bo_error_multipole_dipole_random_skew_6_pole, symbol=r'<math>M_{B_2/B_0,dip}^{\text{rnd,skew}}</math>', units='', deps=['BO error multipole dipole reference position'], obs=[r'Relative value, calculated at <math>r_0</math>.', unicode('Simulations assume Gaussian distribution truncated at ±2σ.', encoding='utf-8'), 'From approved model1 of 2013-05-07'], ),
    Parameter(name='BO error multipole dipole random skew 8-pole', group='FAC', is_derived=False, value=bo_error_multipole_dipole_random_skew_8_pole, symbol=r'<math>M_{B_3/B_0,dip}^{\text{rnd,skew}}</math>', units='', deps=['BO error multipole dipole reference position'], obs=[r'Relative value, calculated at <math>r_0</math>.', unicode('Simulations assume Gaussian distribution truncated at ±2σ.', encoding='utf-8'), 'From approved model1 of 2013-05-07'], ),
    Parameter(name='BO error multipole dipole random skew 10-pole', group='FAC', is_derived=False, value=bo_error_multipole_dipole_random_skew_10_pole, symbol=r'<math>M_{B_4/B_0,dip}^{\text{rnd,skew}}</math>', units='', deps=['BO error multipole dipole reference position'], obs=[r'Relative value, calculated at <math>r_0</math>.', unicode('Simulations assume Gaussian distribution truncated at ±2σ.', encoding='utf-8'), 'From approved model1 of 2013-05-07'], ),
    Parameter(name='BO error multipole dipole random skew 12-pole', group='FAC', is_derived=False, value=bo_error_multipole_dipole_random_skew_12_pole, symbol=r'<math>M_{B_5/B_0,dip}^{\text{rnd,skew}}</math>', units='', deps=['BO error multipole dipole reference position'], obs=[r'Relative value, calculated at <math>r_0</math>.', unicode('Simulations assume Gaussian distribution truncated at ±2σ.', encoding='utf-8'), 'From approved model1 of 2013-05-07'], ),
    Parameter(name='BO error multipole dipole random skew 14-pole', group='FAC', is_derived=False, value=bo_error_multipole_dipole_random_skew_14_pole, symbol=r'<math>M_{B_6/B_0,dip}^{\text{rnd,skew}}</math>', units='', deps=['BO error multipole dipole reference position'], obs=[r'Relative value, calculated at <math>r_0</math>.', unicode('Simulations assume Gaussian distribution truncated at ±2σ.', encoding='utf-8'), 'From approved model1 of 2013-05-07'], ),
    Parameter(name='BO error multipole dipole random skew 16-pole', group='FAC', is_derived=False, value=bo_error_multipole_dipole_random_skew_16_pole, symbol=r'<math>M_{B_7/B_0,dip}^{\text{rnd,skew}}</math>', units='', deps=['BO error multipole dipole reference position'], obs=[r'Relative value, calculated at <math>r_0</math>.', unicode('Simulations assume Gaussian distribution truncated at ±2σ.', encoding='utf-8'), 'From approved model1 of 2013-05-07'], ),
    Parameter(name='BO error multipole dipole random skew 18-pole', group='FAC', is_derived=False, value=bo_error_multipole_dipole_random_skew_18_pole, symbol=r'<math>M_{B_8/B_0,dip}^{\text{rnd,skew}}</math>', units='', deps=['BO error multipole dipole reference position'], obs=[r'Relative value, calculated at <math>r_0</math>.', unicode('Simulations assume Gaussian distribution truncated at ±2σ.', encoding='utf-8'), 'From approved model1 of 2013-05-07'], ),

    Parameter(name='BO error multipole quadrupole reference position', group='FAC', is_derived=False, value=bo_error_multipole_quadrupole_reference_position, symbol=r'<math>r_{0,\text{QUAD}}</math>', units='mm', deps=[], obs=[], ),

    Parameter(name='BO error multipole quadrupole systematic normal 12-pole',group='FAC', is_derived=False, value=bo_error_multipole_quadrupole_systematic_normal_12_pole, symbol=r'<math>M_{B_5/B_1,QUAD}^{\text{sys,normal}}</math>', units='', deps=['BO error multipole quadrupole reference position'], obs=[r'Relative value, calculated at <math>r_0</math>.',], ),
    Parameter(name='BO error multipole quadrupole systematic normal 20-pole', group='FAC', is_derived=False, value=bo_error_multipole_quadrupole_systematic_normal_20_pole, symbol=r'<math>M_{B_9/B_1,QUAD}^{\text{sys,normal}}</math>', units='', deps=['BO error multipole quadrupole reference position'], obs=[r'Relative value, calculated at <math>r_0</math>.'], ),
    Parameter(name='BO error multipole quadrupole systematic normal 28-pole', group='FAC', is_derived=False, value=bo_error_multipole_quadrupole_systematic_normal_28_pole, symbol=r'<math>M_{B_{13}/B_1,QUAD}^{\text{sys,normal}}</math>', units='', deps=['BO error multipole quadrupole reference position'], obs=[r'Relative value, calculated at <math>r_0</math>.'], ),

    Parameter(name='BO error multipole quadrupole random normal 6-pole', group='FAC', is_derived=False, value=bo_error_multipole_quadrupole_random_normal_6_pole, symbol=r'<math>M_{B_2/B_1,QUAD}^{\text{rnd,normal}}</math>', units='', deps=['BO error multipole quadrupole reference position'], obs=[r'Relative value, calculated at <math>r_0</math>.', unicode('Simulations assume Gaussian distribution truncated at ±2σ.', encoding='utf-8'), 'Rotating coil measurement of QF prototype magnets'], ),
    Parameter(name='BO error multipole quadrupole random normal 8-pole', group='FAC', is_derived=False, value=bo_error_multipole_quadrupole_random_normal_8_pole, symbol=r'<math>M_{B_3/B_1,QUAD}^{\text{rnd,normal}}</math>', units='', deps=['BO error multipole quadrupole reference position'], obs=[r'Relative value, calculated at <math>r_0</math>.', unicode('Simulations assume Gaussian distribution truncated at ±2σ.', encoding='utf-8'), 'Rotating coil measurement of QF prototype magnets'], ),
    Parameter(name='BO error multipole quadrupole random normal 10-pole', group='FAC', is_derived=False, value=bo_error_multipole_quadrupole_random_normal_10_pole, symbol=r'<math>M_{B_4/B_1,QUAD}^{\text{rnd,normal}}</math>', units='', deps=['BO error multipole quadrupole reference position'], obs=[r'Relative value, calculated at <math>r_0</math>.', unicode('Simulations assume Gaussian distribution truncated at ±2σ.', encoding='utf-8'), 'Rotating coil measurement of QF prototype magnets'], ),
    Parameter(name='BO error multipole quadrupole random normal 12-pole', group='FAC', is_derived=False, value=bo_error_multipole_quadrupole_random_normal_12_pole, symbol=r'<math>M_{B_5/B_1,QUAD}^{\text{rnd,normal}}</math>', units='', deps=['BO error multipole quadrupole reference position'], obs=[r'Relative value, calculated at <math>r_0</math>.', unicode('Simulations assume Gaussian distribution truncated at ±2σ.', encoding='utf-8'), 'Rotating coil measurement of QF prototype magnets'], ),
    Parameter(name='BO error multipole quadrupole random normal 14-pole', group='FAC', is_derived=False, value=bo_error_multipole_quadrupole_random_normal_14_pole, symbol=r'<math>M_{B_6/B_1,QUAD}^{\text{rnd,normal}}</math>', units='', deps=['BO error multipole quadrupole reference position'], obs=[r'Relative value, calculated at <math>r_0</math>.', unicode('Simulations assume Gaussian distribution truncated at ±2σ.', encoding='utf-8'), 'Rotating coil measurement of QF prototype magnets'], ),
    Parameter(name='BO error multipole quadrupole random normal 16-pole', group='FAC', is_derived=False, value=bo_error_multipole_quadrupole_random_normal_16_pole, symbol=r'<math>M_{B_7/B_1,QUAD}^{\text{rnd,normal}}</math>', units='', deps=['BO error multipole quadrupole reference position'], obs=[r'Relative value, calculated at <math>r_0</math>.', unicode('Simulations assume Gaussian distribution truncated at ±2σ.', encoding='utf-8'), 'Rotating coil measurement of QF prototype magnets'], ),
    Parameter(name='BO error multipole quadrupole random normal 18-pole', group='FAC', is_derived=False, value=bo_error_multipole_quadrupole_random_normal_18_pole, symbol=r'<math>M_{B_8/B_1,QUAD}^{\text{rnd,normal}}</math>', units='', deps=['BO error multipole quadrupole reference position'], obs=[r'Relative value, calculated at <math>r_0</math>.', unicode('Simulations assume Gaussian distribution truncated at ±2σ.', encoding='utf-8'), 'Rotating coil measurement of QF prototype magnets'], ),
    Parameter(name='BO error multipole quadrupole random normal 20-pole', group='FAC', is_derived=False, value=bo_error_multipole_quadrupole_random_normal_20_pole, symbol=r'<math>M_{B_9/B_1,QUAD}^{\text{rnd,normal}}</math>', units='', deps=['BO error multipole quadrupole reference position'], obs=[r'Relative value, calculated at <math>r_0</math>.', unicode('Simulations assume Gaussian distribution truncated at ±2σ.', encoding='utf-8'), 'Rotating coil measurement of QF prototype magnets'], ),

    Parameter(name='BO error multipole quadrupole random skew 6-pole', group='FAC', is_derived=False, value=bo_error_multipole_quadrupole_random_skew_6_pole, symbol=r'<math>M_{B_2/B_1,QUAD}^{\text{rnd,skew}}</math>', units='', deps=['BO error multipole quadrupole reference position'], obs=[r'Relative value, calculated at <math>r_0</math>.', unicode('Simulations assume Gaussian distribution truncated at ±2σ.', encoding='utf-8'), 'Rotating coil measurement of QF prototype magnets'], ),
    Parameter(name='BO error multipole quadrupole random skew 8-pole', group='FAC', is_derived=False, value=bo_error_multipole_quadrupole_random_skew_8_pole, symbol=r'<math>M_{B_3/B_1,QUAD}^{\text{rnd,skew}}</math>', units='', deps=['BO error multipole quadrupole reference position'], obs=[r'Relative value, calculated at <math>r_0</math>.', unicode('Simulations assume Gaussian distribution truncated at ±2σ.', encoding='utf-8'), 'Rotating coil measurement of QF prototype magnets'], ),
    Parameter(name='BO error multipole quadrupole random skew 10-pole', group='FAC', is_derived=False, value=bo_error_multipole_quadrupole_random_skew_10_pole, symbol=r'<math>M_{B_4/B_1,QUAD}^{\text{rnd,skew}}</math>', units='', deps=['BO error multipole quadrupole reference position'], obs=[r'Relative value, calculated at <math>r_0</math>.', unicode('Simulations assume Gaussian distribution truncated at ±2σ.', encoding='utf-8'), 'Rotating coil measurement of QF prototype magnets'], ),
    Parameter(name='BO error multipole quadrupole random skew 12-pole', group='FAC', is_derived=False, value=bo_error_multipole_quadrupole_random_skew_12_pole, symbol=r'<math>M_{B_5/B_1,QUAD}^{\text{rnd,skew}}</math>', units='', deps=['BO error multipole quadrupole reference position'], obs=[r'Relative value, calculated at <math>r_0</math>.', unicode('Simulations assume Gaussian distribution truncated at ±2σ.', encoding='utf-8'), 'Rotating coil measurement of QF prototype magnets'], ),
    Parameter(name='BO error multipole quadrupole random skew 14-pole', group='FAC', is_derived=False, value=bo_error_multipole_quadrupole_random_skew_14_pole, symbol=r'<math>M_{B_6/B_1,QUAD}^{\text{rnd,skew}}</math>', units='', deps=['BO error multipole quadrupole reference position'], obs=[r'Relative value, calculated at <math>r_0</math>.', unicode('Simulations assume Gaussian distribution truncated at ±2σ.', encoding='utf-8'), 'Rotating coil measurement of QF prototype magnets'], ),
    Parameter(name='BO error multipole quadrupole random skew 16-pole', group='FAC', is_derived=False, value=bo_error_multipole_quadrupole_random_skew_16_pole, symbol=r'<math>M_{B_7/B_1,QUAD}^{\text{rnd,skew}}</math>', units='', deps=['BO error multipole quadrupole reference position'], obs=[r'Relative value, calculated at <math>r_0</math>.', unicode('Simulations assume Gaussian distribution truncated at ±2σ.', encoding='utf-8'), 'Rotating coil measurement of QF prototype magnets'], ),
    Parameter(name='BO error multipole quadrupole random skew 18-pole', group='FAC', is_derived=False, value=bo_error_multipole_quadrupole_random_skew_18_pole, symbol=r'<math>M_{B_8/B_1,QUAD}^{\text{rnd,skew}}</math>', units='', deps=['BO error multipole quadrupole reference position'], obs=[r'Relative value, calculated at <math>r_0</math>.', unicode('Simulations assume Gaussian distribution truncated at ±2σ.', encoding='utf-8'), 'Rotating coil measurement of QF prototype magnets'], ),
    Parameter(name='BO error multipole quadrupole random skew 20-pole', group='FAC', is_derived=False, value=bo_error_multipole_quadrupole_random_skew_20_pole, symbol=r'<math>M_{B_9/B_1,QUAD}^{\text{rnd,skew}}</math>', units='', deps=['BO error multipole quadrupole reference position'], obs=[r'Relative value, calculated at <math>r_0</math>.', unicode('Simulations assume Gaussian distribution truncated at ±2σ.', encoding='utf-8'), 'Rotating coil measurement of QF prototype magnets'], ),

    Parameter(name='BO error multipole sextupole reference position', group='FAC', is_derived=False, value=bo_error_multipole_sextupole_reference_position, symbol=r'<math>r_{0,\text{SEXT}}</math>', units='mm', deps=[], obs=[], ),

    Parameter(name='BO error multipole sextupole systematic normal 18-pole', group='FAC', is_derived=False, value=bo_error_multipole_sextupole_systematic_normal_18_pole, symbol=r'<math>M_{B_8/B_2,SEXT}^{\text{sys,normal}}</math>',units='',deps=['BO error multipole sextupole reference position'],obs=[r'Relative value, calculated at <math>r_0</math>.','From approved model3 of 2013-06-05'], ),
    Parameter(name='BO error multipole sextupole systematic normal 30-pole', group='FAC', is_derived=False, value=bo_error_multipole_sextupole_systematic_normal_30_pole, symbol=r'<math>M_{B_{14}/B_2,SEXT}^{\text{sys,normal}}</math>', units='', deps=['BO error multipole sextupole reference position'], obs=[r'Relative value, calculated at <math>r_0</math>.', 'From approved model3 of 2013-06-05'], ),

    Parameter(name='BO error multipole sextupole random normal 8-pole', group='FAC', is_derived=False, value=bo_error_multipole_sextupole_random_normal_8_pole, symbol=r'<math>M_{B_3/B_2,SEXT}^{\text{rnd,normal}}</math>', units='', deps=['BO error multipole sextupole reference position'], obs=[r'Relative value, calculated at <math>r_0</math>.', unicode('Simulations assume Gaussian distribution truncated at ±2σ.', encoding='utf-8'), 'From approved model3 of 2013-06-05'], ),
    Parameter(name='BO error multipole sextupole random normal 10-pole', group='FAC', is_derived=False, value=bo_error_multipole_sextupole_random_normal_10_pole, symbol=r'<math>M_{B_4/B_2,SEXT}^{\text{rnd,normal}}</math>', units='', deps=['BO error multipole sextupole reference position'], obs=[r'Relative value, calculated at <math>r_0</math>.', unicode('Simulations assume Gaussian distribution truncated at ±2σ.', encoding='utf-8'), 'From approved model3 of 2013-06-05'], ),
    Parameter(name='BO error multipole sextupole random normal 12-pole', group='FAC', is_derived=False, value=bo_error_multipole_sextupole_random_normal_12_pole, symbol=r'<math>M_{B_5/B_2,SEXT}^{\text{rnd,normal}}</math>', units='', deps=['BO error multipole sextupole reference position'], obs=[r'Relative value, calculated at <math>r_0</math>.', unicode('Simulations assume Gaussian distribution truncated at ±2σ.', encoding='utf-8'), 'From approved model3 of 2013-06-05'], ),
    Parameter(name='BO error multipole sextupole random normal 14-pole', group='FAC', is_derived=False, value=bo_error_multipole_sextupole_random_normal_14_pole, symbol=r'<math>M_{B_6/B_2,SEXT}^{\text{rnd,normal}}</math>', units='', deps=['BO error multipole sextupole reference position'], obs=[r'Relative value, calculated at <math>r_0</math>.', unicode('Simulations assume Gaussian distribution truncated at ±2σ.', encoding='utf-8'), 'From approved model3 of 2013-06-05'], ),
    Parameter(name='BO error multipole sextupole random normal 16-pole', group='FAC', is_derived=False, value=bo_error_multipole_sextupole_random_normal_16_pole, symbol=r'<math>M_{B_7/B_2,SEXT}^{\text{rnd,normal}}</math>', units='', deps=['BO error multipole sextupole reference position'], obs=[r'Relative value, calculated at <math>r_0</math>.', unicode('Simulations assume Gaussian distribution truncated at ±2σ.', encoding='utf-8'), 'From approved model3 of 2013-06-05'], ),
    Parameter(name='BO error multipole sextupole random normal 18-pole', group='FAC', is_derived=False, value=bo_error_multipole_sextupole_random_normal_18_pole, symbol=r'<math>M_{B_8/B_2,SEXT}^{\text{rnd,normal}}</math>', units='', deps=['BO error multipole sextupole reference position'], obs=[r'Relative value, calculated at <math>r_0</math>.', unicode('Simulations assume Gaussian distribution truncated at ±2σ.', encoding='utf-8'), 'From approved model3 of 2013-06-05'], ),
    Parameter(name='BO error multipole sextupole random normal 20-pole', group='FAC', is_derived=False, value=bo_error_multipole_sextupole_random_normal_20_pole, symbol=r'<math>M_{B_9/B_2,SEXT}^{\text{rnd,normal}}</math>', units='', deps=['BO error multipole sextupole reference position'], obs=[r'Relative value, calculated at <math>r_0</math>.', unicode('Simulations assume Gaussian distribution truncated at ±2σ.', encoding='utf-8'), 'From approved model3 of 2013-06-05'], ),

    Parameter(name='BO error multipole sextupole random skew 8-pole', group='FAC', is_derived=False, value=bo_error_multipole_sextupole_random_skew_8_pole, symbol=r'<math>M_{B_3/B_2,SEXT}^{\text{rnd,skew}}</math>', units='', deps=['BO error multipole sextupole reference position'], obs=[r'Relative value, calculated at <math>r_0</math>.', unicode('Simulations assume Gaussian distribution truncated at ±2σ.', encoding='utf-8'), 'From approved model3 of 2013-06-05'], ),
    Parameter(name='BO error multipole sextupole random skew 10-pole', group='FAC', is_derived=False, value=bo_error_multipole_sextupole_random_skew_10_pole, symbol=r'<math>M_{B_4/B_2,SEXT}^{\text{rnd,skew}}</math>', units='', deps=['BO error multipole sextupole reference position'], obs=[r'Relative value, calculated at <math>r_0</math>.', unicode('Simulations assume Gaussian distribution truncated at ±2σ.', encoding='utf-8'), 'From approved model3 of 2013-06-05'], ),
    Parameter(name='BO error multipole sextupole random skew 12-pole', group='FAC', is_derived=False, value=bo_error_multipole_sextupole_random_skew_12_pole, symbol=r'<math>M_{B_5/B_2,SEXT}^{\text{rnd,skew}}</math>', units='', deps=['BO error multipole sextupole reference position'], obs=[r'Relative value, calculated at <math>r_0</math>.', unicode('Simulations assume Gaussian distribution truncated at ±2σ.', encoding='utf-8'), 'From approved model3 of 2013-06-05'], ),
    Parameter(name='BO error multipole sextupole random skew 14-pole', group='FAC', is_derived=False, value=bo_error_multipole_sextupole_random_skew_14_pole, symbol=r'<math>M_{B_6/B_2,SEXT}^{\text{rnd,skew}}</math>', units='', deps=['BO error multipole sextupole reference position'], obs=[r'Relative value, calculated at <math>r_0</math>.', unicode('Simulations assume Gaussian distribution truncated at ±2σ.', encoding='utf-8'), 'From approved model3 of 2013-06-05'], ),
    Parameter(name='BO error multipole sextupole random skew 16-pole', group='FAC', is_derived=False, value=bo_error_multipole_sextupole_random_skew_16_pole, symbol=r'<math>M_{B_7/B_2,SEXT}^{\text{rnd,skew}}</math>', units='', deps=['BO error multipole sextupole reference position'], obs=[r'Relative value, calculated at <math>r_0</math>.', unicode('Simulations assume Gaussian distribution truncated at ±2σ.', encoding='utf-8'), 'From approved model3 of 2013-06-05'], ),
    Parameter(name='BO error multipole sextupole random skew 18-pole', group='FAC', is_derived=False, value=bo_error_multipole_sextupole_random_skew_18_pole, symbol=r'<math>M_{B_8/B_2,SEXT}^{\text{rnd,skew}}</math>', units='', deps=['BO error multipole sextupole reference position'], obs=[r'Relative value, calculated at <math>r_0</math>.', unicode('Simulations assume Gaussian distribution truncated at ±2σ.', encoding='utf-8'), 'From approved model3 of 2013-06-05'], ),
    Parameter(name='BO error multipole sextupole random skew 20-pole', group='FAC', is_derived=False, value=bo_error_multipole_sextupole_random_skew_20_pole, symbol=r'<math>M_{B_9/B_2,SEXT}^{\text{rnd,skew}}</math>', units='', deps=['BO error multipole sextupole reference position'], obs=[r'Relative value, calculated at <math>r_0</math>.', unicode('Simulations assume Gaussian distribution truncated at ±2σ.', encoding='utf-8'), 'From approved model3 of 2013-06-05'], ),
]
