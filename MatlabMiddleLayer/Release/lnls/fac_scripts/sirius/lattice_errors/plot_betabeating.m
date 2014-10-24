function plot_betabeating(config_fname, mach_fname)


%% sele��o de arquivos de input
if ~exist('config_fname','var')
    [FileName,PathName,~] = uigetfile('*.mat','Select mat file with configs');
    if isnumeric(FileName)
        return
    end
    config_fname = fullfile(PathName, FileName);
end

if ~exist('mach_fname','var')
    [FileName,PathName,~] = uigetfile('*.mat','Select mat file with machines');
    if isnumeric(FileName)
        return
    end
    mach_fname = fullfile(PathName, FileName);
end

% carrega dados de arquivos
data = load(config_fname); config  = data.r;
data = load(mach_fname); mach  = data.machine;
the_ring = config.params.the_ring;


%% calcula �tica
twiss0 = calctwiss(the_ring);
for i=1:length(mach)
    twiss(i) = calctwiss(mach{i});
end


%% plota resultados
symmetry = 5;

f1 = figure;
set(f1, 'Position', [1 1 1000 350]);
h1 = axes('Parent',f1, 'FontSize',14);
hold on;

xmin = 0; xmax = twiss0.pos(end)/(symmetry - 0.0000001);
ymin = 0; ymax = 20;

for i=1:length(mach_aft)
    betax_diff(i,:) = 100*(abs(twiss_bef(i).betax - twiss0.betax))./twiss0.betax;
    betay_diff(i,:) = 100*(abs(twiss_bef(i).betay - twiss0.betay))./twiss0.betay;
    data = betax_diff;
    plot(h1, twiss(i).pos, data, 'Color', [0.4 0.69 1]);
    data = betay_diff;
    plot(h1, twiss_bef(i).pos, -data, 'Color', [1 0.6 0.6]);
end
plot(h1, twiss0.pos,  std(betax_diff), 'Color', [0 0 1.0], 'LineWidth', 2.5);
plot(h1, twiss0.pos, -std(betay_diff), 'Color', [1.0 0 0], 'LineWidth', 2.5);

%plot(twiss0.pos, twiss0.betax, 'Color', [0 0 1], 'LineWidth', 2.5);
%axis([xmin, xmax, ymin, ymax]);

annotation('Parent',h1,'textbox', [0.75 0.87 0.05 0.05],'String',{'Horizontal'},'FontSize',16,'FontWeight','bold','FitBoxToText','off','LineStyle','none');
annotation('Parent',h1,'textbox',[0.75 0.30 0.05 0.05],'String',{'Vertical'},'FontSize',16,'FontWeight','bold','FitBoxToText','off','LineStyle','none');


xlabel('Pos [m]');
ylabel('\delta\beta [%%]');
% axis([xmin, xmax, ymin, ymax]);


