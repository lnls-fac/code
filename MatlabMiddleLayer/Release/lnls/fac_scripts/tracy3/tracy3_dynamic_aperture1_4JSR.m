function tracy3_dynamic_aperture1_4JSR(varargin)

fmapdpFlag = true;

% selects data folder
pathname = lnls_get_root_folder();
pathname = fullfile(pathname, 'data', 'sirius_tracy');
for i=1:length(varargin)
    if (ischar(varargin{i}) && strcmpi(varargin{i}, 'local_dir'))
        pathname = pwd();
    else
        fmapdpFlag = varargin{i};
    end
end

scrsz = get(0,'ScreenSize');
xi = scrsz(4)/12;
yi = scrsz(4)/20;
xf = xi + scrsz(4);
yf = yi + scrsz(4);
size_font = 24;
type_colormap = 'Jet';
limx = 12;
limy = 3.0;
lime = 5;

mostra = 0; % 0 = porcentagem de part perdidas
% 1 = número medio de voltas
% 2 = posicao em que foram perdidas


f=figure('OuterPosition',[xi yi xf yf]);

sb = zeros(2,2);
for j = 1:2
    % loops over random machine, loading and plotting data
    count = 0; countdp = 0;
    
    % selects data folder
    pathname = uigetdir(pathname,'Em qual pasta estao os dados?');
    if (pathname == 0);
        return
    end
    
    % gets number of random machines (= number of rms folders)
    [~, result] = system(['ls ' pathname '| grep rms | wc -l']);
    n_pastas = str2double(result);
    
    for i=1:n_pastas
        % -- FMAP --
        full_name = fullfile(pathname, ['rms', num2str(i, '%02i')]);
        try
            [~, dados1] = tracy3_load_daxy_data(full_name);
            ind = dados1.plane == -1;
            if i == 1, idx_daxy = zeros(size(ind));end;
            switch mostra
                case 0
                    idx_daxy = idx_daxy + ind;
                case 1
                    idx_daxy = idx_daxy + dados1.turn;
                case 2
                    idx_daxy = idx_daxy + mod(dados1.pos,51.8396);
            end
            count = count + 1;
        catch
            disp('fmap nao carregou');
        end
        
        if (fmapdpFlag)
            try
                [~, dados2] = tracy3_load_daex_data(full_name);
                inddp = dados2.plane == -1;
                if i == 1, idx_daex = zeros(size(inddp));end;
                switch mostra
                    case 0
                        idx_daex = idx_daex + inddp;
                    case 1
                        idx_daex = idx_daex + dados2.turn;
                    case 2
                        idx_daex = idx_daex + mod(dados2.pos,51.8396);
                end
                countdp = countdp+1;
            catch
                disp('fmapdp nao carregou');
            end
        end
    end
    
    idx_daxy = (count-idx_daxy)/count*100;
    idx_daxy(1,1) = 100; idx_daxy(1,2) = 0;
    idx_daex = (count-idx_daex)/countdp*100;
    idx_daex(1,1) = 100; idx_daex(1,2) = 0;
    
    sb(j,1) = subplot(2,2,(2*j-1),'Parent',f,'FontSize',size_font,...
        'Position',[0.065 (0.60-(j-1)*0.5) 0.368 0.382]);
    pcolor(sb(j,1), 1000*dados1.x, 1000*dados1.y, idx_daxy);
    colormap(sb(j,1), type_colormap); shading(sb(j,1), 'interp');
    box(sb(j,1),'on');
    xlabel(sb(j,1), 'x (mm)','FontSize',size_font);
    ylabel(sb(j,1), 'y (mm)','FontSize',size_font);
    xlim(sb(j,1), [-limx limx]);
    ylim(sb(j,1), [0 limy]);
    %hold all; plot(1000*x(1,:),1000*v1,'r', 'LineWidth', 2);
    
    sb(j,2) = subplot(2,2,2*j,'Parent',f,'FontSize',size_font,...
        'Position',[0.53 (0.60-(j-1)*0.5) 0.368 0.382]);
    pcolor(sb(j,2), 100*dados2.en, 1000*dados2.x, idx_daex);
    colormap(sb(j,2), type_colormap); shading(sb(j,2), 'interp');
    box(sb(j,2),'on');
    xlabel(sb(j,2), '\delta (%)','FontSize',size_font);
    ylabel(sb(j,2), 'x (mm)','FontSize',size_font);
    xlim(sb(j,2), [-lime lime]);
    ylim(sb(j,2),[-limx,0]);
    
end

annotation(f,'textbox',[0.392 0.604 0.040 0.0402],'String',{'(a)'},...
    'FontSize',24,'FitBoxToText','off','LineStyle','none');

annotation(f,'textbox',[0.856 0.602 0.0409 0.0402],'String',{'(b)'},...
    'FontSize',24,'FitBoxToText','off','LineStyle','none');

annotation(f,'textbox',[0.392 0.104 0.0383 0.0402],'String',{'(c)'},...
    'FontSize',24,'FitBoxToText','off','LineStyle','none');

annotation(f,'textbox', [0.855 0.102 0.0418 0.0402],'String',{'(d)'},...
    'FontSize',24,'FitBoxToText','off','LineStyle','none');

colorbar('peer',sb(2,2), [0.91 0.1 0.013 0.88], 'FontSize',24,...
    'YTick',[0,20,40,60,80,100],'YTickLabel',...
    {'100%','80%','60%','40%','20%','0%'});
% Create textbox
annotation(f,'textbox', [0.317 0.879 0.074 0.048],'String',{'\delta = 0'},...
    'FontSize',24, 'FitBoxToText','off', 'LineStyle','none');
% Create textbox
annotation(f,'textbox', [0.545 0.619 0.127 0.046],'String',{'y = 1 mm'},...
    'FontSize',24, 'FitBoxToText','off', 'LineStyle','none');

