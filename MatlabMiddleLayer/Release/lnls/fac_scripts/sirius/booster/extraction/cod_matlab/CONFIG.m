function r = CONFIG

r.config.label = 'CONFIG';

%% constants
um       = 1e-6;
mrad     = 0.001;
percent  = 0.01;

%% errors specification

r.config.lattice_function  = @sirius_booster_lattice;
% r.config.lattice_func_arg  = [];
r.config.nr_machines       = 50;
r.config.cutoff_errors     = 2;
r.config.errors_delta      = 1;

r.config.families.quads.sigma_x      = 100 * um * 1;
r.config.families.sexts.sigma_x      = 100 * um * 1;
r.config.families.bends.sigma_x      = 100 * um * 1;

r.config.families.quads.sigma_y      = 100 * um * 1;
r.config.families.sexts.sigma_y      = 100 * um * 1;
r.config.families.bends.sigma_y      = 100 * um * 1;

r.config.families.quads.sigma_roll   = 0.50 * mrad * 1;
r.config.families.sexts.sigma_roll   = 0.50 * mrad * 1;
r.config.families.bends.sigma_roll   = 0.50 * mrad * 1;

%para determinar erros de yaw e pitch tomei por base o deslocamento do
%extremo do elemento em relacao a posicao ideal.
r.config.families.quads.sigma_yaw    = 0.70 * mrad * 0;
r.config.families.sexts.sigma_yaw    = 1.50 * mrad * 0;
r.config.families.bends.sigma_yaw    = 0.20 * mrad * 0;

r.config.families.quads.sigma_pitch  = 0.70 * mrad * 0;
r.config.families.sexts.sigma_pitch  = 1.50 * mrad * 0;
r.config.families.bends.sigma_pitch  = 0.20 * mrad * 0;

r.config.families.quads.sigma_e      = 0.2 * percent * 1;
r.config.families.sexts.sigma_e      = 0.2 * percent * 1;
r.config.families.bends.sigma_e      = 0.1 * percent * 1;
r.config.families.bends.sigma_e_kdip = 0.50 * percent * 1;

r.config.families.quads.labels = {'QD','QF'};
r.config.families.quads.nrsegs = [1 2];
r.config.families.sexts.labels = {'SD','SF'};
r.config.families.sexts.nrsegs = ones(1, 2);
r.config.families.bends.labels = {'B'};
r.config.families.bends.nrsegs = 3;

%% loads ring nominal AT model
% r.params.the_ring = r.config.lattice_function(r.config.lattice_func_arg);
r.params.the_ring = r.config.lattice_function();


%% parameters for correction algorithms

bpm_idx = findcells(r.params.the_ring, 'FamName', 'BPM');
select = [1 1 1 1 1 1 1 1 1 1]; select = repmat(select,1,5);
r.params.bpm_idx = bpm_idx(logical(select));

hcm_idx = findcells(r.params.the_ring, 'FamName', 'HCM');
select = [1 1 1 1 1]; select = repmat(select,1,5);
r.params.hcm_idx = hcm_idx(logical(select));

vcm_idx = findcells(r.params.the_ring, 'FamName', 'VCM');
select = [1 1 1 1 1]; select = repmat(select,1,5);
r.params.vcm_idx = vcm_idx(logical(select));

r.params.ele_idx = 1:length(r.params.the_ring);
% r.params.scm_idx = [];
% r.params.scm_idx = [r.params.scm_idx findcells(r.params.the_ring, 'FamName', 'sa2')];
% r.params.scm_idx = [r.params.scm_idx findcells(r.params.the_ring, 'FamName', 'sd2')];
% r.params.kbs_idx = findcells(r.params.the_ring, 'K');
% r.params.kbs_idx = setdiff(r.params.kbs_idx, findcells(r.params.the_ring, 'BendingAngle'));

r.params.cod_correction_flag = true;
r.params.cod_sextupoles_ramp = [0 1];
r.params.cod_svs        = 20:10:50;
r.params.cod_nr_iter    = 3;
r.params.coup_correction_flag = false;
r.params.coup_svs       = 20:20:60;
r.params.coup_nr_iter   = 3;
r.params.optics_correction_flag = false;
r.params.optics_svs     = 180:20:260;
r.params.optics_nr_iter = 2;  
r.params.ripple_flag    = false;

