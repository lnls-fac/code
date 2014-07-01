ebeam_energy    = 3e9 #[eV]
harmonic_number = 864
cavity_state    = 'on'
radiation_state = 'on'
vchamber_state  = 'on'

bends   = ['b1','b2','b3','bc']
quads   = ['qf1', 'qf2', 'qf3', 'qf4']
mrkrs   = ['mia', 'mib']
sexts   = ['sa1', 'sb1']
allfams = bends + quads + mrkrs + sexts



dynap_xy_run          = False
dynap_xy_flatfilename = 'flat_file_v500_ac10_5_bare_in.txt'
dynap_xy_de           = 0
dynap_xy_nr_turns     = 500
dynap_xy_x_nrpts      = 4 #90
dynap_xy_x_min	      = -0.0120 #[m]
dynap_xy_x_max 	      = +0.0120 #[m]
dynap_xy_y_nrpts      = 4 #40
dynap_xy_y_min        = +0.0000 #[m]
dynap_xy_y_max        = +0.0041 #[m]

dynap_ex_run          = False
dynap_ex_flatfilename = 'flat_file_v500_ac10_5_bare_in.txt'
dynap_ex_y            = 0
dynap_ex_nr_turns     = 500
dynap_ex_e_nrpts      = 2 #90
dynap_ex_e_min	      = -0.05 #[m]
dynap_ex_e_max 	      = +0.05 #[m]
dynap_ex_x_nrpts      = 2 #40
dynap_ex_x_min        = -0.015 #[m]
dynap_ex_x_max        = +0.000 #[m]

dynap_ma_run          = True
dynap_ma_flatfilename = 'flat_file_v500_ac10_5_bare_in.txt'
dynap_ma_nr_turns     = 20
dynap_ma_e_e0         = 0.01
dynap_ma_e_tol        = 0.001
dynap_ma_s_min        = 0 #[m]
dynap_ma_s_max        = 518.396/10 + 0.001
dynap_ma_fam_names    = allfams

