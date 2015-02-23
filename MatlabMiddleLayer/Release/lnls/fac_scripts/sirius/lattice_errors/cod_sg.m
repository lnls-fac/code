function [the_ring, hkicks, vkicks, codx, cody, iter, n_times] = cod_sg(params, nr_sing_values,...
                                    the_ring0, max_nr_iters, goal_codx, goal_cody, tolerancia)

if ~exist('goal_codx','var'), goal_codx = zeros(size(params.bpm_idx)); end
if ~exist('goal_cody','var'), goal_cody = zeros(size(params.bpm_idx)); end
if ~exist('tolerancia','var'), tolerancia = 1e-5; end
tolerancia = abs(tolerancia);

the_ring = the_ring0;

scale_x = 200e-6;
scale_y = 200e-6;

S = params.cod_respm.S;
U = params.cod_respm.U;
V = params.cod_respm.V;

corr_list = [params.hcm_idx, params.vcm_idx];

% selection of singular values
iS = diag(1./diag(S));
diS = diag(iS);
diS(nr_sing_values+1:end) = 0;
iS = diag(diS);
CM = -(V*iS*U');

[codx, cody] = calc_cod(the_ring);
best_fm = std([(codx(params.bpm_idx)-goal_codx)/scale_x, ...
               (cody(params.bpm_idx)-goal_cody)/scale_y]);
best_corr = the_ring(corr_list);
factor = 1;
n_times = 0;
for iter = 1:max_nr_iters
    % calcs kicks
    [codx, cody] = calc_cod(the_ring);
    delta_kick = factor*CM * [codx(params.bpm_idx)' - goal_codx(:);...
                              cody(params.bpm_idx)' - goal_cody(:)];
    % sets kicks
    delt_hkicks = delta_kick(1:length(params.hcm_idx))';
    delt_vkicks = factor*delta_kick((1+length(params.hcm_idx)):end)';
    init_hkicks = lnls_get_kickangle(the_ring, params.hcm_idx, 'x');
    init_vkicks = lnls_get_kickangle(the_ring, params.vcm_idx, 'y');
    tota_hkicks = init_hkicks + delt_hkicks;
    tota_vkicks = init_vkicks + delt_vkicks;
    the_ring = lnls_set_kickangle(the_ring, tota_hkicks, params.hcm_idx, 'x');
    the_ring = lnls_set_kickangle(the_ring, tota_vkicks, params.vcm_idx, 'y');
    [codx, cody] = calc_cod(the_ring);
    fm = std([(codx(params.bpm_idx)-goal_codx)/scale_x, ...
              (cody(params.bpm_idx)-goal_cody)/scale_y]);
    residue = abs(best_fm-fm)/best_fm;
    if (fm < best_fm)
        best_fm      = fm;
        best_corr    = the_ring(corr_list);
        factor = 1; % reset the correction strength to 1
    else
        the_ring(corr_list) = best_corr;
        factor = factor * 0.75; % reduces the strength of the correction
        n_times = n_times + 1; % to check how many times it passed here
    end
    % breaks the loop in case convergence is reached
    if residue < tolerancia
        break;
    end
end
hkicks = lnls_get_kickangle(the_ring, params.hcm_idx, 'x');
vkicks = lnls_get_kickangle(the_ring, params.vcm_idx, 'y');
[codx, cody] = calc_cod(the_ring);