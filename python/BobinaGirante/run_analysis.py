import analysis



folder = '/home/ximenes/Desktop/TESTES-BOBINA/Dipolo'
analysis.test_dipole.test_dipole_repetibility(folder, plot_label = 'TEST DIPOLE', harmonics = [1,2,3,4,5,6,7,8,9,10], plot_normal_multipoles_flag = True, plot_skew_multipoles_flag = True, ymin_multipoles = 1e-9, ymin_skew_angle = 1e-2, plot_skew_angle_flag = True)

folder = '/home/ximenes/Desktop/TESTES-BOBINA/Quadrupolo'
analysis.booster.quadrupoles_repetibility(folder, plot_label = 'QUADRUPOLES', harmonics = analysis.booster.default_quad_harmonics, ymin_multipoles = 1e-6, ymin_skew_angle = 1e-2, plot_normal_multipoles_flag = True, plot_skew_multipoles_flag = True, plot_skew_angle_flag = True)
