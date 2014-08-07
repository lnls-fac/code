
import optics
from parameter import Parameter
from definitions import ParameterDefinitions as Prms


label = 'Booster'

parameter_list = [

  Parameter(
    name     = 'Booster beam extraction energy', 
    group    = 'LNLS',
    value    = Prms.bo_beam_extraction_energy,
    symbol   = r'<math>E</math>',
    units    = 'GeV', 
    revision = '2014-08-04',
    deps     = ['Storage ring beam energy']
  ),

  Parameter(
    name     = 'Booster beam extraction gamma factor', 
    group    = 'FAC',
    value    = Prms.bo_beam_extraction_gamma_factor, 
    symbol   = r'<math>\gamma</math>',
    units    = '', 
    revision = '2014-08-01',
    deps     = ['Booster beam extraction energy']
  ),

  Parameter(
    name     = 'Booster beam extraction beta factor', 
    group    = 'FAC',
    value    = Prms.bo_beam_extraction_beta_factor, 
    symbol   = r'<math>\beta</math>',
    units    = '', 
    revision = '2014-08-01',
    deps     = ['Booster beam extraction gamma factor']
  ),

  Parameter(
    name     = 'Booster beam extraction velocity', 
    group    = 'FAC',
    value    = Prms.bo_beam_extraction_velocity, 
    symbol   = r'<math>v</math>',
    units    = '', 
    revision = '2014-08-01',
    deps     = ['Booster beam extraction beta factor']
  ),

  Parameter(
    name     = 'Booster lattice circumference', 
    group    = 'LNLS',
    value    = Prms.bo_lattice_circumference, 
    symbol   = r'<math>C</math>',
    units    = 'm', 
    revision = '2014-08-01',
    deps     = [],
  ),

]
