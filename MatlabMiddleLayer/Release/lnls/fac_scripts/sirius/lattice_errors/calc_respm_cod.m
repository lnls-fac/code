function r = calc_respm_cod(the_ring, bpm_idx, hcm_idx, vcm_idx, no_print)

if ~exist('no_print','var'), print=true; else print=false; end

if print, fprintf(['--- calc_cod_respm [' datestr(now) '] ---\n']); end;

step_kick = 0.00001;

if print
    fprintf('nr bpms: %03i\n', length(bpm_idx));
    fprintf('nr hcms: %03i\n', length(hcm_idx));
    fprintf('nr vcms: %03i\n', length(vcm_idx));
end

% twiss = calctwiss(the_ring); %
% betax = twiss.betax';%
% betay = twiss.betay';%

mxx = zeros(length(bpm_idx), length(hcm_idx));
myx = zeros(length(bpm_idx), length(hcm_idx));
if print, lnls_create_waitbar('Calcs H-COD Response Matrix',0.5,length(hcm_idx)); end
for i=1:length(hcm_idx)
    idx = hcm_idx(i);
    the_ring{idx}.KickAngle = the_ring{idx}.KickAngle - 0.5 * [step_kick 0];
    [codx1 cody1] = calc_cod(the_ring);
%     codx1 = codx1./sqrt(betax);%
%     cody1 = cody1./sqrt(betay);%
    the_ring{idx}.KickAngle = the_ring{idx}.KickAngle + 1.0 * [step_kick 0];
    [codx2 cody2] = calc_cod(the_ring);
%     codx2 = codx2./sqrt(betax);%
%     cody2 = cody2./sqrt(betay);%
    the_ring{idx}.KickAngle = the_ring{idx}.KickAngle - 0.5 * [step_kick 0];
    mxx(:,i) = (codx2(bpm_idx) - codx1(bpm_idx)) / step_kick;
    myx(:,i) = (cody2(bpm_idx) - cody1(bpm_idx)) / step_kick;
    if print, lnls_update_waitbar(i); end
end
if print, lnls_delete_waitbar; end

mxy = zeros(length(bpm_idx), length(vcm_idx));
myy = zeros(length(bpm_idx), length(vcm_idx));
if print, lnls_create_waitbar('Calcs V-COD Response Matrix',0.5,length(vcm_idx)); end
for i=1:length(vcm_idx)
    idx = vcm_idx(i);
    the_ring{idx}.KickAngle = the_ring{idx}.KickAngle - 0.5 * [0 step_kick];
    [codx1 cody1] = calc_cod(the_ring);
    the_ring{idx}.KickAngle = the_ring{idx}.KickAngle + 1.0 * [0 step_kick];
    [codx2 cody2] = calc_cod(the_ring);
    the_ring{idx}.KickAngle = the_ring{idx}.KickAngle - 0.5 * [0 step_kick];
    mxy(:,i) = (codx2(bpm_idx) - codx1(bpm_idx)) / step_kick;
    myy(:,i) = (cody2(bpm_idx) - cody1(bpm_idx)) / step_kick;
    if print, lnls_update_waitbar(i); end
end
if print, lnls_delete_waitbar; end

[U,S,V] = svd([mxx mxy; myx myy],'econ');
r.respm.mxx = mxx;
r.respm.mxy = mxy;
r.respm.myx = myx;
r.respm.myy = myy;
r.respm.U = U;
r.respm.V = V;
r.respm.S = S;

if print
    fprintf('singular values of X+Y cod response matrix:\n');
    for i=1:size(S,1)
        fprintf('%9.2E ', S(i,i));
        if rem(i,10) == 0, fprintf('\n'); end;
    end
    fprintf('\n');
    fprintf('\n');
end

