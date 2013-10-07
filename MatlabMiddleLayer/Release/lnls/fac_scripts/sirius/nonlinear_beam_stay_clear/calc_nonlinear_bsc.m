function calc_nonlinear_bsc(the_ring, n_per, cam_vac)
% calc_nonlinear_bsc(the_ring, nper, cam_vac)
%
% calcula o beam stay clear nao linear para o primeiro superperiodo da rede
% the_ring, que possui n_per periodos. cam_vac eh o valor do raio da camara
% ao long do anel. O calculo deve ser rodado da pasta onde queira-se que os
% dados sejam salvos.



% vamos escolher um nome para o arquivo que sera salvo
name = 'marker_quad';

%agora, vamos selecionar os pontos em que sera calculada a AD
% quero calcular para todos os markers e quadrupolos do 1o super periodo:
spos = findspos(the_ring,1:(length(the_ring)+1));
super_per = spos <= ((spos(end)+0.01)/n_per);
points = findcells(the_ring(super_per),'PassMethod','IdentityPass');
points = points(2:end); % nao quero o marker 'inicio'

points2 = findcells(the_ring(super_per),'K');
points3 = findcells(the_ring(super_per),'BendingAngle');
points2 = setdiff(points2,points3);
points = sort([points, points2]);

%Define sposition of the calculated points
spos = spos(points);


%pedir confimacao de calculo, para dificultar possiveis absurdos
resp = 'n';
while ~strcmp(resp,'s')
    prompt = sprintf('calcular o bsc nao linear para %d pontos da rede?(s/n): ', ...
        length(points));
    resp = input(prompt, 's');
    if strcmp(resp,'n')
        return
    end
end

%agora, tenho que preparar os arquivos para o calculo
%primeiro vamos definir as condicoes iniciais de varredura:
np = 121;

% e quantas voltas eu quero dar
nturns = 500;

% preciso desnormalizar pelo gammax, para que no ponto de beta maximo a
% varredura va ate 12mm.
twissdata = twissring(the_ring(1:points(end)),0,1:points(end)); 
spos_twi = cat(1,twissdata.SPos)';
beta   = cat(1,twissdata.beta);     alpha  = cat(1,twissdata.alpha);
betax  = beta(:,1)';                 betay  = beta(:,2)'; 
alphax = alpha(:,1)';                alphay = alpha(:,2)';
gammax = (1+alphax.^2)./betax;      gammay = (1+alphay.^2)./betay;
[mingammax, ~] = min(gammax);    [mingammay, ~] = min(gammay);
x0 = 1.2*linspace(-cam_vac,cam_vac,np)*sqrt(mingammax);
y0 = 1.2*linspace(-cam_vac,cam_vac,np)*sqrt(mingammay);

%nao quero que as particulas andem exatamente na linha y=0 e x=0 para
%as varreduras em x e y, respectivamente, entao vou gerar uma
%distribuicao gaussiana sigma 0.1mm com corte em um sigma:
y0_rand = get_random_numbers(0.1e-3, np, 1)'*sqrt(mingammay);
x0_rand = get_random_numbers(0.1e-3, np, 1)'*sqrt(mingammax);


bsch_pos = zeros(1,length(points));
bsch_neg = zeros(1,length(points));
bscv_pos = zeros(1,length(points));
bscv_neg = zeros(1,length(points));
fprintf('\n\nOlha, nao bota toda sua feh no que eu vou falar agora nao.\n');
fprintf('Se for pra apostar...\n');
sleep(5);
fprintf('Serio, nao aposte!\n');
fprintf('Mas eu acho que pra terminar, como ja foram\n');
for ii=1:length(points)
    %estimativa de tempo de calculo
    fprintf('%2d calculos de %2d, ainda faltam %5f minutos\n',ii-1,...
        length(points),15/100*nturns/60*(length(points)-ii+1));
    
    % primeiro vamos shiftar a rede para comecar no ponto de calculo
    ind = [points(ii):(length(the_ring)-1) 2:(points(ii)-1)];
    the_ring_calc = the_ring([1 ind end]);
    
    %agora, vamos reescalar a varredura, para ter a mesma precisao:
    x0_rees = x0/sqrt(gammax(points(ii)));
    y0_rees = y0/sqrt(gammay(points(ii)));
    x_rand = x0_rand/sqrt(gammax(points(ii)));
    y_rand = y0_rand/sqrt(gammay(points(ii)));
    
    % agora eu monto as condicoes iniciais
    Rin = [[x0_rees; zeros(1,np);y_rand;zeros(3,np)] [x_rand; zeros(1,np);y0_rees;zeros(3,np)]];
    
    
    %primeiro eu faco um tracking detalhado para ver se as particulas estao
    %furando a camara de vacuo
    Rout=Rin;
    len_ring = length(the_ring_calc);
    nt_det =60; %tempo para elas darem mais de 3 voltas no espaco de fase
    if 3*nt_det >= nturns
        error('Coloque mais voltas em nturns que 3*nt_det');
    end
    for i =1:nt_det
        %track
        Rout = linepass(the_ring_calc,Rout,1:len_ring);
        % look to x and y along all ring if it hit the vac_cham
        ind = (abs(Rout([1 3],:)) >= cam_vac);
        %if x or y hit
        ind = any(ind);
        % at any point of the ring
        ind = any(reshape(ind,length(ind)/len_ring,len_ring)');
        % or if the particle is lost by other means
        Rout = Rout(:,(end-length(ind)+1):end);
        ind = ind | isnan(Rout(1,:));
        %I exclude it from the next tracking
        Rout = Rout(:,~ind);
    end
    %quantas particulas nao foram perdidas
    part_left = size(Rout,2);
    %faz o tracking de varias voltas no anel
    Rout = ringpass(the_ring_calc,Rout,nturns-nt_det);
    
    %agora eu vejo se ele passou a camara de vacuo naquele ponto
    ind = (abs(Rout([1 3],:)) >= cam_vac);
    ind = any(ind); %se passou em x ou y
    ind = reshape(ind,part_left,nturns-nt_det)'; %em alguma das voltas
    ind = any(ind);
    Rout = Rout(:,repmat(~ind,1,nturns-nt_det)); %excluo do vetor saida
    
    %calculo o beam stay clear:
    bsch_pos(ii) = max(Rout(1,:));
    bsch_neg(ii) = min(Rout(1,:));
    bscv_pos(ii) = max(Rout(3,:));
    bscv_neg(ii) = min(Rout(3,:));
    
    %quero plotar o espaco de fase no mc para mostrar a varredura
    if strcmp(the_ring_calc{2}.FamName,'mc');
        part_left = size(Rout,2)/(nturns-nt_det);
        x = reshape(Rout(1,:),part_left,nturns-nt_det)';
        xp = reshape(Rout(2,:),part_left,nturns-nt_det)';
        figure; plot(x,xp,'Marker','.','LineStyle','none'); xlabel('x');ylabel('xp');
        y = reshape(Rout(3,:),part_left,nturns-nt_det)';
        yp = reshape(Rout(4,:),part_left,nturns-nt_det)';
        figure; plot(y,yp,'Marker','.','LineStyle','none'); xlabel('y');ylabel('yp');
        figure; plot(x,y,'Marker','.','LineStyle','none'); xlabel('x');ylabel('y');
        drawnow;
    end   
end

% vamos salvar os dados do BSC nao linear:
save(sprintf('%s',[date name]),'the_ring','points','bsch_pos','bsch_neg','bscv_pos','bscv_neg');


%por fim, vamos gerar um arquivo com o bsc nao linear
fp = fopen('nonlinear_bsc.txt','w');
fprintf(fp,'Beam Stay Clear nao-linear para a rede Sirius_v403-ac20_2\n\n');
fprintf(fp,'Pontos para os quais foi calculado: centro trechos retos, centro dipolos, BPMs, comeco quadrupolos\n\n');
fprintf(fp,'%10s   %11s   %11s   %11s   %11s\n','Position [m]','BSC_Hp [mm]','BSC_Hn [mm]','BSC_Vp [mm]','BSC_Vn [mm]');
fprintf(fp,'%10.5g   %11.5g   %11.5g   %11.5g   %11.5g\n',[spos;[bsch_pos;bsch_neg;bscv_pos;bscv_neg]*1e3]);
fclose(fp);


% vamos calcular o bsc linear para comparar os resultados:
bschl = cam_vac * sqrt(betax/max(betax));
bscvl = cam_vac * sqrt(betay/max(betay));


% também, vamos calcular o não linear, escalado linearmente
[betamax ind] = max(betax(points));
bschnl_pos    = bsch_pos(ind)*sqrt(betax/betamax);
bschnl_neg    = bsch_neg(ind)*sqrt(betax/betamax);
[betamay ind] = max(betay(points));
bscvnl_pos    = bscv_pos(ind)*sqrt(betay/betamay);
bscvnl_neg    = bscv_neg(ind)*sqrt(betay/betamay);


%plota os resultados
fig = figure('OuterPosition',get(0,'screenSize'));

 axes_bscv = subplot(2,1,1,'Parent',fig,'YGrid','on','FontSize',16);
box(axes_bscv,'on');
hold on
plot1(:,1) = plot(spos,[bscv_pos;bscv_neg]*1e3,'MarkerSize',10,'Marker','.','Color','b');
plot1(:,2) = plot(spos_twi,[bscvnl_pos;bscvnl_neg]*1e3,'Color','g');
plot1(:,3) = plot(spos_twi,[bscvl;-bscvl]*1e3,'Color','r');
drawlattice(0,1,axes_bscv,spos(end));
xlabel('Position [m]');
xlim([spos(1) spos(end)]);
ylabel('Vertical Beam Stay Clear [mm]');
legend(plot1(1,:),'show',{'non-linear';'misto';'linear'});


axes_bsch = subplot(2,1,2,'Parent',fig,'YGrid','on','FontSize',16);
box(axes_bsch,'on');
hold on
plot(spos,[bsch_pos;bsch_neg]*1e3,'MarkerSize',10,'Marker','.','Color','b');
plot(spos_twi,[bschnl_pos;bschnl_neg]*1e3,'Color','g');
plot(spos_twi,[bschl;-bschl]*1e3,'Color','r');
drawlattice(0,1,axes_bsch,spos(end));
xlabel('Position [m]');
xlim([spos(1) spos(end)]);
ylabel('Horizontal Beam Stay Clear [mm]');



function rndnr = get_random_numbers(sigma, nrels, cutoff)

%distribuicao uniforme truncada em sqrt(3) sigma:
% rndnr = sqrt(3)*sigma * 2 * (rand(1, nrels) - 0.5);


max_value = cutoff;

rndnr = zeros(nrels,1);
sel = 1:nrels;
while ~isempty(sel)
    rndnr(sel) = randn(1,length(sel));
    sel = find(abs(rndnr) > max_value);
end
rndnr = sigma * rndnr;

