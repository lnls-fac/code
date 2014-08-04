
import optics
from parameter import Parameter


class _P(object):
    ebeam_extraction_energy       = 3.0;       # [GeV]
    ebeam_extraction_gamma_factor = optics.gamma(ebeam_extraction_energy)
    ebeam_extraction_beta_factor  = optics.beta(ebeam_extraction_gamma_factor)
    ebeam_extraction_velocity     = optics.velocity(ebeam_extraction_beta_factor);
    
    ebeam_current         = 2.0 #[mA]
    lattice_version       = '' 
    lattice_circumference = 496.8 #[m]
    lattice_symmetry      = 10
    harmonic_number       = 828

    radiation_integral_I1 =  0.090315779996644 #[m]
    radiation_integral_I2 =  0.433104068989975 #[1/m]
    radiation_integral_I3 =  0.038257877157466 #[1/m^2]
    radiation_integral_I4 = -0.137100015107741 #[1/m]
    radiation_integral_I5 =  1.218542781664562e-05 #[1/m]
    radiation_integral_I6 =  0.019201555654789,    #[1/m]

    optics_mode       = ''
    horizontal_tune   = 19.204749345767866
    vertical_tune     = 7.307442329080478
    longitudinal_tune = 0.004419249840938


parameter_list = [

  Parameter(
    name     = 'Booster ebeam extraction energy', 
    group    = 'LNLS',
    value    = _P.ebeam_extraction_energy,
    symbol   = '<math>E</math>',
    units    = 'GeV', 
    revision = '2014-08-04',
    deps     = ['Storage ring ebeam energy']
  ),

  Parameter(
    name     = 'Booster ebeam extraction gamma factor', 
    group    = 'FAC',
    value    = _P.ebeam_extraction_gamma_factor, 
    symbol   = '<math>\\gamma</math>',
    units    = '', 
    revision = '2014-08-01',
    deps     = ['Booster ebeam extraction energy']
  ),

  Parameter(
    name     = 'Booster ebeam extraction beta factor', 
    group    = 'FAC',
    value    = _P.ebeam_extraction_beta_factor, 
    symbol   = '<math>\\beta</math>',
    units    = '', 
    revision = '2014-08-01',
    deps     = ['Booster ebeam extraction gamma factor']
  ),

  Parameter(
    name     = 'Booster ebeam extraction velocity', 
    group    = 'FAC',
    value    = _P.ebeam_extraction_velocity, 
    symbol   = '<math>v</math>',
    units    = '', 
    revision = '2014-08-01',
    deps     = ['Booster ebeam extraction beta factor']
  ),

  Parameter(
    name     = 'Booster circumference', 
    group    = 'LNLS',
    value    = _P.lattice_circumference, 
    symbol   = '<math>C</math>',
    units    = 'm', 
    revision = '2014-08-01',
    deps     = [],
  ),

]
