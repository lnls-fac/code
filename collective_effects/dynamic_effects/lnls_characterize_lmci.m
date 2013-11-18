function lnls_characterize_lmci(ringdata,budget,I,sigma,n_azi,n_rad,nb,mu, save)
% lnls_characterize_lmci(ringdata,budget,I,sigma,n_azi,n_rad,nb,mu, save)

w = ringdata.w;

%% Load parameters

Zls    = 'Zl';
tau  = ringdata.taue;

imped  = 1:length(budget);
Zl = zeros(size(w));
for i=imped
    quant = budget{i}.quantity;
    Zl   = Zl + quant*budget{i}.(Zls);
end

stage    = ringdata.stage;
w0 = ringdata.w0;       % revolution angular frequency [Hz]
nus = ringdata.nus;     % synchrotron tune
eta = ringdata.eta;     % momentum compaction factor
E = ringdata.E;         % energy [GeV];

%% Calcula Longitudinal mode Coupling
tam = n_azi + 1 + n_azi + n_rad*(2*n_azi + 1);
delta = zeros(tam,length(I));

fprintf('Calculation of Longitudinal Mode Coupling Instability\n');
fprintf('%-20s: %-20.4g\n','Shynchrotron Tune', nus);
fprintf('%-20s: %-20d\n','Azimuthal Modes', n_azi);
fprintf('%-20s: %-20d\n','Radial Modes', n_rad);
fprintf('%-20s: %-20.4g\n\n','Damping Time [ms]', tau*1e3);
fprintf('I [mA]: '); fprintf('%-5.3g ', I*1e3);fprintf('\n');
fprintf('Stable? ');

delta = lnls_calc_longitudinal_mode_couplingopt(w, Zl, n_rad, n_azi, sigma, ...
    I, E, w0, nus, eta, nb, mu);

for i = 1:length(I)
    if any(imag(delta(:,i))*nus*w0*tau > 1)
        fprintf('%-6s','N');
    else
        fprintf('%-6s','Y');
    end
end
fprintf('\n\n');

%% Plot Results

% Create figure
figure1 = figure('OuterPosition',[66           0         929        1057]);

% Create axes
axes1 = axes('Parent',figure1,...
    'Position',[0.0653377630121816 0.0481310156240588 0.878183831672204 0.424150434269331]);
box(axes1,'on');
hold(axes1,'all');
% Create multiple lines using matrix input to plot
plot1 = plot(axes1, I*1e3, sort(real(delta),1));
% Create xlabel
xlabel({'Current per bunch [mA]'},'FontSize',12);
% Create ylabel
ylabel({'Re(\Omega/\omega_s)'},'FontSize',12);
% Create title
title({'Real Tune Shifts'});


% Create axes
axes2 = axes('Parent',figure1,...
    'Position',[0.0697674418604649 0.563326916471794 0.558139534883721 0.405367231638418]);
box(axes2,'on');
hold(axes2,'all');
% Create multiple lines using matrix input to plot
plot2 = plot(axes2, I*1e3,sort(imag(delta)*w0*nus*tau,1));
% Create xlabel
xlabel({'Current per bunch [mA]'},'FontSize',12);
% Create ylabel
ylabel({'\tau_{damp}/\tau_g'},'FontSize',12);
% Create title
title({'Growth Rates'});


% Create textbox
string = {'Plane: Longitudinal'};
string = [string , {'Impedances used:'}];
for i=imped
    string = [string, {sprintf('- %s', budget{i}.name)}];
    if isfield(budget{i},'wrl')
        string = [string, {sprintf('Rs = %3.1f kOhm  fr = %3.1f GHz  Q = %d', ...
            budget{i}.Rsl/1e3, budget{i}.wrl/2/pi/1e9, budget{i}.Ql)}];
    end
end
string = [string ,{' '}, {'Stage of the Machine:'}, {stage},{' '}];
% string = [string ,{' '},{' '}];
% if nb==1
%     string = [string , {'Mode of Operation:  Single Bunch'},{' '}];
% else
%     string = [string ,         {'Mode of Operation:  Multi-Bunch'}];
%     string = [string , {sprintf('     # of bunches:  %d',nb)}];
%     string = [string , {sprintf('     coupled mode:  %d',mu)}];
% end
% string = [string ,{' '},{' '}];
string = [string , {sprintf('Number of azimutal modes:  %d',n_azi)}];
string = [string , {sprintf('Number of radial modes:    %d',n_rad)}];

annotation(figure1,'textbox',...
    [0.672203765227021 0.567164179104478 0.264673311184935 0.399786780383795],...
    'String',string,...
    'FontSize',14,...
    'FitBoxToText','off');

if save
    saveas(figure1,['lmci_' ringdata.stage '.fig']);
end
