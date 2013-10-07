function respm = calc_respm_coupling(the_ring, bpms, hcms, vcms, scms)

stepK = 0.001;

v0 = calc_residue_coupling(the_ring, bpms, hcms, vcms);
M = zeros(length(v0),length(scms));
lnls_create_waitbar('Calcs Coupling Response Matrix',0.5,length(scms));
for i=1:length(scms)
    K = getcellstruct(the_ring, 'PolynomA', scms(i), 1, 2);
    the_ring = setcellstruct(the_ring, 'PolynomA', scms(i), K + stepK/2, 1, 2);
    v2 = calc_residue_coupling(the_ring, bpms, hcms, vcms);
    the_ring = setcellstruct(the_ring, 'PolynomA', scms(i), K - stepK, 1, 2);
    v1 = calc_residue_coupling(the_ring, bpms, hcms, vcms);
    the_ring = setcellstruct(the_ring, 'PolynomA', scms(i), K + stepK/2, 1, 2);
    M(:,i) = (v2 - v1) / stepK;
    lnls_update_waitbar(i)
end
lnls_delete_waitbar;

respm.M = M;

