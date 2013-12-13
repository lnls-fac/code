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

if strcmp(escalax,'log')
    indx = w > 0 ;
    w  =  w(:,indx);
    Zv = Zv(:,indx);
    Zh = Zh(:,indx);
    Zl = Zl(:,indx);
end
% if strcmp(escalay,'log')
%     indl = imag(-Zl) > 0;
%     indv = imag(-Zv) > 0;
%     indh = imag(-Zh) > 0;
%     ind = ~any(~(indl & indv & indh));
%     w  =  w(:,ind);
%     Zv = Zv(:,ind);
%     Zh = Zh(:,ind);
%     Zl = Zl(:,ind);
% end


% Create figure
scrsz = get(0,'ScreenSize');
figure1 = figure('OuterPosition',[scrsz(1)+100 scrsz(2)+40 scrsz(3)*0.9 scrsz(4)*0.9]);

h = 0.27;
v = 0.39;
hs = 0.055;
vs = 0.095;


%% Horizontal Plane
% Create subplot
subplot11 = subplot(2,3,1,'Parent',figure1,'XScale',escalax,...
    'YScale',escalay,'XMinorTick','on','FontSize',16,'Position',[hs (2*vs+v) h v]);
% Uncomment the following line to preserve the Y-limits of the axes
% ylim(subplot1,[-3000000 3000000]);
box(subplot11,'on');
hold(subplot11,'all');
% Create multiple lines using matrix input to semilogx
semilogx11 = semilogx(w,-imag(Zh),'Parent',subplot11);
for i=1:length(budget)
    set(semilogx11(i),'DisplayName',budget{i}.name);
end
% Create xlabel
xlabel('\omega [rad/s]','FontSize',16);
% Create ylabel
if mult_beta
    ylabel('-Im(\beta_x Z_{x}) [\Omega]','FontSize',16);
else
    ylabel('-Im(Z_{x}) [\Omega/m]','FontSize',16);
end
% Create legend
legend1 = legend(subplot11,'show');


% Create subplot
subplot21 = subplot(2,3,4,'Parent',figure1,'XScale',escalax,...
    'YScale',escalay,'XMinorTick','on','FontSize',16,'Position',[hs vs h v]);
% Uncomment the following line to preserve the Y-limits of the axes
% ylim(subplot1,[-3000000 3000000]);
box(subplot21,'on');
hold(subplot21,'all');
% Create multiple lines using matrix input to semilogx
semilogx21 = semilogx(w,real(Zh),'Parent',subplot21);
for i=1:length(budget)
    set(semilogx21(i),'DisplayName',budget{i}.name);
end
% Create xlabel
xlabel('\omega [rad/s]','FontSize',16);
% Create ylabel
if mult_beta
    ylabel('Re(\beta_x Z_{x}) [\Omega]','FontSize',16);
else
    ylabel('Re(Z_{x}) [\Omega/m]','FontSize',16);
end


%% Vertical Plane
% Create subplot
subplot12 = subplot(2,3,2,'Parent',figure1,'XScale',escalax,...
    'YScale',escalay,'XMinorTick','on','FontSize',16,'Position',[(2*hs+h) (2*vs+v) h v]);
% Uncomment the following line to preserve the Y-limits of the axes
% ylim(subplot1,[-3000000 3000000]);
box(subplot12,'on');
hold(subplot12,'all');
% Create multiple lines using matrix input to semilogx
semilogx12 = semilogx(w,-imag(Zv),'Parent',subplot12);
for i=1:length(budget)
    set(semilogx12(i),'DisplayName',budget{i}.name);
end
% Create xlabel
xlabel('\omega [rad/s]','FontSize',16);
% Create ylabel
if mult_beta
    ylabel('-Im(\beta_y Z_{y}) [\Omega]','FontSize',16);
else
    ylabel('-Im(Z_{y}) [\Omega/m]','FontSize',16);
end

% Create subplot
subplot22 = subplot(2,3,5,'Parent',figure1,'XScale',escalax,...
    'YScale',escalay,'XMinorTick','on','FontSize',16,'Position',[(2*hs+h) vs h v]);
% Uncomment the following line to preserve the Y-limits of the axes
% ylim(subplot1,[-3000000 3000000]);
box(subplot22,'on');
hold(subplot22,'all');
% Create multiple lines using matrix input to semilogx
semilogx22 = semilogx(w,real(Zv),'Parent',subplot22);
for i=1:length(budget)
    set(semilogx22(i),'DisplayName',budget{i}.name);
end
% Create xlabel
xlabel('\omega [rad/s]','FontSize',16);
% Create ylabel

if mult_beta
    ylabel('Re(\beta_y Z_{y}) [\Omega]','FontSize',16);
else
    ylabel('Re(Z_{y}) [\Omega/m]','FontSize',16);
end


%% Longitudinal Plane
% Create subplot
subplot13 = subplot(2,3,3,'Parent',figure1,'XScale',escalax,...
    'YScale',escalay,'XMinorTick','on','FontSize',16,'Position',[(3*hs+2*h) (2*vs+v) h v]);
% Uncomment the following line to preserve the Y-limits of the axes
% ylim(subplot1,[-3000000 3000000]);
box(subplot13,'on');
hold(subplot13,'all');
% Create multiple lines using matrix input to semilogx
semilogx13 = semilogx(w,-imag(Zl),'Parent',subplot13);
for i=1:length(budget)
    set(semilogx13(i),'DisplayName',budget{i}.name);
end
% Create xlabel
xlabel('\omega [rad/s]','FontSize',16);
% Create ylabel
ylabel('-Im(Z_{L}) [\Omega]','FontSize',16);


% Create subplot
subplot23 = subplot(2,3,6,'Parent',figure1,'XScale',escalax,...
    'YScale',escalay,'XMinorTick','on','FontSize',16,'Position',[(3*hs+2*h) vs h v]);
% Uncomment the following line to preserve the Y-limits of the axes
% ylim(subplot1,[-3000000 3000000]);
box(subplot23,'on');
hold(subplot23,'all');
% Create multiple lines using matrix input to semilogx
semilogx23 = semilogx(w,real(Zl),'Parent',subplot23);
for i=1:length(budget)
    set(semilogx23(i),'DisplayName',budget{i}.name);
end
% Create xlabel
xlabel('\omega [rad/s]','FontSize',16);
% Create ylabel
ylabel('Re(Z_{L}) [\Omega]','FontSize',16);

if save
    if ~exist('name','var')
        name = 'no_name';
    end
    saveas(figure1,['impedance_' name '.fig']);
end

