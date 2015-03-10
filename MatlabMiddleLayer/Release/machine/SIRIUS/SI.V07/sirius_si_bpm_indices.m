function idx = sirius_si_bpm_indices(the_ring)

idx = [];
idx = [idx findcells(the_ring, 'FamName', 'bpm')];
idx = sort(idx);
idx = reshape(idx,[],1);
