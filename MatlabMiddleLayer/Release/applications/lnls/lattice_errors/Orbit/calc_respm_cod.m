function r = calc_respm_cod(the_ring, bpm_idx, hcm_idx, vcm_idx, nper, print)

if ~exist('print','var'), print=false; end
if ~exist('nper','var'), nper=1;end

if print, fprintf(['\nCalculating COD Response Matrix [' datestr(now) ']:\n']); end;

if print
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

