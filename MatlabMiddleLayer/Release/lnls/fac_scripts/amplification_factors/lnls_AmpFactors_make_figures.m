function lnls_AmpFactors_make_figures(res)
% Example code for uicontrol reference page
if ~iscell(res)
    res = {res};
end

global ctrl hax
% Create a figure and an axes to contain a 3-D surface plot.
figure('Position',[984, 200, 882, 636]);
hax = axes('Units','pixels', 'Position',[100.8, 86.2, 741.2, 408.8]);


% Popup to control the configuration
string = {'orbx','orby','corx','cory','coup','betx','bety'};
uicontrol('Style','text','Position',[534.3 607 70 20],'String','Effect');
ctrl.efct = uicontrol('Style', 'popup','String', string,'Position', [534.3 587 70 20]);

% Popup to control the configuration
string = {'empty'};
uicontrol('Style','text','Position',[764 607 100 20],'String','Points Avgd.');
ctrl.wre2clc = uicontrol('Style', 'popup','String', string,'Position', [764 587 100 20]);

sys_names = fieldnames(res{1});
sys_names = sys_names(~strcmp('name',sys_names));
% Popup to control the configuration
uicontrol('Style','text','Position',[167.3 607 70 20],'String','System');
ctrl.sys = uicontrol('Style', 'popup','String', sys_names,...
    'Position', [167.3 587 70 20],'Callback', {@fun_sys,res});

string = getcellstruct(res,'name',1:length(res));
% Popup to control the configuration
uicontrol('Style','text','Position',[20 607 120 20],'String','Configuration');
ctrl.config = uicontrol('Style', 'popup','String', string,...
    'Position', [20 587 120 20],'Callback', {@fun_config,res});

% Popup to control the configuration
string = {'misx','misy','exci','roll'};
uicontrol('Style','text','Position',[397 607 100 20],'String','Type of Error');
ctrl.err = uicontrol('Style', 'popup', 'String', string,'Position', [397 587 100 20]);

sys_names = fieldnames(res{1});
res_names = fieldnames(res{1}.(sys_names{2}).results);
% Popup to control the configuration
uicontrol('Style','text','Position',[284.7 607 80 20],'String','Elements');
ctrl.res = zeros(1,length(res_names));
for i=1:length(res_names)
    ctrl.res(i) = uicontrol('Style', 'checkbox','String', res_names{i},'Min',0,...
        'Max',1, 'Position', [284.7 587-20*(i-1) 80 20]);
end

uicontrol('Style','text','Position',[646.7 607 90 20],'String','Error Value');
ctrl.errVal = uicontrol('Style','edit','String','1.0','Position',[646.7 587 90 20]);

uicontrol('Style', 'pushbutton', 'String', 'Plot',...
    'Position', [579 544 50 20],'Callback', {@plot_curve,res});

uicontrol('Style', 'pushbutton', 'String', 'Clear',...
    'Position', [651 544 50 20],'Callback', @clear_plot);

uicontrol('Style', 'pushbutton', 'String', 'Figure',...
    'Position', [723 544 50 20],'Callback', @create_figure);


ctrl.sumsqr = [];
end


%% CallBack definition
function fun_config(hObj,event, res)
global ctrl
val_conf = get(hObj,'Value');
sys_names = fieldnames(res{val_conf});
sys_names = sys_names(~strcmp('name',sys_names));
set(ctrl.sys,'String',sys_names);

val_sys = get(ctrl.sys,'Value');str_sys = get(ctrl.sys,'String');
str_sys = str_sys{val_sys};
set(ctrl.wre2clc,'Value',1);
set(ctrl.wre2clc,'String',res{val_conf}.(str_sys).where2calclabels);

delete(ctrl.res(:));
res_names = fieldnames(res{val_conf}.(str_sys).results);
ctrl.res = zeros(1,length(res_names));
for i=1:length(res_names)
    ctrl.res(i) = uicontrol('Style', 'checkbox','String', res_names{i},'Min',0,...
        'Max',1, 'Position', [284.7 587-20*(i-1) 80 20]);
end
end

function fun_sys(hObj,event,res)
global ctrl
val_sys = get(hObj,'Value');str_sys = get(ctrl.sys,'String');
str_sys = str_sys{val_sys};
val_conf = get(ctrl.config,'Value');
set(ctrl.wre2clc,'Value',1);
set(ctrl.wre2clc,'String',res{val_conf}.(str_sys).where2calclabels);

delete(ctrl.res(:));
res_names = fieldnames(res{val_conf}.(str_sys).results);
ctrl.res = zeros(1,length(res_names));
for i=1:length(res_names)
    ctrl.res(i) = uicontrol('Style', 'checkbox','String', res_names{i},'Min',0,...
        'Max',1, 'Position', [284.7 587-20*(i-1) 80 20]);
end

end

function plot_curve(hObj,event,res)
global ctrl hax
val_conf = get(ctrl.config,'Value');str_conf = get(ctrl.config,'String');
str_conf = str_conf{val_conf};

val_sys = get(ctrl.sys,'Value'); str_sys = get(ctrl.sys,'String');
str_sys = str_sys{val_sys};

val_err = get(ctrl.err,'Value');str_err = get(ctrl.err,'String');
str_err = str_err{val_err};

val_efct = get(ctrl.efct,'Value');str_efct = get(ctrl.efct,'String');
str_efct = str_efct{val_efct};

val_clc = get(ctrl.wre2clc,'Value');str_clc = get(ctrl.wre2clc,'String');
str_clc = str_clc{val_clc};

str_errVal = get(ctrl.errVal,'String'); val_errVal = str2double(str_errVal);

chil = get(hax,'Children');
j=0;
for i=1:length(chil)
    dispname = get(chil(i),'DisplayName');
    if ~isempty(dispname)
        j = j+1;
    end
end

hold(hax,'all');
color = {'b','r','g','c','m','y','k'};
cor = color{mod(j,length(color))+1};

erro = [];
pos = [];
mrk = {'','o','+','x','*'};
res_vals = get(ctrl.res,'Value');
if iscell(res_vals),res_vals = cell2mat(res_vals)';end
ind = logical(res_vals);
if ~any(ind)
    fprintf('Please, select at least one type of element to plot.\n');
    return;
end
for i=1:length(ind)
    string = get(ctrl.res(i),'String');
    r = res{val_conf}.(str_sys).results.(string);
    if ind(i) && isfield(r,str_err) && isfield(r.(str_err),str_efct)
        data = r.(str_err).(str_efct)*val_errVal;
        if any(size(data)==1)
            erro = [erro, data];
            pos  = [pos, r.pos];
            plot(hax,r.pos,data,[cor, mrk{i}],'MarkerSize',8,'LineStyle','none');
        else
            erro = [erro data(val_clc,:)];
            pos  = [pos, r.pos];
            plot(hax,r.pos,data(val_clc,:),[cor, mrk{i}],'MarkerSize',8,'LineStyle','none');
        end
    end
end
if isempty(erro)
    fprintf('None of the elements has this type of error.\n');
    return;
end
[pos I] = sort(pos);
erro = erro(I);

% color = {'b','r','g','m','c'};
string = [str_conf, '.', str_sys, '.', str_err, '.', str_efct, '.', str_clc,'.',str_errVal];
plot(hax, pos, erro,'Color',cor, 'DisplayName',string,'LineWidth',2);

sumsqr = sprintf('%8.4f',sqrt(res{val_conf}.(str_sys).symmetry*sum(erro.^2)));
ctrl.sumsqr(j+1) = uicontrol('Style','text','Position',[100+90*j 20 80 20],'String',sumsqr);

if isempty(chil)
    maxy = max(erro);
    lnls_drawlattice(res{val_conf}.(str_sys).the_ring,res{val_conf}.(str_sys).symmetry,-maxy/20,true,maxy/21,true,hax);
%     xlim(hax,[0,findspos(res{val_conf}.(str_sys).the_ring)/res{val_conf}.(str_sys).symmetry]);
    ylim(hax,[-maxy/10, maxy]*1.05);
    set(hax,'XGrid','on','YGrid','on');
end
old_ylim = get(hax,'ylim');
if old_ylim/1.05 < max(erro)
    ylim([old_ylim(1), max(erro)*1.05]);
end
end


function clear_plot(hObj,event)
global hax ctrl
hold(hax,'off');
delete(ctrl.sumsqr(:));
ctrl.sumsqr = [];
cla(hax)

end

function create_figure(hObj,event)
global hax ctrl

a = figure('Position', [405 203 1000 600]);
ax = copyobj(hax,a);
set(ax,'FontSize',16, 'Units', 'Normalized');
set(ax,'YGrid','on','XGrid','on', 'Position',[0.118 0.142 0.836 0.775], 'box','on');
xlabel(ax,'Pos [m]','FontSize',16);
val = get(ctrl.efct,'Value');string = get(ctrl.efct,'String');
string = upper(string{val});
ylabel(ax,[string ' [\mum]'],'FontSize',16);
chil = get(ax,'Children');
pl = [];
text = {};
for i=1:length(chil)
    dispname = get(chil(i),'DisplayName');
    if ~isempty(dispname)
        pl = [pl chil(i)];
        text = [text, {dispname}];
    end
end
if ~isempty(pl)
    legend(pl,'show',text,'Location','Best');
end
end
