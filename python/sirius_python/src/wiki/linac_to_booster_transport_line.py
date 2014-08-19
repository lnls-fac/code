#!/usr/bin/python
# -*- coding: utf-8 -*-

from parameter import Parameter
from definitions import ParameterDefinitions as Prms


label = 'Linac to booster transport line'

parameter_list = [

  Parameter(
    name     = 'Linac to booster transport line operation energy',
    group    = 'GIA',
    value    = Prms.tb_operation_energy,
    symbol   = r'<math>E</math>',
    units    = 'MeV',
    revision = '2014-08-04',
    deps     = [],
    obs      = [],
  ),

  Parameter(
    name     = 'Linac to booster transport line total length',
    group    = 'FAC',
    value    = Prms.tb_total_length,
    symbol   = r'<math>L</math>',
    units    = 'm',
    revision = '2014-08-04',
    deps     = [],
    obs      = ['Includes septum.'],
  ),

  Parameter(
    name     = 'Linac to booster transport line number of dipoles',
    group    = 'FAC',
    value    = Prms.tb_number_of_dipoles,
    symbol   = r'<math>N_\text{DIP}</math>',
    units    = '',
    revision = '2014-08-04',
    deps     = [],
    obs      = [],
  ),

  Parameter(
    name     = 'Linac to booster transport line number of quadrupoles',
    group    = 'FAC',
    value    = Prms.tb_number_of_quadrupoles,
    symbol   = r'<math>N_\text{QUAD}</math>',
    units    = '',
    revision = '2014-08-04',
    deps     = [],
    obs      = [],
  ),

  Parameter(
    name     = 'Linac to booster transport line maximum quadrupole gradient',
    group    = 'FAC',
    value    = Prms.tb_maximum_quadrupole_gradient,
    symbol   = r"<math>B'_\text{max}</math>",
    units    = 'T/m',
    revision = '2014-08-04',
    deps     = [],
    obs      = [],
  ),

]
