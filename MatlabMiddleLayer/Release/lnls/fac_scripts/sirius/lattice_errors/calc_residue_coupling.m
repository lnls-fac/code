function v = calc_residue_coupling(the_ring, bpms, hcms, vcms)

nr_bpms = length(bpms);
nr_hcms = length(hcms);

[M Dispersion] = get_response_matrix(the_ring, bpms, hcms, vcms);
Mxy = M(nr_bpms+1:end, 1:nr_hcms);
Myx = M(1:nr_bpms, nr_hcms+1:end);
%v = [Mxy(:); Myx(:)];
dispersion_weight = (length(Mxy(:)) + length(Myx(:)))/length(bpms);
v = [10*dispersion_weight * Dispersion(bpms,3); Mxy(:); Myx(:)];


function [M Dispersion] = get_response_matrix(the_ring, bpms, hcms, vcms)

[M44, T] = findm44(the_ring,0,1:length(the_ring)+1);
compactionFactor = mcf(the_ring);
E0 = getenergy('Model');
Circumference = findspos(the_ring, length(the_ring)+1);
const = lnls_constants;
Gamma = E0 / (const.E0/1000);
etac = Gamma^(-2) - compactionFactor;
[TD, r.tunes, r.chromaticity] = twissring(the_ring, 0, 1:length(the_ring)+1, 'chrom', 1e-8);
Dispersion  = [TD.Dispersion]';

M = zeros(2*length(bpms), length(hcms)+length(vcms));

for j=1:length(hcms)
    for i=1:length(bpms)
        [cxx cxy cyx cyy] = get_C(M44,T,bpms(i),hcms(j),Dispersion,etac,Circumference);
        M(i,j) = cxx;
        M(length(bpms)+i, j) = cxy;
    end
end
for j=1:length(vcms)
    for i=1:length(bpms)
        [cxx cxy cyx cyy] = get_C(M44,T,bpms(i),vcms(j),Dispersion,etac,Circumference);
        M(i,j+length(hcms)) = cyx;
        M(length(bpms)+i,length(hcms)+j) = cyy;
    end
end


function [cxx cxy cyx cyy] = get_C(M44,T,i,j,Dispersion,etac,Circumference)

R_j = T(:,:,j);
R_i = T(:,:,i);
M_i = R_i * M44 * inv(R_i);
if (i>j)   
    R_ij = R_i/R_j;
else
    R_ij = R_i * (T(:,:,end)/R_j);
end
%C = R_ij / (diag([1 1 1 1])-M44);
C = inv((diag([1 1 1 1])-M_i)) * R_ij;

cxx = C(1,2) - 0 * Dispersion(i,1) * Dispersion(j,1) / etac / Circumference;
cxy = C(3,2) - 0 * Dispersion(i,3) * Dispersion(j,1) / etac / Circumference;
cyx = C(1,4) - 0 * Dispersion(i,1) * Dispersion(j,3) / etac / Circumference;
cyy = C(3,4) - 0 * Dispersion(i,3) * Dispersion(j,3) / etac / Circumference;
