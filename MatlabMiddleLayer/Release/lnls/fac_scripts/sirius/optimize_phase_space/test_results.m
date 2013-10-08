
% first, we load the lattice
lattice_errors([pwd '/cod_matlab']);
machines = load([pwd '/cod_matlab/CONFIG_machines_cod_corrected.mat']);
storage_ring = machines.machine;

param.energy_deviation  = [-4, -2, 0, 2, 4]*1e-2;
param.radius_resolution = 0.3e-4;
param.nr_turns          = 1000;
param.points_angle      = repmat([1/2+1e-3, 4/5, 1-1e-3]*pi, length(param.energy_deviation), 1);
param.points_radius     = repmat([2, 2.5,  8]*1e-3,     length(param.energy_deviation), 1);
param.quiet_mode        = true;

x = zeros(length(storage_ring),length(param.points_angle(1,:)));
y = zeros(length(storage_ring),length(param.points_angle(1,:)));
x_en = zeros(length(storage_ring),length(param.energy_deviation));
en0 = sum(param.energy_deviation <= 0);
for ii = 1:length(storage_ring)
    r = lnls_dynapt(storage_ring{ii},param);
    x(ii,:) = r.points_x(en0,:);
    y(ii,:) = r.points_y(en0,:);
    x_en(ii,:) = r.points_x(:,end)'; 
    fprintf('Ja foi: %d\n', ii);
end

%%

x_ave = mean(x,1);
x_rms = std(x);
x_plus = x_ave - x_rms;
x_min = x_ave + x_rms;

y_ave = mean(y,1);
y_rms = std(y);
y_plus = y_ave + y_rms;
y_min = y_ave - y_rms;

x_en_ave = mean(x_en,1);
x_en_rms = std(x_en);
x_en_plus = x_en_ave - x_en_rms;
x_en_min = x_en_ave + x_en_rms;
ener = param.energy_deviation;


scrsz = get(0,'ScreenSize');
scrsz = [1, 1, 1/4, 1].*scrsz;
% Booster drawing:
figure1 = figure('OuterPosition', scrsz);
axes11 = subplot(2,1,1,'Parent',figure1,'YGrid','on','XGrid','on','FontSize',16);
ylabel(axes11,'y [mm]'); xlabel(axes11,'x [mm]');
hold(axes11,'on');
plot(x_ave*1e3,  y_ave*1e3, 'LineWidth',3,'LineStyle','-', 'Parent',axes11);
plot(x_plus*1e3, y_plus*1e3,'LineWidth',1,'LineStyle','--', 'Parent',axes11);
plot(x_min*1e3,  y_min*1e3, 'LineWidth',1,'LineStyle','--', 'Parent',axes11);

axes12 = subplot(2,1,2,'Parent',figure1,'YGrid','on','XGrid','on','FontSize',16);
ylabel(axes12,'x [mm]'); xlabel(axes12,'ener [%]');
hold(axes12,'on');
plot(ener*1e2,  x_en_ave*1e3, 'LineWidth',3,'LineStyle','-', 'Parent',axes12);
plot(ener*1e2, x_en_plus*1e3,'LineWidth',1,'LineStyle','--', 'Parent',axes12);
plot(ener*1e2,  x_en_min*1e3, 'LineWidth',1,'LineStyle','--', 'Parent',axes12);