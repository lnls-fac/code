function r = CONFIG

r.config.label = 'CONFIG';
r.questiona = false;

%% constants
um       = 1e-6;
nm       = 1e-9;
mrad     = 0.001;
urad     = 1e-6;
percent  = 0.01;
ppm      = 1e-6;


%% definition of the nominal AT model
r.config.lattice_function  = @sirius_si_lattice;
r.config.lattice_func_arg1  = 'b'; % old ac10
r.config.lattice_func_arg2  = '00'; % old ac10
%r.config.lattice_function  = 'thering_withids.mat';


if ischar(r.config.lattice_function)
    data = load(r.config.lattice_function);
    r.params.the_ring = data.thering;
else
    r.params.the_ring = r.config.lattice_function(r.config.lattice_func_arg1,r.config.lattice_func_arg2);
end

r.config.nr_machines         = 1;
r.config.simulate_multipoles = true;
r.config.simulate_static     = true;
r.config.simulate_dynamic    = false;

%se verdadeiro, a órbita de referência será uma simulação do processo de
%bba. Atualmente, pegamos a orbita nos quadrupolos mais proximos ao bpm e
%atribuimos o deslocamento no centro do quadrupolo como sendo a orbita bba
%no bpm. O erro estático do bpm representa a precisao do 'bba'.
r.params.correct2bba_orbit = true;


%% Static
r.config.static.cutoff_errors = 1;
r.config.static.errors_delta  = [1.0];


% erros estaticos, de alinhamento e excitacao
r.config.static.families.quads.sigma_x      = 40 * um * 1;
r.config.static.families.sexts.sigma_x      = 40 * um * 1;
r.config.static.families.bends.sigma_x      = 40 * um * 1;
r.config.static.families.cbend.sigma_x      = 40 * um * 1;

r.config.static.families.quads.sigma_y      = 40 * um * 1;
r.config.static.families.sexts.sigma_y      = 40 * um * 1;
r.config.static.families.bends.sigma_y      = 40 * um * 1;
r.config.static.families.cbend.sigma_y      = 40 * um * 1;

r.config.static.families.quads.sigma_roll   = 0.20 * mrad * 1;
r.config.static.families.sexts.sigma_roll   = 0.20 * mrad * 1;
r.config.static.families.bends.sigma_roll   = 0.20 * mrad * 1;
r.config.static.families.cbend.sigma_roll   = 0.20 * mrad * 1;

% r.config.static.families.quads.sigma_yaw    = 0.10 * mrad * 0;
% r.config.static.families.sexts.sigma_yaw    = 0.10 * mrad * 0;
% r.config.static.families.bends.sigma_yaw    = 0.05 * mrad * 0;
% r.config.static.families.cbend.sigma_yaw    = 0.10 * mrad * 0;
% 
% r.config.static.families.quads.sigma_pitch  = 0.10 * mrad * 0;
% r.config.static.families.sexts.sigma_pitch  = 0.10 * mrad * 0;
% r.config.static.families.bends.sigma_pitch  = 0.05 * mrad * 0;
% r.config.static.families.cbend.sigma_pitch  = 0.10 * mrad * 0;

r.config.static.families.quads.sigma_e      = 0.05 * percent * 1;
r.config.static.families.sexts.sigma_e      = 0.05 * percent * 1;
r.config.static.families.bends.sigma_e      = 0.05 * percent * 1;
r.config.static.families.cbend.sigma_e      = 0.05 * percent * 1;
r.config.static.families.bends.sigma_e_kdip = 0.10 * percent * 1;


% definição de famílias para erros estáticos
r.config.static.families.quads.labels = {'qaf','qbd2','qbf','qbd1','qad','qf1','qf2','qf3','qf4'};
r.config.static.families.quads.nrsegs = ones(1,9);
r.config.static.families.sexts.labels = {'sa1','sb1','sd2','sf2','sb2','sd1','sf1','sa2','sd3'};
r.config.static.families.sexts.nrsegs = ones(1, 9);
r.config.static.families.bends.labels = {'b1','b2','b3'};
r.config.static.families.bends.nrsegs = [2 2 2];
r.config.static.families.cbend.labels = {'bc'};
r.config.static.families.cbend.nrsegs = 2;


% os erros estáticos e dinâmicos dos bpms tem interpretacao diferente dos
% erros dos outros elementos. Eles medem o erro do bpm em relação à orbita
% para a qual estamos corrigindo. Assim, no caso de correcao para a orbita
% bba, o erro estático mede o erro do método de bba, enquanto o erro
% dinâmico mede a única, verdadeira e absoluta vibraçao do bpm.
r.config.static.families.bpm.labels = {'BPM'};
r.config.static.families.bpm.nrsegs = 1;
r.config.static.families.bpm.sigma_y    = 10 * um * 0;
r.config.static.families.bpm.sigma_x    = 10 * um * 0;

r.config.static.girder.girder_error_flag = false;
r.config.static.girder.correlated_errors = false;
r.config.static.girder.sigma_x     = 100 * um * 1;
r.config.static.girder.sigma_y     = 100 * um * 1;
r.config.static.girder.sigma_roll  =  0.20 * mrad * 1;
% r.config.static.girder.sigma_yaw   =  20 * mrad * 0;
% r.config.static.girder.sigma_pitch =  20 * mrad * 0;


% parameters for slow correction algorithms

%cod
selection = [1 1 1 1  1 1  1 1 1 1];
selection = repmat(selection, 1, 20);
r.params.static.bpm_idx = findcells(r.params.the_ring, 'FamName', 'BPM');
r.params.static.bpm_idx = r.params.static.bpm_idx(logical(selection));

selection = [1 1 1 1   1 1 1 1];
selection = repmat(selection, 1, 20);
r.params.static.hcm_idx = findcells(r.params.the_ring, 'FamName', 'hcm');
r.params.static.hcm_idx = r.params.static.hcm_idx(logical(selection));

selection = [1 1 1   1 1 1];
selection = repmat(selection, 1, 20);
r.params.static.vcm_idx = findcells(r.params.the_ring, 'FamName', 'vcm');
r.params.static.vcm_idx = r.params.static.vcm_idx(logical(selection));
r.params.static.cod_correction_flag = true;
r.params.static.cod_sextupoles_ramp = [0 1];
r.params.static.cod_svs        = 120:20:280;
r.params.static.cod_nr_iter    = 3;

%optics
r.params.static.kbs_idx = findcells(r.params.the_ring, 'K');
r.params.static.kbs_idx = setdiff(r.params.static.kbs_idx, findcells(r.params.the_ring, 'BendingAngle'));
r.params.static.optics_correction_flag = false;
r.params.static.optics_svs     = 180:20:260;
r.params.static.optics_nr_iter = 2; 

%coupling
r.params.static.scm_idx = [];
r.params.static.scm_idx = [r.params.static.scm_idx findcells(r.params.the_ring, 'FamName', 'sd2')];
r.params.static.coup_correction_flag = false;
r.params.static.coup_svs       = 'all';
r.params.static.coup_nr_iter   = 3;
r.params.static.coup_residual  = 0.5 / 100;

%tune
r.params.static.tune_correction_flag = true;
r.params.static.tune_families         = {'qaf','qbd2','qbf','qbd1','qad'};
r.params.static.tune_goal            = [46.17987 14.15001];
r.params.static.tune_max_iter        = 10;
r.params.static.tune_tolerancia      = 1e-6;


%% Multipoles
r.config.multipoles.cutoff_errors = 2;


% famílias dos multipolos
r.config.multipoles.families.quads.labels = {'qaf','qbd2','qbf','qbd1','qad','qf1','qf2','qf3','qf4'};
r.config.multipoles.families.quads.nrsegs = ones(1,9);
r.config.multipoles.families.quads.main_multipole = 2;% positive for normal negative for skew
r.config.multipoles.families.quads.r0 = 11.7e-3;
r.config.multipoles.families.sexts.labels = {'sa1','sb1','sd2','sf2','sb2','sd1','sf1','sa2','sd3'};
r.config.multipoles.families.sexts.nrsegs = ones(1, 9);
r.config.multipoles.families.sexts.main_multipole = 3;% positive for normal negative for skew
r.config.multipoles.families.sexts.r0 = 11.7e-3;
r.config.multipoles.families.bends.labels = {'b1','b2','b3', 'bc'};
r.config.multipoles.families.bends.nrsegs = [2 2 2 2];
r.config.multipoles.families.bends.main_multipole = 1;% positive for normal negative for skew
r.config.multipoles.families.bends.r0 = 11.7e-3;


r.config.multipoles.families.quads.sys.order       = [ 3    4     5     6    10 ]; % 1 for dipole
r.config.multipoles.families.quads.sys.main_values = [3e-8 1e-5 -2e-8 -3e-5 8e-5]; 
r.config.multipoles.families.quads.sys.skew_values = [0.0  0.0   0.0   0.0  0.0 ];
r.config.multipoles.families.quads.rms.order       = [ 3   4   5   6   7   8   9   10];
r.config.multipoles.families.quads.rms.main_values = 0*ones(1,8)*4e-5; 
r.config.multipoles.families.quads.rms.skew_values = 0*ones(1,8)*1e-5;

r.config.multipoles.families.sexts.sys.order       = [ 9     15 ];
r.config.multipoles.families.sexts.sys.main_values = [4e-6 -1e-7]; 
r.config.multipoles.families.sexts.sys.skew_values = [0.0   0.0 ]; 
r.config.multipoles.families.sexts.rms.order       = [4   5   6   7   8   9   10  11];
r.config.multipoles.families.sexts.rms.main_values = 0*ones(1,8)*4e-5; 
r.config.multipoles.families.sexts.rms.skew_values = 0*ones(1,8)*1e-5;

r.config.multipoles.families.bends.sys.order       = [ 3   4   5   6   7 ]; % 1 for dipole
r.config.multipoles.families.bends.sys.main_values = [-9   3   10 -8   6 ]*1e-5;  
r.config.multipoles.families.bends.sys.skew_values = [0.0 0.0 0.0 0.0 0.0]; 
r.config.multipoles.families.bends.rms.order       = [ 3   4   5   6   7   8   9 ];
r.config.multipoles.families.bends.rms.main_values = 0*ones(1,7)*4e-5;
r.config.multipoles.families.bends.rms.skew_values = 0*ones(1,7)*1e-5;

%% Dynamic

r.config.dynamic.cutoff_errors = 1;

%erros dinâmicos, de vibracao e ripple
r.config.dynamic.families.quads.sigma_x      = 5 * nm * 1;
r.config.dynamic.families.sexts.sigma_x      = 5 * nm * 1;
r.config.dynamic.families.bends.sigma_x      = 5 * nm * 1;
r.config.dynamic.families.cbend.sigma_x      = 5 * nm * 1;

r.config.dynamic.families.quads.sigma_y      = 5 * nm * 1;
r.config.dynamic.families.sexts.sigma_y      = 5 * nm * 1;
r.config.dynamic.families.bends.sigma_y      = 5 * nm * 1;
r.config.dynamic.families.cbend.sigma_y      = 5 * nm * 1;
% 
% r.config.dynamic.families.quads.sigma_roll   = 2 * urad * 1;
% r.config.dynamic.families.sexts.sigma_roll   = 2 * urad * 1;
% r.config.dynamic.families.bends.sigma_roll   = 2 * urad * 1;
% r.config.dynamic.families.cbend.sigma_roll   = 2 * urad * 1;

% r.config.dynamic.families.quads.sigma_yaw    = 10 * urad * 0;
% r.config.dynamic.families.sexts.sigma_yaw    = 10 * urad * 0;
% r.config.dynamic.families.bends.sigma_yaw    =  5 * urad * 0;
% r.config.dynamic.families.cbend.sigma_yaw    = 10 * urad * 0;
% 
% r.config.dynamic.families.quads.sigma_pitch  = 10 * urad * 0;
% r.config.dynamic.families.sexts.sigma_pitch  = 10 * urad * 0;
% r.config.dynamic.families.bends.sigma_pitch  =  5 * urad * 0;
% r.config.dynamic.families.cbend.sigma_pitch  = 10 * urad * 0;

% r.config.dynamic.families.quads.sigma_e      = 5 * ppm * 1;
% r.config.dynamic.families.sexts.sigma_e      = 5 * ppm * 1;
% r.config.dynamic.families.bends.sigma_e      = 5 * ppm * 1;
% r.config.dynamic.families.cbend.sigma_e      = 5 * ppm * 1;
% r.config.dynamic.families.bends.sigma_e_kdip = 1 * ppm * 1;

% definicao de família para erros dinâmicos
r.config.dynamic.families.quads.labels = {'qaf','qbd2','qbf','qbd1','qad','qf1','qf2','qf3','qf4'};
r.config.dynamic.families.quads.nrsegs = ones(1,9);
r.config.dynamic.families.sexts.labels = {'sa1','sb1','sd2','sf2','sb2','sd1','sf1','sa2','sd3'};
r.config.dynamic.families.sexts.nrsegs = ones(1, 9);
r.config.dynamic.families.bends.labels = {'b1','b2','b3'};
r.config.dynamic.families.bends.nrsegs = [2 2 2];
r.config.dynamic.families.cbend.labels = {'bc'};
r.config.dynamic.families.cbend.nrsegs = 2;

% os erros estáticos e dinâmicos dos bpms tem interpretacao diferente dos
% erros dos outros elementos. Eles medem o erro do bpm em relação à orbita
% para a qual estamos corrigindo. Assim, no caso de correcao para a orbita
% bba, o erro estático mede o erro do método de bba, enquanto o erro
% dinâmico mede a única, verdadeira e absoluta vibraçao do bpm.
r.config.dynamic.families.bpm.labels = {'BPM'};
r.config.dynamic.families.bpm.nrsegs = 1;
r.config.dynamic.families.bpm.sigma_y    = 120 * nm * 1;
r.config.dynamic.families.bpm.sigma_x    = 120 * nm * 1;


r.config.dynamic.girder.girder_error_flag = true;
r.config.dynamic.girder.correlated_errors = true;
r.config.dynamic.girder.sigma_x     = 10 * nm * 1;
r.config.dynamic.girder.sigma_y     = 10 * nm * 1;
% r.config.dynamic.girder.sigma_roll  =  2 * urad * 1;
% r.config.dynamic.girder.sigma_yaw   =  2 * urad * 0;
% r.config.dynamic.girder.sigma_pitch =  2 * urad * 0;


% definicao de parametros para a correcao de orbita rapida
selection = [1 0 0 0  1 1  0 0 0 1];
selection = repmat(selection, 1, 20);
r.params.dynamic.bpm_idx = findcells(r.params.the_ring, 'FamName', 'BPM');
r.params.dynamic.bpm_idx = r.params.dynamic.bpm_idx(logical(selection(2:(end-1))));

selection = [1 1 1 1];
selection = repmat(selection, 1, 20);
r.params.dynamic.hcm_idx = findcells(r.params.the_ring, 'FamName', 'crhv');
r.params.dynamic.hcm_idx = r.params.dynamic.hcm_idx(logical(selection(2:(end-1))));

selection = [1 1 1 1];
selection = repmat(selection, 1, 20);
r.params.dynamic.vcm_idx = findcells(r.params.the_ring, 'FamName', 'crhv');
r.params.dynamic.vcm_idx = r.params.dynamic.vcm_idx(logical(selection(2:(end-1))));

r.params.dynamic.cod_correction_flag = true;
r.config.dynamic.calc_respm_cod_each_machine = true;
r.params.dynamic.cod_svs        = 20:20:160;
r.params.dynamic.cod_nr_iter    = 3;

