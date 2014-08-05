# -*- coding: utf-8 -*-

import optics
from parameter import Parameter


def mark_math(name):
    return '<math>' + name + '</math>'

'''

-- equilibrium parameters with dipoles only --

sr_equil_Jx_dipoles = {value = 1 - sr_equil_I4_dipoles.value/sr_equil_I2_dipoles.value, unit = ''}
sr_equil_Jy_dipoles = {value = 1.0, unit = ''}
sr_equil_Js_dipoles = {value = 4.0 - sr_equil_Jx_dipoles.value - sr_equil_Jy_dipoles.value, unit = ''}
sr_equil_alpha1_dipoles = {value = sr_equil_I1_dipoles.value / sr_latt_circumference.value, unit = ''}
sr_equil_rf_energy_acceptance_dipoles = {value = calc_rf_energy_acceptance(sr_equil_overvoltage_dipoles.value, sr_ebeam_energy.value, sr_equil_U0_dipoles.value, sr_rf_harmonic_number.value, sr_equil_alpha1_dipoles.value), unit = '%'}
sr_equil_nat_emitt_dipoles = {value = calc_natural_emittance(sr_ebeam_gamma.value, sr_equil_Jx_dipoles.value, sr_equil_I2_dipoles.value, sr_equil_I5_dipoles.value), unit = 'nm.rad'}
sr_equil_nat_sigmae_dipoles = {value = calc_energy_spread(sr_ebeam_gamma.value, sr_equil_I2_dipoles.value, sr_equil_I3_dipoles.value, sr_equil_I4_dipoles.value), unit = '%'}

-- radiation integrals for IDs --

sr_equil_U0_IDs = {value = calc_U0(sr_ebeam_energy.value, sr_equil_I2_IDs.value), unit = 'keV'}
sr_equil_Jx = {value = 1 - sr_equil_I4.value/sr_equil_I2.value, unit = ''}
sr_equil_Jy = {value = 1.0, unit = ''}
sr_equil_Js = {value = 4.0 - sr_equil_Jx.value - sr_equil_Jy.value, unit = ''}
sr_equil_U0 = {value = sr_equil_U0_dipoles.value + sr_equil_U0_IDs.value, unit = 'keV'}
sr_equil_overvoltage = {value = (1e6*sr_rf_total_voltage.value)/(sr_equil_U0.value*1e3), unit = ''}
sr_equil_sync_phase = {value = calc_sync_phase(sr_equil_overvoltage.value), unit = 'deg'}
sr_equil_alpha1 = {value = sr_equil_I1.value / sr_latt_circumference.value, unit = ''}
sr_equil_rf_energy_acceptance = {value = calc_rf_energy_acceptance(sr_equil_overvoltage.value, sr_ebeam_energy.value, sr_equil_U0.value, sr_rf_harmonic_number.value, sr_equil_alpha1.value), unit = '%'}
sr_equil_nat_emitt  = {value = calc_natural_emittance(sr_ebeam_gamma.value, sr_equil_Jx.value, sr_equil_I2.value, sr_equil_I5.value), unit = 'nm.rad'}
sr_equil_nat_sigmae = {value = calc_energy_spread(sr_ebeam_gamma.value, sr_equil_I2.value, sr_equil_I3.value, sr_equil_I4.value), unit = '%'}

--optics

sr_optics_tune_x_freq = {value = 1000*sr_rev_frequency.value * (sr_optics_tune_x.value - math.floor(sr_optics_tune_x.value)), unit = 'kHz'}
sr_optics_tune_y_freq = {value = 1000*sr_rev_frequency.value * (sr_optics_tune_y.value - math.floor(sr_optics_tune_y.value)), unit = 'kHz'}
sr_optics_tune_s_freq = {value = 1000*sr_rev_frequency.value * (sr_optics_tune_s.value - math.floor(sr_optics_tune_s.value)), unit = 'kHz'}

**************************************************************************************************************

function p.linear_momentum_compaction_from_dipoles (frame) return get_parameter(sr_equil_alpha1_dipoles,frame.args) end
function p.rf_energy_acceptance_from_dipoles       (frame) return get_parameter(sr_equil_rf_energy_acceptance_dipoles,frame.args) end
function p.horizontal_damping_partition_number_from_dipoles   (frame) return get_parameter(sr_equil_Jx_dipoles,frame.args) end
function p.vertical_damping_partition_number_from_dipoles     (frame) return get_parameter(sr_equil_Jy_dipoles,frame.args) end
function p.longitudinal_damping_partition_number_from_dipoles (frame) return get_parameter(sr_equil_Js_dipoles,frame.args) end
function p.natural_emittance_from_dipoles                     (frame) return get_parameter(sr_equil_nat_emitt_dipoles,frame.args) end
function p.natural_energy_spread_from_dipoles                 (frame) return get_parameter(sr_equil_nat_sigmae_dipoles,frame.args) end

function p.energy_loss_per_turn_from_IDs  (frame) return get_parameter(sr_equil_U0_IDs,frame.args) end

function p.energy_loss_per_turn       (frame) return get_parameter(sr_equil_U0,frame.args) end
function p.overvoltage                (frame) return get_parameter(sr_equil_overvoltage,frame.args) end
function p.synchronous_phase          (frame) return get_parameter(sr_equil_sync_phase,frame.args) end
function p.linear_momentum_compaction (frame) return get_parameter(sr_equil_alpha1,frame.args) end
function p.rf_energy_acceptance       (frame) return get_parameter(sr_equil_rf_energy_acceptance,frame.args) end
function p.horizontal_damping_partition_number   (frame) return get_parameter(sr_equil_Jx,frame.args) end
function p.vertical_damping_partition_number     (frame) return get_parameter(sr_equil_Jy,frame.args) end
function p.longitudinal_damping_partition_number (frame) return get_parameter(sr_equil_Js,frame.args) end
function p.natural_emittance                     (frame) return get_parameter(sr_equil_nat_emitt,frame.args) end
function p.natural_energy_spread                 (frame) return get_parameter(sr_equil_nat_sigmae,frame.args) end

function p.horizontal_betatron_frequency   (frame) return get_parameter(sr_optics_tune_x_freq,frame.args) end
function p.vertical_betatron_frequency     (frame) return get_parameter(sr_optics_tune_y_freq,frame.args) end
function p.longitudinal_betatron_frequency (frame) return get_parameter(sr_optics_tune_s_freq,frame.args) end

'''

class _P(object):
    
    ebeam_energy            = 3.0       # [GeV]
    ebeam_gamma_factor      = optics.gamma(ebeam_energy)
    ebeam_beta_factor       = optics.beta(ebeam_gamma_factor)
    ebeam_velocity          = optics.velocity(ebeam_beta_factor)
    ebeam_magnetic_rigidity = optics.brho(ebeam_energy, ebeam_beta_factor)
    
    ebeam_current                     = 350.0 #[mA]
    lattice_version                   = 'V500' 
    lattice_circumference             = 518.396 #[m]
    lattice_symmetry                  = 10
    length_of_long_straight_sections  = 7.0 #[m]
    length_of_short_straight_sections = 6.0 #[m]
    harmonic_number                   = 864
    total_RF_voltage                  = 2.7 #[MV]
    
    revolution_period = optics.revolution_period(lattice_circumference, ebeam_velocity) 
    revolution_frequency = optics.revolution_frequency(revolution_period)
    rf_frequency = optics.rf_frequency(revolution_frequency, harmonic_number)
    
    number_of_electrons = optics.number_of_electrons(ebeam_current, revolution_period)

    number_of_long_straight_sections  = lattice_symmetry
    number_of_short_straight_sections = lattice_symmetry
    number_of_B1_dipoles              = 4 * lattice_symmetry
    number_of_B2_dipoles              = 4 * lattice_symmetry
    number_of_B3_dipoles              = 4 * lattice_symmetry
    number_of_BC_dipoles              = 2 * lattice_symmetry
    
    hardedge_length_of_B1_dipoles =  0.828080 #[m] 
    hardedge_length_of_B2_dipoles =  1.228262 #[m]
    hardedge_length_of_B3_dipoles =  0.428011 #[m]
    hardedge_length_of_BC_dipoles =  0.125394 #[m]
    dipole_low_magnetic_field     =  0.583502298783241 #[T]
    dipole_high_magnetic_field    =  1.949975668803368 #[T]
    dipole_low_magnetic_field_bending_radius = optics.rho(ebeam_magnetic_rigidity, dipole_low_magnetic_field)
    dipole_high_magnetic_field_bending_radius = optics.rho(ebeam_magnetic_rigidity, dipole_high_magnetic_field)
    dipole_low_magnetic_field_critical_energy = optics.critical_energy(ebeam_gamma_factor, dipole_low_magnetic_field_bending_radius)
    dipole_high_magnetic_field_critical_energy = optics.critical_energy(ebeam_gamma_factor, dipole_high_magnetic_field_bending_radius)
    radiation_integral_I1_from_dipoles =  0.090315779996644     #[m]
    radiation_integral_I2_from_dipoles =  0.433104068989975     #[1/m]
    radiation_integral_I3_from_dipoles =  0.038257877157466     #[1/m^2]
    radiation_integral_I4_from_dipoles = -0.137100015107741     #[1/m]
    radiation_integral_I5_from_dipoles =  1.218542781664562e-05 #[1/m]
    radiation_integral_I6_from_dipoles =  0.019201555654789     #[1/m]
    radiation_integral_I1_from_IDs =  0.0 #[m]
    radiation_integral_I2_from_IDs =  0.0 #[1/m]
    radiation_integral_I3_from_IDs =  0.0 #[1/m^2]
    radiation_integral_I4_from_IDs =  0.0 #[1/m]
    radiation_integral_I5_from_IDs =  0.0 #[1/m]
    radiation_integral_I6_from_IDs =  0.0 #[1/m] 
    radiation_integral_I1 = radiation_integral_I1_from_dipoles + radiation_integral_I1_from_IDs #[m]
    radiation_integral_I2 = radiation_integral_I2_from_dipoles + radiation_integral_I2_from_IDs #[m]
    radiation_integral_I3 = radiation_integral_I3_from_dipoles + radiation_integral_I3_from_IDs #[m]
    radiation_integral_I4 = radiation_integral_I4_from_dipoles + radiation_integral_I4_from_IDs #[m]
    radiation_integral_I5 = radiation_integral_I5_from_dipoles + radiation_integral_I5_from_IDs #[m]
    radiation_integral_I6 = radiation_integral_I6_from_dipoles + radiation_integral_I6_from_IDs #[m]
    
    optics_mode       = 'AC10.5'
    horizontal_tune   = 46.179867828110417
    vertical_tune     = 14.149994739104255
    longitudinal_tune = 0.004421565111775
    
    energy_loss_per_turn_from_dipoles = optics.U0(ebeam_energy, radiation_integral_I2_from_dipoles)
    overvoltage_from_dipoles = optics.overvoltage(total_RF_voltage, energy_loss_per_turn_from_dipoles)
    synchronous_phase_from_dipoles = optics.sync_phase(overvoltage_from_dipoles)


label = 'Storage ring'

parameter_list = [

  Parameter(
    name     = 'Storage ring ebeam energy', 
    group    = 'LNLS',
    value    = _P.ebeam_energy,
    symbol   = mark_math(r'E'),
    units    = 'GeV', 
    revision = '2014-08-04',
    deps     = [],
    obs      = '',
  ),

  Parameter(
    name     = 'Storage ring ebeam gamma factor', 
    group    = 'FAC',
    value    = _P.ebeam_gamma_factor, 
    symbol   = mark_math(r'\gamma'),
    units    = '', 
    revision = '2014-08-01',
    deps     = ['Storage ring ebeam energy'],
    obs      = '',
  ),

  Parameter(
    name     = 'Storage ring ebeam beta factor', 
    group    = 'FAC',
    value    = _P.ebeam_beta_factor, 
    symbol   = mark_math(r'\beta'),
    units    = '', 
    revision = '2014-08-01',
    deps     = ['Storage ring ebeam gamma factor'],
    obs      = '',
  ),

  Parameter(
    name     = 'Storage ring ebeam velocity', 
    group    = 'FAC',
    value    = _P.ebeam_velocity, 
    symbol   = mark_math(r'v'),
    units    = '', 
    revision = '2014-08-01',
    deps     = ['Storage ring ebeam beta factor'],
    obs      = '',
  ),
                  
  Parameter(
    name     = 'Storage ring ebeam magnetic rigidity', 
    group    = 'FAC',
    value    = _P.ebeam_magnetic_rigidity, 
    symbol   = mark_math(r'(B\rho) = \frac{p}{ec} = \frac{E}{ec^2}'),
    units    = 'T.m', 
    revision = '2014-08-01',
    deps     = ['Storage ring ebeam energy'],
    obs      = '',
  ),
                  
  Parameter(
    name     = 'Storage ring ebeam current', 
    group    = 'FAC',
    value    = _P.ebeam_current, 
    symbol   = mark_math(r'I'),
    units    = 'mA', 
    revision = '2014-08-01',
    deps     = [],
    obs      = '',
  ),

  Parameter(
    name     = 'Storage ring lattice version', 
    group    = 'FAC',
    value    = _P.lattice_version, 
    symbol   = '',
    units    = '', 
    revision = '2014-08-01',
    deps     = [],
    obs      = '',
  ),

  Parameter(
    name     = 'Storage ring circumference', 
    group    = 'LNLS',
    value    = _P.lattice_circumference, 
    symbol   = mark_math(r'C'),
    units    = 'm', 
    revision = '2014-08-01',
    deps     = [],
    obs      = '',
  ),
                  
  Parameter(
    name     = 'Storage ring lattice symmetry', 
    group    = 'FAC',
    value    = _P.lattice_symmetry, 
    symbol   = mark_math(r'N_{SUPERCELLS}'),
    units    = '', 
    revision = '2014-08-01',
    deps     = [],
    obs      = '',
  ),
                  
  Parameter(
    name     = 'Storage ring number of long straight sections', 
    group    = 'FAC',
    value    = _P.number_of_long_straight_sections ,
    symbol   = mark_math(r'N_{lss}'),
    units    = '', 
    revision = '2014-08-01',
    deps     = [],
    obs      = '',
  ),
                  
  Parameter(
    name     = 'Storage ring number of short straight sections', 
    group    = 'FAC',
    value    = _P.number_of_short_straight_sections ,
    symbol   = mark_math(r'N_{sss}'),
    units    = '', 
    revision = '2014-08-01',
    deps     = [],
    obs      = '',
  ),
                  
  Parameter(
    name     = 'Storage ring length of long straight sections', 
    group    = 'FAC',
    value    = _P.length_of_long_straight_sections, 
    symbol   = mark_math(r'L_{lss}'),
    units    = 'm', 
    revision = '2014-08-01',
    deps     = [],
    obs      = '',
  ),
                  
  Parameter(
    name     = 'Storage ring length of short straight sections', 
    group    = 'FAC',
    value    = _P.length_of_short_straight_sections, 
    symbol   = mark_math(r'L_{sss}'),
    units    = 'm', 
    revision = '2014-08-01',
    deps     = [],
    obs      = '',
  ),
                  
  Parameter(
    name     = 'Storage ring harmonic number', 
    group    = 'FAC',
    value    = _P.harmonic_number, 
    symbol   = mark_math(r'h'),
    units    = '', 
    revision = '2014-08-01',
    deps     = [],
    obs      = '',
  ),
                  
  Parameter(name = 'Storage ring total RF voltage', 
    group    = 'FAC',
    value    = _P.total_RF_voltage, 
    symbol   = mark_math(r'V_{RF}'),
    units    = 'MV', 
    revision = '2014-08-01',
    deps     = [],
    obs      = '',
  ),              
  
  Parameter(name = 'Storage ring revolution period', 
    group    = 'FAC',
    value    = _P.revolution_period, 
    symbol   = mark_math(r'T_{rev}'),
    units    = unicode('μs', encoding='utf-8'), 
    revision = '2014-08-01',
    deps     = ['Storage ring circumference', 'Storage ring ebeam velocity'],
    obs      = '',
  ),
 
  Parameter(name = 'Storage ring revolution frequency', 
    group    = 'FAC',
    value    = _P.revolution_frequency, 
    symbol   = mark_math(r'f_{rev}'),
    units    = u'MHz', 
    revision = '2014-08-01',
    deps     = ['Storage ring revolution period'],
    obs      = '',
  ),

  Parameter(name = 'Storage ring RF frequency', 
    group    = 'FAC',
    value    = _P.rf_frequency, 
    symbol   = mark_math(r'f_{RF}'),
    units    = u'MHz', 
    revision = '2014-08-01',
    deps     = ['Storage ring revolution frequency', 'Storage ring harmonic number'],
    obs      = '',
  ),

  Parameter(name = 'Storage ring number of electrons', 
    group    = 'FAC',
    value    = _P.number_of_electrons, 
    symbol   = mark_math(r'N'),
    units    = u'', 
    revision = '2014-08-01',
    deps     = ['Storage ring ebeam current', 'Storage ring revolution period'],
    obs      = '',
  ),
 
  Parameter(name = 'Storage ring number of B1 dipoles', 
    group    = 'FAC',
    value    = _P.number_of_B1_dipoles, 
    symbol   = mark_math(r'N_{B1}'),
    units    = '', 
    revision = '2014-08-01',
    deps     = [],
    obs      = '',
  ), 
            
  Parameter(name = 'Storage ring number of B2 dipoles', 
    group    = 'FAC',
    value    = _P.number_of_B2_dipoles, 
    symbol   = mark_math(r'N_{B2}'),
    units    = '', 
    revision = '2014-08-01',
    deps     = [],
    obs      = '',
  ), 
                  
  Parameter(name = 'Storage ring number of B3 dipoles', 
    group    = 'FAC',
    value    = _P.number_of_B3_dipoles, 
    symbol   = mark_math(r'N_{B3}'),
    units    = '', 
    revision = '2014-08-01',
    deps     = [],
    obs      = '',
  ), 
         
  Parameter(name = 'Storage ring number of BC dipoles', 
    group    = 'FAC',
    value    = _P.number_of_BC_dipoles, 
    symbol   = mark_math(r'N_{BC}'),
    units    = '', 
    revision = '2014-08-01',
    deps     = [],
    obs      = '',
  ), 
                           
  Parameter(name = 'Storage ring hardedge length of B1 dipoles', 
    group    = 'FAC',
    value    = _P.hardedge_length_of_B1_dipoles, 
    symbol   = mark_math(r'L_{B1}'),
    units    = 'm', 
    revision = '2014-08-01',
    deps     = [],
    obs      = '',
  ),  
                
  Parameter(name = 'Storage ring hardedge length of B2 dipoles', 
    group    = 'FAC',
    value    = _P.hardedge_length_of_B2_dipoles, 
    symbol   = mark_math(r'L_{B2}'),
    units    = 'm', 
    revision = '2014-08-01',
    deps     = [],
    obs      = '',
  ),  
                  
  Parameter(name = 'Storage ring hardedge length of B3 dipoles', 
    group    = 'FAC',
    value    = _P.hardedge_length_of_B3_dipoles, 
    symbol   = mark_math(r'L_{B3}'),
    units    = 'm', 
    revision = '2014-08-01',
    deps     = [],
    obs      = '',
  ),  
                  
  Parameter(name = 'Storage ring hardedge length of BC dipoles', 
    group    = 'FAC',
    value    = _P.hardedge_length_of_BC_dipoles, 
    symbol   = mark_math(r'L_{BC}'),
    units    = 'm', 
    revision = '2014-08-01',
    deps     = [],
    obs      = '',
  ),  
                  
  Parameter(name = 'Storage ring dipole low magnetic field', 
    group    = 'FAC',
    value    = _P.dipole_low_magnetic_field, 
    symbol   = mark_math(r'B_{low}'),
    units    = 'T', 
    revision = '2014-08-01',
    deps     = [],
    obs      = '',
  ), 
                
  Parameter(name = 'Storage ring dipole high magnetic field', 
    group    = 'FAC',
    value    = _P.dipole_high_magnetic_field, 
    symbol   = mark_math(r'B_{high}'),
    units    = 'T', 
    revision = '2014-08-01',
    deps     = [],
    obs      = '',
  ), 
                  
  Parameter(name = 'Storage ring dipole low magnetic field bending radius', 
    group    = 'FAC',
    value    = _P.dipole_low_magnetic_field_bending_radius,
    symbol   = mark_math(r'\rho_{low} = \frac{ec/p}{B_{low}} = \frac{(B\rho)}{B_{low}}'),
    units    = 'm', 
    revision = '2014-08-01',
    deps     = ['Storage ring ebeam magnetic rigidity', 'Storage ring dipole low magnetic field'],
    obs      = '',
  ), 
                
  Parameter(name = 'Storage ring dipole high magnetic field bending radius', 
    group    = 'FAC',
    value    = _P.dipole_high_magnetic_field_bending_radius,
    symbol   = mark_math(r'\rho_{high} = \frac{ec/p}{B_{high}} = \frac{(B\rho)}{B_{high}}'),
    units    = 'm', 
    revision = '2014-08-01',
    deps     = ['Storage ring ebeam magnetic rigidity', 'Storage ring dipole high magnetic field'],
    obs      = '',
  ), 
  
  Parameter(name = 'Storage ring dipole low magnetic field critical energy', 
    group    = 'FAC',
    value    = _P.dipole_low_magnetic_field_critical_energy,
    symbol   = mark_math(r'\epsilon_{c,low} = \frac{3}{2} \hbar c \frac{\gamma^3}{\rho_{low}}'),
    units    = 'keV', 
    revision = '2014-08-01',
    deps     = ['Storage ring ebeam gamma factor', 'Storage ring dipole low magnetic field bending radius'],
    obs      = '',
  ), 
                
  Parameter(name = 'Storage ring dipole high magnetic field critical energy', 
    group    = 'FAC',
    value    = _P.dipole_high_magnetic_field_critical_energy,
    symbol   = mark_math(r'\epsilon_{c,high} = \frac{3}{2} \hbar c \frac{\gamma^3}{\rho_{high}}'),
    units    = 'keV', 
    revision = '2014-08-01',
    deps     = ['Storage ring ebeam gamma factor', 'Storage ring dipole high magnetic field bending radius'],
    obs      = '',
  ), 
                  
                  
  Parameter(name = 'Storage ring radiation integral I1 from dipoles', 
    group    = 'FAC',
    value    = _P.radiation_integral_I1_from_dipoles, 
    symbol   = mark_math(r'I_{1,DIP} = \oint{\frac{\eta_x}{\rho_x} ds}'),
    units    = 'm', 
    revision = '2014-08-01',
    deps     = ['Storage ring ebeam magnetic rigidity', 'Storage ring lattice version', 'Storage ring optics mode'],
    obs      = '',
  ), 
                  
  Parameter(name = 'Storage ring radiation integral I2 from dipoles', 
    group    = 'FAC',
    value    = _P.radiation_integral_I2_from_dipoles, 
    symbol   = mark_math(r'I_{2,DIP} = \oint{\frac{1}{\rho_x^2} ds}'),
    units    = '1/m', 
    revision = '2014-08-01',
    deps     = ['Storage ring ebeam magnetic rigidity', 'Storage ring lattice version'],
    obs      = '',
  ), 
   
  Parameter(name = 'Storage ring radiation integral I3 from dipoles', 
    group    = 'FAC',
    value    = _P.radiation_integral_I3_from_dipoles, 
    symbol   = mark_math(r'I_{3,DIP} = \oint{\frac{1}{|\rho_x|^3} ds}'),
    units    = '1/m^2', 
    revision = '2014-08-01',
    deps     = ['Storage ring ebeam magnetic rigidity', 'Storage ring lattice version'],
    obs      = '',
  ), 
                  
  Parameter(name = 'Storage ring radiation integral I4 from dipoles', 
    group    = 'FAC',
    value    = _P.radiation_integral_I4_from_dipoles, 
    symbol   = mark_math(r'I_{4,DIP} = \frac{\eta_x(s_0) \tan \theta(s_0)}{\rho_x^2} + \oint{\frac{\eta_x}{\rho_x^3} \left(1 + 2 \rho_x^2 k\right) ds} + \frac{\eta_x(s_1) \tan \theta(s_1)}{\rho_x^2}'),
    units    = '1/m', 
    revision = '2014-08-01',
    deps     = ['Storage ring ebeam magnetic rigidity', 'Storage ring lattice version'],
    obs      = '',
  ),   
                  
  Parameter(name = 'Storage ring radiation integral I5 from dipoles', 
    group    = 'FAC',
    value    = _P.radiation_integral_I5_from_dipoles, 
    symbol   = mark_math(r'I_{5,DIP} = \oint{\frac{H_x}{|\rho_x|^3} ds}'),
    units    = '1/m', 
    revision = '2014-08-01',
    deps     = ['Storage ring ebeam magnetic rigidity', 'Storage ring lattice version', 'Storage ring optics mode'],
    obs      = r"<math>H_x \equiv \gamma_x \eta_x^2 + 2 \alpha_x \eta_x \eta_x^' + \beta_x {\eta_x^'}^2</math>",
  ),  
                  
  Parameter(name = 'Storage ring radiation integral I6 from dipoles', 
    group    = 'FAC',
    value    = _P.radiation_integral_I6_from_dipoles, 
    symbol   = mark_math(r'I_{6,DIP} = \oint{k^2 \eta_x^2 ds}'),
    units    = '1/m', 
    revision = '2014-08-01',
    deps     = ['Storage ring ebeam magnetic rigidity', 'Storage ring lattice version', 'Storage ring optics mode'],
    obs      = '',
  ),            
  
  Parameter(name = 'Storage ring radiation integral I1 from IDs', 
    group    = 'FAC',
    value    = _P.radiation_integral_I1_from_IDs, 
    symbol   = mark_math(r'I_{1,IDs} = \oint{\frac{\eta_x}{\rho_x} ds}'),
    units    = 'm', 
    revision = '2014-08-01',
    deps     = ['Storage ring ebeam magnetic rigidity', 'Storage ring lattice version', 'Storage ring optics mode'],
    obs      = '',
  ), 
                  
  Parameter(name = 'Storage ring radiation integral I2 from IDs', 
    group    = 'FAC',
    value    = _P.radiation_integral_I2_from_IDs, 
    symbol   = mark_math(r'I_{2,IDs} = \oint{\frac{1}{\rho_x^2} ds}'),
    units    = '1/m', 
    revision = '2014-08-01',
    deps     = ['Storage ring ebeam magnetic rigidity', 'Storage ring lattice version'],
    obs      = '',
  ), 
   
  Parameter(name = 'Storage ring radiation integral I3 from IDs', 
    group    = 'FAC',
    value    = _P.radiation_integral_I3_from_IDs, 
    symbol   = mark_math(r'I_{3,IDs} = \oint{\frac{1}{|\rho_x|^3} ds}'),
    units    = '1/m^2', 
    revision = '2014-08-01',
    deps     = ['Storage ring ebeam magnetic rigidity', 'Storage ring lattice version'],
    obs      = '',
  ), 
                  
  Parameter(name = 'Storage ring radiation integral I4 from IDs', 
    group    = 'FAC',
    value    = _P.radiation_integral_I4_from_IDs, 
    symbol   = mark_math(r'I_{4,IDs} = \frac{\eta_x(s_0) \tan \theta(s_0)}{\rho_x^2} + \oint{\frac{\eta_x}{\rho_x^3} \left(1 + 2 \rho_x^2 k\right) ds} + \frac{\eta_x(s_1) \tan \theta(s_1)}{\rho_x^2}'),
    units    = '1/m', 
    revision = '2014-08-01',
    deps     = ['Storage ring ebeam magnetic rigidity', 'Storage ring lattice version'],
    obs      = '',
  ),   
                  
  Parameter(name = 'Storage ring radiation integral I5 from IDs', 
    group    = 'FAC',
    value    = _P.radiation_integral_I5_from_IDs, 
    symbol   = mark_math(r'I_{5,IDs} = \oint{\frac{H_x}{|\rho_x|^3} ds}'),
    units    = '1/m', 
    revision = '2014-08-01',
    deps     = ['Storage ring ebeam magnetic rigidity', 'Storage ring lattice version', 'Storage ring optics mode'],
    obs      = r"<math>H_x \equiv \gamma_x \eta_x^2 + 2 \alpha_x \eta_x \eta_x^' + \beta_x {\eta_x^'}^2</math>",
  ),  
                  
  Parameter(name = 'Storage ring radiation integral I6 from IDs', 
    group    = 'FAC',
    value    = _P.radiation_integral_I6_from_IDs, 
    symbol   = mark_math(r'I_{6,IDs} = \oint{k^2 \eta_x^2 ds}'),
    units    = '1/m', 
    revision = '2014-08-01',
    deps     = ['Storage ring ebeam magnetic rigidity', 'Storage ring lattice version', 'Storage ring optics mode'],
    obs      = '',
  ),                 
  
  Parameter(name = 'Storage ring radiation integral I1', 
    group    = 'FAC',
    value    = _P.radiation_integral_I1, 
    symbol   = mark_math(r'I_{1} = I_{1,DIP} + I_{1,IDs}'),
    units    = 'm', 
    revision = '2014-08-01',
    deps     = ['Storage ring radiation integral I1 from dipoles', 'Storage ring radiation integral I1 from IDs'],
    obs      = '',
  ), 
                  
  Parameter(name = 'Storage ring radiation integral I2', 
    group    = 'FAC',
    value    = _P.radiation_integral_I2, 
    symbol   = mark_math(r'I_{2} = I_{2,DIP} + I_{2,IDs}'),
    units    = '1/m', 
    revision = '2014-08-01',
    deps     = ['Storage ring radiation integral I2 from dipoles', 'Storage ring radiation integral I2 from IDs'],
    obs      = '',
  ), 
   
  Parameter(name = 'Storage ring radiation integral I3', 
    group    = 'FAC',
    value    = _P.radiation_integral_I3, 
    symbol   = mark_math(r'I_{3} = I_{3,DIP} + I_{3,IDs}'),
    units    = '1/m^2', 
    revision = '2014-08-01',
    deps     = ['Storage ring radiation integral I3 from dipoles', 'Storage ring radiation integral I3 from IDs'],
    obs      = '',
  ), 
                  
  Parameter(name = 'Storage ring radiation integral I4', 
    group    = 'FAC',
    value    = _P.radiation_integral_I4, 
    symbol   = mark_math(r'I_{4} = I_{4,DIP} + I_{4,IDs}'),
    units    = '1/m', 
    revision = '2014-08-01',
    deps     = ['Storage ring radiation integral I4 from dipoles', 'Storage ring radiation integral I4 from IDs'],
    obs      = '',
  ),   
                  
  Parameter(name = 'Storage ring radiation integral I5', 
    group    = 'FAC',
    value    = _P.radiation_integral_I5, 
    symbol   = mark_math(r'I_5 = \oint{\frac{H_x}{|\rho_x|^3} ds} = I_{5,DIP} + I_{5,IDs}'),
    units    = '1/m', 
    revision = '2014-08-01',
    deps     = ['Storage ring radiation integral I5 from dipoles', 'Storage ring radiation integral I5 from IDs'],
    obs      = r"<math>H_x \equiv \gamma_x \eta_x^2 + 2 \alpha_x \eta_x \eta_x^' + \beta_x {\eta_x^'}^2</math>",
  ),  
                  
  Parameter(name = 'Storage ring radiation integral I6', 
    group    = 'FAC',
    value    = _P.radiation_integral_I6, 
    symbol   = mark_math(r'I_{6} = I_{6,DIP} + I_{6,IDs}'),
    units    = '1/m', 
    revision = '2014-08-01',
    deps     = ['Storage ring radiation integral I6 from dipoles', 'Storage ring radiation integral I6 from IDs'],
    obs      = '',
  ),   
   
  Parameter(name = 'Storage ring optics mode', 
    group    = 'FAC',
    value    = _P.optics_mode, 
    symbol   = '',
    units    = '', 
    revision = '2014-08-01',
    deps     = [],
    obs      = '',
  ),
  
  Parameter(name = 'Storage ring horizontal tune', 
    group    = 'FAC',
    value    = _P.horizontal_tune, 
    symbol   = mark_math(r'\nu_x'),
    units    = '', 
    revision = '2014-08-01',
    deps     = ['Storage ring lattice version', 'Storage ring optics mode'],
    obs      = '',
  ),    
                
  Parameter(name = 'Storage ring vertical tune', 
    group    = 'FAC',
    value    = _P.vertical_tune, 
    symbol   = mark_math(r'\nu_y'),
    units    = '', 
    revision = '2014-08-01',
    deps     = ['Storage ring lattice version', 'Storage ring optics mode'],
    obs      = '',
  ),  
                  
  Parameter(name = 'Storage ring longitudinal tune', 
    group    = 'FAC',
    value    = _P.longitudinal_tune, 
    symbol   = mark_math(r'\nu_s'),
    units    = '', 
    revision = '2014-08-01',
    deps     = ['Storage ring lattice version', 'Storage ring optics mode'],
    obs      = '',
  ),                            
  
  Parameter(name = 'Storage ring energy loss per turn from dipoles', 
    group    = 'FAC',
    value    = _P.energy_loss_per_turn_from_dipoles,
    symbol   = mark_math(r'U_{0,DIP} = \oint{P_\gamma dt} = \frac{C_\gamma}{2\pi} E^4_0 I_{2,DIP}'),
    units    = 'keV', 
    revision = '2014-08-01',
    deps     = ['Storage ring ebeam energy', 'Storage ring radiation integral I2 from dipoles'],
    obs      = '',
  ),                            
  
  Parameter(name = 'Storage ring overvoltage from dipoles', 
    group    = 'FAC',
    value    = _P.overvoltage_from_dipoles,
    symbol   = mark_math(r'q_{DIP} = \frac{eV_{RF}}{U_{0,DIP}}'),
    units    = '', 
    revision = '2014-08-01',
    deps     = ['Storage ring total RF voltage', 'Storage ring energy loss per turn from dipoles'],
    obs      = '',
  ),                            
  
  Parameter(name = 'Storage ring synchronous phase from dipoles', 
    group    = 'FAC',
    value    = _P.synchronous_phase_from_dipoles, 
    symbol   = mark_math(r'\phi_0 = \pi - \arcsin\left(\frac{1}{q_{DIP}}\right)'),
    units    = unicode('°', encoding='utf-8'),
    revision = '2014-08-01',
    deps     = ['Storage ring overvoltage from dipoles'],
    obs      = '',
  ),
                            
  
#  Parameter(name = 'Storage ring ', 
#    group    = 'FAC',
#    value    = _P., 
#    symbol   = mark_math(r''),
#    units    = '', 
#    revision = '2014-08-01',
#    deps     = [],
#    obs      = '',
#  ),
#                            
#  
#  Parameter(name = 'Storage ring ', 
#    group    = 'FAC',
#    value    = _P., 
#    symbol   = mark_math(r''),
#    units    = '', 
#    revision = '2014-08-01',
#    deps     = [],
#    obs      = '',
#  ),
#                            
#  
#  Parameter(name = 'Storage ring ', 
#    group    = 'FAC',
#    value    = _P., 
#    symbol   = mark_math(r''),
#    units    = '', 
#    revision = '2014-08-01',
#    deps     = [],
#    obs      = '',
#  ),
#                            
#  
#  Parameter(name = 'Storage ring ', 
#    group    = 'FAC',
#    value    = _P., 
#    symbol   = mark_math(r''),
#    units    = '', 
#    revision = '2014-08-01',
#    deps     = [],
#    obs      = '',
#  ),
#                            
#  
#  Parameter(name = 'Storage ring ', 
#    group    = 'FAC',
#    value    = _P., 
#    symbol   = mark_math(r''),
#    units    = '', 
#    revision = '2014-08-01',
#    deps     = [],
#    obs      = '',
#  ),
#                            
#  
#  Parameter(name = 'Storage ring ', 
#    group    = 'FAC',
#    value    = _P., 
#    symbol   = mark_math(r''),
#    units    = '', 
#    revision = '2014-08-01',
#    deps     = [],
#    obs      = '',
#  ),
#                            
#  
#  Parameter(name = 'Storage ring ', 
#    group    = 'FAC',
#    value    = _P., 
#    symbol   = mark_math(r''),
#    units    = '', 
#    revision = '2014-08-01',
#    deps     = [],
#    obs      = '',
#  ),
#                            
#  
#  Parameter(name = 'Storage ring ', 
#    group    = 'FAC',
#    value    = _P., 
#    symbol   = mark_math(r''),
#    units    = '', 
#    revision = '2014-08-01',
#    deps     = [],
#    obs      = '',
#  ),
#                            
#  
#  Parameter(name = 'Storage ring ', 
#    group    = 'FAC',
#    value    = _P., 
#    symbol   = mark_math(r''),
#    units    = '', 
#    revision = '2014-08-01',
#    deps     = [],
#    obs      = '',
#  ),


]
