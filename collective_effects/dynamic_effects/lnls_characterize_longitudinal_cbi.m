function lnls_characterize_longitudinal_cbi(ringdata, budget, azi_modes, save)

w = ringdata.w;

%% Load parameters

tau  = ringdata.taue;
sigma = ringdata.sigma;
nb = ringdata.nb;
w0 = ringdata.w0; 
nus = ringdata.nus;
eta = ringdata.eta;
I_tot = ringdata.I_tot;
E = ringdata.E;

Zl = zeros(1,length(w));
imped  = 1:length(budget);

for j=imped
    Z     = budget{j}.Zl;
    quant = budget{j}.quantity;
    Zl    = Zl + Z*quant;
end

%% Calc coherent tune-shifts
fprintf('Calculation of Longitudinal Coupled Bunch Instability and Tune Shifts\n');
fprintf('%-20s: %-20.4g\n','Shynchrotron Tune', nus);
fprintf('%-20s: %-20.4g\n\n','Damping Time [ms]', tau*1e3);
fprintf('Number of unstable Modes Modes\n');
fprintf('%-5d ', azi_modes);fprintf('\n');
fprintf('%s',repmat('-',1,30)); fprintf('\n');

deltaw = [];

for m=azi_modes
    deltaw0 = lnls_calc_longitudinal_cbi(w, Zl, sigma, nb, w0, nus, eta, E, I_tot, m);
    deltaw = [ deltaw; deltaw0];
    n = imag(deltaw0) > 1/tau ;
    n = sum(n);
    fprintf('%-5d ',n);
end

fprintf('\n\n\n');

rel_tuneshift  = real(deltaw)/w0/nus;
rel_growth   = imag(deltaw)*tau;

%% Plot Results

% Create figure
scrsz = get(0,'ScreenSize');
figure1 = figure('OuterPosition',[scrsz(1)+100 scrsz(2)+300 scrsz(3)*0.9 scrsz(4)*0.5]);

h = 0.30;
v = 0.80;
hs = 0.055;
vs = 0.12;


% Create subplot
subplot11 = subplot(1,3,1,'Parent',figure1,'FontSize',16,'Position',[hs vs h v]);
box(subplot11,'on');
hold(subplot11,'all');
% Create multiple lines using matrix input to plot
plot11 = plot(subplot11, (1:nb)-1,rel_growth);
xlim([0 (nb-1)]);
xlabel({'Coupled Bunch Mode'},'FontSize',16);
ylabel({'\tau_{damp}/\tau_g'},'FontSize',16);
for i=1:length(azi_modes)
    leg = sprintf('m = %d',azi_modes(i));
    set(plot11(i),'DisplayName',leg);
end
% Create legend
legend11 = legend('show');
set(legend11);
%     'Position',[0.529848800834203 0.116465863453815 0.0848540145985393 0.12]);



% Create subplot
subplot12 = subplot(1,2,2,'Parent',figure1,'FontSize',16,'Position',[(5/2*hs+h) vs h v]);
box(subplot12,'on');
hold(subplot12,'all');
% Create multiple lines using matrix input to plot
plot12 = plot(subplot12, (1:nb)-1,rel_tuneshift);
xlim([0 (nb-1)]);
xlabel({'Coupled Bunch Mode'},'FontSize',16);
ylabel({'Re(\Omega - m*\nu_s)/\nu_s'},'FontSize',16);



% Create textbox

string = [{'Plane:Longitudinal'}, {' '}]; 

string = [string , {'Impedances used:'}];
for i=imped
    string = [string, {sprintf('- %s', budget{i}.name)}];
end
string = [string , {' '}, {'Stage of the Machine:'}, {ringdata.stage}];

annotation(figure1,'textbox',...
    [(hs*7/2+2*h) vs h*3/5 v],...
    'String',string,...
    'FontSize',16,...
    'FitBoxToText','off');

if save
    saveas(figure1,['longitudinal_cbi_' ringdata.stage '.fig']);
end
