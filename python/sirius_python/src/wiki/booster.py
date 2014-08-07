
import optics
from parameter import Parameter


class _P(object):
    beam_extraction_energy       = 3.0;       # [GeV]
    beam_extraction_gamma_factor = optics.gamma(beam_extraction_energy)
    beam_extraction_beta_factor  = optics.beta(beam_extraction_gamma_factor)
    beam_extraction_velocity     = optics.velocity(beam_extraction_beta_factor);
    
    beam_current         = 2.0 #[mA]
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

    
label = 'Booster'

parameter_list = [

  Parameter(
    name     = 'Booster beam extraction energy', 
    group    = 'LNLS',
    value    = _P.beam_extraction_energy,
    symbol   = r'<math>E</math>',
    units    = 'GeV', 
    revision = '2014-08-04',
    deps     = ['Storage ring beam energy']
  ),

  Parameter(
    name     = 'Booster beam extraction gamma factor', 
    group    = 'FAC',
    value    = _P.beam_extraction_gamma_factor, 
    symbol   = r'<math>\gamma</math>',
    units    = '', 
    revision = '2014-08-01',
    deps     = ['Booster beam extraction energy']
  ),

  Parameter(
    name     = 'Booster beam extraction beta factor', 
    group    = 'FAC',
    value    = _P.beam_extraction_beta_factor, 
    symbol   = r'<math>\beta</math>',
    units    = '', 
    revision = '2014-08-01',
    deps     = ['Booster beam extraction gamma factor']
  ),

  Parameter(
    name     = 'Booster beam extraction velocity', 
    group    = 'FAC',
    value    = _P.beam_extraction_velocity, 
    symbol   = r'<math>v</math>',
    units    = '', 
    revision = '2014-08-01',
    deps     = ['Booster beam extraction beta factor']
  ),

  Parameter(
    name     = 'Booster lattice circumference', 
    group    = 'LNLS',
    value    = _P.lattice_circumference, 
    symbol   = r'<math>C</math>',
    units    = 'm', 
    revision = '2014-08-01',
    deps     = [],
  ),

]
