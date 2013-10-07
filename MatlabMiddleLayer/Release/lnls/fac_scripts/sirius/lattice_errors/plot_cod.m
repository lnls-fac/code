function plot_cod(config,corrected)

%fconfig = 'cod_matlab';
fconfig = '';

%% config do script

Nper = 1;
%corrected = true;
if ~exist('config', 'var'), config = 'CONFIG_V402_AC10_4'; end;
if ~exist('corrected', 'var'), corrected = true; end;

%% carrega dados
if ~exist('corrected','var'), corrected = false; end;

if corrected
    y_units = '[um]';
    titled   = 'After Correction';
    fname = fullfile(fconfig, [config '_codx_corrected.dat']);
    codx = dlmread(fname);
    fname = fullfile(fconfig, [config '_cody_corrected.dat']);
    cody = dlmread(fname);
else
    y_units = '[mm]';
    titled   = 'Before Correction';
    fname = fullfile(fconfig, [config '_codx_sextoff_nocor.dat']);
    codx = dlmread(fname);
    fname = fullfile(fconfig, [config '_cody_sextoff_nocor.dat']);
    cody = dlmread(fname);
end

fname = fullfile(fconfig, [config '_corrector_hkicks.dat']);
hkicks = dlmread(fname); 
fname = fullfile(fconfig, [config '_corrector_vkicks.dat']);
vkicks = dlmread(fname); 

data = load(fullfile(fconfig, [config '_the_ring.mat'])); the_ring = data.the_ring; 
bpms = findcells(the_ring, 'FamName', 'BPM');
hcms = findcells(the_ring, 'FamName', 'hcm');
vcms = findcells(the_ring, 'FamName', 'vcm');
hkicks = hkicks(:,hcms);
vkicks = vkicks(:,vcms);


%% calc estatisticas

% clc;

codx_avg = mean(codx);
codx_rms = sqrt(sum(codx.^2) / size(codx,1));
codx_max = max(codx);
codx_min = min(codx);

cody_avg = mean(cody);
cody_rms = sqrt(sum(cody.^2) / size(cody,1));
cody_max = max(cody);
cody_min = min(cody);

hkick_rms = sqrt(sum(hkicks(:).^2)/length(hkicks(:)));
vkick_rms = sqrt(sum(vkicks(:).^2)/length(vkicks(:)));

fprintf(['max(HCOD rms)        ' y_units ': %6.3f\n'], max(codx_rms));
fprintf(['max(VCOD rms)        ' y_units ': %6.3f\n'], max(cody_rms));
fprintf(['max(HCOD rms) @ bpms ' y_units ': %6.3f\n'], max(codx_rms(bpms)));
fprintf(['max(VCOD rms) @ bpms ' y_units ': %6.3f\n'], max(cody_rms(bpms)));
fprintf(['rms,max(HKick)     [urad]: %6.3f , %6.3f\n'], 1e3*hkick_rms, 1e3*max(abs(hkicks(:))));
fprintf(['rms,max(VKick)     [urad]: %6.3f , %6.3f\n'], 1e3*vkick_rms, 1e3*max(abs(vkicks(:))));


%% plota resultados

twiss  = calctwiss(the_ring);

figure1 = figure('Color', [1 1 1], 'Position', [249,227,1305,606]);

% Create axes
axes1 = axes('Parent',figure1,...
    'Position',[0.0704980842911877 0.112847222222222 0.90727969348659 0.782986111111111],...
    'FontSize',20);

box(axes1,'on');
hold(axes1,'all');

% Create title
title(axes1,titled,'FontSize',30);

sel_pos_x = (codx >= 0);
plot(twiss.pos, abs(codx), 'Color', [0.7 0.7 1.0]);
plot(twiss.pos, codx_rms, 'b', 'LineWidth', 2.5);

sel_neg_y = (cody <= 0);
plot(twiss.pos, -abs(cody), 'Color', [1.0 0.7 0.7]);
plot(twiss.pos, -cody_rms, 'r', 'LineWidth', 2.5);

plot([0 twiss.pos(end)], [0 0], 'k');

max_x = twiss.pos(end)/Nper;
min_x = 0;
max_y = max(codx(:));
min_y = min(-cody(:));

xlabel('s [m]','FontSize',20);
ylabel(['COD' y_units],'FontSize',20);

%drawlattice(1*min_y,10,axes1,max_x);


%global THERING; THERING = the_ring; drawlattice(min_y - (-min_y)/2, (-1*min_y)/2, gca, max_x);
axis([min_x, max_x, 1.3*min_y, max_y]);
