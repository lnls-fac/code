#!/usr/bin/python
# -*- coding: utf-8 -*-

from parameter import Parameter
from definitions import ParameterDefinitions as Prms


tb_beam_energy = 150.0 # [MeV]

tb_lattice_length = 21.2475 # [m]
tb_magnet_dipole_number = 4
tb_magnet_quadrupole_number = 13
tb_magnet_septum_number = 1
tb_magnet_quadrupole_maximum_gradient = 10.0 # [T/m]

tb_magnet_dipole_arc_length = 0.300 # [m]
tb_magnet_septum_arc_length = 0.5000 # [m]

tb_magnet_dipole_deflection_angle = 15.0 # [°]
tb_magnet_septum_deflection_angle = 21.75 # [°]

tb_magnet_dipole_sagitta = 9.8 # [mm]
tb_septum_dipole_sagitta = 23.7 # [mm]

tb_magnet_quadrupole_qa1_hardedge_length = 0.05 # [m]
tb_magnet_quadrupole_qa2_hardedge_length = 0.10 # [m]
tb_magnet_quadrupole_qa3_hardedge_length = 0.10 # [m]
tb_magnet_quadrupole_qb1_hardedge_length = 0.10 # [m]
tb_magnet_quadrupole_qb2_hardedge_length = 0.10 # [m]
tb_magnet_quadrupole_qc1_hardedge_length = 0.10 # [m]
tb_magnet_quadrupole_qc2_hardedge_length = 0.10 # [m]
tb_magnet_quadrupole_qc3_hardedge_length = 0.10 # [m]
tb_magnet_quadrupole_qd1_hardedge_length = 0.10 # [m]
tb_magnet_quadrupole_qd2_hardedge_length = 0.10 # [m]
tb_magnet_quadrupole_qe1_hardedge_length = 0.10 # [m]
tb_magnet_quadrupole_qe2_hardedge_length = 0.10 # [m]

parameter_list = [
  Parameter(name='TB beam energy', group='GIA', is_derived=False, value=tb_beam_energy, symbol=r'<math>E</math>', units='MeV', deps=[], obs=[], ),
  Parameter(name='TB beam gamma factor', group='FAC', is_derived=True, value='gamma(1.0e-3*"TB beam energy")', symbol=r'<math>\gamma</math>', units='', deps=[], obs=[], ),
  Parameter(name='TB beam beta factor', group='FAC', is_derived=True, value='beta("TB beam gamma factor")', symbol=r'<math>\beta</math>', units='', deps=[], obs=[], ),
  Parameter(name='TB beam velocity', group='FAC', is_derived=True, value='velocity("TB beam beta factor")', symbol=r'<math>v</math>', units='', deps=[], obs=[], ),
  Parameter(name='TB beam magnetic rigidity', group='FAC', is_derived=True, value='brho(1.0e-3*"TB beam energy", "TB beam beta factor")', symbol=r'<math>(B\rho)</math>', units=unicode('T·m', encoding='utf-8'), deps=[], obs=[r'<math>(B\rho)=\frac{p}{ec}=\frac{E}{ec^2}</math>'], ),

  Parameter(name='TB lattice length', group='FAC', is_derived=False, value=tb_lattice_length, symbol=r'<math>L</math>', units='m', deps=[], obs=['Includes septum.'], ),

  Parameter(name='TB magnet dipole number', group='FAC', is_derived=False, value=tb_magnet_dipole_number, symbol=r'<math>N_\text{dip}</math>', units='', deps=[], obs=[], ),
  Parameter(name='TB magnet quadrupole number', group='FAC', is_derived=False, value=tb_magnet_quadrupole_number, symbol=r'<math>N_\text{QUAD}</math>', units='', deps=[], obs=[], ),
  Parameter(name='TB magnet septum number', group='FAC', is_derived=False, value=tb_magnet_septum_number, symbol=r'<math>N_\text{sep}</math>', units='', deps=[], obs=[], ),
  Parameter(name='TB magnet quadrupole maximum gradient', group='FAC', is_derived=False, value=tb_magnet_quadrupole_maximum_gradient, symbol=r"<math>B'_\text{max}</math>", units='T/m', deps=[], obs=[], ),
  Parameter(name='TB magnet dipole deflection angle', group='FAC', is_derived=False, value=tb_magnet_dipole_deflection_angle, symbol=r'<math>\theta_\text{dip}</math>', units=unicode('°',encoding='utf-8'), deps=[], obs=[], ),
  Parameter(name='TB magnet septum deflection angle', group='FAC', is_derived=False, value=tb_magnet_septum_deflection_angle, symbol=r'<math>\theta_\text{sep}</math>', units=unicode('°',encoding='utf-8'), deps=[], obs=[], ),
  Parameter(name='TB magnet dipole arc length', group='FAC', is_derived=False, value=tb_magnet_dipole_arc_length, symbol=r'<math>L_\text{dip}</math>', units='m', deps=[], obs=[], ),
  Parameter(name='TB magnet septum arc length', group='FAC', is_derived=False, value=tb_magnet_septum_arc_length, symbol=r'<math>L_\text{sep}</math>', units='m', deps=[], obs=[], ),
  Parameter(name='TB magnet dipole bending radius', group='FAC', is_derived=True, value='"TB magnet dipole arc length"/deg2rad("TB magnet dipole deflection angle")', symbol=r'<math>\rho_\text{dip}</math>', units='m', deps=[],   obs=[r'<math>\rho_\text{dip}=\frac{L_\text{dip}}{\theta_\text{dip}}</math>'], ),
  Parameter(name='TB magnet septum bending radius', group='FAC', is_derived=True, value='"TB magnet septum arc length"/deg2rad("TB magnet septum deflection angle")', symbol=r'<math>\rho_\text{sep}</math>', units='m', deps=[],   obs=[r'<math>\rho_\text{sep}=\frac{L_\text{sep}}{\theta_\text{sep}}</math>'], ),
  Parameter(name='TB magnet dipole magnetic field', group='FAC', is_derived=True, value='"TB beam magnetic rigidity"/"TB magnet dipole bending radius"', symbol=r'<math>B_\text{dip}</math>', units='T', deps=[],   obs=[r'<math>B_\text{dip}=\frac{(B\rho)}{\rho_\text{dip}}</math>'], ),
  Parameter(name='TB magnet septum magnetic field', group='FAC', is_derived=True, value='"TB beam magnetic rigidity"/"TB magnet septum bending radius"', symbol=r'<math>B_\text{sep}</math>', units='T', deps=[],   obs=[r'<math>B_\text{sep}=\frac{(B\rho)}{\rho_\text{sep}}</math>'], ),
  Parameter(name='TB magnet dipole sagitta', group='FAC', is_derived=False, value=tb_magnet_dipole_sagitta, symbol=r'<math>S_\text{dip}</math>', units='mm', deps=[], obs=[], ),
  Parameter(name='TB magnet septum sagitta', group='FAC', is_derived=False, value=tb_septum_dipole_sagitta, symbol=r'<math>S_\text{sep}</math>', units='mm', deps=[], obs=[], ),
  Parameter(name='TB magnet quadrupole qa1 hardedge length', group='FAC', is_derived=False, value=tb_magnet_quadrupole_qa1_hardedge_length, symbol=r'<math>L_\text{QA1}</math>', units='m', deps=[], obs=[], ),
  Parameter(name='TB magnet quadrupole qa2 hardedge length', group='FAC', is_derived=False, value=tb_magnet_quadrupole_qa2_hardedge_length, symbol=r'<math>L_\text{QA2}</math>', units='m', deps=[], obs=[], ),
  Parameter(name='TB magnet quadrupole qa3 hardedge length', group='FAC', is_derived=False, value=tb_magnet_quadrupole_qa3_hardedge_length, symbol=r'<math>L_\text{QA3}</math>', units='m', deps=[], obs=[], ),
  Parameter(name='TB magnet quadrupole qb1 hardedge length', group='FAC', is_derived=False, value=tb_magnet_quadrupole_qb1_hardedge_length, symbol=r'<math>L_\text{QB1}</math>', units='m', deps=[], obs=[], ),
  Parameter(name='TB magnet quadrupole qb2 hardedge length', group='FAC', is_derived=False, value=tb_magnet_quadrupole_qb2_hardedge_length, symbol=r'<math>L_\text{QB2}</math>', units='m', deps=[], obs=[], ),
  Parameter(name='TB magnet quadrupole qc1 hardedge length', group='FAC', is_derived=False, value=tb_magnet_quadrupole_qc1_hardedge_length, symbol=r'<math>L_\text{QC1}</math>', units='m', deps=[], obs=[], ),
  Parameter(name='TB magnet quadrupole qc2 hardedge length', group='FAC', is_derived=False, value=tb_magnet_quadrupole_qc2_hardedge_length, symbol=r'<math>L_\text{QC2}</math>', units='m', deps=[], obs=[], ),
  Parameter(name='TB magnet quadrupole qc3 hardedge length', group='FAC', is_derived=False, value=tb_magnet_quadrupole_qc3_hardedge_length, symbol=r'<math>L_\text{QC3}</math>', units='m', deps=[], obs=[], ),
  Parameter(name='TB magnet quadrupole qd1 hardedge length', group='FAC', is_derived=False, value=tb_magnet_quadrupole_qd1_hardedge_length, symbol=r'<math>L_\text{QD1}</math>', units='m', deps=[], obs=[], ),
  Parameter(name='TB magnet quadrupole qd2 hardedge length', group='FAC', is_derived=False, value=tb_magnet_quadrupole_qd2_hardedge_length, symbol=r'<math>L_\text{QD2}</math>', units='m', deps=[], obs=[], ),
  Parameter(name='TB magnet quadrupole qe1 hardedge length', group='FAC', is_derived=False, value=tb_magnet_quadrupole_qe1_hardedge_length, symbol=r'<math>L_\text{QE1}</math>', units='m', deps=[], obs=[], ),
  Parameter(name='TB magnet quadrupole qe2 hardedge length', group='FAC', is_derived=False, value=tb_magnet_quadrupole_qe2_hardedge_length, symbol=r'<math>L_\text{QE2}</math>', units='m', deps=[], obs=[], ),
]
