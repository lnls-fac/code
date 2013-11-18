function lnls_characterize_transverse_cbi(ringdata, budget,plane, azi_modes, chrom, save)

w = ringdata.w;

%% Load parameters
if strcmp(plane,'v')
    betas = 'betay';
    Zts    = 'Zv';
    tau  = ringdata.tauy;
    nut = ringdata.nuty;
    label = 'Vertical';
else
    betas = 'betax';
    Zts    = 'Zh';
    tau  = ringdata.taux;
    nut = ringdata.nutx;
    label = 'Horizontal';
end

sigma = ringdata.sigma;
nb = ringdata.nb;
w0 = ringdata.w0; 
nus = ringdata.nus;
eta = ringdata.eta;
I_tot = ringdata.I_tot;
E = ringdata.E;

Zt = zeros(1,length(w));
imped  = 1:length(budget);

for j=imped
    Z     = budget{j}.(Zts);
    beta  = budget{j}.(betas);
    quant = budget{j}.quantity;
    Zt    = Zt + Z*beta*quant;
end

%% Calc coherent tune-shifts

fprintf('Calculation of %s Coupled Bunch Instability and Tune Shifts\n', label);
fprintf('%-20s: %-20.4g\n','Betatron Tune', nut);
fprintf('%-20s: %-20.4g\n\n','Damping Time [ms]', tau*1e3);
fprintf('%-7s # of unstable Modes Modes\n','Chrom');
fprintf('%-7s ',' ');fprintf('%-5d ', azi_modes);fprintf('\n');
fprintf('%s',repmat('-',1,40)); fprintf('\n');

imtune_shift = [];
retune_shift = [];
imidx = [];
reidx = [];
n_uns_modes = [];
for i=chrom
    g_rate = [];
    ig_rate = [];
    tu_shift = [];
    itu_shift = [];
    n_uns_mode = [];
    fprintf('%-5.3g:  ',i);
    for m=azi_modes
        deltaw = lnls_calc_transverse_cbi(w,Zt, sigma, nb, w0, nus, nut, i, eta, m, E, I_tot);
        [gmax igmax] = max(imag(deltaw));
        if i==0 && m==0;
            deltaw0 = deltaw;
        end
        g_rate = [g_rate, gmax];
        ig_rate = [ig_rate, igmax];
        [tumax itumax] = max(abs(real(deltaw)));
        tu_shift = [tu_shift, real(deltaw(itumax))];
        itu_shift = [itu_shift, itumax];
        n = imag(deltaw) > 1/tau ;
        n = sum(n);
        n_uns_mode = [n_uns_mode, n];
        fprintf('%-5d ',n);
    end
    fprintf('\n');
    imtune_shift = [imtune_shift; g_rate];
    imidx        = [imidx; ig_rate];
    retune_shift = [retune_shift; tu_shift];
    reidx        = [reidx; itu_shift];
    n_uns_modes  = [n_uns_modes; n_uns_mode];
end
fprintf('\n\n');
rel_tuneshift = retune_shift'/w0/nus;
rel_tuneshift0  = real(deltaw0)/w0/nus;
rel_growth    = imtune_shift'*tau;
rel_growth0   = imag(deltaw0)*tau;

%% Plot Results

% Create figure
scrsz = get(0,'ScreenSize');
figure1 = figure('OuterPosition',[scrsz(1)+100 scrsz(2)+40 scrsz(3)*0.9 scrsz(4)*0.9]);

h = 0.27;
v = 0.39;
hs = 0.055;
vs = 0.09;

% Create subplot
subplot11 = subplot(2,3,1,'Parent',figure1,'FontSize',16,'Position',[hs (2*vs+v) h v]);
box(subplot11,'on');
hold(subplot11,'all');
% Create multiple lines using matrix input to plot
plot11 = plot(subplot11, chrom,rel_tuneshift);
for i=1:length(azi_modes)
    leg = sprintf('m = %d',azi_modes(i));
    set(plot11(i),'DisplayName',leg);
end
% Create xlabel
xlabel({'Chromaticity'},'FontSize',16);
% Create ylabel
ylabel({'Re(\Omega - \nu_b)/\nu_s'},'FontSize',16);
% Create title
title({'Tune Shift of the most shifted coupled bunch mode'},'FontSize',16);
% Create legend
legend11 = legend('show');
set(legend11,...
    'Position',[0.529848800834203 0.116465863453815 0.0848540145985393 0.12]);



% Create subplot
subplot21 = subplot(2,3,4,'Parent',figure1,'FontSize',16,'Position',[hs vs*2/3 h v]);
box(subplot21,'on');
hold(subplot21,'all');
% Create multiple lines using matrix input to plot
plot21 = plot(subplot21, (1:nb)-1,rel_tuneshift0);
xlim([0 (nb-1)]);
% Create xlabel
xlabel({'Coupled Bunch Mode'},'FontSize',16);
% Create ylabel
ylabel({'Re(\Omega - \nu_b)/\nu_s'},'FontSize',16);
% Create title
title({'Tune shifts @ zero chromaticity and m=0'},'FontSize',16);


% Create subplot
subplot13 = subplot(2,3,3,'Parent',figure1,'FontSize',16,'Position',[(3*hs+2*h) (2*vs+v) h v]);
box(subplot13,'on');
hold(subplot13,'all');
% Create multiple lines using matrix input to plot
plot(subplot13, chrom,rel_growth);
% Create xlabel
xlabel({'Chromaticity'},'FontSize',16);
% Create ylabel
ylabel({'\tau_{damp}/\tau_g'},'FontSize',16);
% Create title
title({'Growth Rates of the most unstable coupled bunch mode'},'FontSize',16);
% Create legend

% Create subplot
subplot23 = subplot(2,3,6,'Parent',figure1,'FontSize',16,'Position',[(3*hs+2*h) vs*2/3 h v]);
box(subplot23,'on');
hold(subplot23,'all');
% Create multiple lines using matrix input to plot
plot23 = plot(subplot23, (1:nb)-1,rel_growth0);
xlim([0 (nb-1)]);
% Create xlabel
xlabel({'Coupled Bunch Mode'},'FontSize',16);
% Create ylabel
ylabel({'\tau_{damp}/\tau_g'},'FontSize',16);
% Create title
title({'Growth rates @ zero chromaticity and m=0'},'FontSize',16);

% Create subplot
subplot12 = subplot(2,3,2,'Parent',figure1,'FontSize',16,'Position',[(2*hs+h) (2*vs+v) h v]);
box(subplot12,'on');
hold(subplot12,'all');
% Create multiple lines using matrix input to plot
plot12 = plot(subplot12, chrom,n_uns_modes');
% Create xlabel
xlabel({'Chromaticity'},'FontSize',16);
% Create ylabel
ylabel({'#'},'FontSize',16);
% Create title
title({'Number of Unstable Coupled Bunch Modes'},'FontSize',16);

% Create textbox

if strcmp(plane,'v')
    string = [{'Plane: Vertical'}, {' '}]; 
else
    string = [{'Plane: Horizontal'}, {' '}]; 
end
string = [string , {'Impedances used:'}];
for i=imped
    string = [string, {sprintf('- %s', budget{i}.name)}];
end
string = [string , {' '}, {'Stage of the Machine:'}, {ringdata.stage}];

annotation(figure1,'textbox',...
    [(hs*3/2+h) vs h*3/5 v],...
    'String',string,...
    'FontSize',16,...
    'FitBoxToText','off');

if save
    saveas(figure1,['transverse_cbi_' plane '_' ringdata.stage '.fig']);
end
