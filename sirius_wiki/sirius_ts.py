#!/usr/bin/python
# -*- coding: utf-8 -*-

from parameter import Parameter
from definitions import ParameterDefinitions as Prms

parameter_list = [
  Parameter(name='TS beam energy', group='GIA', is_derived=False, value=Prms.ts_beam_energy, symbol=r'<math>E</math>', units='GeV', deps=[], obs=[], ),
  Parameter(name='TS beam gamma factor', group='FAC', is_derived=False, value=Prms.ts_beam_gamma_factor, symbol=r'<math>\gamma</math>', units='', deps=['TS beam energy'], obs=[], ),
  Parameter(name='TS beam beta factor', group='FAC', is_derived=False, value=Prms.ts_beam_beta_factor, symbol=r'<math>\beta</math>', units='', deps=['TS beam gamma factor'], obs=[], ),
  Parameter(name='TS beam velocity', group='FAC', is_derived=False, value=Prms.ts_beam_velocity, symbol=r'<math>v</math>', units='', deps=['TS beam beta factor'], obs=[], ),
  Parameter(name='TS beam magnetic rigidity', group='FAC', is_derived=False, value=Prms.ts_beam_magnetic_rigidity, symbol=r'<math>(B\rho)</math>', units=unicode('T·m', encoding='utf-8'), deps=['TS beam energy'], obs=[r'<math>(B\rho)=\frac{p}{ec}=\frac{E}{ec^2}</math>'], ),

  Parameter(name='TS lattice length', group='FAC', is_derived=False, value=Prms.ts_total_length, symbol=r'<math>L</math>', units='m', deps=[], obs=['Includes septum.'], ),
  Parameter(name='TS magnet dipole number', group='FAC', is_derived=False, value=Prms.ts_number_of_dipoles, symbol=r'<math>N_\text{DIP}</math>', units='', deps=[], obs=[], ),
  Parameter(name='TS magnet quadrupole number', group='FAC', is_derived=False, value=Prms.ts_number_of_quadrupoles, symbol=r'<math>N_\text{QUAD}</math>', units='', deps=[], obs=[], ),

  Parameter(name='TS magnet quadrupole maximum gradient', group='FAC', is_derived=False, value=Prms.ts_maximum_quadrupole_gradient, symbol=r"<math>B'_\text{max}</math>", units='T/m', deps=[], obs=[], ),
  Parameter(name='TS magnet dipole hardedge length', group='FAC', is_derived=False, value=Prms.ts_hardedge_length_of_dipoles, symbol=r'<math>L_\text{DIP}</math>', units='m', deps=[], obs=[], ),

  Parameter(name='TS magnet septum hardedge length', group='FAC', is_derived=False, value=Prms.ts_hardedge_length_of_extraction_septum, symbol=r'<math>L_\text{sep,ext}</math>', units='m', deps=[], obs=[], ),

  Parameter(name='TS hardedge length of thick injection septum', group='FAC', is_derived=False, value=Prms.ts_hardedge_length_of_thick_injection_septum, symbol=r'<math>L_\text{thick sep,inj}</math>', units='m', deps=[], obs=[], ),



  Parameter(name='TS hardedge length of thin injection septum', group='FAC', is_derived=False, value=Prms.ts_hardedge_length_of_thin_injection_septum, symbol=r'<math>L_\text{thin sep,inj}</math>', units='m', deps=[], obs=[], ),
  Parameter(name='TS deflection angle of dipoles', group='FAC', is_derived=False, value=Prms.ts_dipole_deflection_angle, symbol=r'<math>\theta_\text{DIP}</math>', units=unicode('°',encoding='utf-8'), deps=[], obs=[], ),
  Parameter(name='TS deflection angle of extraction septum', group='FAC', is_derived=False, value=Prms.ts_extraction_septum_deflection_angle, symbol=r'<math>\theta_\text{sep,ext}</math>', units=unicode('°',encoding='utf-8'), deps=[], obs=[], ),
  Parameter(name='TS deflection angle of thick injection septum', group='FAC', is_derived=False, value=Prms.ts_thick_injection_septum_deflection_angle, symbol=r'<math>\theta_\text{thick sep,inj}</math>', units=unicode('°',encoding='utf-8'), deps=[], obs=[], ),
  Parameter(name='TS deflection angle of thin injection septum', group='FAC', is_derived=False, value=Prms.ts_thin_injection_septum_deflection_angle, symbol=r'<math>\theta_\text{thin sep,inj}</math>', units=unicode('°',encoding='utf-8'), deps=[], obs=[], ),
  Parameter(name='TS dipole bending radius', group='FAC', is_derived=False, value=Prms.ts_dipole_bending_radius, symbol=r'<math>\rho_\text{DIP}</math>', units='m', deps=['TS hardedge length of dipoles',        'TS deflection angle of dipoles'],   obs     =[r'<math>\rho_\text{DIP}=\frac{L_\text{DIP}}{\theta_\text{DIP}}</math>'],
  Parameter(name='TS extraction septum bending radius', group='FAC', is_derived=False, value=Prms.ts_extraction_septum_bending_radius, symbol=r'<math>\rho_\text{sep,ext}</math>', units='m', deps=['TS hardedge length of extraction septum',        'TS deflection angle of extraction septum'],   obs     =[r'<math>\rho_\text{sep,ext}=\frac{L_\text{sep,ext}}{\theta_\text{sep,ext}}</math>'],
  Parameter(name='TS thick injection septum bending radius', group='FAC', is_derived=False, value=Prms.ts_thick_injection_septum_bending_radius, symbol=r'<math>\rho_\text{thick sep,inj}</math>', units='m', deps=['TS hardedge length of thick injection septum',        'TS deflection angle of thick injection septum'],   obs     =[r'<math>\rho_\text{thick sep,inj}=\frac{L_\text{thick sep,inj}}{\theta_\text{thick sep,inj}}</math>'],
  Parameter(name='TS thin injection septum bending radius', group='FAC', is_derived=False, value=Prms.ts_thin_injection_septum_bending_radius, symbol=r'<math>\rho_\text{thin sep,inj}</math>', units='m', deps=['TS hardedge length of thin injection septum',        'TS deflection angle of thin injection septum'],   obs     =[r'<math>\rho_\text{thin sep,inj}=\frac{L_\text{thin sep,inj}}{\theta_\text{thin sep,inj}}</math>'],
  Parameter(name='TS dipole magnetic field', group='FAC', is_derived=False, value=Prms.ts_dipole_magnetic_field, symbol=r'<math>B_\text{DIP}</math>', units='T', deps=['TS beam magnetic rigidity',        'TS dipole bending radius'],   obs     =[r'<math>B_\text{DIP}=\frac{(B\rho)}{\rho_\text{DIP}}</math>'],
  Parameter(name='TS extraction septum magnetic field', group='FAC', is_derived=False, value=Prms.ts_extraction_septum_magnetic_field, symbol=r'<math>B_\text{sep,ext}</math>', units='T', deps=['TS beam magnetic rigidity',        'TS extraction septum bending radius'],   obs     =[r'<math>B_\text{sep,ext}=\frac{(B\rho)}{\rho_\text{sep,ext}}</math>'],
  Parameter(name='TS thick injection septum magnetic field', group='FAC', is_derived=False, value=Prms.ts_thick_injection_septum_magnetic_field, symbol=r'<math>B_\text{thick sep,inj}</math>', units='T', deps=['TS beam magnetic rigidity',        'TS thick injection septum bending radius'],   obs     =[r'<math>B_\text{thick sep,inj}=\frac{(B\rho)}{\rho_\text{thick sep,inj}}</math>'],
  Parameter(name='TS thin injection septum magnetic field', group='FAC', is_derived=False, value=Prms.ts_thin_injection_septum_magnetic_field, symbol=r'<math>B_\text{thin sep,inj}</math>', units='T', deps=['TS beam magnetic rigidity',        'TS thin injection septum bending radius'],   obs     =[r'<math>B_\text{thin sep,inj}=\frac{(B\rho)}{\rho_\text{thin sep,inj}}</math>'],
  Parameter(name='TS dipole sagitta', group='FAC', is_derived=False, value=Prms.ts_dipole_sagitta, symbol=r'<math>S_\text{DIP}</math>', units='mm', deps=[], obs=[], ),
  Parameter(name='TS extraction septum sagitta', group='FAC', is_derived=False, value=Prms.ts_extraction_septum_sagitta, symbol=r'<math>S_\text{sep,ext}</math>', units='mm', deps=[], obs=[], ),
  Parameter(name='TS thick injection septum sagitta', group='FAC', is_derived=False, value=Prms.ts_thick_injection_septum_sagitta, symbol=r'<math>S_\text{thick sep,inj}</math>', units='mm', deps=[], obs=[], ),
  Parameter(name='TS thin injection septum sagitta', group='FAC', is_derived=False, value=Prms.ts_thin_injection_septum_sagitta, symbol=r'<math>S_\text{thin sep,inj}</math>', units='mm', deps=[], obs=[], ),
  Parameter(name='TS number of dipoles', group='FAC', is_derived=False, value=Prms.ts_number_of_dipoles, symbol=r'<math>N_\text{DIP}</math>', units='', deps=[], obs=[], ),
  Parameter(name='TS number of extraction septa', group='FAC', is_derived=False, value=Prms.ts_number_of_extraction_septa, symbol=r'<math>N_\text{sep,ext}</math>', units='', deps=[], obs=[], ),
  Parameter(name='TS number of thick injection septa', group='FAC', is_derived=False, value=Prms.ts_number_of_thick_injection_septa, symbol=r'<math>N_\text{thick sep,inj}</math>', units='', deps=[], obs=[], ),
  Parameter(name='TS number of thin injection septa', group='FAC', is_derived=False, value=Prms.ts_number_of_thin_injection_septa, symbol=r'<math>N_\text{thin sep,inj}</math>', units='', deps=[], obs=[], ),
  Parameter(name='TS magnet quadrupole hardedge length', group='FAC', is_derived=False, value=Prms.ts_hardedge_length_of_QA1_quadrupoles, symbol=r'<math>L_\text{quad}</math>', units='m', deps=[], obs=[], ),
  Parameter(name='TS magnet quadrupole hardedge strength', group='FAC', is_derived=False, value=Prms.ts_QA1_quadrupole_strength, symbol=r'<math>K_\text{quad}</math>', units='m<sup>-2</sup>', deps=[], obs=[], ),
  Parameter(name='TS magnet quadrupole hardedge gradient', group='FAC', is_derived=True, value=Prms.ts_QA1_quadrupole_gradient, symbol=r'<math>G_\text{quad}</math>', units='m<sup>-2</sup>', deps=[], obs=[], ),
  Parameter(name='TS bpm number', group='FAC', is_derived=False, value=Prms.ts_number_of_beam_position_monitors, symbol=r'<math>N_\text{BPM}</math>', units='', deps=[], obs=[], ),
  Parameter(name='TS magnet hcm number', group='FAC', is_derived=False, value=Prms.ts_number_of_horizontal_dipole_correctors, symbol=r'<math>N_\text{HCM}</math>', units='', deps=[], obs=[], ),
  Parameter(name='TS magnet vcm number', group='FAC', is_derived=False, value=Prms.ts_number_of_vertical_dipole_correctors, symbol=r'<math>N_\text{VCM}</math>', units='', deps=[], obs=[], ),
  Parameter(name='TS magnet hcm maximum strength', group='FAC', is_derived=False, value=Prms.ts_horizontal_dipole_corrector_maximum_strength, symbol=r'<math>\theta^\text{x, max}</math>', units=unicode('mrad', encoding='utf-8'), deps=[], obs=[], ),
  Parameter(name='TS magnet vcm maximum strength', group='FAC', is_derived=False, value=Prms.ts_vertical_dipole_corrector_maximum_strength, symbol=r'<math>\theta^\text{y, max}</math>', units=unicode('mrad', encoding='utf-8'), deps=[], obs=[], ),
]
