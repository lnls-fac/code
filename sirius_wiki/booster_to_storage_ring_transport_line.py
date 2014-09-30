#!/usr/bin/python
# -*- coding: utf-8 -*-

from parameter import Parameter
from definitions import ParameterDefinitions as Prms


label = 'Booster to storage ring transport line'

parameter_list = [

  Parameter(
    name     = 'Booster to storage ring transport line beam energy',
    group    = 'GIA',
    value    = Prms.ts_beam_energy,
    symbol   = r'<math>E</math>',
    units    = 'GeV',
    deps     = [],
    obs      = [],
  ),

  Parameter(
    name     = 'Booster to storage ring transport line beam gamma factor',
    group    = 'FAC',
    value    = Prms.ts_beam_gamma_factor,
    symbol   = r'<math>\gamma</math>',
    units    = '',
    deps     = ['Booster to storage ring transport line beam energy'],
    obs      = [],
  ),

  Parameter(
    name     = 'Booster to storage ring transport line beam beta factor',
    group    = 'FAC',
    value    = Prms.ts_beam_beta_factor,
    symbol   = r'<math>\beta</math>',
    units    = '',
    deps     = ['Booster to storage ring transport line beam gamma factor'],
    obs      = [],
  ),

  Parameter(
    name     = 'Booster to storage ring transport line beam velocity',
    group    = 'FAC',
    value    = Prms.ts_beam_velocity,
    symbol   = r'<math>v</math>',
    units    = '',
    deps     = ['Booster to storage ring transport line beam beta factor'],
    obs      = [],
  ),
                  
  Parameter(
    name     = 'Booster to storage ring transport line beam magnetic rigidity',
    group    = 'FAC',
    value    = Prms.ts_beam_magnetic_rigidity,
    symbol   = r'<math>(B\rho)</math>',
    units    = unicode('T·m', encoding='utf-8'),
    deps     = ['Booster to storage ring transport line beam energy'],
    obs      = [r'<math>(B\rho) = \frac{p}{ec} = \frac{E}{ec^2}</math>'],
  ),
                  
  Parameter(
    name     = 'Booster to storage ring transport line total length',
    group    = 'FAC',
    value    = Prms.ts_total_length,
    symbol   = r'<math>L</math>',
    units    = 'm',
    deps     = [],
    obs      = ['Includes septum.'],
  ),

  Parameter(
    name     = 'Booster to storage ring transport line number of dipoles',
    group    = 'FAC',
    value    = Prms.ts_number_of_dipoles,
    symbol   = r'<math>N_\text{DIP}</math>',
    units    = '',
    deps     = [],
    obs      = [],
  ),

  Parameter(
    name     = 'Booster to storage ring transport line number of quadrupoles',
    group    = 'FAC',
    value    = Prms.ts_number_of_quadrupoles,
    symbol   = r'<math>N_\text{QUAD}</math>',
    units    = '',
    deps     = [],
    obs      = [],
  ),

  Parameter(
    name     = 'Booster to storage ring transport line maximum quadrupole gradient',
    group    = 'FAC',
    value    = Prms.ts_maximum_quadrupole_gradient,
    symbol   = r"<math>B'_\text{max}</math>",
    units    = 'T/m',
    deps     = [],
    obs      = [],
  ),

  Parameter(
    name     = 'Booster to storage ring transport line hardedge length of dipoles',
    group    = 'FAC',
    value    = Prms.ts_hardedge_length_of_dipoles,
    symbol   = r'<math>L_\text{DIP}</math>',
    units    = 'm',
    deps     = [],
    obs      = [],
  ),
                
  Parameter(
    name     = 'Booster to storage ring transport line hardedge length of extraction septum',
    group    = 'FAC',
    value    = Prms.ts_hardedge_length_of_extraction_septum,
    symbol   = r'<math>L_\text{sep,ext}</math>',
    units    = 'm',
    deps     = [],
    obs      = [],
  ),
                
  Parameter(
    name     = 'Booster to storage ring transport line hardedge length of thick injection septum',
    group    = 'FAC',
    value    = Prms.ts_hardedge_length_of_thick_injection_septum,
    symbol   = r'<math>L_\text{thick sep,inj}</math>',
    units    = 'm',
    deps     = [],
    obs      = [],
  ),
                
  Parameter(
    name     = 'Booster to storage ring transport line hardedge length of thin injection septum',
    group    = 'FAC',
    value    = Prms.ts_hardedge_length_of_thin_injection_septum,
    symbol   = r'<math>L_\text{thin sep,inj}</math>',
    units    = 'm',
    deps     = [],
    obs      = [],
  ),
                
  Parameter(
    name     = 'Booster to storage ring transport line deflection angle of dipoles',
    group    = 'FAC',
    value    = Prms.ts_dipole_deflection_angle,
    symbol   = r'<math>\theta_\text{DIP}</math>',
    units    = unicode('°',encoding='utf-8'),
    deps     = [],
    obs      = [],
  ),
                  
  Parameter(
    name     = 'Booster to storage ring transport line deflection angle of extraction septum',
    group    = 'FAC',
    value    = Prms.ts_extraction_septum_deflection_angle,
    symbol   = r'<math>\theta_\text{sep,ext}</math>',
    units    = unicode('°',encoding='utf-8'),
    deps     = [],
    obs      = [],
  ),
                  
  Parameter(
    name     = 'Booster to storage ring transport line deflection angle of thick injection septum',
    group    = 'FAC',
    value    = Prms.ts_thick_injection_septum_deflection_angle,
    symbol   = r'<math>\theta_\text{thick sep,inj}</math>',
    units    = unicode('°',encoding='utf-8'),
    deps     = [],
    obs      = [],
  ),
                  
  Parameter(
    name     = 'Booster to storage ring transport line deflection angle of thin injection septum',
    group    = 'FAC',
    value    = Prms.ts_thin_injection_septum_deflection_angle,
    symbol   = r'<math>\theta_\text{thin sep,inj}</math>',
    units    = unicode('°',encoding='utf-8'),
    deps     = [],
    obs      = [],
  ),
                  
  Parameter(
    name     = 'Booster to storage ring transport line dipole bending radius',
    group    = 'FAC',
    value    = Prms.ts_dipole_bending_radius,
    symbol   = r'<math>\rho_\text{DIP}</math>',
    units    = 'm',
    deps     = ['Booster to storage ring transport line hardedge length of dipoles',
                'Booster to storage ring transport line deflection angle of dipoles'],
    obs      = [r'<math>\rho_\text{DIP} = \frac{L_\text{DIP}}{\theta_\text{DIP}}</math>'],
  ),
  
  Parameter(
    name     = 'Booster to storage ring transport line extraction septum bending radius',
    group    = 'FAC',
    value    = Prms.ts_extraction_septum_bending_radius,
    symbol   = r'<math>\rho_\text{sep,ext}</math>',
    units    = 'm',
    deps     = ['Booster to storage ring transport line hardedge length of extraction septum',
                'Booster to storage ring transport line deflection angle of extraction septum'],
    obs      = [r'<math>\rho_\text{sep,ext} = \frac{L_\text{sep,ext}}{\theta_\text{sep,ext}}</math>'],
  ),
  
  Parameter(
    name     = 'Booster to storage ring transport line thick injection septum bending radius',
    group    = 'FAC',
    value    = Prms.ts_thick_injection_septum_bending_radius,
    symbol   = r'<math>\rho_\text{thick sep,inj}</math>',
    units    = 'm',
    deps     = ['Booster to storage ring transport line hardedge length of thick injection septum',
                'Booster to storage ring transport line deflection angle of thick injection septum'],
    obs      = [r'<math>\rho_\text{thick sep,inj} = \frac{L_\text{thick sep,inj}}{\theta_\text{thick sep,inj}}</math>'],
  ),
  
  Parameter(
    name     = 'Booster to storage ring transport line thin injection septum bending radius',
    group    = 'FAC',
    value    = Prms.ts_thin_injection_septum_bending_radius,
    symbol   = r'<math>\rho_\text{thin sep,inj}</math>',
    units    = 'm',
    deps     = ['Booster to storage ring transport line hardedge length of thin injection septum',
                'Booster to storage ring transport line deflection angle of thin injection septum'],
    obs      = [r'<math>\rho_\text{thin sep,inj} = \frac{L_\text{thin sep,inj}}{\theta_\text{thin sep,inj}}</math>'],
  ),
  
  Parameter(
    name     = 'Booster to storage ring transport line dipole magnetic field',
    group    = 'FAC',
    value    = Prms.ts_dipole_magnetic_field,
    symbol   = r'<math>B_\text{DIP}</math>',
    units    = 'T',
    deps     = ['Booster to storage ring transport line beam magnetic rigidity',
                'Booster to storage ring transport line dipole bending radius'],
    obs      = [r'<math>B_\text{DIP} = \frac{(B\rho)}{\rho_\text{DIP}}</math>'],
  ),
                
  Parameter(
    name     = 'Booster to storage ring transport line extraction septum magnetic field',
    group    = 'FAC',
    value    = Prms.ts_extraction_septum_magnetic_field,
    symbol   = r'<math>B_\text{sep,ext}</math>',
    units    = 'T',
    deps     = ['Booster to storage ring transport line beam magnetic rigidity',
                'Booster to storage ring transport line extraction septum bending radius'],
    obs      = [r'<math>B_\text{sep,ext} = \frac{(B\rho)}{\rho_\text{sep,ext}}</math>'],
  ),
                
  Parameter(
    name     = 'Booster to storage ring transport line thick injection septum magnetic field',
    group    = 'FAC',
    value    = Prms.ts_thick_injection_septum_magnetic_field,
    symbol   = r'<math>B_\text{thick sep,inj}</math>',
    units    = 'T',
    deps     = ['Booster to storage ring transport line beam magnetic rigidity',
                'Booster to storage ring transport line thick injection septum bending radius'],
    obs      = [r'<math>B_\text{thick sep,inj} = \frac{(B\rho)}{\rho_\text{thick sep,inj}}</math>'],
  ),
                
  Parameter(
    name     = 'Booster to storage ring transport line thin injection septum magnetic field',
    group    = 'FAC',
    value    = Prms.ts_thin_injection_septum_magnetic_field,
    symbol   = r'<math>B_\text{thin sep,inj}</math>',
    units    = 'T',
    deps     = ['Booster to storage ring transport line beam magnetic rigidity',
                'Booster to storage ring transport line thin injection septum bending radius'],
    obs      = [r'<math>B_\text{thin sep,inj} = \frac{(B\rho)}{\rho_\text{thin sep,inj}}</math>'],
  ),
                
  Parameter(
    name     = 'Booster to storage ring transport line dipole sagitta',
    group    = 'FAC',
    value    = Prms.ts_dipole_sagitta,
    symbol   = r'<math>S_\text{DIP}</math>',
    units    = 'mm',
    deps     = [],
    obs      = [],
  ),
                
  Parameter(
    name     = 'Booster to storage ring transport line extraction septum sagitta',
    group    = 'FAC',
    value    = Prms.ts_extraction_septum_sagitta,
    symbol   = r'<math>S_\text{sep,ext}</math>',
    units    = 'mm',
    deps     = [],
    obs      = [],
  ),
                
  Parameter(
    name     = 'Booster to storage ring transport line thick injection septum sagitta',
    group    = 'FAC',
    value    = Prms.ts_thick_injection_septum_sagitta,
    symbol   = r'<math>S_\text{thick sep,inj}</math>',
    units    = 'mm',
    deps     = [],
    obs      = [],
  ),
                
  Parameter(
    name     = 'Booster to storage ring transport line thin injection septum sagitta',
    group    = 'FAC',
    value    = Prms.ts_thin_injection_septum_sagitta,
    symbol   = r'<math>S_\text{thin sep,inj}</math>',
    units    = 'mm',
    deps     = [],
    obs      = [],
  ),
                
  Parameter(
    name     = 'Booster to storage ring transport line number of dipoles',
    group    = 'FAC',
    value    = Prms.ts_number_of_dipoles,
    symbol   = r'<math>N_\text{DIP}</math>',
    units    = '',
    deps     = [],
    obs      = [],
  ),
                
  Parameter(
    name     = 'Booster to storage ring transport line number of extraction septa',
    group    = 'FAC',
    value    = Prms.ts_number_of_extraction_septa,
    symbol   = r'<math>N_\text{sep,ext}</math>',
    units    = '',
    deps     = [],
    obs      = [],
  ),
                
  Parameter(
    name     = 'Booster to storage ring transport line number of thick injection septa',
    group    = 'FAC',
    value    = Prms.ts_number_of_thick_injection_septa,
    symbol   = r'<math>N_\text{thick sep,inj}</math>',
    units    = '',
    deps     = [],
    obs      = [],
  ),
                
  Parameter(
    name     = 'Booster to storage ring transport line number of thin injection septa',
    group    = 'FAC',
    value    = Prms.ts_number_of_thin_injection_septa,
    symbol   = r'<math>N_\text{thin sep,inj}</math>',
    units    = '',
    deps     = [],
    obs      = [],
  ),
                
  Parameter(
    name     = 'Booster to storage ring transport line hardedge length of QA1 quadrupoles',
    group    = 'FAC',
    value    = Prms.ts_hardedge_length_of_QA1_quadrupoles,
    symbol   = r'<math>L_\text{QA1}</math>',
    units    = 'm',
    deps     = [],
    obs      = [],
  ),
                  
  Parameter(
    name     = 'Booster to storage ring transport line hardedge length of QA2 quadrupoles',
    group    = 'FAC',
    value    = Prms.ts_hardedge_length_of_QA2_quadrupoles,
    symbol   = r'<math>L_\text{QA2}</math>',
    units    = 'm',
    deps     = [],
    obs      = [],
  ),
                  
  Parameter(
    name     = 'Booster to storage ring transport line hardedge length of QB1 quadrupoles',
    group    = 'FAC',
    value    = Prms.ts_hardedge_length_of_QB1_quadrupoles,
    symbol   = r'<math>L_\text{QB1}</math>',
    units    = 'm',
    deps     = [],
    obs      = [],
  ),
                  
  Parameter(
    name     = 'Booster to storage ring transport line hardedge length of QB2 quadrupoles',
    group    = 'FAC',
    value    = Prms.ts_hardedge_length_of_QB2_quadrupoles,
    symbol   = r'<math>L_\text{QB2}</math>',
    units    = 'm',
    deps     = [],
    obs      = [],
  ),
                  
  Parameter(
    name     = 'Booster to storage ring transport line hardedge length of QC1 quadrupoles',
    group    = 'FAC',
    value    = Prms.ts_hardedge_length_of_QC1_quadrupoles,
    symbol   = r'<math>L_\text{QC1}</math>',
    units    = 'm',
    deps     = [],
    obs      = [],
  ),
                  
  Parameter(
    name     = 'Booster to storage ring transport line hardedge length of QC2 quadrupoles',
    group    = 'FAC',
    value    = Prms.ts_hardedge_length_of_QC2_quadrupoles,
    symbol   = r'<math>L_\text{QC2}</math>',
    units    = 'm',
    deps     = [],
    obs      = [],
  ),
                  
  Parameter(
    name     = 'Booster to storage ring transport line hardedge length of QC3 quadrupoles',
    group    = 'FAC',
    value    = Prms.ts_hardedge_length_of_QC3_quadrupoles,
    symbol   = r'<math>L_\text{QC3}</math>',
    units    = 'm',
    deps     = [],
    obs      = [],
  ),

  Parameter(
    name     = 'Booster to storage ring transport line hardedge length of QC4 quadrupoles',
    group    = 'FAC',
    value    = Prms.ts_hardedge_length_of_QC4_quadrupoles,
    symbol   = r'<math>L_\text{QC4}</math>',
    units    = 'm',
    deps     = [],
    obs      = [],
  ),
                  
  Parameter(
    name     = 'Booster to storage ring transport line QA1 quadrupole strength',
    group    = 'FAC',
    value    = Prms.ts_QA1_quadrupole_strength,
    symbol   = r'<math>K_\text{QA1}</math>',
    units    = 'm<sup>-2</sup>',
    deps     = [],
    obs      = [],
  ),
                  
  Parameter(
    name     = 'Booster to storage ring transport line QA2 quadrupole strength',
    group    = 'FAC',
    value    = Prms.ts_QA2_quadrupole_strength,
    symbol   = r'<math>K_\text{QA2}</math>',
    units    = 'm<sup>-2</sup>',
    deps     = [],
    obs      = [],
  ),
                  
  Parameter(
    name     = 'Booster to storage ring transport line QB1 quadrupole strength',
    group    = 'FAC',
    value    = Prms.ts_QB1_quadrupole_strength,
    symbol   = r'<math>K_\text{QB1}</math>',
    units    = 'm<sup>-2</sup>',
    deps     = [],
    obs      = [],
  ),
                  
  Parameter(
    name     = 'Booster to storage ring transport line QB2 quadrupole strength',
    group    = 'FAC',
    value    = Prms.ts_QB2_quadrupole_strength,
    symbol   = r'<math>K_\text{QB2}</math>',
    units    = 'm<sup>-2</sup>',
    deps     = [],
    obs      = [],
  ),
                  
  Parameter(
    name     = 'Booster to storage ring transport line QC1 quadrupole strength',
    group    = 'FAC',
    value    = Prms.ts_QC1_quadrupole_strength,
    symbol   = r'<math>K_\text{QC1}</math>',
    units    = 'm<sup>-2</sup>',
    deps     = [],
    obs      = [],
  ),
                  
  Parameter(
    name     = 'Booster to storage ring transport line QC2 quadrupole strength',
    group    = 'FAC',
    value    = Prms.ts_QC2_quadrupole_strength,
    symbol   = r'<math>K_\text{QC2}</math>',
    units    = 'm<sup>-2</sup>',
    deps     = [],
    obs      = [],
  ),
                  
  Parameter(
    name     = 'Booster to storage ring transport line QC3 quadrupole strength',
    group    = 'FAC',
    value    = Prms.ts_QC3_quadrupole_strength,
    symbol   = r'<math>K_\text{QC3}</math>',
    units    = 'm<sup>-2</sup>',
    deps     = [],
    obs      = [],
  ),

  Parameter(
    name     = 'Booster to storage ring transport line QC4 quadrupole strength',
    group    = 'FAC',
    value    = Prms.ts_QC4_quadrupole_strength,
    symbol   = r'<math>K_\text{QC4}</math>',
    units    = 'm<sup>-2</sup>',
    deps     = [],
    obs      = [],
  ),
                  
  Parameter(
    name     = 'Booster to storage ring transport line QA1 quadrupole gradient',
    group    = 'FAC',
    value    = Prms.ts_QA1_quadrupole_gradient,
    symbol   = r"<math>B'_\text{QA1}</math>",
    units    = unicode('T·m<sup>-1</sup>', encoding='utf-8'),
    deps     = ['Booster to storage ring transport line QA1 quadrupole strength',
                'Booster to storage ring transport line beam magnetic rigidity'],
    obs      = [r"<math>B'_\text{QA1} = (B\rho) K_\text{QA1}</math>"],
  ),
                  
  Parameter(
    name     = 'Booster to storage ring transport line QA2 quadrupole gradient',
    group    = 'FAC',
    value    = Prms.ts_QA2_quadrupole_gradient,
    symbol   = r"<math>B'_\text{QA2}</math>",
    units    = unicode('T·m<sup>-1</sup>', encoding='utf-8'),
    deps     = ['Booster to storage ring transport line QA2 quadrupole strength',
                'Booster to storage ring transport line beam magnetic rigidity'],
    obs      = [r"<math>B'_\text{QA2} = (B\rho) K_\text{QA2}</math>"],
  ),
                  
  Parameter(
    name     = 'Booster to storage ring transport line QB1 quadrupole gradient',
    group    = 'FAC',
    value    = Prms.ts_QB1_quadrupole_gradient,
    symbol   = r"<math>B'_\text{QB1}</math>",
    units    = unicode('T·m<sup>-1</sup>', encoding='utf-8'),
    deps     = ['Booster to storage ring transport line QB1 quadrupole strength',
                'Booster to storage ring transport line beam magnetic rigidity'],
    obs      = [r"<math>B'_\text{QB1} = (B\rho) K_\text{QB1}</math>"],
  ),
                  
  Parameter(
    name     = 'Booster to storage ring transport line QB2 quadrupole gradient',
    group    = 'FAC',
    value    = Prms.ts_QB2_quadrupole_gradient,
    symbol   = r"<math>B'_\text{QB2}</math>",
    units    = unicode('T·m<sup>-1</sup>', encoding='utf-8'),
    deps     = ['Booster to storage ring transport line QB2 quadrupole strength',
                'Booster to storage ring transport line beam magnetic rigidity'],
    obs      = [r"<math>B'_\text{QB2} = (B\rho) K_\text{QB2}</math>"],
  ),
                  
  Parameter(
    name     = 'Booster to storage ring transport line QC1 quadrupole gradient',
    group    = 'FAC',
    value    = Prms.ts_QC1_quadrupole_gradient,
    symbol   = r"<math>B'_\text{QC1}</math>",
    units    = unicode('T·m<sup>-1</sup>', encoding='utf-8'),
    deps     = ['Booster to storage ring transport line QC1 quadrupole strength',
                'Booster to storage ring transport line beam magnetic rigidity'],
    obs      = [r"<math>B'_\text{QC1} = (B\rho) K_\text{QC1}</math>"],
  ),
                  
  Parameter(
    name     = 'Booster to storage ring transport line QC2 quadrupole gradient',
    group    = 'FAC',
    value    = Prms.ts_QC2_quadrupole_gradient,
    symbol   = r"<math>B'_\text{QC2}</math>",
    units    = unicode('T·m<sup>-1</sup>', encoding='utf-8'),
    deps     = ['Booster to storage ring transport line QC2 quadrupole strength',
                'Booster to storage ring transport line beam magnetic rigidity'],
    obs      = [r"<math>B'_\text{QC2} = (B\rho) K_\text{QC2}</math>"],
  ),
                  
  Parameter(
    name     = 'Booster to storage ring transport line QC3 quadrupole gradient',
    group    = 'FAC',
    value    = Prms.ts_QC3_quadrupole_gradient,
    symbol   = r"<math>B'_\text{QC3}</math>",
    units    = unicode('T·m<sup>-1</sup>', encoding='utf-8'),
    deps     = ['Booster to storage ring transport line QC3 quadrupole strength',
                'Booster to storage ring transport line beam magnetic rigidity'],
    obs      = [r"<math>B'_\text{QC3} = (B\rho) K_\text{QC3}</math>"],
  ),

  Parameter(
    name     = 'Booster to storage ring transport line QC4 quadrupole gradient',
    group    = 'FAC',
    value    = Prms.ts_QC4_quadrupole_gradient,
    symbol   = r"<math>B'_\text{QC4}</math>",
    units    = unicode('T·m<sup>-1</sup>', encoding='utf-8'),
    deps     = ['Booster to storage ring transport line QC4 quadrupole strength',
                'Booster to storage ring transport line beam magnetic rigidity'],
    obs      = [r"<math>B'_\text{QC4} = (B\rho) K_\text{QC4}</math>"],
  ),
                  
]
