function the_ring = set_sextupoles(the_ring0, strength, sext_str)

the_ring = the_ring0;

sext_idx = getappdata(0, 'Sextupole_Idx');
    
if isstruct(the_ring{1})    
    the_ring = setcellstruct(the_ring, 'PolynomB', sext_idx, strength * sext_str, 1, 3);
else
    for i=1:length(the_ring)
        the_ring{i} = setcellstruct(the_ring{i}, 'PolynomB', sext_idx, strength * sext_str, 1, 3);
    end
end