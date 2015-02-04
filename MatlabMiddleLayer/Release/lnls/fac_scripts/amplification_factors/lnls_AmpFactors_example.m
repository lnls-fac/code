function res = lnls_AmpFactors_example(the_ring, name)
% function res = lnls_AmpFactors_example(the_ring, name)
%
% Calculates amplification factors for magnets, bpms and girders for the
% lattice the_ring.
% The user must make a local copy of this function in the working directory
% and change the parameters within it to use.
% A folder with the configuration name defined through the variable "name"
% will be created in the working directory and the a copy of the output of
% this function will be saved as a .mat file inside this folder.
% the output is the correct format to be used in the function
% lnls_AmpFactors_make_figures(res) for visualization of the data.
%
% See also lnls_AmpFactors_make_figures lnls_mag_amp_factors
% lnls_bpms_amp_factors lnls_girder_amp_factors
% lnls_AmpFactors_make_txtSummary


mia = findcells(the_ring,'FamName','mia');
mib = findcells(the_ring,'FamName','mib');
mc  = findcells(the_ring,'FamName','mc');

res.name = name;
%Parameters for slow orbit amplification factor calculations
res.slow.mis_err = 30e-6;
res.slow.rot_err = 0.1e-3;
res.slow.exc_err = 1e-4;
res.slow.the_ring = the_ring;
res.slow.symmetry = 20;

res.slow.where2calclabels = {'all'};
res.slow.where2calc = {1:length(the_ring)};

res.slow.cod_cor.bpm_idx = findcells(the_ring,'FamName','bpm');
res.slow.cod_cor.hcm_idx = findcells(the_ring,'FamName','hcm');
res.slow.cod_cor.vcm_idx = findcells(the_ring,'FamName','vcm');
res.slow.cod_cor.cod_respm = calc_respm_cod(the_ring, res.slow.cod_cor.bpm_idx,...
                            res.slow.cod_cor.hcm_idx, res.slow.cod_cor.vcm_idx);
res.slow.cod_cor.cod_respm = res.slow.cod_cor.cod_respm.respm;
res.slow.cod_cor.nr_sv = 280;
res.slow.cod_cor.nr_iter = 3;

res.slow.labels = {'qfa','qdb2','qfb','qdb1','qda','qf1','qf2','qf3','qf4', ...
    'sda','sfa','sd1','sf1','sd2','sd3','sf2','sf3','sd4','sd5','sf4','sd6','sdb','sfb', ...
                                                              'b1','b2','b3','bc'};
res.slow.nrsegs = [ones(1,9), ...
                   ones(1, 14),...
                   [2 2 2 2]];

res.slow.results.bpm       = lnls_bpms_amp_factors(res.slow);
res.slow.results.mags      = lnls_mag_amp_factors(res.slow);
res.slow.results.girder_on = lnls_girder_amp_factors(res.slow, true);

%fast orbit correction system
res.fast = res.slow;
res.fast.where2calclabels = {'mia','mib','mc'};
res.fast.where2calc = {mia, mib, mc};
res.fast.cod_cor.bpm_idx = res.slow.cod_cor.bpm_idx(logical(repmat([1,0,0,0,1,1,0,0,1],1,20)));
res.fast.cod_cor.hcm_idx = findcells(the_ring,'FamName','crhv');
res.fast.cod_cor.vcm_idx = res.fast.cod_cor.hcm_idx;
res.fast.cod_cor.cod_respm = calc_respm_cod(the_ring, res.fast.cod_cor.bpm_idx,...
                            res.fast.cod_cor.hcm_idx, res.fast.cod_cor.vcm_idx);
res.fast.cod_cor.cod_respm = res.fast.cod_cor.cod_respm.respm;
res.fast.cod_cor.nr_sv = 160;
res.fast.cod_cor.nr_iter = 3;

res.fast.results.mags       = lnls_mag_amp_factors(res.fast);
res.fast.results.bpm        = lnls_bpms_amp_factors(res.fast);
res.fast.results.girder_off = lnls_girder_amp_factors(res.fast, false);


% Without Correction
res.wocor = res.slow;
res.wocor = rmfield(res.wocor,{'cod_cor','results'});
res.wocor.where2calclabels = {'all','mia','mib','mc'};
res.wocor.where2calc = {1:length(the_ring), mia, mib, mc};

res.wocor.results.mags   = lnls_mag_amp_factors(res.wocor);
res.wocor.results.girder = lnls_girder_amp_factors(res.wocor, true);

%% Save results

try
    cd(name);
catch
    mkdir(name);
    cd(name);
end

save([name '.mat'],'res');

cd('..');
