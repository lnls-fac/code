function  [res val] = optimize_fun(storage_ring, storage_ring_ref, vec, opt, chr)

%first, lets build our extended vector;
extvec = [];
for ii = 1:length(opt.fam)
    extvec = [extvec vec(ii)*ones(1,opt.size(ii))];
end

% lets apply our vector to the ring
storage_ring = setcellstruct(storage_ring, 'PolynomB', opt.ind, extvec, 3);
storage_ring_ref = setcellstruct(storage_ring_ref, 'PolynomB', opt.ind, extvec, 3);

% now, lets correct the chromaticity
storage_ring_ref = fitchrom2(storage_ring_ref,chr.value,chr.fam{1},chr.fam{2});
val = zeros(1,length(chr.fam));
for ii = 1:length(chr.fam)
    val(ii) = storage_ring_ref{chr.ind{ii}(1)}.PolynomB(3);
    storage_ring = setcellstruct(storage_ring, 'PolynomB',chr.ind{ii}, val(ii),3);
end


nturns = 1000;
nt = nextpow2(nturns);
nturns = 2^nt + 6 - mod(2^nt,6);
x_amps = [0.1, 5 , 6 , 7 , 8  , 9 , 0.1, 11]*1e-3;
y_amps = [1  , 1 , 1 , 1 , 1  , 1  , 200,   1]*1e-5;
other  = zeros(1,length(x_amps));
rin = [x_amps; other; y_amps; other; other; other];
rout = ringpass(storage_ring,rin,nturns);

if any(isnan(rout(end,(end-length(x_amps)+1):end)))
    res = inf;
    return
end

% tentativa de inverter a coxinha:
ind = (rout(1,:) < -7.5e-3) & (rout(1,:) > -8e-3);
maxxp = max(rout(2,ind)); minxp = min(rout(2,ind));
res = 1.8 - (maxxp - minxp)*1e3;

% tentativa de aumentar o tune em altas amplitudes
% res = 11 + 1e3*(rout(1,1) - rout(1,2));


% tentativa de diminuir o tuneshift
coordx  = reshape(rout(1,:),length(rin(1,:)),nturns);
coordxl = reshape(rout(2,:),length(rin(1,:)),nturns);
coordy  = reshape(rout(3,:),length(rin(1,:)),nturns);
coordyl = reshape(rout(4,:),length(rin(1,:)),nturns);
tunex = lnls_calcnaff(coordx, coordxl);
tuney = lnls_calcnaff(coordy, coordyl);

diffx = tunex(2:(length(x_amps)-1)) - tunex(1);
diffy = tuney(2:(length(x_amps)-1)) - tuney(1);
res = 5*sum(sqrt(diffx.^2 + diffy.^2));
    