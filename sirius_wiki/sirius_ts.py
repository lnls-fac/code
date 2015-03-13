#!/usr/bin/python
# -*- coding: utf-8 -*-

from parameter import Parameter
from definitions import ParameterDefinitions as Prms


ts_beam_energy            = 3.0 # [GeV]

ts_lattice_length = 27.88 # [m]

ts_magnet_dipole_number = 2
ts_magnet_dipole_deflection_angle = 7.2 # [°]
ts_magnet_dipole_hardedge_length = 1.152 #[m]
ts_magnet_dipole_sagitta = 18.1 # [mm]

ts_magnet_extraction_septum_number = 2
ts_magnet_extraction_septum_deflection_angle = -3.60 # [°]
ts_magnet_extraction_septum_hardedge_length = 0.85 # [m]
ts_magnet_extraction_septum_sagitta = 6.7 # [mm]

ts_magnet_thick_injection_septum_number = 1
ts_magnet_thick_injection_septum_deflection_angle = 6.2 # [°]
ts_magnet_thick_injection_septum_hardedge_length = 1.100 # [m]
ts_magnet_thick_injection_septum_sagitta = 14.9 # [mm]

ts_magnet_thin_injection_septum_number = 1
ts_magnet_thin_injection_septum_deflection_angle = 4.73 # [°]
ts_magnet_thin_injection_septum_hardedge_length = 1.400 # [m]
ts_magnet_thin_injection_septum_sagitta = 14.4 # [mm]

ts_magnet_quadrupole_number = 8
ts_magnet_quadrupole_maximum_gradient = 25.0 # [T/m]
ts_magnet_quadrupole_hardedge_length = 0.2 # [m]
ts_magnet_quadrupole_hardedge_strength = 0.85 # [1/m^2]

ts_magnet_hcm_number = 3
ts_magnet_hcm_maximum_strength = 0.35 # [mrad]
ts_magnet_vcm_number = 5
ts_magnet_vcm_maximum_strength = 0.35 # [mrad]

ts_bpm_number = 5

parameter_list = [
  Parameter(name='TS beam energy', group='GIA', is_derived=False, value=ts_beam_energy, symbol=r'<math>E</math>', units='GeV', deps=[], obs=[], ),
  Parameter(name='TS beam gamma factor', group='FAC', is_derived=True, value='gamma("TS beam energy")', symbol=r'<math>\gamma</math>', units='', deps=[], obs=[], ),
  Parameter(name='TS beam beta factor', group='FAC', is_derived=True, value='beta("TS beam gamma factor")', symbol=r'<math>\beta</math>', units='', deps=[], obs=[], ),
  Parameter(name='TS beam velocity', group='FAC', is_derived=True, value='velocity("TS beam beta factor")', symbol=r'<math>v</math>', units='', deps=[], obs=[], ),
  Parameter(name='TS beam magnetic rigidity', group='FAC', is_derived=True, value='brho("TS beam energy", "TS beam beta factor")', symbol=r'<math>(B\rho)</math>', units=unicode('T·m', encoding='utf-8'), deps=[], obs=[r'<math>(B\rho)=\frac{p}{ec}=\frac{E}{ec^2}</math>'], ),

  Parameter(name='TS lattice length', group='FAC', is_derived=False, value=ts_lattice_length, symbol=r'<math>L</math>', units='m', deps=[], obs=['Includes septum.'], ),

  Parameter(name='TS magnet dipole number', group='FAC', is_derived=False, value=ts_magnet_dipole_number, symbol=r'<math>N_\text{dip}</math>', units='', deps=[], obs=[], ),
  Parameter(name='TS magnet dipole deflection angle', group='FAC', is_derived=False, value=ts_magnet_dipole_deflection_angle, symbol=r'<math>\theta_\text{dip}</math>', units=unicode('°',encoding='utf-8'), deps=[], obs=[], ),
  Parameter(name='TS magnet dipole hardedge length', group='FAC', is_derived=False, value=ts_magnet_dipole_hardedge_length, symbol=r'<math>L_\text{dip}</math>', units='m', deps=[], obs=[], ),
  Parameter(name='TS magnet dipole hardedge bending radius', group='FAC', is_derived=True, value='"TS magnet dipole hardedge length"/deg2rad("TS magnet dipole deflection angle")', symbol=r'<math>\rho_\text{dip}</math>', units='m', deps=[], obs=[r'<math>\rho_\text{dip}=\frac{L_\text{dip}}{\theta_\text{dip}}</math>'], ),
  Parameter(name='TS magnet dipole hardedge magnetic field', group='FAC', is_derived=True, value='"TS beam magnetic rigidity"/"TS magnet dipole hardedge bending radius"', symbol=r'<math>B_\text{dip}</math>', units='T', deps=[],   obs=[r'<math>B_\text{dip}=\frac{(B\rho)}{\rho_\text{dip}}</math>'], ),
  Parameter(name='TS magnet dipole hardedge sagitta', group='FAC', is_derived=False, value=ts_magnet_dipole_sagitta, symbol=r'<math>S_\text{dip}</math>', units='mm', deps=[], obs=[], ),
  Parameter(name='TS magnet extraction setpum number', group='FAC', is_derived=False, value=ts_magnet_extraction_septum_number, symbol=r'<math>N_\text{sep,ext}</math>', units='', deps=[], obs=[], ),
  Parameter(name='TS magnet extraction septum deflection angle', group='FAC', is_derived=False, value=ts_magnet_extraction_septum_deflection_angle, symbol=r'<math>\theta_\text{sep,ext}</math>', units=unicode('°',encoding='utf-8'), deps=[], obs=[], ),
  Parameter(name='TS magnet extraction septum hardedge length', group='FAC', is_derived=False, value=ts_magnet_extraction_septum_hardedge_length, symbol=r'<math>L_\text{sep,ext}</math>', units='m', deps=[], obs=[], ),
  Parameter(name='TS magnet extraction septum hardedge bending radius', group='FAC', is_derived=True, value='"TS magnet extraction septum hardedge length"/deg2rad("TS magnet extraction septum deflection angle")', symbol=r'<math>\rho_\text{sep,ext}</math>', units='m', deps=[],   obs=[r'<math>\rho_\text{sep,ext}=\frac{L_\text{sep,ext}}{\theta_\text{sep,ext}}</math>'], ),
  Parameter(name='TS magnet extraction septum hardedge magnetic field', group='FAC', is_derived=True, value='"TS beam magnetic rigidity"/"TS magnet extraction septum hardedge bending radius"', symbol=r'<math>B_\text{sep,ext}</math>', units='T', deps=[], obs=[r'<math>B_\text{sep,ext}=\frac{(B\rho)}{\rho_\text{sep,ext}}</math>'], ),
  Parameter(name='TS magnet extraction septum hardedge sagitta', group='FAC', is_derived=False, value=ts_magnet_extraction_septum_sagitta, symbol=r'<math>S_\text{sep,ext}</math>', units='mm', deps=[], obs=[], ),
  Parameter(name='TS magnet thick injection septum number', group='FAC', is_derived=False, value=ts_magnet_thick_injection_septum_number, symbol=r'<math>N_\text{thick sep,inj}</math>', units='', deps=[], obs=[], ),
  Parameter(name='TS magnet thick injection septum deflection angle', group='FAC', is_derived=False, value=ts_magnet_thick_injection_septum_deflection_angle, symbol=r'<math>\theta_\text{thick sep,inj}</math>', units=unicode('°',encoding='utf-8'), deps=[], obs=[], ),
  Parameter(name='TS magnet thick injection septum hardedge length', group='FAC', is_derived=False, value=ts_magnet_thick_injection_septum_hardedge_length, symbol=r'<math>L_\text{thick sep,inj}</math>', units='m', deps=[], obs=[], ),
  Parameter(name='TS magnet thick injection septum hardedge bending radius', group='FAC', is_derived=True, value='"TS magnet thick injection septum hardedge length"/deg2rad("TS magnet thick injection septum deflection angle")', symbol=r'<math>\rho_\text{thick sep,inj}</math>', units='m', deps=[],   obs=[r'<math>\rho_\text{thick sep,inj}=\frac{L_\text{thick sep,inj}}{\theta_\text{thick sep,inj}}</math>'], ),
  Parameter(name='TS magnet thick injection septum hardedge magnetic field', group='FAC', is_derived=True, value='"TS beam magnetic rigidity"/"TS magnet thick injection septum hardedge bending radius"', symbol=r'<math>B_\text{thick sep,inj}</math>', units='T', deps=[],   obs=[r'<math>B_\text{thick sep,inj}=\frac{(B\rho)}{\rho_\text{thick sep,inj}}</math>'], ),
  Parameter(name='TS magnet thick injection septum hardedge sagitta', group='FAC', is_derived=False, value=ts_magnet_thick_injection_septum_sagitta, symbol=r'<math>S_\text{thick sep,inj}</math>', units='mm', deps=[], obs=[], ),
  Parameter(name='TS magnet thin injection septum number', group='FAC', is_derived=False, value=ts_magnet_thin_injection_septum_number, symbol=r'<math>N_\text{thin sep,inj}</math>', units='', deps=[], obs=[], ),
  Parameter(name='TS magnet thin injection septum deflection angle', group='FAC', is_derived=False, value=ts_magnet_thin_injection_septum_deflection_angle, symbol=r'<math>\theta_\text{thin sep,inj}</math>', units=unicode('°',encoding='utf-8'), deps=[], obs=[], ),
  Parameter(name='TS magnet thin injection septum hardedge length', group='FAC', is_derived=False, value=ts_magnet_thin_injection_septum_hardedge_length, symbol=r'<math>L_\text{thin sep,inj}</math>', units='m', deps=[], obs=[], ),
  Parameter(name='TS magnet thin injection septum hardedge bending radius', group='FAC', is_derived=True, value='"TS magnet thin injection septum hardedge length"/deg2rad("TS magnet thin injection septum deflection angle")', symbol=r'<math>\rho_\text{thin sep,inj}</math>', units='m', deps=[],   obs=[r'<math>\rho_\text{thin sep,inj}=\frac{L_\text{thin sep,inj}}{\theta_\text{thin sep,inj}}</math>'], ),
  Parameter(name='TS magnet thin injection septum hardedge magnetic field', group='FAC', is_derived=True, value='"TS beam magnetic rigidity"/"TS magnet thin injection septum hardedge bending radius"', symbol=r'<math>B_\text{thin sep,inj}</math>', units='T', deps=[],   obs=[r'<math>B_\text{thin sep,inj}=\frac{(B\rho)}{\rho_\text{thin sep,inj}}</math>'], ),
  Parameter(name='TS magnet thin injection septum hardedge sagitta', group='FAC', is_derived=False, value=ts_magnet_thin_injection_septum_sagitta, symbol=r'<math>S_\text{thin sep,inj}</math>', units='mm', deps=[], obs=[], ),
  Parameter(name='TS magnet quadrupole number', group='FAC', is_derived=False, value=ts_magnet_quadrupole_number, symbol=r'<math>N_\text{QUAD}</math>', units='', deps=[], obs=[], ),
  Parameter(name='TS magnet quadrupole maximum gradient', group='FAC', is_derived=False, value=ts_magnet_quadrupole_maximum_gradient, symbol=r"<math>B'_\text{max}</math>", units='T/m', deps=[], obs=[], ),
  Parameter(name='TS magnet quadrupole hardedge length', group='FAC', is_derived=False, value=ts_magnet_quadrupole_hardedge_length, symbol=r'<math>L_\text{quad}</math>', units='m', deps=[], obs=[], ),
  Parameter(name='TS magnet quadrupole hardedge strength', group='FAC', is_derived=False, value=ts_magnet_quadrupole_hardedge_strength, symbol=r'<math>K_\text{quad}</math>', units='m<sup>-2</sup>', deps=[], obs=[], ),
  Parameter(name='TS magnet quadrupole hardedge gradient', group='FAC', is_derived=True, value='"TS beam magnetic rigidity"*"TS magnet quadrupole hardedge strength"', symbol=r'<math>G_\text{quad}</math>', units='m<sup>-2</sup>', deps=[], obs=[], ),
  Parameter(name='TS magnet hcm number', group='FAC', is_derived=False, value=ts_magnet_hcm_number, symbol=r'<math>N_\text{HCM}</math>', units='', deps=[], obs=[], ),
  Parameter(name='TS magnet hcm maximum strength', group='FAC', is_derived=False, value=ts_magnet_hcm_maximum_strength, symbol=r'<math>\theta^\text{x, max}</math>', units=unicode('mrad', encoding='utf-8'), deps=[], obs=[], ),
  Parameter(name='TS magnet vcm number', group='FAC', is_derived=False, value=ts_magnet_vcm_number, symbol=r'<math>N_\text{VCM}</math>', units='', deps=[], obs=[], ),
  Parameter(name='TS magnet vcm maximum strength', group='FAC', is_derived=False, value=ts_magnet_vcm_maximum_strength, symbol=r'<math>\theta^\text{y, max}</math>', units=unicode('mrad', encoding='utf-8'), deps=[], obs=[], ),

  Parameter(name='TS bpm number', group='FAC', is_derived=False, value=ts_bpm_number, symbol=r'<math>N_\text{BPM}</math>', units='', deps=[], obs=[], ),
]
