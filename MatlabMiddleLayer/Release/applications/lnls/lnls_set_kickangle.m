function new_ring = lnls_set_kickangle(old_ring, kicks, ind, plane)

new_ring = old_ring;
if ischar(plane) 
    if plane == 'x'
        pl = 1;
    elseif plane == 'y'
        pl = 2;
    else
        error('Value assigned to plane is not valid');
    end
elseif isnumeric(plane)
    if any(plane == [1,2])
        pl = plane;
    else
        error('Value assigned to plane is not valid');
    end
end

for ii=1:length(ind)
    if strcmp(new_ring{ind(ii)}.PassMethod, 'CorrectorPass')
        new_ring{ind(ii)}.KickAngle(pl) =  kicks(ii);
    elseif  strcmp(new_ring{ind(ii)}.PassMethod, 'ThinMPolePass')
        if pl == 1
            new_ring{ind(ii)}.PolynomB(1) = - kicks(ii); %from angle to field
        else
            new_ring{ind(ii)}.PolynomA(1) = kicks(ii);
        end
    elseif any(strcmp(new_ring{ind(ii)}.PassMethod, { ...
            'BndMPoleSymplectic4Pass', 'BndMPoleSymplectic4RadPass', ...
            'StrMPoleSymplectic4Pass', 'StrMPoleSymplectic4RadPass'}))
        if pl == 1
            new_ring{ind(ii)}.PolynomB(1)= -kicks(ii)/new_ring{ind(ii)}.Length;
        else
            new_ring{ind(ii)}.PolynomA(1)= kicks(ii)/new_ring{ind(ii)}.Length;
        end
    else
        error('Element cannot be used as corrector.')
    end
end
