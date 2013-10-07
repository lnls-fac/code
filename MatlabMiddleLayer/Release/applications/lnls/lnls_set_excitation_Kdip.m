function new_ring = lnls_set_excitation_Kdip(errors, indices, old_ring)

new_ring = old_ring;


for i=1:size(indices,1)
    for j=1:size(indices,2)
        idx = indices(i,j);
        if isfield(new_ring{idx}, 'BendingAngle')
            new_ring{idx}.PolynomB(2) = new_ring{idx}.PolynomB(2) * (1 + errors(i)); % não funciona com 'BendLinearPass'
        else
            error('lnls_set_excitation_Kdip: not a dipole!');
        end
    end
end
