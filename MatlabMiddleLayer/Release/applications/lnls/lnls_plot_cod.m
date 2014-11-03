function lnls_plot_cod


prompt = {'Submachine (bo/si)', 'COD unit (um/mm)', 'symmetry', 'plot title'};
defaultanswer = {'bo', 'um', '10', 'Booster V901'};
answer = inputdlg(prompt,'Select submachine and trackcpp algorithms to run',1,defaultanswer);
if isempty(answer), return; end;
submachine = answer{1};
unit = answer{2};
symmetry = str2double(answer{3});
plot_title = answer{4};
size_font = 16;

% selects file with random machines and loads it
%fname = '/home/fac_files/data/sirius/bo/beam_dynamics/oficial/v900/multi.cod.physap/cod_matlab/CONFIG_machines_cod_corrected_multi.mat';
if ~exist('fname','var') || ~exist(fname, 'file')
    default_path = fullfile(lnls_get_root_folder(), 'data','sirius',submachine);
    [FileName,PathName,~] = uigetfile('*.mat','select matlab file with random machines', default_path);
    if isnumeric(FileName)
        return
    end
    fname = fullfile(PathName, FileName);
end
r = load(fname); machine = r.machine;

% selects section of the lattice for the plot.
s = findspos(machine{1}, 1:length(machine{1}));
s_max = s(end)/symmetry;
sel = (s <= s_max); 
s = s(sel);

% calcs closed-orbit, store them in matriz
if strcmpi(unit, 'um')
    factor = 1e6;
elseif strcmpi(unit, 'mm')
    factor = 1e3;
end
codrx = zeros(length(machine), length(machine{1}));
codry = zeros(length(machine), length(machine{1}));
codpx = zeros(length(machine), length(machine{1}));
codpy = zeros(length(machine), length(machine{1}));
hcms = findcells(machine{1}, 'FamName', 'hcm');
vcms = findcells(machine{1}, 'FamName', 'vcm');
bpms = findcells(machine{1}, 'FamName', 'bpm');
kickx = zeros(length(machine), length(hcms));
kicky = zeros(length(machine), length(vcms));
for i=1:length(machine)
    orb = findorbit4(machine{i}, 0, 1:length(machine{i}));
    codrx(i,:) = factor * orb(1,:);
    codry(i,:) = factor * orb(3,:);
    codpx(i,:) = orb(2,:);
    codpy(i,:) = orb(4,:);
    kickx(i,:) = getcellstruct(machine{i}, 'KickAngle', hcms, 1, 1);
    kicky(i,:) = getcellstruct(machine{i}, 'KickAngle', vcms, 1, 2);
end

fprintf('std kickx kicky [urad]: %.3f %.3f\n', 1e6*std(kickx(:)), 1e6*std(kicky(:)));
fprintf('max kickx kicky [urad]: %.3f %.3f\n', 1e6*max(abs(kickx(:))), 1e6*max(abs(kicky(:))));
fprintf(['max rms corrected cod @ all  (x,y) [' unit ']: %.3f %.3f\n'], max(std(codrx(:,:))), max(std(codry(:,:))));
fprintf(['max rms corrected cod @ bpms (x,y) [' unit ']: %.3f %.3f\n'], max(std(codrx(:,bpms))), max(std(codry(:,bpms))));

% calcs stats
x = codrx(:,sel); 
y = codry(:,sel);
x_std = std(x);
y_std = std(y);
kickx = abs(kickx(:)); kicky = abs(kicky(:));
fprintf('kickx [um] (max, std): %f\n', 1e6*max(kickx), 1e6*std(kicky));
fprintf('kicky [um] (max, std): %f\n', 1e6*max(kicky), 1e6*std(kicky));


figure; hold all;
max_y = max(max(x));
min_y = min(min(y));
lnls_drawlattice(machine{1}, symmetry, min_y - 0.1 * (max_y-min_y), 1, 0.05 * (max_y-min_y)/2);

for i=1:size(x,1)
    plot(s, abs(x(i,:)),  'color', [0.5 0.5 1.0]);
    plot(s, -abs(y(i,:)), 'color', [1.0 0.5 0.5]);
end
plot(s, abs(x_std),  'color', [0 0 1], 'LineWidth', 3);
plot(s, -abs(y_std),  'color', [1 0 0], 'LineWidth', 3);
line([min(s) max(s)], [0 0], 'Color', [0,0,0]);
axis([min(s), max(s), (min_y - 0.1*(max_y-min_y) - 0.05 * (max_y-min_y)/2 - 0.05 * (max_y-min_y)), max_y]);
grid('on');
box('on');
xlabel('s [m]', 'FontSize', size_font); ylabel(['COD [' unit ']'], 'FontSize', size_font);
set(gca, 'FontSize', 15);
title(plot_title, 'FontSize', size_font);

