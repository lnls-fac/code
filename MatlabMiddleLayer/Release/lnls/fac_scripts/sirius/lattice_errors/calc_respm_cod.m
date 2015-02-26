function r = calc_respm_cod(the_ring, bpm_idx, hcm_idx, vcm_idx, nper, no_print)

if ~exist('no_print','var'), no_print=false; end
if ~exist('nper','var'), nper=1;end

if no_print, fprintf(['--- calc_cod_respm [' datestr(now) '] ---\n']); end;

step_kick = 0.00001;

if no_print
    fprintf('nr bpms: %03i\n', length(bpm_idx));
    fprintf('nr hcms: %03i\n', length(hcm_idx));
    fprintf('nr vcms: %03i\n', length(vcm_idx));
end

Mxx = zeros(length(bpm_idx), length(hcm_idx));
Myx = zeros(length(bpm_idx), length(hcm_idx));
Mxy = zeros(length(bpm_idx), length(vcm_idx));
Myy = zeros(length(bpm_idx), length(vcm_idx));

len_bpm = length(bpm_idx)/nper;
len_hcm = length(hcm_idx)/nper;
len_vcm = length(vcm_idx)/nper;
if any(logical(mod([len_bpm,len_hcm,len_vcm],1))), 
    len_bpm = len_bpm*nper;
    len_hcm = len_hcm*nper;
    len_vcm = len_vcm*nper;
    nper = 1;
else
    hcm_idx = hcm_idx(1:len_hcm);
    vcm_idx = vcm_idx(1:len_vcm);
end


% if no_print, lnls_create_waitbar('Calcs H-COD Response Matrix',0.5,len_hcm); end
% for i=1:len_hcm
%     idx = hcm_idx(i);
%     init_hkick = lnls_get_kickangle(the_ring, idx, 'x');
%     the_ring = lnls_set_kickangle(the_ring, init_hkick - 0.5* step_kick, idx, 'x');
%     [codx1, cody1] = calc_cod(the_ring);
%     the_ring = lnls_set_kickangle(the_ring, init_hkick + 0.5* step_kick, idx, 'x');
%     [codx2, cody2] = calc_cod(the_ring);
%     the_ring = lnls_set_kickangle(the_ring, init_hkick, idx, 'x');
%     mxx(:,i) = (codx2(bpm_idx) - codx1(bpm_idx)) / step_kick;
%     myx(:,i) = (cody2(bpm_idx) - cody1(bpm_idx)) / step_kick;
%     if no_print, lnls_update_waitbar(i); end
% end
% if no_print, lnls_delete_waitbar; end
% if no_print, lnls_create_waitbar('Calcs V-COD Response Matrix',0.5,len_vcm); end
% for i=1:len_vcm
%     idx = vcm_idx(i);
%     init_vkick = lnls_get_kickangle(the_ring, idx, 'y');
%     the_ring = lnls_set_kickangle(the_ring, init_vkick - 0.5* step_kick, idx, 'y');
%     [codx1, cody1] = calc_cod(the_ring);
%     the_ring = lnls_set_kickangle(the_ring, init_vkick + 0.5* step_kick, idx, 'y');
%     [codx2, cody2] = calc_cod(the_ring);
%     the_ring = lnls_set_kickangle(the_ring, init_vkick, idx, 'y');
%     mxy(:,i) = (codx2(bpm_idx) - codx1(bpm_idx)) / step_kick;
%     myy(:,i) = (cody2(bpm_idx) - cody1(bpm_idx)) / step_kick;
%     if no_print, lnls_update_waitbar(i); end
% end
% if no_print, lnls_delete_waitbar; end

M = get_response_matrix(the_ring, bpm_idx, hcm_idx, vcm_idx);
M = mat2cell(M, [length(bpm_idx),length(bpm_idx)],[len_hcm, len_vcm]);
mxx = M{1,1};
mxy = M{1,2};
myx = M{2,1};
myy = M{2,2};

for i=0:(nper-1)
    indcs = (i*len_hcm+1):((i+1)*len_hcm);
    Mxx(:,indcs) = circshift(mxx,len_bpm*i);
    Myx(:,indcs) = circshift(myx,len_bpm*i);

    indcs = (i*len_vcm+1):((i+1)*len_vcm);
    Mxy(:,indcs) = circshift(mxy,len_bpm*i); %the last bpm turns into the first
    Myy(:,indcs) = circshift(myy,len_bpm*i);
end

r.respm.mxx = Mxx;
r.respm.mxy = Mxy;
r.respm.myx = Myx;
r.respm.myy = Myy;

[U,S,V] = svd([Mxx Mxy; Myx Myy],'econ');
r.respm.U = U;
r.respm.V = V;
r.respm.S = S;

if no_print
    fprintf('singular values of X+Y cod response matrix:\n');
    for i=1:size(S,1)
        fprintf('%9.2E ', S(i,i));
        if rem(i,10) == 0, fprintf('\n'); end;
    end
    fprintf('\n');
    fprintf('\n');
end

