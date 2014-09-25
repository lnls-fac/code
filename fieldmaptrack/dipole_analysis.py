import matplotlib.pyplot as plt
import numpy as np
from multiprocessing import Process

def calc_sagitta(half_dipole_length, trajectory):
    
    rx = trajectory.rx
    rz = trajectory.rz
    
    if rz[-1] < half_dipole_length:
        raise DipoleAnalysisException('trajectory path does not exit dipole')
    
    i = 0
    while (rz[i] < half_dipole_length):
        i += 1
    sagitta = rx[0] - rx[i]
    return sagitta
        
    
def fieldmap_analysis(
        label,
        file_name,
        missing_integral_analysis = False,
        threshold_field_fraction = 0.3,
        field_extrapolation_exponents = None,
        ):
    
    if field_extrapolation_exponents is None:
        field_extrapolation_exponents = (2,3,4,5,6,7,8,9,10)
    
    # loads fieldmap from file
    # ========================
    fm = fieldmaptrack.fieldmap.FieldMap(file_name)
    
    # plots basic data
    # ================
   
    # -- longitudinal profile at (x,y) = (0,0)
    x = fm.rz
    y = fm.by[fm.ry_zero][fm.rx_zero,:]
    plt.plot(x,y)
    plt.grid(True)
    plt.xlabel('rz [mm]'), plt.ylabel('by [mm]')
    plt.title(label + '\n' + 'Longitudinal profile of vertical field')
    plt.savefig(label + '_fig01' + '_by-vs-z.pdf')
    plt.clf()
    
    # -- transversal profile at (y,z) = (0,0)
    x = fm.rx
    y = fm.by[fm.ry_zero][:,fm.rz_zero]
    plt.plot(x,y)
    plt.grid(True)
    plt.xlabel('rx [mm]'), plt.ylabel('by [T]')
    plt.title(label + '\n' + 'Transverse profile of vertical field')
    plt.savefig(label + '_fig02' + '_by-vs-x.pdf')
    plt.clf()
    
    
    # calculates missing integrals
    # ============================
    if missing_integral_analysis:
        fm.field_extrapolation_analysis(threshold_field_fraction = threshold_field_fraction, 
                                        polyfit_exponents = field_extrapolation_exponents)

    # prints basic raw information on the fieldmap
    # ============================================
    print('--- fieldmap ---')
    print(fm)
    
    
def reference_trajectory(
        fieldmap,
        beam_energy,
        beam_current,
        s_length,
        s_nrpts,
        force_midplane,
        ):
    
    ebeam = fieldmaptrack.beam.Beam(energy = beam_energy, current = beam_current)
    
    # Runge-Kutta trajectory calculation
    # ==================================
    traj = fieldmaptrack.track.Trajectory(beam=ebeam, fieldmap=fieldmap)
    init_rx, init_ry, init_rz = 0.0, 0.0, 0.0
    init_px, init_py, init_pz = 0.0, 0.0, 1.0
    traj.calc_trajectory(init_rx=init_rx, init_ry=init_ry, init_rz=init_rz,   
                         init_px=init_px, init_py=init_py, init_pz=init_pz, 
                         s_length=s_length, 
                         s_nrpts=s_nrpts, 
                         force_midplane=force_midplane)
    
    
    
    monomials = [0,1,2,3,4,5,6,7]
    grid = np.linspace(-5,5,21)
    polynom_a, polynom_b = traj.calc_multipoles(perpendicular_grid, multipolar_monomials)
    


    
def run(label,
        file_name,
        beam_energy,
        beam_current,
        init_rx, init_ry, init_rz,
        init_px, init_py, init_pz,
        s_length,
        s_nrpts,
        force_midplane,
        threshold_field_fraction = 0.3,
        field_extrapolation_exponents = None,
        multipolar_monomials = None,
        perpendicular_grid = None,
        missing_integral_analysis = False
        ):
    
    if field_extrapolation_exponents is None:
        field_extrapolation_exponents = (2,3,4,5,6,7,8,9,10)
    if multipolar_monomials is None:
        multipolar_monomials = (0,1,2,3,4,5,6,7,8)
    if perpendicular_grid is None:
        perpendicular_grid = np.linspace(-5,5,11)
    
    print('DIPOLE ANALYSIS')
    print('===============')
         
    print('{0:<35s} {1}'.format('label:', label))
    
    # loads fieldmap from file
    # ========================
    fm = fmap.FieldMap(file_name)
    ebeam = beam.Beam(energy = beam_energy, current = beam_current)
    
    # plots basic data
    # ================
   
    # -- longitudinal profile at (x,y) = (0,0)
    x = fm.rz
    y = fm.by[fm.ry_zero][fm.rx_zero,:]
    plt.plot(x,y)
    plt.grid(True)
    plt.xlabel('rz [mm]'), plt.ylabel('by [mm]')
    plt.title(label + '\n' + 'Longitudinal profile of vertical field')
    plt.savefig(label + '_fig01' + '_by-vs-z.pdf')
    plt.clf()
    
    # -- transversal profile at (y,z) = (0,0)
    x = fm.rx
    y = fm.by[fm.ry_zero][:,fm.rz_zero]
    plt.plot(x,y)
    plt.grid(True)
    plt.xlabel('rx [mm]'), plt.ylabel('by [T]')
    plt.title(label + '\n' + 'Transverse profile of vertical field')
    plt.savefig(label + '_fig02' + '_by-vs-x.pdf')
    plt.clf()
    
    
    # calculates missing integrals
    # ============================
    if missing_integral_analysis:
        fm.field_extrapolation_analysis(threshold_field_fraction = threshold_field_fraction, 
                                        polyfit_exponents = field_extrapolation_exponents)

    # prints basic raw information on the fieldmap
    # ============================================
    print('--- fieldmap ---')
    print(fm)
    fm.clear_extrapolation_coefficients()
    
    
    # Runge-Kutta trajectory calculation
    # ==================================
    traj = track.Trajectory(beam=ebeam, fieldmap=fm)
    traj.calc_trajectory(init_rx=init_rx, init_ry=init_ry, init_rz=init_rz,   
                         init_px=init_px, init_py=init_py, init_pz=init_pz, 
                         s_length=s_length, 
                         s_nrpts=s_nrpts, 
                         force_midplane=force_midplane)
    
    
    
    monomials = [0,1,2,3,4,5,6,7]
    grid = np.linspace(-5,5,21)
    polynom_a, polynom_b = traj.calc_multipoles(perpendicular_grid, multipolar_monomials)
    

    # calcs sagitta
    sagitta = calc_sagitta(fm.length/2.0, traj)
    
    # prints basic information on the trajectory
    # =========================================    
    print('--- trajectory (half magnet) ---')
    print(traj)
    print('{0:<35s} {1} mm'.format('sagitta:', sagitta))
    
    
   
      
    # Plots trajectory data
    # =====================
    
    # -- trajectory on rectangular grid
    x = traj.rz
    y = traj.rx
    plt.plot(x,y)
    plt.grid(True)
    plt.xlabel('rz [mm]'), plt.ylabel('rx [mm]')
    plt.title(label + '\n' + 'Trajectory')
    plt.savefig(label + '_fig03' + '_zx-trajectory.pdf')
    plt.clf()    
    # -- vertical field on trajectory
    x = traj.s
    y = traj.by
    plt.plot(x,y)
    plt.grid(True)
    plt.xlabel('s [mm]'), plt.ylabel('by [T]')
    plt.title(label + '\n' + 'Vertical field on trajectory')
    plt.savefig(label + '_fig04' + '_by-vs-s-trajectory.pdf')
    plt.clf()    
    