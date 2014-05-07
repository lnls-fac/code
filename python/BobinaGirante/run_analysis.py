import analysis

folder = '/home/ximenes/Desktop/TESTES-BOBINA/Dipolo'
analysis.booster.test_dipole_repetibility(folder, plot_label = 'TEST DIPOLE')

folder = '/home/ximenes/Desktop/TESTES-BOBINA/Quadrupolo'
analysis.booster.quadrupoles_repetibility(folder, plot_label = 'QUADRUPOLES', harmonics = analysis.booster.default_quad_harmonics, ymin = 1e-6)