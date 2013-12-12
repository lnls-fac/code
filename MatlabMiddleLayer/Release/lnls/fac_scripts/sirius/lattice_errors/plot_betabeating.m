function plot_betabeating(machine_fname, thering_fname)

clc;

machbef_fname = fullfile('CONFIG_V200_AC20_2_symm', 'CONFIG_V200_AC20_2_symm_machines_cod_corrected.mat');
machaft_fname = fullfile('CONFIG_V200_AC20_2_symm', 'CONFIG_V200_AC20_2_symm_machines_cod_coup_opt_corrected.mat');
thering_fname = fullfile('CONFIG_V200_AC20_2_symm', 'CONFIG_V200_AC20_2_symm_the_ring.mat');

%% seleção de arquivos de input
if ~exist('machbef_fname','var')
    [FileName,PathName,FilterIndex] = uigetfile('*.mat','Select mat file with machines (before symm)');
    if isnumeric(FileName)
        return
    end
    machbef_fname = fullfile(PathName, FileName);
end

if ~exist('machaft_fname','var')
    [FileName,PathName,FilterIndex] = uigetfile('*.mat','Select mat file with machines (after symm)');
    if isnumeric(FileName)
        return
    end
    machaft_fname = fullfile(PathName, FileName);
end

if ~exist('thering_fname','var')
    [FileName,PathName,FilterIndex] = uigetfile('*.mat','Select mat file with nominal THERING');
    if isnumeric(FileName)
        return
    end
    thering_fname = fullfile(PathName, FileName);
end

% carrega dados de arquivos
data = load(machbef_fname); mach_bef  = data.machine;
data = load(machaft_fname); mach_aft  = data.machine;
data = load(thering_fname); the_ring = data.the_ring;


%% calcula ótica
twiss0 = calctwiss(the_ring);
for i=1:length(mach_bef)
    twiss_bef(i) = calctwiss(mach_bef{i});
    twiss_aft(i) = calctwiss(mach_aft{i});
end


%% plota resultados
symmetry = 5;

f1 = figure;
hold all;

xmin = 0; xmax = twiss0.pos(end)/(symmetry - 0.0000001);
ymin = 0; ymax = 20;

for i=1:length(mach_aft)
    betax_bef_diff(i,:) = 100*(twiss_bef(i).betax - twiss0.betax)./twiss0.betax;
    betay_bef_diff(i,:) = 100*(twiss_bef(i).betay - twiss0.betay)./twiss0.betay;
    betax_aft_diff(i,:) = 100*(twiss_aft(i).betax - twiss0.betax)./twiss0.betax;
    betay_aft_diff(i,:) = 100*(twiss_aft(i).betay - twiss0.betay)./twiss0.betay;
    data = betax_bef_diff;
    data(betax_bef_diff<0) = 0;
    plot(twiss_bef(i).pos, data, 'Color', [0.7 0.7 1.0]);
    data = betay_bef_diff;
    data(betay_bef_diff>0) = 0;
    plot(twiss_bef(i).pos, data, 'Color', [1.0 0.7 0.7]);
end
plot(twiss0.pos, sqrt(sum(betax_bef_diff.^2)/size(betax_bef_diff,1)), 'Color', [0 0 1.0], 'LineWidth', 2.5);
plot(twiss0.pos, sqrt(sum(betax_aft_diff.^2)/size(betax_aft_diff,1)), 'Color', [0 0 1.0], 'LineWidth', 2.5);
plot(twiss0.pos, -sqrt(sum(betay_bef_diff.^2)/size(betay_bef_diff,1)), 'Color', [1.0 0 0], 'LineWidth', 2.5);
plot(twiss0.pos, -sqrt(sum(betay_aft_diff.^2)/size(betay_aft_diff,1)), 'Color', [1.0 0 0], 'LineWidth', 2.5);

%plot(twiss0.pos, twiss0.betax, 'Color', [0 0 1], 'LineWidth', 2.5);
%axis([xmin, xmax, ymin, ymax]);



xlabel('Pos [m]');
ylabel('\edlta\beta [%%]');
%axis([xmin, xmax, ymin, ymax]);


