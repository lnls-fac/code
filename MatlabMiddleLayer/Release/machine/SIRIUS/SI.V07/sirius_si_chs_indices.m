function idx = sirius_si_chs_indices(the_ring)

idx = [];
idx = [idx findcells(the_ring, 'FamName', 'sfa')];
idx = [idx findcells(the_ring, 'FamName', 'sd1')];
idx = [idx findcells(the_ring, 'FamName', 'sd2')];
idx = [idx findcells(the_ring, 'FamName', 'sf2')];
idx = [idx findcells(the_ring, 'FamName', 'sf3')];
idx = [idx findcells(the_ring, 'FamName', 'sd5')];
idx = [idx findcells(the_ring, 'FamName', 'sd6')];
idx = [idx findcells(the_ring, 'FamName', 'sfb')];
idx = sort(idx);