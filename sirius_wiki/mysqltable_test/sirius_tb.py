#!/usr/bin/python
# -*- coding: utf-8 -*-

from parameter import Parameter
from definitions import ParameterDefinitions as Prms


label = 'Linac to booster transport line'

parameter_list = [

  Parameter(
    name     = 'Linac to booster transport line beam energy',
    group    = 'GIA',
    value    = Prms.tb_beam_energy,
    symbol   = r'<math>E</math>',
    units    = 'MeV',
    deps     = [],
    obs      = [],
  ),

  Parameter(
    name     = 'Linac to booster transport line beam gamma factor',
    group    = 'FAC',
    value    = Prms.tb_beam_gamma_factor,
    symbol   = r'<math>\gamma</math>',
    units    = '',
    deps     = ['Linac to booster transport line beam energy'],
    obs      = [],
  ),

  Parameter(
    name     = 'Linac to booster transport line beam beta factor',
    group    = 'FAC',
    value    = Prms.tb_beam_beta_factor,
    symbol   = r'<math>\beta</math>',
    units    = '',
    deps     = ['Linac to booster transport line beam gamma factor'],
    obs      = [],
  ),

  Parameter(
    name     = 'Linac to booster transport line beam velocity',
    group    = 'FAC',
    value    = Prms.tb_beam_velocity,
    symbol   = r'<math>v</math>',
    units    = '',
    deps     = ['Linac to booster transport line beam beta factor'],
    obs      = [],
  ),
                  
  Parameter(
    name     = 'Linac to booster transport line beam magnetic rigidity',
    group    = 'FAC',
    value    = Prms.tb_beam_magnetic_rigidity,
    symbol   = r'<math>(B\rho)</math>',
    units    = unicode('T·m', encoding='utf-8'),
    deps     = ['Linac to booster transport line beam energy'],
    obs      = [r'<math>(B\rho) = \frac{p}{ec} = \frac{E}{ec^2}</math>'],
  ),
                  
  Parameter(
    name     = 'Linac to booster transport line total length',
    group    = 'FAC',
    value    = Prms.tb_total_length,
    symbol   = r'<math>L</math>',
    units    = 'm',
    deps     = [],
    obs      = ['Includes septum.'],
  ),

  Parameter(
    name     = 'Linac to booster transport line number of dipoles',
    group    = 'FAC',
    value    = Prms.tb_number_of_dipoles,
    symbol   = r'<math>N_\text{DIP}</math>',
    units    = '',
    deps     = [],
    obs      = [],
  ),

  Parameter(
    name     = 'Linac to booster transport line number of quadrupoles',
    group    = 'FAC',
    value    = Prms.tb_number_of_quadrupoles,
    symbol   = r'<math>N_\text{QUAD}</math>',
    units    = '',
    deps     = [],
    obs      = [],
  ),

  Parameter(
    name     = 'Linac to booster transport line number of septa',
    group    = 'FAC',
    value    = Prms.tb_number_of_septa,
    symbol   = r'<math>N_\text{sep}</math>',
    units    = '',
    deps     = [],
    obs      = [],
  ),
                
  Parameter(
    name     = 'Linac to booster transport line maximum quadrupole gradient',
    group    = 'FAC',
    value    = Prms.tb_maximum_quadrupole_gradient,
    symbol   = r"<math>B'_\text{max}</math>",
    units    = 'T/m',
    deps     = [],
    obs      = [],
  ),

  Parameter(
    name     = 'Linac to booster transport line deflection angle of dipole',
    group    = 'FAC',
    value    = Prms.tb_dipole_deflection_angle,
    symbol   = r'<math>\theta_\text{DIP}</math>',
    units    = unicode('°',encoding='utf-8'),
    deps     = [],
    obs      = [],
  ),
                  
  Parameter(
    name     = 'Linac to booster transport line deflection angle of septum',
    group    = 'FAC',
    value    = Prms.tb_septum_deflection_angle,
    symbol   = r'<math>\theta_\text{sep}</math>',
    units    = unicode('°',encoding='utf-8'),
    deps     = [],
    obs      = [],
  ),
                  
  Parameter(
    name     = 'Linac to booster transport line arc length of dipole',
    group    = 'FAC',
    value    = Prms.tb_arc_length_of_dipole,
    symbol   = r'<math>L_\text{DIP}</math>',
    units    = 'm',
    deps     = [],
    obs      = [],
  ),
                
  Parameter(
    name     = 'Linac to booster transport line arc length of septum',
    group    = 'FAC',
    value    = Prms.tb_arc_length_of_septum,
    symbol   = r'<math>L_\text{sep}</math>',
    units    = 'm',
    deps     = [],
    obs      = [],
  ),
                
  Parameter(
    name     = 'Linac to booster transport line dipole bending radius',
    group    = 'FAC',
    value    = Prms.tb_dipole_bending_radius,
    symbol   = r'<math>\rho_\text{DIP}</math>',
    units    = 'm',
    deps     = ['Linac to booster transport line arc length of dipole',
                'Linac to booster transport line deflection angle of dipole'],
    obs      = [r'<math>\rho_\text{DIP} = \frac{L_\text{DIP}}{\theta_\text{DIP}}</math>'],
  ),
  
  Parameter(
    name     = 'Linac to booster transport line septum bending radius',
    group    = 'FAC',
    value    = Prms.tb_septum_bending_radius,
    symbol   = r'<math>\rho_\text{sep}</math>',
    units    = 'm',
    deps     = ['Linac to booster transport line arc length of septum',
                'Linac to booster transport line deflection angle of septum'],
    obs      = [r'<math>\rho_\text{sep} = \frac{L_\text{sep}}{\theta_\text{sep}}</math>'],
  ),
  
  Parameter(
    name     = 'Linac to booster transport line dipole magnetic field',
    group    = 'FAC',
    value    = Prms.tb_dipole_magnetic_field,
    symbol   = r'<math>B_\text{DIP}</math>',
    units    = 'T',
    deps     = ['Linac to booster transport line beam magnetic rigidity',
                'Linac to booster transport line dipole bending radius'],
    obs      = [r'<math>B_\text{DIP} = \frac{(B\rho)}{\rho_\text{DIP}}</math>'],
  ),
                
  Parameter(
    name     = 'Linac to booster transport line septum magnetic field',
    group    = 'FAC',
    value    = Prms.tb_septum_magnetic_field,
    symbol   = r'<math>B_\text{sep}</math>',
    units    = 'T',
    deps     = ['Linac to booster transport line beam magnetic rigidity',
                'Linac to booster transport line septum bending radius'],
    obs      = [r'<math>B_\text{sep} = \frac{(B\rho)}{\rho_\text{sep}}</math>'],
  ),
                
  Parameter(
    name     = 'Linac to booster transport line dipole sagitta',
    group    = 'FAC',
    value    = Prms.tb_dipole_sagitta,
    symbol   = r'<math>S_\text{DIP}</math>',
    units    = 'mm',
    deps     = [],
    obs      = [],
  ),
                
  Parameter(
    name     = 'Linac to booster transport line septum sagitta',
    group    = 'FAC',
    value    = Prms.tb_septum_sagitta,
    symbol   = r'<math>S_\text{sep}</math>',
    units    = 'mm',
    deps     = [],
    obs      = [],
  ),
                
  Parameter(
    name     = 'Linac to booster transport line hardedge length of QA1 quadrupoles',
    group    = 'FAC',
    value    = Prms.tb_hardedge_length_of_QA1_quadrupoles,
    symbol   = r'<math>L_\text{QA1}</math>',
    units    = 'm',
    deps     = [],
    obs      = [],
  ),
                  
  Parameter(
    name     = 'Linac to booster transport line hardedge length of QA2 quadrupoles',
    group    = 'FAC',
    value    = Prms.tb_hardedge_length_of_QA2_quadrupoles,
    symbol   = r'<math>L_\text{QA2}</math>',
    units    = 'm',
    deps     = [],
    obs      = [],
  ),
                  
  Parameter(
    name     = 'Linac to booster transport line hardedge length of QA3 quadrupoles',
    group    = 'FAC',
    value    = Prms.tb_hardedge_length_of_QA3_quadrupoles,
    symbol   = r'<math>L_\text{QA3}</math>',
    units    = 'm',
    deps     = [],
    obs      = [],
  ),
                  
  Parameter(
    name     = 'Linac to booster transport line hardedge length of QB1 quadrupoles',
    group    = 'FAC',
    value    = Prms.tb_hardedge_length_of_QB1_quadrupoles,
    symbol   = r'<math>L_\text{QB1}</math>',
    units    = 'm',
    deps     = [],
    obs      = [],
  ),
                  
  Parameter(
    name     = 'Linac to booster transport line hardedge length of QB2 quadrupoles',
    group    = 'FAC',
    value    = Prms.tb_hardedge_length_of_QB2_quadrupoles,
    symbol   = r'<math>L_\text{QB2}</math>',
    units    = 'm',
    deps     = [],
    obs      = [],
  ),
                  
  Parameter(
    name     = 'Linac to booster transport line hardedge length of QC1 quadrupoles',
    group    = 'FAC',
    value    = Prms.tb_hardedge_length_of_QC1_quadrupoles,
    symbol   = r'<math>L_\text{QC1}</math>',
    units    = 'm',
    deps     = [],
    obs      = [],
  ),
                  
  Parameter(
    name     = 'Linac to booster transport line hardedge length of QC2 quadrupoles',
    group    = 'FAC',
    value    = Prms.tb_hardedge_length_of_QC2_quadrupoles,
    symbol   = r'<math>L_\text{QC2}</math>',
    units    = 'm',
    deps     = [],
    obs      = [],
  ),
                  
  Parameter(
    name     = 'Linac to booster transport line hardedge length of QC3 quadrupoles',
    group    = 'FAC',
    value    = Prms.tb_hardedge_length_of_QC3_quadrupoles,
    symbol   = r'<math>L_\text{QC3}</math>',
    units    = 'm',
    deps     = [],
    obs      = [],
  ),
                  
  Parameter(
    name     = 'Linac to booster transport line hardedge length of QD1 quadrupoles',
    group    = 'FAC',
    value    = Prms.tb_hardedge_length_of_QD1_quadrupoles,
    symbol   = r'<math>L_\text{QD1}</math>',
    units    = 'm',
    deps     = [],
    obs      = [],
  ),
                  
  Parameter(
    name     = 'Linac to booster transport line hardedge length of QD2 quadrupoles',
    group    = 'FAC',
    value    = Prms.tb_hardedge_length_of_QD2_quadrupoles,
    symbol   = r'<math>L_\text{QD2}</math>',
    units    = 'm',
    deps     = [],
    obs      = [],
  ),
                  
  Parameter(
    name     = 'Linac to booster transport line hardedge length of QE1 quadrupoles',
    group    = 'FAC',
    value    = Prms.tb_hardedge_length_of_QE1_quadrupoles,
    symbol   = r'<math>L_\text{QE1}</math>',
    units    = 'm',
    deps     = [],
    obs      = [],
  ),
                  
  Parameter(
    name     = 'Linac to booster transport line hardedge length of QE2 quadrupoles',
    group    = 'FAC',
    value    = Prms.tb_hardedge_length_of_QE2_quadrupoles,
    symbol   = r'<math>L_\text{QE2}</math>',
    units    = 'm',
    deps     = [],
    obs      = [],
  ),
                  
]
