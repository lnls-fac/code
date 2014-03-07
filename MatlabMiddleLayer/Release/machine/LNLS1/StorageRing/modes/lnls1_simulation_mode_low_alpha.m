function lnls1_simulation_mode_low_alpha

lnls1_set_id_field('AWG01', 0);
lnls1_set_id_field('AWG09', 0);
lnls1_set_id_field('AON11', 0);
lnls1_set_id_field('AWS07', 0);

% negative alpha (6-fold symmetry)
% setpv('QF',     'Physics',   2.688);
% setpv('QD',     'Physics',  -2.95392);
% setpv('QD',     'Physics',  -2.944);
% setpv('QF',     'Physics',   2.68);
% setpv('QD',     'Physics',  -2.957);
% setpv('QFC',    'Physics',   2.144);
% setpv('SD',     'Physics', -41.44);
% setpv('SF',     'Physics',  51.39);
setpv('QF',     'Physics',   2.68);
setpv('QD',     'Physics',  -2.957);
setpv('QFC',    'Physics',   2.164);
setpv('SD',     'Physics', -27.97);
setpv('SF',     'Physics',  45.91);

% % low-alpha (3-fold symmetry)
% [~, ~, b_rho] = lnls_beta_gamma(1.15);
% sn = (0.25/0.27);
% setpv('A6QF01',  'Physics',   7.7/b_rho * sn);
% setpv('A6QF02',  'Physics',   10.3/b_rho * sn);
% 
% setpv('A2QD01',  'Physics',   -12.5/b_rho * sn);
% setpv('A2QF01',  'Physics',   16.8/b_rho * sn);
% setpv('A2QD03',  'Physics',   -9.0/b_rho * sn);
% setpv('A2QF03',  'Physics',   9.1/b_rho * sn);
% setpv('A2QD05',  'Physics',   -12.5/b_rho * sn);
% setpv('A2QF05',  'Physics',   16.8/b_rho * sn);
% setpv('A2QD07',  'Physics',   -9.0/b_rho * sn);
% setpv('A2QF07',  'Physics',   9.1/b_rho * sn);
% setpv('A2QD09',  'Physics',   -12.5/b_rho * sn);
% setpv('A2QF09',  'Physics',   16.8/b_rho * sn);
% setpv('A2QD11',  'Physics',   -9.0/b_rho * sn);
% setpv('A2QF11',  'Physics',   9.1/b_rho * sn);
% 
% setpv('A6SD01',  'Physics',   -246/b_rho * 0);
% setpv('A6SD02',  'Physics',   -246/b_rho * 0);
% setpv('A6SF',    'Physics',    326/b_rho * 0);
