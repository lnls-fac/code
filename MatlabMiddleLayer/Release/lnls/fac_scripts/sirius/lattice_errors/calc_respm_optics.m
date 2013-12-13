function respm = calc_respm_optics(the_ring0, kbs_idx)

delta_k = 0.001;
the_ring = the_ring0;

v0 = calc_residue_optics(the_ring, the_ring0);
M = zeros(length(v0), length(kbs_idx));
lnls_create_waitbar('optics',0.25,length(kbs_idx));
for i=1:length(kbs_idx)
    k_init = getcellstruct(the_ring, 'K', kbs_idx(i));
    the_ring = setcellstruct(the_ring, 'K', kbs_idx(i), k_init - 0.5 * delta_k);
    the_ring = setcellstruct(the_ring, 'PolynomB', kbs_idx(i), k_init - 0.5 * delta_k, 1, 2);
    v1 = calc_residue_optics(the_ring, the_ring0);
    the_ring = setcellstruct(the_ring, 'K', kbs_idx(i), k_init + 1.0 * delta_k);
    the_ring = setcellstruct(the_ring, 'PolynomB', kbs_idx(i), k_init + 1.0 * delta_k, 1, 2);
    v2 = calc_residue_optics(the_ring, the_ring0);
    the_ring = setcellstruct(the_ring, 'K', kbs_idx(i), k_init - 0.5 * delta_k);
    the_ring = setcellstruct(the_ring, 'PolynomB', kbs_idx(i), k_init - 0.5 * delta_k, 1, 2);
    M(:,i) = (v2 - v1) / delta_k;
    lnls_update_waitbar(i);
end
lnls_delete_waitbar;

[U,S,V] = svd(M,'econ');
respm.M = M;
respm.U = U;
respm.V = V;
respm.S = S;
    