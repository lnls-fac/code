function tracy3_dynamic_aperture1_4JSR(varargin)

fmapdpFlag = true;
default_dir = lnls_get_root_folder();
for i=1:length(varargin)
    if (ischar(varargin{i}) && strcmpi(varargin{i}, 'local_dir'))
        default_dir = pwd();
    else
        fmapdpFlag = varargin{i};
    end
end

size_font = 24;
limx = 12;
limy = 3.0;
lime = 5;


% selects data folder
default_dir = fullfile(default_dir, 'data', 'sirius_tracy');
pathname = uigetdir(default_dir,'Em qual pasta estao os dados?');
if (pathname == 0);
    return
end

% gets number of random machines (= number of rms folders)
[~, result] = system(['ls ' pathname '| grep rms | wc -l']);
n_pastas = str2double(result);
%n_pastas = 12;

% loops over random machine, loading and plotting data
count = 0; countdp = 0;
% v1 = zeros(1,90);
% v2 = zeros(1,49);

for i=1:n_pastas
    % -- FMAP --
    full_name = fullfile(pathname, ['rms', num2str(i, '%02i')]);
    try
        [~, dados1] = tracy3_load_daxy_data(full_name);
        ind = dados1.plane == -1;
        if ~exist('idx_fmap','var')
            idx_fmap = ind;
        else
            idx_fmap = idx_fmap + ind;
        end
        count = count + 1;
    catch
        disp('fmap nao carregou');
    end
    
    if (fmapdpFlag)
        try
            [~, dados2] = tracy3_load_daex_data(full_name);

            inddp = dados2.plane == -1;
            if ~exist('idx_fmapdp','var')
                idx_fmapdp = inddp;
            else
                idx_fmapdp = idx_fmapdp + inddp;
            end
            countdp = countdp+1;
        catch
            disp('fmapdp nao carregou');
        end
    end
end

% v1 = v1 / count;
% v2 = v2 / count;
% 
idx_fmap = (count-idx_fmap)/count*100;
idx_fmap(1,1) = 100; idx_fmap(1,2) = 0;
idx_fmapdp = (count-idx_fmapdp)/countdp*100;
idx_fmapdp(1,1) = 100; idx_fmapdp(1,2) = 0;

scrsz = get(0,'ScreenSize');
xi = scrsz(4)/12;
yi = scrsz(4)/20;
xf = xi + scrsz(4);
yf = yi + scrsz(4);

f=figure('OuterPosition',[xi yi xf yf]);
sb(1,1) = subplot(2,2,1,'Parent',f,'FontSize',size_font,...
    'Position',[0.065 0.60 0.368 0.382]);
pcolor(sb(1,1), 1000*dados1.x, 1000*dados1.y, idx_fmap);
colormap(sb(1,1), 'Gray'); shading(sb(1,1), 'interp');
box(sb(1,1),'on');
xlabel(sb(1,1), 'x (mm)','FontSize',size_font);
ylabel(sb(1,1), 'y (mm)','FontSize',size_font);
xlim(sb(1,1), [-limx limx]);
ylim(sb(1,1), [0 limy]);
annotation(f,'textbox',...
    [0.392 0.604 0.040 0.0402],...
    'String',{'(a)'},...
    'FontSize',24,...
    'FitBoxToText','off',...
    'LineStyle','none');
%hold all; plot(1000*x(1,:),1000*v1,'r', 'LineWidth', 2);

sb(1,2) = subplot(2,2,2,'Parent',f,'FontSize',size_font,...
    'Position',[0.53 0.60 0.368 0.382]);
pcolor(sb(1,2), 100*dados2.en, 1000*dados2.x, idx_fmapdp);
colormap(sb(1,2), 'Gray'); shading(sb(1,2), 'interp');
box(sb(1,2),'on');
xlabel(sb(1,2), '\delta (%)','FontSize',size_font);
ylabel(sb(1,2), 'x (mm)','FontSize',size_font);
xlim(sb(1,2), [-lime lime]);
ylim(sb(1,2),[-limx,0]);
annotation(f,'textbox',...
    [0.856 0.602 0.0409 0.0402],...
    'String',{'(b)'},...
    'FontSize',24,...
    'FitBoxToText','off',...
    'LineStyle','none');
%hold all; plot(100*en(1,:),1000*v2,'r', 'LineWidth', 2);

clear idx_fmap idx_fmapdp;


% selects data folder
pathname = uigetdir(pathname,'Em qual pasta estao os dados?');
if (pathname == 0);
    return
end



% gets number of random machines (= number of rms folders)
[~, result] = system(['ls ' pathname '| grep rms | wc -l']);
n_pastas = str2double(result);
%n_pastas = 12;

% loops over random machine, loading and plotting data
count = 0; countdp = 0;
% v1 = zeros(1,90);
% v2 = zeros(1,49);

for i=1:n_pastas
    % -- FMAP --
    full_name = fullfile(pathname, ['rms', num2str(i, '%02i')]);
    try
        [~, dados1 ] = tracy3_load_daxy_data(full_name);
        ind = dados1.plane == -1;
        if ~exist('idx_fmap','var')
            idx_fmap = ind;
        else
            idx_fmap = idx_fmap + ind;
        end
        count = count + 1;
    catch
        disp('fmap nao carregou');
    end
    
    if (fmapdpFlag)
        try
            [~, dados2] = tracy3_load_daex_data(full_name);

            inddp = dados2.plane == -1;
            if ~exist('idx_fmapdp','var')
                idx_fmapdp = inddp;
            else
                idx_fmapdp = idx_fmapdp + inddp;
            end
            countdp = countdp+1;
        catch
            disp('fmapdp nao carregou');
        end
    end
end

% v1 = v1 / count;
% v2 = v2 / count;

idx_fmap = (count-idx_fmap)/count*100;
idx_fmap(1,1) = 100; idx_fmap(1,2) = 0;
idx_fmapdp = (count-idx_fmapdp)/countdp*100;
idx_fmapdp(1,1) = 100; idx_fmapdp(1,2) = 0;

sb(2,1) = subplot(2,2,3,'Parent',f,'FontSize',size_font,...
    'Position',[0.065 0.1 0.368 0.382]);
pcolor(sb(2,1), 1000*dados1.x, 1000*dados1.y, idx_fmap);
colormap(sb(2,1), 'Gray'); shading(sb(2,1), 'interp');
box(sb(2,1),'on');
xlabel(sb(2,1), 'x (mm)','FontSize',size_font);
ylabel(sb(2,1), 'y (mm)','FontSize',size_font);
xlim(sb(2,1), [-limx limx]);
ylim(sb(2,1), [0 limy]);
annotation(f,'textbox',...
    [0.392 0.104 0.0383 0.0402],...
    'String',{'(c)'},...
    'FontSize',24,...
    'FitBoxToText','off',...
    'LineStyle','none');
%hold all; plot(1000*x(1,:),1000*v1,'r', 'LineWidth', 2);

sb(2,2) = subplot(2,2,4,'Parent',f,'FontSize',size_font,...
    'Position',[0.53 0.1 0.368 0.382]);
pcolor(sb(2,2), 100*dados2.en, 1000*dados2.x, idx_fmapdp);
colormap(sb(2,2), 'Gray'); shading(sb(2,2), 'interp');
box(sb(2,2),'on');
xlabel(sb(2,2), '\delta (%)','FontSize',size_font);
ylabel(sb(2,2), 'x (mm)','FontSize',size_font);
xlim(sb(2,2), [-lime lime]);
ylim(sb(2,2),[-limx,0]);
annotation(f,'textbox',...
    [0.855 0.102 0.0418 0.0402],...
    'String',{'(d)'},...
    'FontSize',24,...
    'FitBoxToText','off',...
    'LineStyle','none');
%hold all; plot(100*en(1,:),1000*v2,'r', 'LineWidth', 2);


colorbar('peer',sb(2,2),...
    [0.91 0.1 0.013 0.88],...
    'FontSize',24,'YTick',[0,20,40,60,80,100],'YTickLabel',...
    {'100%','80%','60%','40%','20%','0%'});

% Create textbox
annotation(f,'textbox',...
    [0.317 0.879 0.074 0.048],...
    'String',{'\delta = 0'},...
    'FontSize',24,...
    'FitBoxToText','off',...
    'LineStyle','none');

% Create textbox
annotation(f,'textbox',...
    [0.545 0.619 0.127 0.046],...
    'String',{'y = 1 mm'},...
    'FontSize',24,...
    'FitBoxToText','off',...
    'LineStyle','none');

