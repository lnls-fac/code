function respm = calc_respm_cod(the_ring, bpm_idx, hcm_idx, vcm_idx, no_print)

if ~exist('no_print','var'), print=true; else print=false; end

if print, fprintf(['--- calc_cod_respm [' datestr(now) '] ---\n']); end;

step_kick = 0.00001;

if print
    fprintf('nr bpms: %03i\n', length(bpm_idx));
    fprintf('nr hcms: %03i\n', length(hcm_idx));
    fprintf('nr vcms: %03i\n', length(vcm_idx));
end

mxx = zeros(length(bpm_idx), length(hcm_idx));
myx = zeros(length(bpm_idx), length(hcm_idx));
lnls_create_waitbar('Calcs H-COD Response Matrix',0.5,length(hcm_idx));
for i=1:length(hcm_idx)
    idx = hcm_idx(i);
    the_ring{idx}.KickAngle = the_ring{idx}.KickAngle - 0.5 * [step_kick 0];
    [codx1 cody1] = calc_cod(the_ring);
    the_ring{idx}.KickAngle = the_ring{idx}.KickAngle + 1.0 * [step_kick 0];
    [codx2 cody2] = calc_cod(the_ring);
    the_ring{idx}.KickAngle = the_ring{idx}.KickAngle - 0.5 * [step_kick 0];
    mxx(:,i) = (codx2(bpm_idx) - codx1(bpm_idx)) / step_kick;
    myx(:,i) = (cody2(bpm_idx) - cody1(bpm_idx)) / step_kick;
    lnls_update_waitbar(i);
end
lnls_delete_waitbar;

mxy = zeros(length(bpm_idx), length(vcm_idx));
myy = zeros(length(bpm_idx), length(vcm_idx));
lnls_create_waitbar('Calcs V-COD Response Matrix',0.5,length(vcm_idx));
for i=1:length(vcm_idx)
    idx = vcm_idx(i);
    the_ring{idx}.KickAngle = the_ring{idx}.KickAngle - 0.5 * [0 step_kick];
    [codx1 cody1] = calc_cod(the_ring);
    the_ring{idx}.KickAngle = the_ring{idx}.KickAngle + 1.0 * [0 step_kick];
    [codx2 cody2] = calc_cod(the_ring);
    the_ring{idx}.KickAngle = the_ring{idx}.KickAngle - 0.5 * [0 step_kick];
    mxy(:,i) = (codx2(bpm_idx) - codx1(bpm_idx)) / step_kick;
    myy(:,i) = (cody2(bpm_idx) - cody1(bpm_idx)) / step_kick;
    lnls_update_waitbar(i);
end
lnls_delete_waitbar;

[U,S,V] = svd([mxx mxy; myx myy],'econ');
respm.mxx = mxx;
respm.mxy = mxy;
respm.myx = myx;
respm.myy = myy;
respm.U = U;
respm.V = V;
respm.S = S;

if print
    fprintf('singular values of X+Y cod response matrix:\n');
    for i=1:size(S,1)
        fprintf('%9.2E ', S(i,i));
        if rem(i,10) == 0, fprintf('\n'); end;
    end
    fprintf('\n');
    fprintf('\n');
end

