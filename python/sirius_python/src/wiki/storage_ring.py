
import optics
from parameter import Parameter


class _P(object):
    ebeam_energy        = 3.0;       # [GeV]
    ebeam_gamma_factor  = optics.gamma(ebeam_energy)
    ebeam_beta_factor   = optics.beta(ebeam_gamma_factor)
    ebeam_velocity      = optics.velocity(ebeam_beta_factor);
    
    ebeam_current         = 350.0 #[mA]
    lattice_version       = 'V500' 
    lattice_circumference = 518.396 #[m]
    lattice_symmetry      = 10
    lattice_length_lss    = 7.0 #[m]
    lattice_length_sss    = 6.0 #[m]
    harmonic_number       = 864
    total_RF_voltage      = 2.7 #[MV]
    
    hardedge_length_of_b1 =  0.828080 #[m] 
    hardedge_length_of_b2 =  1.228262 #[m]
    hardedge_length_of_b3 =  0.428011 #[m]
    hardedge_length_of_bc =  0.125394 #[m]
    dipole_low_field      =  0.583502298783241 #[T]
    dipole_high_field     =  1.949975668803368 #[T]
    radiation_integral_I1 =  0.090315779996644 #[m]
    radiation_integral_I2 =  0.433104068989975 #[1/m]
    radiation_integral_I3 =  0.038257877157466 #[1/m^2]
    radiation_integral_I4 = -0.137100015107741 #[1/m]
    radiation_integral_I5 =  1.218542781664562e-05 #[1/m]
    radiation_integral_I6 =  0.019201555654789,    #[1/m]
    radiation_integral_I1_from_IDs =  0.0 #[m]
    radiation_integral_I2_from_IDs =  0.0 #[1/m]
    radiation_integral_I3_from_IDs =  0.0 #[1/m^2]
    radiation_integral_I4_from_IDs =  0.0 #[1/m]
    radiation_integral_I5_from_IDs =  0.0 #[1/m]
    radiation_integral_I6_from_IDs =  0.0 #[1/m] 
    optics_mode       = 'AC10.5'
    horizontal_tune   = 46.179867828110417
    vertical_tune     = 14.149994739104255
    longitudinal_tune = 0.004421565111775


parameter_list = [

  Parameter(
    name     = 'Storage ring ebeam energy', 
    group    = 'LNLS',
    value    = _P.ebeam_energy,
    symbol   = '<math>E</math>',
    units    = 'GeV', 
    revision = '2014-08-04',
    deps     = []
  ),

  Parameter(
    name     = 'Storage ring ebeam gamma factor', 
    group    = 'FAC',
    value    = _P.ebeam_gamma_factor, 
    symbol   = '<math>\\gamma</math>',
    units    = '', 
    revision = '2014-08-01',
    deps     = ['Storage ring ebeam energy']
  ),

  Parameter(
    name     = 'Storage ring ebeam beta factor', 
    group    = 'FAC',
    value    = _P.ebeam_beta_factor, 
    symbol   = '<math>\\beta</math>',
    units    = '', 
    revision = '2014-08-01',
    deps     = ['Storage ring ebeam gamma factor']
  ),

  Parameter(
    name     = 'Storage ring ebeam velocity', 
    group    = 'FAC',
    value    = _P.ebeam_velocity, 
    symbol   = '<math>v</math>',
    units    = '', 
    revision = '2014-08-01',
    deps     = ['Storage ring ebeam beta factor']
  ),

  Parameter(
    name     = 'Storage ring circumference', 
    group    = 'LNLS',
    value    = _P.lattice_circumference, 
    symbol   = '<math>C</math>',
    units    = 'm', 
    revision = '2014-08-01',
    deps     = [],
  ),

]
