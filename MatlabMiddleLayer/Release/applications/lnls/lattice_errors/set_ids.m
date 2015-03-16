function the_ring = set_ids(old_the_ring, state)

the_ring = old_the_ring;
idx = findcells(the_ring, 'XGrid');

if strcmpi(state, 'off')
    the_ring = setcellstruct(the_ring, 'PassMethod', idx, 'IdentityPass');
else
    the_ring = setcellstruct(the_ring, 'PassMethod', idx, 'LNLSThinEPUPass');
end