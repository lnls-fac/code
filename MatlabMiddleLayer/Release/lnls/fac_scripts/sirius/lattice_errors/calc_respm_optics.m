function respm = calc_respm_optics(the_ring, tune, bpms, hcms, vcms, kbs, nper)

if ~exist('nper','var'), nper = 1; end
stepK = 0.001;

fprintf('nr quadcorr: %03i\n', length(kbs));

v0 = calc_residue_optics(the_ring, tune, bpms, hcms, vcms, nper);
M = zeros(length(v0),length(kbs));


len_kbs = length(kbs)/nper;
if logical(mod(len_kbs,1))
    len_kbs = len_kbs*nper;
    nper = 1;
end

lnls_create_waitbar('Calcs Optics Response Matrix',0.5,len_kbs);
K = getcellstruct(the_ring, 'PolynomB', kbs(1:len_kbs), 1, 2);
for i1=1:len_kbs
    the_ring_calc = setcellstruct(the_ring, 'PolynomB', kbs(i1), K(i1) + stepK/2, 1, 2);
    v2 = calc_residue_optics(the_ring_calc, tune, bpms, hcms, vcms, nper); % the replication for equivalent
    the_ring_calc = setcellstruct(the_ring, 'PolynomB', kbs(i1), K(i1) - stepK/2, 1, 2);% skews is done
    v1 = calc_residue_optics(the_ring_calc, tune, bpms, hcms, vcms, nper);% inside this function
    M(:,i1:len_kbs:end) = (v2 - v1) / stepK;
    lnls_update_waitbar(i1)
end
lnls_delete_waitbar;

respm.M = M;
[U,S,V] = svd(M,'econ');
respm.U = U;
respm.V = V;
respm.S = S;