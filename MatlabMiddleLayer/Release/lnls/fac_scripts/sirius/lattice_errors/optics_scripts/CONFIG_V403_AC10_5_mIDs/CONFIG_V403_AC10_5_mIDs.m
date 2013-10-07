function r = CONFIG_V403_AC10_5_mIDs

r.config.label = 'CONFIG_V403_AC10_5_mIDs';

%% constants
um       = 1e-6;
nm       = 1e-9;
mrad     = 0.001;
percent  = 0.01;

%% errors specification

r.config.lattice_function  = @sirius_lattice;
r.config.lattice_func_arg  = 'AC10';
%r.config.lattice_function  = 'thering_withids.mat';
r.config.cutoff_errors = 1;
r.config.errors_delta  = [1.0];

r.config.nr_machines       = 10;

r.config.families.quads.sigma_x      = 30 * um * 1;
r.config.families.sexts.sigma_x      = 30 * um * 1;
r.config.families.sexts_bba.sigma_x  = 30 * um * 1;
r.config.families.bends.sigma_x      = 30 * um * 1;
r.config.families.cbend.sigma_x      = 30 * um * 1;

r.config.families.quads.sigma_y      = 30 * um * 1;
r.config.families.sexts.sigma_y      = 30 * um * 1;
r.config.families.sexts_bba.sigma_y  = 30 * um * 1;
r.config.families.bends.sigma_y      = 30 * um * 1;
r.config.families.cbend.sigma_y      = 30 * um * 1;

r.config.families.quads.sigma_roll     = 0.20 * mrad * 1;
r.config.families.sexts.sigma_roll     = 0.20 * mrad * 1;
r.config.families.sexts_bba.sigma_roll = 0.20 * mrad * 1;
r.config.families.bends.sigma_roll     = 0.20 * mrad * 1;
r.config.families.cbend.sigma_roll     = 0.20 * mrad * 1;

r.config.families.quads.sigma_yaw     = 0.10 * mrad * 0;
r.config.families.sexts.sigma_yaw     = 0.10 * mrad * 0;
r.config.families.sexts_bba.sigma_yaw = 0.10 * mrad * 0;
r.config.families.bends.sigma_yaw     = 0.05 * mrad * 0;
r.config.families.cbend.sigma_yaw     = 0.10 * mrad * 0;

r.config.families.quads.sigma_pitch     = 0.10 * mrad * 0;
r.config.families.sexts.sigma_pitch     = 0.10 * mrad * 0;
r.config.families.sexts_bba.sigma_pitch = 0.10 * mrad * 0;
r.config.families.bends.sigma_pitch     = 0.05 * mrad * 0;
r.config.families.cbend.sigma_pitch     = 0.10 * mrad * 0;

r.config.families.quads.sigma_e      = 0.05 * percent * 1;
r.config.families.sexts.sigma_e      = 0.05 * percent * 1;
r.config.families.sexts_bba.sigma_e  = 0.05 * percent * 1;
r.config.families.bends.sigma_e      = 0.05 * percent * 1;
r.config.families.cbend.sigma_e      = 0.05 * percent * 1;
r.config.families.bends.sigma_e_kdip = 0.50 * percent * 0;

r.config.families.quads.labels = {'qaf','qbd2','qbf','qbd1','qad','qf1','qf2','qf3','qf4'};
r.config.families.quads.nrsegs = ones(1,9);
r.config.families.sexts.labels = {'sa1','sb1','sd2','sf2','sb2'};
r.config.families.sexts.nrsegs = ones(1, 5);
r.config.families.sexts_bba.labels = {'sd1','sf1','sa2','sd3'};
r.config.families.sexts_bba.nrsegs = ones(1, 4);
r.config.families.bends.labels = {'b1','b2','b3'};
r.config.families.bends.nrsegs = [2 2 2];
r.config.families.cbend.labels = {'bc'};
r.config.families.cbend.nrsegs = 2;

%% loads ring nominal AT model
if ischar(r.config.lattice_function)
    data = load(r.config.lattice_function);
    r.params.the_ring = data.thering;
else
    r.params.the_ring = r.config.lattice_function(r.config.lattice_func_arg);
end


%% parameters for correction algorithms

selection = [1 1 1 1  1 1  1 1 1 1];
selection = repmat(selection, 1, 20);
r.params.bpm_idx = findcells(r.params.the_ring, 'FamName', 'BPM');
r.params.bpm_idx = r.params.bpm_idx(logical(selection));

selection = [1 1 1 1   1 1 1 1];
selection = repmat(selection, 1, 20);
r.params.hcm_idx = findcells(r.params.the_ring, 'FamName', 'hcm');
r.params.hcm_idx = r.params.hcm_idx(logical(selection));

selection = [1 1 1   1 1 1];
selection = repmat(selection, 1, 20);
r.params.vcm_idx = findcells(r.params.the_ring, 'FamName', 'vcm');
r.params.vcm_idx = r.params.vcm_idx(logical(selection));

r.params.scm_idx = [];
r.params.scm_idx = [r.params.scm_idx findcells(r.params.the_ring, 'FamName', 'sa2')];
r.params.scm_idx = [r.params.scm_idx findcells(r.params.the_ring, 'FamName', 'sb2')];
% r.params.scm_idx = [r.params.scm_idx findcells(r.params.the_ring, 'FamName', 'sa1')];
% r.params.scm_idx = [r.params.scm_idx findcells(r.params.the_ring, 'FamName', 'sd1')];
% r.params.scm_idx = [r.params.scm_idx findcells(r.params.the_ring, 'FamName', 'sf1')];
% r.params.scm_idx = [r.params.scm_idx findcells(r.params.the_ring, 'FamName', 'sd2')];
% r.params.scm_idx = [r.params.scm_idx findcells(r.params.the_ring, 'FamName', 'sd3')];
% r.params.scm_idx = [r.params.scm_idx findcells(r.params.the_ring, 'FamName', 'sf2')];
% r.params.scm_idx = [r.params.scm_idx findcells(r.params.the_ring, 'FamName', 'sb1')];

r.params.kbs_idx = findcells(r.params.the_ring, 'K');
r.params.kbs_idx = setdiff(r.params.kbs_idx, findcells(r.params.the_ring, 'BendingAngle'));

r.params.cod_correction_flag = true;
r.params.cod_sextupoles_ramp = [0 1];
r.params.cod_svs        = 120;
r.params.cod_nr_iter    = 3;

r.params.coup_correction_flag = false;
%r.params.coup_svs       = [100:50:250 280];
%r.params.coup_svs       = [20 30 40];
r.params.coup_svs       = 'all';
r.params.coup_nr_iter   = 3;

r.params.optics_correction_flag = false;
r.params.optics_svs     = 180:20:260;
r.params.optics_nr_iter = 2; 
r.params.coup_residual  = 0.5 / 100;

r.params.ripple_flag = false;
