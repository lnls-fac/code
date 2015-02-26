function respm = calc_respm_coupling(the_ring, bpms, hcms, vcms, scms, nper)

if ~exist('nper','var'), nper = 1; end
stepK = 0.001;

fprintf('nr skewcorr: %03i\n', length(scms));

v0 = calc_residue_coupling(the_ring, bpms, hcms, vcms);
M = zeros(length(v0),length(scms));


len_v0 = length(v0)/nper;
len_scms = length(scms)/nper;
if any(logical(mod([len_v0,len_scms],1)))
    len_scms = len_scms*nper;
    nper = 1;
end

lnls_create_waitbar('Calcs Coupling Response Matrix',0.5,len_scms);
K = getcellstruct(the_ring, 'PolynomA', scms(1:len_scms), 1, 2);
for i1=1:len_scms
    the_ring_calc = setcellstruct(the_ring, 'PolynomA', scms(i1), K(i1) + stepK/2, 1, 2);
    v2 = calc_residue_coupling(the_ring_calc, bpms, hcms, vcms, nper); % the replication for equivalent
    the_ring_calc = setcellstruct(the_ring, 'PolynomA', scms(i1), K(i1) - stepK/2, 1, 2);% skews is done
    v1 = calc_residue_coupling(the_ring_calc, bpms, hcms, vcms, nper);% inside this function
    M(:,i1:len_scms:end) = (v2 - v1) / stepK;
    lnls_update_waitbar(i1)
end
lnls_delete_waitbar;

respm.M = M;
[U,S,V] = svd(M,'econ');
respm.U = U;
respm.V = V;
respm.S = S;