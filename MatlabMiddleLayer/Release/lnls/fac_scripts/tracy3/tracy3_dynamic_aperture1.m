function tracy3_dynamic_aperture1(fmapdpFlag)

f=figure;
fa = axes('Parent',f,'YGrid','on','XGrid','on');
box(fa,'on');
hold(fa,'all');
xlabel('x [mm]','FontSize',20);
ylabel('z [mm]','FontSize',20);

if(fmapdpFlag)
    fdp=figure;
    fdpa = axes('Parent',fdp,'YGrid','on','XGrid','on');
    box(fdpa,'on');
    hold(fdpa,'all');
    xlabel('dp [%]','FontSize',20);
    ylabel('x [mm]','FontSize',20);
end

%path = ['/home/ABTLUS/liu/Sirius/SiriusB1LE/bare/physap/'];
%default = '/home/ABTLUS/fernando.sa/redes_tracy/Sirius/Sirius_v200/';
default = '/opt/sirius_tracy/';

drawnow;

path = uigetdir(default,'Em qual pasta estao os dados?');
if (path==0);
    path = default;
else
    path = [path '/'];
end;
% path = ['/home/ABTLUS/fernando.sa/redes_tracy/Booster/Boo03_02/multipolos/1ra_simulacao_mais_rms_vaccham/'];

[status result] = system(['ls ' path '| grep rms | wc -l']);
n_pastas = str2double(result);

for i=1:n_pastas
%pathname = uigetdir(pwd,'Em qual pasta est�o os dados?');
    diretorio = sprintf('rms%02d',i);
    pathname = [path diretorio '/'];
    full_name = fullfile(pathname,'fmap.out');
    [~, fmap] = hdrload(full_name);
    
    
    
    for j=1:length(fmap')
        if fmap(j,1) ~= fmap(1,1)
            k=j-1;
            break;
        end
    end
    l = length(fmap')/k;
    
    abertura = [];
    for j=0:(l-1)
        m=k;
        controle=0;
        while ((controle < 1) && (m>=1))
            if (fmap(j*k+m,3)==0)
                controle=controle+1;
            end
            m=m-1;
        end
        abertura=[abertura; fmap(j*k+m+1,:)];
    end
    
    plot(fa,1000*abertura(:,1),1000*abertura(:,2));%,'DisplayName',diretorio);
    title(fa,{full_name},'Interpreter','none','FontSize',30);
    
    if (fmapdpFlag)
        full_name = fullfile(pathname,'fmapdp.out');
        [~, fmapdp] = hdrload(full_name);
        
        
        teste=fmapdp(1,1);
        for j=1:length(fmapdp')
            if fmapdp(j,1) ~= teste
                k=j-1;
                break;
            end
        end
        l = length(fmapdp')/k;
        
        abertura = [];
        for j=0:(l-1)
            m=1;
            controle=0;
            while ((controle < 1) && (m<=k))
                if (fmapdp(j*k+m,3)==0)
                    controle=controle+1;
                end
                m=m+1;
            end
            abertura=[abertura; fmapdp(j*k+m-1,:)];
        end
        
        
        plot(fdpa,100*abertura(:,1),1000*abertura(:,2));%,'DisplayName',diretorios{i});
        title(fdpa,{full_name},'Interpreter','none','FontSize',30);
    end
    
end

% legend1 = legend(fa,'show');
% set(legend1,...
%     'Position',[0.727810304449646 0.183255269320842 0.13521662763466 0.341256830601093]);
% 
% if fmapdpFlag
%     legend2 = legend(fdpa,'show');
%     set(legend2,...
%         'Position',[0.727810304449646 0.183255269320842 0.13521662763466 0.341256830601093]);
end
