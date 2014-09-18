import analysis

#folder = '/home/ximenes/Desktop/TESTES-BOBINA/BQF03 - Curva Excitacao/Fonte 300A/Ligacao_Desfocalizador/01_Sequencia'
#folder = '/home/ximenes/Desktop/TESTES-BOBINA/BQF03 - Curva Excitacao/Fonte 300A/01_Sequencia'
#folder = '/home/ximenes/Desktop/TESTES-BOBINA/BQF03 - Curva Excitacao/Fonte 070A/01_Sequencia'
folder = '/home/ximenes/Desktop/TESTES-BOBINA/BQF03-novos/Novos_TVE'
folder = '/home/ximenes/Desktop/TESTES-BOBINA/BQF03-novos/Antigos TVE'
folder = '/home/ximenes/Desktop/TESTES-BOBINA/BQF03-novos/Novos Ceramica'
folder = '/home/ximenes/Desktop/TESTES-BOBINA/BQF03-novos/Antigos Ceramica'
#analysis.booster.quadrupoles_excitation(folder = folder, plot_label = 'BOOSTER QUADRUPOLES EXCITATION', harmonics = analysis.booster.default_quad_harmonics, ymin_multipoles = 1e-6, ymin_skew_angle = 1e-2, plot_normal_multipoles_flag = True, plot_skew_multipoles_flag = True, plot_skew_angle_flag = True)
analysis.booster.quadrupoles_repetibility(folder = folder, plot_label = 'QUADRUPOLES', harmonics = analysis.booster.default_quad_harmonics, ymin_multipoles = 1e-8, ymin_skew_angle = 1e-2, plot_normal_multipoles_flag = True, plot_skew_multipoles_flag = True, plot_skew_angle_flag = True)

#folder = '/home/ximenes/Desktop/TESTES-BOBINA/BQF03 - Curva Excitacao/Fonte 130A/Ligacao_Desfocalizador/Repetibilidade'
#analysis.booster.quadrupoles_repetibility(folder = folder, plot_label = 'QUADRUPOLES', harmonics = analysis.booster.default_quad_harmonics, ymin_multipoles = 1e-8, ymin_skew_angle = 1e-2, plot_normal_multipoles_flag = True, plot_skew_multipoles_flag = True, plot_skew_angle_flag = True)



#folder = '/home/ximenes/Desktop/TESTES-BOBINA/Dipolo'
#analysis.test_dipole.test_dipole_repetibility(folder = folder, plot_label = 'TEST DIPOLE', harmonics = [1,2,3,4,5,6,7,8,9,10], plot_normal_multipoles_flag = True, plot_skew_multipoles_flag = True, ymin_multipoles = 1e-9, ymin_skew_angle = 1e-2, plot_skew_angle_flag = True)

