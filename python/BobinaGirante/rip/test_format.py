import analysis.rotating_coil_measurements as abg

    
fname = '/home/ximenes/Desktop/BC0001_D_BOB_+0000A_140425_154023.dat'
r = abg.RotatingCoilMeasurement(
    fname = fname, 
    label = 'test',
    max_harmonic_order = 15)
r.print_multipoles()
abg.plot_multipoles(data = [r], main_harmonic_order = 4, r0 = 17.5, plot_label = 'teste', harmonics = [1,2,3,4], ymin = 1e-6)

