#!/usr/bin/python
# -*- coding: utf-8 -*-

import optics
from parameter import Parameter
from definitions import ParameterDefinitions as Prms


label = 'Booster'

parameter_list = [

  Parameter(
    name     = 'Booster beam injection energy', 
    group    = 'LNLS',
    value    = Prms.bo_beam_injection_energy,
    symbol   = r'<math>E_\text{inj}</math>',
    units    = 'GeV', 
    revision = '2014-08-04',
    deps     = []
  ),

  Parameter(
    name     = 'Booster beam injection gamma factor', 
    group    = 'FAC',
    value    = Prms.bo_beam_injection_gamma_factor, 
    symbol   = r'<math>\gamma_\text{inj}</math>',
    units    = '', 
    revision = '2014-08-01',
    deps     = ['Booster beam injection energy']
  ),

  Parameter(
    name     = 'Booster beam injection beta factor', 
    group    = 'FAC',
    value    = Prms.bo_beam_injection_beta_factor, 
    symbol   = r'<math>\beta_\text{inj}</math>',
    units    = '', 
    revision = '2014-08-01',
    deps     = ['Booster beam injection gamma factor']
  ),

  Parameter(
    name     = 'Booster beam injection velocity', 
    group    = 'FAC',
    value    = Prms.bo_beam_injection_velocity, 
    symbol   = r'<math>v_\text{inj}</math>',
    units    = '', 
    revision = '2014-08-01',
    deps     = ['Booster beam injection beta factor']
  ),

  Parameter(
    name     = 'Booster beam extraction energy', 
    group    = 'LNLS',
    value    = Prms.bo_beam_extraction_energy,
    symbol   = r'<math>E_\text{ext}</math>',
    units    = 'GeV', 
    revision = '2014-08-04',
    deps     = []
  ),

  Parameter(
    name     = 'Booster beam extraction gamma factor', 
    group    = 'FAC',
    value    = Prms.bo_beam_extraction_gamma_factor, 
    symbol   = r'<math>\gamma_\text{ext}</math>',
    units    = '', 
    revision = '2014-08-01',
    deps     = ['Booster beam extraction energy']
  ),

  Parameter(
    name     = 'Booster beam extraction beta factor', 
    group    = 'FAC',
    value    = Prms.bo_beam_extraction_beta_factor, 
    symbol   = r'<math>\beta_\text{ext}</math>',
    units    = '', 
    revision = '2014-08-01',
    deps     = ['Booster beam extraction gamma factor']
  ),

  Parameter(
    name     = 'Booster beam extraction velocity', 
    group    = 'FAC',
    value    = Prms.bo_beam_extraction_velocity, 
    symbol   = r'<math>v_\text{ext}</math>',
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
  
  Parameter(
    name     = 'Booster lattice symmetry', 
    group    = 'FAC',
    value    = Prms.bo_lattice_symmetry, 
    symbol   = r'<math>N_\text{SUPERCELLS}</math>',
    units    = '', 
    revision = '2014-08-01',
    deps     = [],
    obs      = '',
  ),

  Parameter(
    name     = 'Booster beam current', 
    group    = 'FAC',
    value    = Prms.bo_beam_current, 
    symbol   = r'<math>I</math>',
    units    = 'mA', 
    revision = '2014-08-01',
    deps     = [],
    obs      = '',
  ),

  Parameter(
    name     = 'Booster revolution period', 
    group    = 'FAC',
    value    = Prms.bo_extraction_revolution_period, 
    symbol   = r'<math>T_\text{rev}</math>',
    units    = unicode('μs', encoding='utf-8'), 
    revision = '2014-08-01',
    deps     = ['Booster lattice circumference',
                'Booster beam extraction velocity'],
    obs      = '',
  ),
 
  Parameter(
    name     = 'Booster revolution frequency', 
    group    = 'FAC',
    value    = Prms.bo_extraction_revolution_frequency, 
    symbol   = r'<math>f_\text{rev}</math>',
    units    = u'MHz', 
    revision = '2014-08-01',
    deps     = ['Booster revolution period'],
    obs      = '',
  ),

  Parameter(
    name     = 'Booster cycling frequency',
    group    = 'FAC',
    value    = Prms.bo_cycling_frequency,
    symbol   = r'<math>f_\text{cycle}</math>',
    units    = 'Hz',
    revision = '2014-08-01',
    deps     = [],
    obs      = '',
  ),

  Parameter(
    name = 'Booster horizontal betatron tune', 
    group    = 'FAC',
    value    = Prms.bo_horizontal_betatron_tune, 
    symbol   = r'<math>\nu_x</math>',
    units    = '', 
    revision = '2014-08-01',
    deps     = ['Booster lattice version',
                'Booster optics mode'],
    obs      = '',
  ),    
                
  Parameter(
    name = 'Booster vertical betatron tune', 
    group    = 'FAC',
    value    = Prms.bo_vertical_betatron_tune, 
    symbol   = r'<math>\nu_y</math>',
    units    = '', 
    revision = '2014-08-01',
    deps     = ['Booster lattice version',
                'Booster optics mode'],
    obs      = '',
  ),  
                  
  Parameter(
    name = 'Booster synchrotron tune', 
    group    = 'FAC',
    value    = Prms.bo_synchrotron_tune, 
    symbol   = r'<math>\nu_s</math>',
    units    = '', 
    revision = '2014-08-01',
    deps     = ['Booster lattice version', 
                'Booster optics mode'],
    obs      = '',
  ),

  Parameter(
    name     = 'Booster lattice version', 
    group    = 'FAC',
    value    = Prms.bo_lattice_version, 
    symbol   = '',
    units    = '', 
    revision = '2014-08-01',
    deps     = [],
    obs      = '',
  ),

  Parameter(
    name = 'Booster optics mode', 
    group    = 'FAC',
    value    = Prms.bo_optics_mode, 
    symbol   = '',
    units    = '', 
    revision = '2014-08-01',
    deps     = [],
    obs      = '',
  ),

  Parameter(
    name     = 'Booster harmonic number', 
    group    = 'FAC',
    value    = Prms.bo_harmonic_number, 
    symbol   = r'<math>h</math>',
    units    = '', 
    revision = '2014-08-01',
    deps     = [],
    obs      = '',
  ),

  Parameter(
    name = 'Booster radiation integral I1', 
    group    = 'FAC',
    value    = Prms.bo_radiation_integral_I1, 
    symbol   = r'<math>I_\text{1} = \oint{\frac{\eta_x}{\rho_x}\,ds}</math>',
    units    = 'm', 
    revision = '2014-08-01',
    deps     = ['Booster beam magnetic rigidity',
                'Booster lattice version', 'Booster optics mode'],
    obs      = '',
  ), 
                  
  Parameter(
    name = 'Booster radiation integral I2', 
    group    = 'FAC',
    value    = Prms.bo_radiation_integral_I2, 
    symbol   = r'<math>I_\text{2} = \oint{\frac{1}{\rho_x^2}\,ds}</math>',
    units    = '1/m', 
    revision = '2014-08-01',
    deps     = ['Booster beam magnetic rigidity',
                'Booster lattice version'],
    obs      = '',
  ), 
   
  Parameter(
    name = 'Booster radiation integral I3', 
    group    = 'FAC',
    value    = Prms.bo_radiation_integral_I3, 
    symbol   = r'<math>I_\text{3} = \oint{\frac{1}{|\rho_x|^3}\,ds}</math>',
    units    = '1/m^2', 
    revision = '2014-08-01',
    deps     = ['Booster beam magnetic rigidity',
                'Booster lattice version'],
    obs      = '',
  ), 
                  
  Parameter(
    name = 'Booster radiation integral I4', 
    group    = 'FAC',
    value    = Prms.bo_radiation_integral_I4, 
    symbol   = r'<math>I_\text{4} = \frac{\eta_x(s_0) \tan \theta(s_0)}{\rho_x^2} + \oint{\frac{\eta_x}{\rho_x^3} \left(1 + 2 \rho_x^2 k\right)\,ds} + \frac{\eta_x(s_1) \tan \theta(s_1)}{\rho_x^2}</math>',
    units    = '1/m', 
    revision = '2014-08-01',
    deps     = ['Booster beam magnetic rigidity',
                'Booster lattice version'],
    obs      = '',
  ),   
                  
  Parameter(
    name = 'Booster radiation integral I5', 
    group    = 'FAC',
    value    = Prms.bo_radiation_integral_I5, 
    symbol   = r'<math>I_\text{5} = \oint{\frac{H_x}{|\rho_x|^3}\,ds}</math>',
    units    = '1/m', 
    revision = '2014-08-01',
    deps     = ['Booster beam magnetic rigidity',
                'Booster lattice version',
                'Booster optics mode'],
    obs      = r"<math>H_x \equiv \gamma_x \eta_x^2 + 2 \alpha_x \eta_x \eta_x^' + \beta_x {\eta_x^'}^2</math>",
  ),  
                  
  Parameter(
    name = 'Booster radiation integral I6', 
    group    = 'FAC',
    value    = Prms.bo_radiation_integral_I6, 
    symbol   = r'<math>I_\text{6} = \oint{k^2 \eta_x^2\,ds}</math>',
    units    = '1/m', 
    revision = '2014-08-01',
    deps     = ['Booster beam magnetic rigidity',
                'Booster lattice version',
                'Booster optics mode'],
    obs      = '',
  ),

  Parameter(
    name = 'Booster linear momentum compaction',
    group    = 'FAC',
    value    = Prms.bo_linear_momentum_compaction,
    symbol   = r'<math>\alpha_\text{1} = \frac{I_\text{1}}{C}</math>',
    units    = '', 
    revision = '2014-08-01',
    deps     = ['Booster radiation integral I1',
                'Booster lattice circumference'],
    obs      = '',
  ),
 
  Parameter(
    name     = 'Booster beam magnetic rigidity', 
    group    = 'FAC',
    value    = Prms.bo_beam_extraction_magnetic_rigidity, 
    symbol   = r'<math>(B\rho) = \frac{p}{ec} = \frac{E}{ec^2}</math>',
    units    = 'T.m', 
    revision = '2014-08-01',
    deps     = ['Booster beam extraction energy'],
    obs      = '',
  ),

]
