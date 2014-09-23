function kicks = lnls_get_kickangle(ring, ind, plane)

kicks = zeros(size(ind));
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
    if strcmp(ring{ind(ii)}.PassMethod, 'CorrectorPass')
        kicks(ii) = ring{ind(ii)}.KickAngle(pl);
    elseif  strcmp(ring{ind(ii)}.PassMethod, 'ThinMPolePass')
        if pl == 1
            kicks(ii) = -ring{ind(ii)}.PolynomB(1);
        else
            kicks(ii) = ring{ind(ii)}.PolynomA(1);
        end
    elseif any(strcmp(ring{ind(ii)}.PassMethod, { ...
            'BndMPoleSymplectic4Pass', 'BndMPoleSymplectic4RadPass', ...
            'StrMPoleSymplectic4Pass', 'StrMPoleSymplectic4RadPass'}))
        if pl == 1
            kicks(ii) = -ring{ind(ii)}.PolynomB(1)*ring{ind(ii)}.Length;
        else
            kicks(ii) = ring{ind(ii)}.PolynomA(1)*ring{ind(ii)}.Length;
        end
    else
        error('Element cannot be used as corrector.')
    end
end