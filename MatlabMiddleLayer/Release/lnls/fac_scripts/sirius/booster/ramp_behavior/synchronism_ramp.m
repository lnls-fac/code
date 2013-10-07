function synchronism_ramp()

freq = 2;
T0 = 496.8/299792458;
dt = T0:10*T0:(0.5/freq-T0);
Ei = 0.150;
Ef = 3;

[E dEdt] = energy_ramp(Ef, Ei, freq, dt);

alpha = 4e-3;

deltat = alpha*E./dEdt;

fi = figure('Units','normalized', 'Position',[0.31 0.37 0.57 0.52] );
axes1 = axes('Parent',fi,'YGrid','on','XGrid','on','FontSize',20);
hold all;
plot(E, deltat*1000);
title(axes1,'Synchromism during ramp','FontSize',20);
xlabel(axes1,'Energy [GeV]','FontSize',20);
ylabel(axes1,'Synchronism [ms]','FontSize',20);
ylim(axes1,[0 1]);
box(axes1,'on');





