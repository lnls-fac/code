function delta = calc_longitudinal_mode_coupling(w,Z, n_rad, n_azi, sigma, I_tot, ...
    E, w0, nus, eta)

c = 299792458;

nb = 1;
pmin = ceil((w(1)-(n_azi*nus)*w0)/(w0*nb)); % arredonda em dire��o a +infinito
pmax = ceil((w(end)-(nb-1 + n_azi*nus)*w0)/(w0*nb))-1; % arredonda em dire��o a -infinito

p = pmin:pmax;
wp = w0*(p*nb + 1*nus);
interpol_Z = interp1(w,Z,wp);

K = I_tot*w0*eta/(2*pi)/(nus*w0)^2/(E*1e9)/(sigma/c)^2;

A = zeros((1 + 2*n_azi)*(1+n_rad),(1 + 2*n_azi)*(1+n_rad));
M = zeros((1 + 2*n_azi)*(1+n_rad),(1 + 2*n_azi)*(1+n_rad));

for m = (-n_azi):n_azi
    if m>=0
        em = 1;
    else
        em = (-1)^m;
    end
    for k = 0:n_rad
        Imk = em/sqrt(factorial(abs(m)+k)*factorial(k))* ...
            (wp*sigma/c/sqrt(2)).^(abs(m)+2*k).*exp(-(wp*sigma/c/sqrt(2)).^2);
        ind1 = n_azi + 1 + m + k*(2*n_azi + 1);
        for n = (-n_azi):n_azi
            if n>=0
                en = 1;
            else
                en = (-1)^n;
            end
            for l = 0:n_rad
                Inl = en/sqrt(factorial(abs(n)+l)*factorial(l)) .* ...
                    (wp*sigma/c/sqrt(2)).^(abs(n)+2*l).*exp(-(wp*sigma/c/sqrt(2)).^2);
                ind2 = n_azi + 1 + n + l*(2*n_azi + 1);
                M(ind1,ind2) = 1i*(1i)^(m-n)*m*K*sum((interpol_Z./wp).*Imk.*Inl);
                if m==n && k==l
                    A(ind1,ind2) = m + M(ind1,ind2);
                else
                    A(ind1,ind2) = M(ind1,ind2);
                end
            end
        end
    end
end

delta = eig(A);