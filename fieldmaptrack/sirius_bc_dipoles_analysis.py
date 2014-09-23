#!/usr/bin/python3 

from fieldmaptrack import beam
from fieldmaptrack import dipole_analysis

label             = 'BC_model1_controlgap_8mm' # parameter: identification label
fieldmap_filename = '/home/ximenes/fac_files/data/magnet_modelling/sirius/bc/fieldmaps/2014-09-05_Dipolo_Anel_BC_Modelo1_gap_lateral_8mm_-50_50mm_-2000_2000mm.txt' # parameter
ebeam_energy      = 3.0   # parameter: electron beam energy [GeV]
ebeam_current     = 350   # parameter: electron beam current [mA]
init_rx           = 0.0   # parameter: initial x position [mm] of the electron for RK tracking (rectangular grid)
init_ry           = 0.0   # parameter: initial y position [mm] of the electron for RK tracking (rectangular grid)
init_rz           = 0.0   # parameter: initial z position [mm] of the electron for RK tracking (rectangular grid)
init_px           = 0.0   # parameter: initial px/p0 position [mm] of the electron for RK tracking (rectangular grid)
init_py           = 0.0   # parameter: initial py/p0 position [mm] of the electron for RK tracking (rectangular grid)
init_pz           = 1.0   # parameter: initial pz/p0 position [mm] of the electron for RK tracking (rectangular grid)
s_length          = 800.0 # parameter: total path length to track through RK
s_nrpts           = 2001  # parameter: number of points in RK
force_midplane    = True          # parameter: force trajectory on midplane (setting ry = py = 0)
missing_integral_analysis = False # parameter: does missing integral analysis with extrapolation functions
threshold_field_fraction  = 0.3   # parameter: for missing integrals analysis of fieldmap
polyfit_exponents         = [2,3,4,5,6,7,8,9,10] # parameter: for extrapolating fieldmap

if __name__ == "__main__":
    dipole_analysis.run(
        label = label,
        file_name = fieldmap_filename,
        beam_energy = ebeam_energy,
        beam_current = ebeam_current,
        init_rx=init_rx, init_ry=init_ry, init_rz=init_rz,
        init_px=init_px, init_py=init_py, init_pz=init_pz,
        s_length=s_length,
        s_nrpts=s_nrpts,
        force_midplane=force_midplane,
        threshold_field_fraction=threshold_field_fraction,
        polyfit_exponents=polyfit_exponents,
    )
