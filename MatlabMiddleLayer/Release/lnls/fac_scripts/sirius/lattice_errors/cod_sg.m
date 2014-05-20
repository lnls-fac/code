function [the_ring hkicks vkicks codx cody] = cod_sg(params, nr_sing_values, the_ring0, nr_iterations, goal_codx, goal_cody)

the_ring = the_ring0;

S = params.cod_respm.S;
U = params.cod_respm.U;
V = params.cod_respm.V;

% selection of singular values
iS = diag(1./diag(S));
diS = diag(iS);
diS(nr_sing_values+1:end) = 0;
iS = diag(diS);
CM = -(V*iS*U');

for k=1:nr_iterations
    % calcs kicks
    [codx cody] = calc_cod(the_ring);
    delta_kick = CM * [codx(params.bpm_idx)' - goal_codx(:); cody(params.bpm_idx)' - goal_cody(:)];
    % sets kicks
    delt_hkicks = delta_kick(1:length(params.hcm_idx));
    delt_vkicks = delta_kick((1+length(params.hcm_idx)):end);
    init_hkicks = getcellstruct(the_ring, 'KickAngle', params.hcm_idx, 1, 1);
    init_vkicks = getcellstruct(the_ring, 'KickAngle', params.vcm_idx, 1, 2);
    tota_hkicks = init_hkicks + delt_hkicks;
    tota_vkicks = init_vkicks + delt_vkicks;
    the_ring = setcellstruct(the_ring, 'KickAngle', params.hcm_idx, tota_hkicks, 1, 1);
    the_ring = setcellstruct(the_ring, 'KickAngle', params.vcm_idx, tota_vkicks, 1, 2);
end
hkicks = getcellstruct(the_ring, 'KickAngle', params.hcm_idx, 1, 1);
vkicks = getcellstruct(the_ring, 'KickAngle', params.vcm_idx, 1, 2);
[codx cody] = calc_cod(the_ring);