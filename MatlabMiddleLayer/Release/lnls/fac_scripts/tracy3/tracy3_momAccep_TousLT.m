function tracy3_momAccep_TousLT(the_ring, varargin)


params.emit0 = 2.8e-10;
params.E     = 3e9;
params.N     = 100e-3/864/1.601e-19*1.72e-6;
params.sigE  = 0.8e-3; 
params.sigS  = 3.5e-3;
params.K     = 0.01;
accepRF      = 0.041;

% default = '/home/fac_files/data/sirius_tracy/';
% path = uigetdir(default,'Em qual pasta estao os dados?');
% if (path==0);
%     return
% end;
% full_name = fullfile(path,'momAccept.out');
full_name = '/home/fac_files/data/sirius_tracy/sr/calcs/v500/ac10_5/test_momAccep_fun/tracy3/momAccept.out';
try
    a = importdata(full_name, ' ', 3);
catch
    disp('nao carregou');
    return;
end

spos  = str2num(char(a.textdata{:,2}))'; spos = spos(1:end/2);
accep = str2num(char(a.textdata{:,3}));
accep = reshape(accep, length(accep)/2, 2)';
Accep(1,:) = [0.0 spos 518.396/10];
Accep(2,:) = min([accep(1,1) min(abs(accep)) accep(1,1)], accepRF);


[~, a] = hdrload('MA_ele.txt');
% [Accep(1,:), ind] = unique(a(:,1)');
% Accep(2,:) = min(min(abs(a(ind,2:3)')),accep_rf);

figure; plot(spos,accep*100,'b', 'Marker','.','DisplayName','tracy');
hold all
plot(a(:,1), a(:,[2 4])*100,'r','Marker','.','DisplayName','elegant');
xlim([0, 52])
xlabel('Pos [m]'); ylabel('Momentum Acceptance [%]');


twi = calctwiss(the_ring);

LT = lnls_tau_touschek_inverso(params,Accep,twi);



%% exposicao dos resultados

%imprime o tempo de vida
fprintf('\n Tempo de vida médio: %10.5f h \n',1/LT.AveRate/60/60);


color = {'b','r','g','m','c','k','y'};
esp_lin = 5;
size_font = 24;
limx = 15;
limy = 5;
lime = 6;

% Create multiple lines using matrix input to plot

scrsz = get(0,'ScreenSize');
xi = scrsz(4)/6;
yi = scrsz(4)/10;
xf = xi + scrsz(4)*(2/3);
yf = yi + scrsz(4)*(2/3);
f=figure('OuterPosition',[xi yi xf yf]);
fa = axes('Parent',f,'YGrid','on','XGrid','on','FontSize',size_font);
box(fa,'on');
hold(fa,'all');
xlabel('x [mm]','FontSize',size_font);
ylabel('z [mm]','FontSize',size_font);

plot1 = zeros(1,3);
plot1(1,:) = plot(fa, X, M, 'LineWidth',2,'LineStyle','--');
set(plot1(1,1),'Color', color);
set(plot1(1,2),'LineWidth',esp_lin,'Color',color, 'LineStyle','-');
set(plot1(1,3),'Color', color);
xlim(fa,[-limx limx]);
ylim(fa,[0 limy]);
%          title(fa, {[pathname '/fmap.out']},'Interpreter','none','FontSize',size_font);

cell_leg_text = {};
for  ii=1:size(plot1,1)
    leg_text = inputdlg(['Digite a ', int2str(ii), '-esima legenda'],'Legenda',1);
    cell_leg_text(end+1) = leg_text;
end
title_text = inputdlg('Digite um Título para os Gráficos','Título',1);
legend1 = legend(plot1(:,2),'show',cell_leg_text);
set(legend1, 'Location','NorthEast');
title(fa,['DA - ' title_text{1}]);
xlim(fa, [-limx limx]);
ylim(fa,[0 limy]);

