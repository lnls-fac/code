function tracy3_dynamic_aperture(fmapdpFlag, n_calls, nr_rms)

color_vec = {'b','r','g','m','c','k','y'};
esp_lin = 5;
size_font = 24;
limx = 15;
limy = 5;
lime = 6;
scrsz = get(0,'ScreenSize');
xi = scrsz(4)/6;
yi = scrsz(4)/10;
xf = xi + scrsz(4)*(2/3);
yf = yi + scrsz(4)*(2/3);


path = '/home/fac_files/data/sirius_tracy/';

cell_leg_text = cell(1,n_calls);
pl = zeros(n_calls,3);
pldp = zeros(n_calls,3);
for i=1:n_calls
    path = uigetdir(path,'Em qual pasta estao os dados?');
    if (path==0);
        return
    end;
    
    onda =  [];
    offda = [];
    
    [~, result] = system(['ls ' path '| grep rms | wc -l']);
    n_pastas = str2double(result);
    rms_mode = true;
    if n_pastas == 0
        rms_mode = false;
        n_pastas = 1;
    end
    if nr_rms == 0, nr_rms = n_pastas; end
    
    cell_leg_text(i) = inputdlg(['Digite a ', int2str(i), '-esima legenda'],'Legenda',1);

    j=1;
    m=1;
    for k=1:min([n_pastas, nr_rms]);
        pathname = path;
        if rms_mode, pathname = fullfile(path,sprintf('rms%02d',k)); end
        
        try
%             onda(j,:,:) = tracy3_load_fmap_data(pathname);
            onda(j,:,:) = tracy3_load_daxy_data(pathname);
            j = j + 1;
        catch
            fprintf('%-2d-%-3d: xy nao carregou\n',i,k);
        end
        
        if (fmapdpFlag)
            try
%                 offda(m,:,:) = tracy3_load_fmapdp_data(pathname);
                offda(m,:,:) = tracy3_load_daex_data(pathname);
                m = m + 1;
            catch
                fprintf('%-2d-%-3d: ex nao carregou\n',i,k);
            end
        end
        
    end
    
    aveOnda = mean(onda,1);
    aveOffda = mean(offda,1);
    if rms_mode
        rmsOnda = std(onda,1);
        rmsOffda = std(offda,1);
    end
   
    %% exposição dos resultados
       
    color = color_vec{i};

    if i == 1
        f=figure('OuterPosition',[xi yi xf yf]);
        fa = axes('Parent',f,'YGrid','on','XGrid','on','FontSize',size_font);
        box(fa,'on');
        hold(fa,'all');
        xlabel('x [mm]','FontSize',size_font);
        ylabel('z [mm]','FontSize',size_font);
        xlim(fa,[-limx limx]);
        ylim(fa,[0 limy]);
    end
    
    
    pl(i,2) = plot(fa, 1000*aveOnda(1,:,1), 1000*aveOnda(1,:,2), ...
        'LineWidth',esp_lin,'Color',color, 'LineStyle','-');
    if rms_mode
        pl(i,1) = plot(fa, 1000*aveOnda(1,:,1),1000*(rmsOnda(1,:,2)+aveOnda(1,:,2)),...
            'LineWidth',2,'LineStyle','--','Color', color);
        pl(i,3) = plot(fa, 1000*aveOnda(1,:,1), 1000*(aveOnda(1,:,2)-rmsOnda(1,:,2)),...
            'LineWidth',2,'LineStyle','--','Color', color);
    end
    
    if fmapdpFlag
        if i == 1
            fdp=figure('OuterPosition',[xi yi xf yf]);
            fdpa = axes('Parent',fdp,'YGrid','on','XGrid','on','FontSize',size_font);
            box(fdpa,'on');
            hold(fdpa,'all');
            xlabel('dp [%]','FontSize',size_font);
            ylabel('x [mm]','FontSize',size_font);
            xlim(fdpa,[-lime lime]);
            ylim(fdpa,[-limx,0]);
        end
        
        pldp(i,2) = plot(fdpa, 100*aveOffda(1,:,1),1000*aveOffda(1,:,2),...
            'LineWidth',esp_lin,'Color',color, 'LineStyle','-');
        if rms_mode
            pldp(i,1) = plot(fdpa, 100*aveOffda(1,:,1), 1000*(rmsOffda(1,:,2)+aveOffda(1,:,2)),...
                'LineWidth',2,'LineStyle','--','Color', color);
            pldp(i,3) = plot(fdpa, 100*aveOffda(1,:,1),1000*(aveOffda(1,:,2)-rmsOffda(1,:,2)),...
                'LineWidth',2,'LineStyle','--','Color', color);
        end
    end
    
    disp('------------');
    drawnow;
end

title_text = inputdlg('Digite um Título para os Gráficos','Título',1);
legend(pl(:,2),'show',cell_leg_text, 'Location','Best');
legend(pldp(:,2),'show',cell_leg_text, 'Location','Best');
title(fa,['DA - ' title_text{1}]);
title(fdpa,['MA - ' title_text{1}]);

