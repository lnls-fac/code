function idx = sirius_si_cvf_indices(the_ring)

idx = [];
idx = [idx findcells(the_ring, 'FamName', 'cf')];
idx = sort(idx);
idx = reshape(idx,[],1);
