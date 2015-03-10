function idx = sirius_si_cvs_indices(the_ring)

idx = [];
idx = [idx findcells(the_ring, 'FamName', 'sfa')];
idx = [idx findcells(the_ring, 'FamName', 'sd1')];
idx = [idx findcells(the_ring, 'FamName', 'sd3')];
idx = [idx findcells(the_ring, 'FamName', 'sd4')];
idx = [idx findcells(the_ring, 'FamName', 'sd6')];
idx = [idx findcells(the_ring, 'FamName', 'sfb')];
idx = sort(idx);
idx = reshape(idx, [], 1);
