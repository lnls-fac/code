function tracy3_dynamic_aperture_4JSR(fmapdpFlag, nrecalls, nr_rms, varargin)


first_call = true;
if ~isempty(varargin)
    first_call = false;
    default = varargin{5};
    fa = varargin{1};
    plot1 = varargin{2};
    if fmapdpFlag
        fdpa = varargin{3};
        plot1dp = varargin{4};
    end
    
end

if first_call
    default = '/home/fac_files/data/sirius_tracy/';
end

path = uigetdir(default,'Em qual pasta estao os dados?');
if (path==0);
    return
else
    path = [path '/'];
end;

onda =  [];
offda = [];

[status result] = system(['ls ' path '| grep rms | wc -l']);
n_pastas = str2double(result);
if nr_rms == 0, nr_rms = n_pastas; end

for i=1:min([n_pastas, nr_rms]);
    diretorio = sprintf('rms%02d',i);
    pathname = [path diretorio '/'];
    full_name = fullfile(pathname,'fmap.out');
    try
        [~, fmap] = hdrload(full_name);
    catch
        disp('nao carregou');
    end
    
    % Agora, eu tenho que encontrar a DA
    %primeiro eu identifico quantos x e y existem
    npx = length(unique(fmap(:,1)));
    npy = size(fmap,1)/npx;
    %agora eu pego a coluna da frequencia x
    x = fmap(:,1);
    y = fmap(:,2);
    fx = fmap(:,3);
    % e a redimensiono para que todos os valores calculados para x iguais
    %fiquem na mesma coluna:
    x = reshape(x,npy,npx);
    y = reshape(y,npy,npx);
    fx = reshape(fx,npy,npx);
    % e vejo qual o primeiro valor nulo dessa frequencia, para identificar
    % a borda da DA
    y  = flipud(y);
    fx = flipud(fx);
    [~,ind] = min(fx,[],1);
    
    % por fim, defino a DA
    x = x(1,:);
    y = unique(y(ind,:)','rows');
    
    onda(end+1,:,:) = [x', y'];
    
    if (fmapdpFlag)
        full_name = fullfile(pathname,'fmapdp.out');
        try
            [~, fmapdp] = hdrload(full_name);
        catch
        end
        
        
        % Agora, eu tenho que encontrar a DA
        %primeiro eu identifico quantos x e y existem
        npe = length(unique(fmapdp(:,1)));
        npx = size(fmapdp,1)/npe;
        %agora eu pego a coluna da frequencia x
        en = fmapdp(:,1);
        x = fmapdp(:,2);
        fen = fmapdp(:,3);
        % e a redimensiono para que todos os valores calculados para x iguais
        %fiquem na mesma coluna:
        en = reshape(en,npx,npe);
        x = reshape(x,npx,npe);
        fen = reshape(fen,npx,npe);
        % e vejo qual o primeiro valor nulo dessa frequencia, para identificar
        % a borda da DA
        [~,ind] = min(fen,[],1);
        
        % por fim, defino a DA
        en = en(1,:);
        x = unique(x(ind,:)','rows');
        
        offda(end+1,:,:) = [en', x'];
    end
    
end%carrega e prepara os dados

onda_mean = mean(onda,1);
onda_rms = std(onda,1);
offda_mean = mean(offda,1);
offda_rms = std(offda,1);

esp_lin = 2;
size_font = 24;
limx = 12;
limy = 3.5;
lime = 6;

    transp = 0.4;
    color=0.4*ones(1,3);

linestyle_vec = {'--','-.','..'};
try
    linestyle = linestyle_vec{size(plot1,1) - nrecalls};
catch 
end
if first_call
    linestyle = '-';
end

% Create multiple lines using matrix input to plot

M = 1000*[(onda_rms(1,:,2)+onda_mean(1,:,2)), fliplr((onda_mean(1,:,2)-onda_rms(1,:,2)))];
X = 1000*[onda_mean(1,:,1), fliplr(onda_mean(1,:,1))];

if first_call
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
    if (nrecalls ~= 1)
        plot1 = zeros(nrecalls,2);
        plot1(1,1) = fill(X, M,color,'Parent',fa, 'LineStyle','none');
        alpha(plot1(1,1),transp);
        plot1(1,2) = plot(fa, 1000*onda_mean(1,:,1), 1000*onda_mean(1,:,2));
        set(plot1(1,2),'LineWidth',esp_lin,'Color','k', 'LineStyle',linestyle);
    else
        plot1 = zeros(1,2);
        plot1(1,1) = fill(X, M,color,'Parent',fa, 'LineStyle','none');
        alpha(plot1(1,1),transp);
        plot1(1,2) = plot(fa, 1000*onda_mean(1,:,1), 1000*onda_mean(1,:,2));
        set(plot1(1,2),'LineWidth',esp_lin,'Color','k', 'LineStyle',linestyle);
        xlim(fa,[-limx limx]);
        ylim(fa,[0 limy]);
        %          title(fa, {[pathname '/fmap.out']},'Interpreter','none','FontSize',size_font);
    end
else
    idx = size(plot1,1) + 1 - nrecalls;
    plot1(idx,1) = fill(X, M,color,'Parent',fa, 'LineStyle','none');
    alpha(plot1(idx,1),transp);
    plot1(idx,2) = plot(fa, 1000*onda_mean(1,:,1), 1000*onda_mean(1,:,2));
    set(plot1(idx,2),'LineWidth',esp_lin,'Color','k', 'LineStyle',linestyle);

    if nrecalls == 1
        cell_leg_text = {};
        for  ii=1:size(plot1,1)
            leg_text = inputdlg(['Digite a ', int2str(ii), '-esima legenda'],'Legenda',1);
            cell_leg_text(end+1) = leg_text;
        end
        legend1 = legend(plot1(:,2),'show',cell_leg_text);
        set(legend1, 'Location','NorthEast');
        xlim(fa, [-limx limx]);
        ylim(fa,[0 limy]);
    end
    %      title(fa, {[pathname '/fmap.out']},'Interpreter','none','FontSize',size_font);
end


if fmapdpFlag
    
    M = 1000*[(offda_rms(1,:,2)+offda_mean(1,:,2)); offda_mean(1,:,2); (offda_mean(1,:,2)-offda_rms(1,:,2))];
    X = 100*offda_mean(1,:,1);
    
    if first_call
        fdp=figure('OuterPosition',[xi yi xf yf]);
        fdpa = axes('Parent',fdp,'YGrid','on','XGrid','on','FontSize',size_font);
        box(fdpa,'on');
        hold(fdpa,'all');
        xlabel('dp [%]','FontSize',size_font);
        ylabel('x [mm]','FontSize',size_font);
        if (nrecalls ~= 1)
            plot1dp = zeros(nrecalls,3);
            plot1dp(1,:) = plot(fdpa, X, M, 'LineWidth',2,'LineStyle','--');
            set(plot1dp(1,1),'Color', color);
            set(plot1dp(1,2),'LineWidth',esp_lin,'Color',color, 'LineStyle','-');
            set(plot1dp(1,3),'Color', color);
        else
            plot1dp = zeros(1,3);
            plot1dp(1,:) = plot(fdpa, X, M, 'LineWidth',2,'LineStyle','--');
            set(plot1dp(1,1),'Color', color);
            set(plot1dp(1,2),'LineWidth',esp_lin,'Color',color, 'LineStyle','-');
            set(plot1dp(1,3),'Color', color);
            xlim(fdpa,[-lime lime]);
            ylim(fdpa,[-limx,0]);
            %              title(fdpa, {[pathname '/fmapdp.out']},'Interpreter','none','FontSize',size_font);
        end
    else
        
        plot1dp(idx,:) = plot(fdpa, X, M, 'LineWidth',2,'LineStyle','--');
        set(plot1dp(idx,1),'Color', color);
        set(plot1dp(idx,2),'LineWidth',esp_lin,'Color',color, 'LineStyle','-');
        set(plot1dp(idx,3),'Color', color);
        
        if nrecalls == 1
            legend2 = legend(plot1dp(:,2),'show',cell_leg_text);
            set(legend2, 'Location','SouthEast');
            xlim(fdpa, [-lime lime]);
            ylim(fdpa,[-limx,0]);
        end
        
       
        
    end
end

drawnow;

if (nrecalls ~= 1)
    tracy3_dynamic_aperture_4JSR(fmapdpFlag,nrecalls-1,nr_rms,fa,plot1,fdpa,plot1dp,path);
end
