import analysis

def specs_booster_quadrupole(main_multipole = 0.5):
   
    r0 = 17.5/1000 # [m]
    main_harmonic_order = 2
    harmonics = [1,2,3,4,5,6,7,8,9,10,11]
    LNn_avg_norm = [0,1,  0,0,0,-1e-3,0,0,0,1.1e-3,8e-5]
    LNn_std_norm = [0,0,  7e-4,4e-4,4e-4,4e-4,4e-4,4e-4,4e-4,4e-4,0]
    LSn_avg_norm = [0,0,  0,0,0,0,0,0,0,0,0]
    LSn_std_norm = [0,0,  1e-4,5e-4,1e-6,1e-6,1e-6,1e-6,1e-6,1e-6,0]
    (LNn_avg, LNn_std, LSn_avg, LSn_std) = analysis.calc_absolute_multipoles(main_harmonic_order = main_harmonic_order, 
                                                                    r0 = r0, harmonics = harmonics, 
                                                                    LNn_avg_norm, LNn_std_norm, 
                                                                    LSn_avg_norm, LSn_std_norm)
    m = analysis.RotatingCoilMeasurement(harmonics = harmonics, 
                                LNn_avg = LNn_avg, 
                                LNn_std = LNn_std,
                                LSn_avg = LSn_avg, 
                                LSn_std = LSn_std)
    return m




def analysis_booster_quadrupoles():
    ''' booster quadrupoles '''
    m0 = specs_booster_quadrupole()
    m0.print_multipoles()
    m1 = analysis.RotatingCoilMeasurement('BQF_03_Medida_01.dat')
    m1.print_multipoles()
    m2 = analysis.RotatingCoilMeasurement('BQF_03_Medida_02.dat')
    m2.print_multipoles()
    m3 = analysis.RotatingCoilMeasurement('BQF_03_Medida_03.dat')
    m3.print_multipoles()
    data = [m0, m1, m2, m3]
    analysis.rotating_coil_measurements.plot_multipoles(data, plot_label = 'tests', alpha_blending = 0.4, colors = analysis.colors_happy, min_y = 1e-8)
