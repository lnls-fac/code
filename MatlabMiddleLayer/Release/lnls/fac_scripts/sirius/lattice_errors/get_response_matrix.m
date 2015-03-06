function M = get_response_matrix(the_ring, bpms, hcms, vcms)
% M(y,x) --> y : orbit    x: corrector

[M44, T] = findm44(the_ring,0,1:length(the_ring)+1);

len_hcms = length(hcms);
len_vcms = length(vcms);
len_bpms = length(bpms);

mxx = zeros(len_bpms, len_hcms);
myx = zeros(len_bpms, len_hcms);
mxy = zeros(len_bpms, len_vcms);
myy = zeros(len_bpms, len_vcms);

for i=1:len_bpms
    for j=1:len_hcms
        [cxx, cyx, ~, ~] = get_C(M44,T,bpms(i),hcms(j),the_ring{j}.Length);
        mxx(i,j) = cxx;
        myx(i,j) = cyx;
    end
    for j=1:len_vcms
        [~, ~, cxy, cyy] = get_C(M44,T,bpms(i),vcms(j),the_ring{j}.Length);
        mxy(i,j) = cxy;
        myy(i,j) = cyy;
    end
end

M = [mxx, mxy; myx, myy];


function [cxx, cyx, cxy, cyy] = get_C(M44,T,i,j,len)
% cxy --> orbit at bpm x due to kick in corrector y

R_j = T(:,:,j);
R_i = T(:,:,i);
M_i = R_i * M44 / R_i;
if (i>j)   
    R_ij = R_i/R_j;
else
    R_ij = R_i * (T(:,:,end) / R_j);
end
%C = R_ij / (diag([1 1 1 1])-M44);
C = (diag([1 1 1 1])-M_i) \ R_ij;

cxx = (len/2) * C(1,1) + C(1,2);
cyx = (len/2) * C(3,1) + C(3,2);
cxy = (len/2) * C(1,3) + C(1,4);
cyy = (len/2) * C(3,3) + C(3,4);