#!/usr/bin/python
# -*- coding: utf-8 -*-

from parameter import Parameter
from definitions import ParameterDefinitions as Prms


li_beam_energy = 150.0 # [MeV]
li_beam_multi_bunch_minimum_pulse_charge = 3.0 # [nC]
li_beam_multi_bunch_minimum_pulse_duration = 150.0 # [ns]
li_beam_multi_bunch_maximum_pulse_duration = 300.0 # [ns]
li_beam_single_bunch_minimum_pulse_charge = 1.0 # [nC]
li_beam_single_bunch_maximum_pulse_duration = 1.0 # [ns]

li_rf_frequency = 3.0 # [GHz]

li_optics_maximum_normalized_emittance = 50.0 # [π·mm·mrad]
li_optics_maximum_rms_energy_spread = 0.5 # [%]

li_error_maximum_pulse_to_pulse_energy_variation = 0.25 # [%]
li_error_maximum_pulse_to_pulse_jitter = 100.0 # [ps]

li_repetition_rate = 2.0 # [Hz]


parameter_list = [
  Parameter(name='LI beam energy', group='GIA', is_derived=False, value=li_beam_energy, symbol=r'<math>E^\text{mb}</math>', units='MeV', deps=[], obs=[], ),
  Parameter(name='LI beam multi-bunch minimum pulse charge', group='GIA', is_derived=False, value=li_beam_multi_bunch_minimum_pulse_charge, symbol=r'<math>q_{\text{pulse,min}}^\text{mb}</math>', units='nC', deps=[], obs=[], ),
  Parameter(name='LI beam multi-bunch minimum pulse duration', group='GIA', is_derived=False, value=li_beam_multi_bunch_minimum_pulse_duration, symbol=r'<math>\tau_{\text{pulse,min}}^\text{mb}</math>', units='ns', deps=[], obs=[], ),
  Parameter(name='LI beam multi-bunch maximum pulse duration', group='GIA', is_derived=False, value=li_beam_multi_bunch_maximum_pulse_duration, symbol=r'<math>\tau_{\text{pulse,max}}^\text{mb}</math>', units='ns', deps=[], obs=[], ),
  Parameter(name='LI beam single-bunch minimum pulse charge', group='GIA', is_derived=False, value=li_beam_single_bunch_minimum_pulse_charge, symbol=r'<math>q_{\text{pulse,min}}^\text{sb}</math>', units='nC', deps=[], obs=[], ),
  Parameter(name='LI beam single-bunch maximum pulse duration', group='GIA', is_derived=False, value=li_beam_single_bunch_maximum_pulse_duration, symbol=r'<math>\tau_{\text{pulse,max}}^\text{sb}</math>', units='ns', deps=[], obs=[], ),

  Parameter(name='LI rf frequency', group='GIA', is_derived=False, value=li_rf_frequency, symbol=r'<math>f_\text{RF}^\text{mb}</math>', units='GHz', deps=[], obs=[], ),

  Parameter(name='LI optics maximum normalized emittance', group='GIA', is_derived=False, value=li_optics_maximum_normalized_emittance, symbol=r'<math>\epsilon_{N,\text{max}}^\text{mb}</math>', units=unicode('π·mm·mrad', encoding='utf-8'), deps=[], obs=[], ),
  Parameter(name='LI optics maximum rms energy spread', group='GIA', is_derived=False, value=li_optics_maximum_rms_energy_spread, symbol=r'<math>\epsilon_{N,\text{max}}^\text{mb}</math>', units='%', deps=[], obs=[], ),

  Parameter(name='LI error maximum pulse to pulse energy variation', group='GIA', is_derived=False, value=li_error_maximum_pulse_to_pulse_energy_variation, symbol=r'<math>\Delta E_{\text{pulse,max}}^\text{mb}</math>', units='%', deps=[], obs=[], ),
  Parameter(name='LI error maximum pulse to pulse jitter', group='GIA', is_derived=False, value=li_error_maximum_pulse_to_pulse_jitter, symbol=r'<math>\Delta t_{\text{pulse,max}}^\text{mb}</math>', units='ps', deps=[], obs=[], ),

  Parameter(name='LI repetition rate', group='GIA', is_derived=False, value=li_repetition_rate, symbol=r'<math>f_{\text{rep}}^\text{mb}</math>', units='Hz', deps=[], obs=[], ),
]
