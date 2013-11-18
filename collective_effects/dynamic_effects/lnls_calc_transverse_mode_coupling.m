function delta = calc_transverse_mode_coupling(w,Z, n_rad, n_azi, sigma, I_tot, ...
    E, w0, beta, nut, nus, eta, chrom)

c = 299792458;

nb = 1;
nucro = nut/eta*chrom;
pmin = ceil((w(1)-(n_azi*nus + nut)*w0)/(w0*nb)); % arredonda em dire��o a +infinito
pmax = ceil((w(end)-(nb-1 + nut + n_azi*nus)*w0)/(w0*nb))-1; % arredonda em dire��o a -infinito

p = pmin:pmax;
wp = w0*(p*nb + nut + 0*nus);
wpcro = wp - nucro*w0;
interpol_Z = interp1(w,Z,wp);

K = I_tot*w0/(4*pi)/(nus*w0)/(E*1e9)*beta;

tam = n_azi + 1 + n_azi + n_rad*(2*n_azi + 1);
A = zeros(tam,tam);
M = zeros(tam,tam);

for m = (-n_azi):n_azi
    if m>=0
        em = 1;
    else
        em = (-1)^m;
    end
    for k = 0:n_rad
        Imk = em/sqrt(factorial(abs(m)+k)*factorial(k))* ...
            (wpcro*sigma/c/sqrt(2)).^(abs(m)+2*k).*exp(-(wpcro*sigma/c/sqrt(2)).^2);
        ind1 = n_azi + 1 + m + k*(2*n_azi + 1);
        for n = (-n_azi):n_azi
            if n>=0
                en = 1;
            else
                en = (-1)^n;
            end
            for l = 0:n_rad
                Inl = en/sqrt(factorial(abs(n)+l)*factorial(l)) .* ...
                    (wpcro*sigma/c/sqrt(2)).^(abs(n)+2*l).*exp(-(wpcro*sigma/c/sqrt(2)).^2);
                ind2 = n_azi + 1 + n + l*(2*n_azi + 1);
                M(ind1,ind2) = -1i*(1i)^(m-n)*K*sum(interpol_Z.*Imk.*Inl);
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


