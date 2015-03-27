function plot_impedances(w, budget, escalax, escalay, mult_beta, save, name)
% Funcao que plota impedancias:
% plot_impedances(w, budget, escalax, escalay, mult_beta, save)
%
% Inputs:
% - budget eh uma array de celulas, sendo que cada celula contem uma estrutura
%   com os seguintes campos obrigatorios:
%       name = nome do elemento ao qual a impedancia pertence
%       Zl = impedancia longitudinal [Ohm]
%       Zv = impedancia vertical [Ohm/m]
%       Zh = impedancia horizontal [Ohm/m]
%       w  = frequencia angular [rad/s]
%       quantity = n??mero desse elemento no anel
%       betax = beta horizontal media nas posicoes desses elementos
%       betay = beta vertical media nas posicoes desses elementos
% - escalax = escolha se a escala x sera logaritmica, 'log', ou 'linear'
% - escalay = escolha se a escala y sera logaritmica, 'log', ou 'linear'
% - mult_beta = escolha se deve-se plotar Zt ou betat*Zt. true ou false

Zh = zeros(length(budget),length(w));
Zv = Zh;
Zl = Zh;
if mult_beta
    for i=1:length(budget)
        Zh(i,:) = budget{i}.Zh*budget{i}.quantity*budget{i}.betax;
        Zv(i,:) = budget{i}.Zv*budget{i}.quantity*budget{i}.betay;
        Zl(i,:) = budget{i}.Zl*budget{i}.quantity;
    end
else
    for i=1:length(budget)
        Zh(i,:) = budget{i}.Zh*budget{i}.quantity;
        Zv(i,:) = budget{i}.Zv*budget{i}.quantity;
        Zl(i,:) = budget{i}.Zl*budget{i}.quantity;
    end
end

DispNames = getcellstruct(budget,'name',1:length(budget));
labelx = 'bla';
labely = 'blo';

create_figures(w, Zl, escalax, escalay, labelx, labely, DispNames, save, name);

create_figures(w, Zh, escalax, escalay, labelx, labely, DispNames, save, name);

create_figures(w, Zv, escalax, escalay, labelx, labely, DispNames, save, name);



function create_figures(w, Z, scalex, scaley, labelx, labely, DispNames, save, name)

if strcmp(scalex,'log')
    indx = w > 0 ;
    w = w(:,indx);
    Z = Z(:,indx);
end
w = repmat(w,size(Z,1),1);
indp = ones(size(Z));
indn = [];
IZpos = imag(-Z);
IZneg = imag(Z);
if strcmp(scaley,'log')
    indn = imag(-Z) < 0;
    indp = imag(-Z) > 0;
    IZpos(indn) = 0;
    IZneg(indp) = 0;
end


% Create figure
f1 = figure('Position',[1,1,1100,680]);


% Real Axes
axes1 = axes('Parent',f1,'Position',[0.088 0.103 0.885 0.432],...
    'FontSize',16, 'YScale',scaley,'YMinorTick','on',...
                   'XScale',scalex,'XMinorTick','on');
box(axes1,'on'); hold(axes1,'all'); grid(axes1,'on');

plot(w',abs(real(Z))','Parent',axes1,'LineWidth',2);
xlabel(labelx,'FontSize',16);
ylabel(['Re(',labely,') [\Omega]'],'FontSize',16);
xlim(axes1,[min(w(:));            max(w(:))]);
ylim(axes1,[min(abs(real(Z(:)))); max(abs(real(Z(:))))]);



% Imaginary Axes
axes2 = axes('Parent',f1,'Position',[0.088 0.536 0.885 0.432],...
    'FontSize',16,'YScale',scaley,'YMinorTick','on',...
                  'XScale',scalex,'XMinorTick','on',...
    'XTickLabel',{''});
box(axes2,'on');hold(axes2,'all');grid(axes2,'on');

plot1 = zeros(1,size(Z,1));
for i=1:size(Z,1)
    plot1(i) = plot(w(i,:),IZpos(i,:),'Parent',axes2,'LineWidth',2,...
                    'DisplayName',DispNames{i});
end
legend(axes2,'show','Location','Best');
for i=1:size(Z,1)
plot(w(i,:),IZneg(i,:),'Parent',axes2,'LineWidth',2,...
    'Color',get(plot1(i),'Color'),'LineStyle','--');
end
ylabel(['-Im(',labely,') [\Omega]'],'FontSize',16);
xlim(axes2,[min([w(indp);w(indn)]), max([w(indp);w(indn)])]);
ylim(axes2,[min([IZpos(indp); IZneg(indn)]), ...
            max([IZpos(indp); IZneg(indn)])]);

if save
    if ~exist('name','var')
        name = 'no_name';
    end
    saveas(f1,['impedance_' name '.fig']);
end

