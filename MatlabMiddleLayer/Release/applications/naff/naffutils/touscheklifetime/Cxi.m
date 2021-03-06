function y = Cxi(t)
 y = -3/2*exp(-t)+ ...
    t/2.*quad('log(u)./u.*exp(-u)',t,10) + ...
    0.5*(3*t-t.*log(t)+2).*quad('exp(-u)./u',t,10);
