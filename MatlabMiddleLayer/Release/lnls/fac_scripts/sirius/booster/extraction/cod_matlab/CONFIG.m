function r = CONFIG

r.config.label = 'CONFIG';
r.question = false;

%% constants
um       = 1e-6;
nm       = 1e-9;
mrad     = 0.001;
urad     = 1e-6;
percent  = 0.01;
ppm      = 1e-6;

%% errors specification

r.config.lattice_function  = @sirius_booster_lattice;
% r.config.lattice_func_arg  = [];

r.params.the_ring = r.config.lattice_function();


r.config.nr_machines       = 20;
r.config.simulate_static  = true;
r.config.simulate_dynamic = false;

%se verdadeiro, a órbita de referência será uma simulação do processo de
%bba. Atualmente, pegamos a orbita nos quadrupolos mais proximos ao bpm e
%atribuimos o deslocamento no centro do quadrupolo como sendo a orbita bba
%no bpm. O erro estático do bpm representa a precisao do 'bba'.
r.params.correct2bba_orbit = false;


%% Static
r.config.static.cutoff_errors = 2;
r.config.static.errors_delta  = 1.0;

r.config.static.families.bends.sigma_x      = 100 * um * 1;
r.config.static.families.quads.sigma_x      = 100 * um * 1;
r.config.static.families.sexts.sigma_x      = 100 * um * 1;

r.config.static.families.sexts.sigma_y      = 100 * um * 1;
r.config.static.families.quads.sigma_y      = 100 * um * 1;
r.config.static.families.bends.sigma_y      = 100 * um * 1;

r.config.static.families.sexts.sigma_roll   = 0.50 * mrad * 1;
r.config.static.families.quads.sigma_roll   = 0.50 * mrad * 1;
r.config.static.families.bends.sigma_roll   = 0.50 * mrad * 1;


%para determinar erros de yaw e pitch tomei por base o deslocamento do
%extremo do elemento em relacao a posicao ideal.
% r.config.static.families.quads.sigma_yaw    = 0.70 * mrad * 0;
% r.config.static.families.sexts.sigma_yaw    = 1.50 * mrad * 0;
% r.config.static.families.bends.sigma_yaw    = 0.20 * mrad * 0;
% 
% r.config.static.families.quads.sigma_pitch  = 0.70 * mrad * 0;
% r.config.static.families.sexts.sigma_pitch  = 1.50 * mrad * 0;
% r.config.static.families.bends.sigma_pitch  = 0.20 * mrad * 0;

r.config.static.families.quads.sigma_e      = 0.2 * percent * 1;
r.config.static.families.sexts.sigma_e      = 0.2 * percent * 1;
r.config.static.families.bends.sigma_e      = 0.1 * percent * 1;
r.config.static.families.bends.sigma_e_kdip = 1.50 * percent * 1;

r.config.static.families.quads.labels = {'QD','QF'};
r.config.static.families.quads.nrsegs = [1 2];
r.config.static.families.sexts.labels = {'SD','SF'};
r.config.static.families.sexts.nrsegs = ones(1, 2);
r.config.static.families.bends.labels = {'B'};
r.config.static.families.bends.nrsegs = 14;


% os erros estáticos e dinâmicos dos bpms tem interpretacao diferente dos
% erros dos outros elementos. Eles medem o erro do bpm em relação à orbita
% para a qual estamos corrigindo. Assim, no caso de correcao para a orbita
% bba, o erro estático mede o erro do método de bba, enquanto o erro
% dinâmico mede a única, verdadeira e absoluta vibraçao do bpm.
r.config.static.families.bpm.labels = {'BPM'};
r.config.static.families.bpm.nrsegs = 1;
r.config.static.families.bpm.sigma_y    = 100 * um * 1;
r.config.static.families.bpm.sigma_x    = 100 * um * 1;


r.config.static.girder.girder_error_flag = false;
r.config.static.girder.correlated_errors = false;
r.config.static.girder.sigma_x     = 100 * um * 1;
r.config.static.girder.sigma_y     = 100 * um * 1;
r.config.static.girder.sigma_roll  =  0.20 * mrad * 1;
% r.config.static.girder.sigma_yaw   =  20 * mrad * 0;
% r.config.static.girder.sigma_pitch =  20 * mrad * 0;


% parameters for slow correction algorithms

%cod
bpm_idx = findcells(r.params.the_ring, 'FamName', 'BPM');
select = [1 1 1 1 1 1 1 1 1 1]; select = repmat(select,1,5);
r.params.static.bpm_idx = bpm_idx(logical(select));

hcm_idx = findcells(r.params.the_ring, 'FamName', 'HCM');
select = [1 1 1 1 1]; select = repmat(select,1,5);
r.params.static.hcm_idx = hcm_idx(logical(select));

vcm_idx = findcells(r.params.the_ring, 'FamName', 'VCM');
select = [1 1 1 1 1]; select = repmat(select,1,5);
r.params.static.vcm_idx = vcm_idx(logical(select));

r.params.static.cod_correction_flag = true;
r.params.static.cod_sextupoles_ramp = [0 1];
r.params.static.cod_svs        = 20:10:50;
r.params.static.cod_nr_iter    = 3;

%coupling
r.params.static.coup_correction_flag = false;

%optics
r.params.static.optics_correction_flag = false;


%% Dynamic

r.config.dynamic.cutoff_errors = 2;

%erros dinâmicos, de vibracao e ripple
r.config.dynamic.families.quads.sigma_x      = 0.4 * um * 1;
r.config.dynamic.families.sexts.sigma_x      = 2.5 * um * 1;
r.config.dynamic.families.bends.sigma_x      = 2.5 * um * 1;

r.config.dynamic.families.quads.sigma_y      = 10 * um * 1;
r.config.dynamic.families.sexts.sigma_y      = 10 * um * 1;
r.config.dynamic.families.bends.sigma_y      =  8 * um * 1;

% r.config.dynamic.families.quads.sigma_roll   = 2 * urad * 1;
% r.config.dynamic.families.sexts.sigma_roll   = 2 * urad * 1;
% r.config.dynamic.families.bends.sigma_roll   = 2 * urad * 1;

% r.config.dynamic.families.quads.sigma_yaw    = 10 * urad * 0;
% r.config.dynamic.families.sexts.sigma_yaw    = 10 * urad * 0;
% r.config.dynamic.families.bends.sigma_yaw    =  5 * urad * 0;
 
% r.config.dynamic.families.quads.sigma_pitch  = 10 * urad * 0;
% r.config.dynamic.families.sexts.sigma_pitch  = 10 * urad * 0;
% r.config.dynamic.families.bends.sigma_pitch  =  5 * urad * 0;

% r.config.dynamic.families.quads.sigma_e      = 5 * ppm * 1;
% r.config.dynamic.families.sexts.sigma_e      = 5 * ppm * 1;
% r.config.dynamic.families.bends.sigma_e      = 5 * ppm * 1;
% r.config.dynamic.families.bends.sigma_e_kdip = 1 * ppm * 1;

% definicao de família para erros dinâmicos
r.config.dynamic.families.quads.labels = {'QD','QF'};
r.config.dynamic.families.quads.nrsegs = [1 2];
r.config.dynamic.families.sexts.labels = {'SD','SF'};
r.config.dynamic.families.sexts.nrsegs = ones(1, 2);
r.config.dynamic.families.bends.labels = {'B'};
r.config.dynamic.families.bends.nrsegs = 14;


% os erros estáticos e dinâmicos dos bpms tem interpretacao diferente dos
% erros dos outros elementos. Eles medem o erro do bpm em relação à orbita
% para a qual estamos corrigindo. Assim, no caso de correcao para a orbita
% bba, o erro estático mede o erro do método de bba, enquanto o erro
% dinâmico mede a única, verdadeira e absoluta vibraçao do bpm.
r.config.dynamic.families.bpm.labels = {'BPM'};
r.config.dynamic.families.bpm.nrsegs = 1;
r.config.dynamic.families.bpm.sigma_y    = 120 * nm * 1;
r.config.dynamic.families.bpm.sigma_x    = 120 * nm * 1;


r.config.dynamic.girder.girder_error_flag = false;
r.config.dynamic.girder.correlated_errors = false;
r.config.dynamic.girder.sigma_x     = 100 * nm * 1;
r.config.dynamic.girder.sigma_y     = 100 * nm * 1;
% r.config.dynamic.girder.sigma_roll  =  2 * urad * 1;
% r.config.dynamic.girder.sigma_yaw   =  2 * urad * 0;
% r.config.dynamic.girder.sigma_pitch =  2 * urad * 0;


% definicao de parametros para a correcao de orbita rapida
r.params.dynamic.cod_correction_flag = false;
