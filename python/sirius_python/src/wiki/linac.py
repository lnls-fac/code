#!/usr/bin/python
# -*- coding: utf-8 -*-

from parameter import Parameter
from definitions import ParameterDefinitions as Prms


label = 'Linac'

parameter_list = [

  Parameter(
    name     = 'Linac multi-bunch beam energy',
    group    = 'GIA',
    value    = Prms.li_multi_bunch_beam_energy,
    symbol   = r'<math>E^\text{mb}</math>',
    units    = 'MeV',
    revision = '2014-08-04',
    deps     = [],
    obs      = [],
  ),

  Parameter(
    name     = 'Linac multi-bunch RF frequency',
    group    = 'GIA',
    value    = Prms.li_multi_bunch_rf_frequency,
    symbol   = r'<math>f_\text{RF}^\text{mb}</math>',
    units    = 'GHz',
    revision = '2014-08-04',
    deps     = [],
    obs      = [],
  ),

  Parameter(
    name     = 'Linac multi-bunch maximum normalized emittance',
    group    = 'GIA',
    value    = Prms.li_multi_bunch_maximum_normalized_emittance,
    symbol   = r'<math>\epsilon_{N,\text{max}}^\text{mb}</math>',
    units    = unicode('π·mm·mrad', encoding='utf-8'),
    revision = '2014-08-04',
    deps     = [],
    obs      = [],
  ),

  Parameter(
    name     = 'Linac multi-bunch maximum rms energy spread',
    group    = 'GIA',
    value    = Prms.li_multi_bunch_maximum_rms_energy_spread,
    symbol   = r'<math>\epsilon_{N,\text{max}}^\text{mb}</math>',
    units    = '%',
    revision = '2014-08-04',
    deps     = [],
    obs      = [],
  ),

  Parameter(
    name     = 'Linac multi-bunch maximum pulse to pulse energy variation',
    group    = 'GIA',
    value    = Prms.li_multi_bunch_maximum_pulse_to_pulse_energy_variation,
    symbol   = r'<math>\Delta E_{\text{pulse,max}}^\text{mb}</math>',
    units    = '%',
    revision = '2014-08-04',
    deps     = [],
    obs      = [],
  ),

  Parameter(
    name     = 'Linac multi-bunch maximum pulse to pulse jitter',
    group    = 'GIA',
    value    = Prms.li_multi_bunch_maximum_pulse_to_pulse_jitter,
    symbol   = r'<math>\Delta t_{\text{pulse,max}}^\text{mb}</math>',
    units    = '%',
    revision = '2014-08-04',
    deps     = [],
    obs      = [],
  ),

  Parameter(
    name     = 'Linac multi-bunch minimum pulse charge',
    group    = 'GIA',
    value    = Prms.li_multi_bunch_minimum_pulse_charge,
    symbol   = r'<math>q_{\text{pulse,min}}^\text{mb}</math>',
    units    = '%',
    revision = '2014-08-04',
    deps     = [],
    obs      = [],
  ),

  Parameter(
    name     = 'Linac multi-bunch minimum pulse duration',
    group    = 'GIA',
    value    = Prms.li_multi_bunch_minimum_pulse_duration,
    symbol   = r'<math>\tau_{\text{pulse,min}}^\text{mb}</math>',
    units    = 'ns',
    revision = '2014-08-04',
    deps     = [],
    obs      = [],
  ),

  Parameter(
    name     = 'Linac multi-bunch maximum pulse duration',
    group    = 'GIA',
    value    = Prms.li_multi_bunch_maximum_pulse_duration,
    symbol   = r'<math>\tau_{\text{pulse,max}}^\text{mb}</math>',
    units    = 'ns',
    revision = '2014-08-04',
    deps     = [],
    obs      = [],
  ),

  Parameter(
    name     = 'Linac multi-bunch repetition rate',
    group    = 'GIA',
    value    = Prms.li_multi_bunch_repetition_rate,
    symbol   = r'<math>f_{\text{rep}}^\text{mb}</math>',
    units    = 'Hz',
    revision = '2014-08-04',
    deps     = [],
    obs      = [],
  ),

  Parameter(
    name     = 'Linac single-bunch beam energy',
    group    = 'GIA',
    value    = Prms.li_single_bunch_beam_energy,
    symbol   = r'<math>E^\text{sb}</math>',
    units    = 'MeV',
    revision = '2014-08-04',
    deps     = [],
    obs      = [],
  ),

  Parameter(
    name     = 'Linac single-bunch RF frequency',
    group    = 'GIA',
    value    = Prms.li_single_bunch_rf_frequency,
    symbol   = r'<math>f_\text{RF}^\text{sb}</math>',
    units    = 'GHz',
    revision = '2014-08-04',
    deps     = [],
    obs      = [],
  ),

  Parameter(
    name     = 'Linac single-bunch maximum normalized emittance',
    group    = 'GIA',
    value    = Prms.li_single_bunch_maximum_normalized_emittance,
    symbol   = r'<math>\epsilon_{N,\text{max}}^\text{sb}</math>',
    units    = unicode('π·mm·mrad', encoding='utf-8'),
    revision = '2014-08-04',
    deps     = [],
    obs      = [],
  ),

  Parameter(
    name     = 'Linac single-bunch maximum rms energy spread',
    group    = 'GIA',
    value    = Prms.li_single_bunch_maximum_rms_energy_spread,
    symbol   = r'<math>\epsilon_{N,\text{max}}^\text{sb}</math>',
    units    = '%',
    revision = '2014-08-04',
    deps     = [],
    obs      = [],
  ),

  Parameter(
    name     = 'Linac single-bunch maximum pulse to pulse energy variation',
    group    = 'GIA',
    value    = Prms.li_single_bunch_maximum_pulse_to_pulse_energy_variation,
    symbol   = r'<math>\Delta E_{\text{pulse,max}}^\text{sb}</math>',
    units    = '%',
    revision = '2014-08-04',
    deps     = [],
    obs      = [],
  ),

  Parameter(
    name     = 'Linac single-bunch maximum pulse to pulse jitter',
    group    = 'GIA',
    value    = Prms.li_single_bunch_maximum_pulse_to_pulse_jitter,
    symbol   = r'<math>\Delta t_{\text{pulse,max}}^\text{sb}</math>',
    units    = '%',
    revision = '2014-08-04',
    deps     = [],
    obs      = [],
  ),

  Parameter(
    name     = 'Linac single-bunch minimum pulse charge',
    group    = 'GIA',
    value    = Prms.li_single_bunch_minimum_pulse_charge,
    symbol   = r'<math>q_{\text{pulse,min}}^\text{sb}</math>',
    units    = '%',
    revision = '2014-08-04',
    deps     = [],
    obs      = [],
  ),

  Parameter(
    name     = 'Linac single-bunch maximum pulse duration',
    group    = 'GIA',
    value    = Prms.li_single_bunch_maximum_pulse_duration,
    symbol   = r'<math>\tau_{\text{pulse,max}}^\text{sb}</math>',
    units    = 'ns',
    revision = '2014-08-04',
    deps     = [],
    obs      = [],
  ),

  Parameter(
    name     = 'Linac single-bunch repetition rate',
    group    = 'GIA',
    value    = Prms.li_single_bunch_repetition_rate,
    symbol   = r'<math>f_{\text{rep}}^\text{sb}</math>',
    units    = 'Hz',
    revision = '2014-08-04',
    deps     = [],
    obs      = [],
  ),
]
