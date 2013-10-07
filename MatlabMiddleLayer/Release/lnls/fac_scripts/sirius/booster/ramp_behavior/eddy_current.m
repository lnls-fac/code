function eddy_current()

% Define energy ramp
freq = 2;
dt = (0.0:0.0001:0.5)/freq;
gama0 = 150/0.511;
gamainf = 3e3/0.511;

rho0 = 1.152*50/2/pi;

[gamat dgamatdt] =  energy_ramp(gamainf, gama0, freq, dt(1:end));


global THERING;
THERING = sirius_booster_lattice;
mu0 = 4*pi*1e-7;
condut = 1.35e6; % aco inox 316L austensitico 
hgap = 0.028/2;
a = 30e-3/2; % half width of vacuum chamber
b = 90e-3/2; % half height 
d = 1.2e-3; % espessura
F = 1/2*(1 + b^2*asinh(sqrt(a^2-b^2)/b)/a/sqrt(a^2-b^2));
B = gamat*0.511e3/0.299792458/rho0;
dBdt = dgamatdt*0.511e3/0.299792458/rho0;
deltaK2 = (1/2)*mu0*condut/hgap/rho0*d./B.*dBdt*F;


deltak_norm = -7/16*mu0*condut*d*0.0175*dgamatdt./gamat;


a = findcells(THERING,'FamName','B');
a = a(2:3:end);
bst = getcellstruct(THERING,'PolynomB',a(1),3);
%[~, ~, chrom(1,:)] = twissring(THERING, 0, 1:length(THERING)+1, 'chrom', 1e-8);
for i=0:(length(dt)/50)
    THERING = setcellstruct(THERING,'PolynomB',a,bst + deltaK2(1 + i*50),3);
    [~, ~, chrom(i+1,:)] = twissring(THERING, 0, 1:length(THERING)+1, 'chrom', 1e-8);
end
THERING = setcellstruct(THERING,'PolynomB',a,bst,3);


a = findcells(THERING,'FamName','QF');
kf = getcellstruct(THERING,'PolynomB',a(1),2);
%[~, ~, chrom(1,:)] = twissring(THERING, 0, 1:length(THERING)+1, 'chrom', 1e-8);
for i=0:(length(dt)/50)
    THERING = setcellstruct(THERING,'PolynomB',a,kf*(1+ deltak_norm(1 + i*50)),2);
    [~, tunes(i+1,:), ~] = twissring(THERING, 0, 1:length(THERING)+1, 'chrom', 1e-8);
end
THERING = setcellstruct(THERING,'PolynomB',a,kf,2);



fi = figure('Units','normalized', 'Position', [0.31 0.37 0.57 0.52]);
axes1 = axes('Parent',fi,'FontSize',20);
box(axes1,'on');
hold(axes1,'all');
plot(0.511e-3*gamat(1:50:end),chrom,'Parent',axes1);
title('Chromaticity dependence on dipoles eddy current effect', 'FontSize',20);
xlabel('energy [GeV]', 'fontSize',20); ylabel('\xi', 'FontSize',20);
legend('\xi_x', '\xi_y');

fi2 = figure('Units','normalized', 'Position', [0.31 0.37 0.57 0.52]);
axes2 = axes('Parent',fi2,'FontSize',20);
box(axes2,'on');
hold(axes2,'all');
plot(0.511e-3*gamat(1:50:end),[(tunes(:,1)-tunes(1,1)) (tunes(:,2)-tunes(1,2))],'Parent',axes2);
title('Tune variation dependence on dipoles eddy current effect', 'FontSize',20);
xlabel('energy [GeV]', 'fontSize',20); ylabel('\nu', 'FontSize',20);
legend('\Delta\nu_x', '\Delta\nu_y');

