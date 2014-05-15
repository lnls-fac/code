function varargout = lnls_characterize_tmci(ringdata,budget,I,sigma,plane,n_azi,n_rad,chrom,nb,mu, save)

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

imped  = 1:length(budget);
Zt = zeros(size(w));
for i=imped
    Zt   = Zt + budget{i}.quantity*budget{i}.(Zts)*budget{i}.(betas);
end

stage    = ringdata.stage;
w0 = ringdata.w0;       % revolution angular frequency [Hz]
nus = ringdata.nus;     % synchrotron tune
eta = ringdata.eta;     % momentum compaction factor
E = ringdata.E;         % energy [GeV];

%% Calcula Transeverse mode Coupling
fprintf('Calculation of %s Mode Coupling Instability\n', label);
fprintf('%-20s: %-20.4g\n','Betatron Tune', nut);
fprintf('%-20s: %-20.4g\n','Chromaticity', chrom);
fprintf('%-20s: %-20d\n','Azimuthal Modes', n_azi);
fprintf('%-20s: %-20d\n','Radial Modes', n_rad);
fprintf('%-20s: %-20.4g\n\n','Damping Time [ms]', tau*1e3);
fprintf('I [mA]: '); fprintf('%-5.3g ', I*1e3);fprintf('\n');
fprintf('Stable? ');


delta =lnls_calc_transverse_mode_couplingopt(w, Zt, n_rad, n_azi, sigma, ...
    I, E, w0, nut, nus, eta, chrom, nb, mu);

first = true;
for i = 1:length(I)
    if any(imag(delta(:,i))*nus*w0*tau > 1)
        fprintf('%-6s','N');
        if first
            varargout{1} = I(i);
        end
        first = false;
    else
        fprintf('%-6s','Y');
    end
end
fprintf('\n\n\n');

%% Plot Results

% [real_delta ind] = sort(real(delta));
% for j = 1:size(delta,2)
%     imag_delta(:,j) = imag(delta(ind(:,j),j));
% end
[real_delta, ~] = sort(real(delta));
[imag_delta, ~] = sort(imag(delta));


% Create figure
figure1 = figure('OuterPosition',[66           0         929        1057]);

% Create axes
axes1 = axes('Parent',figure1,...
    'Position',[0.0653377630121816 0.0481310156240588 0.878183831672204 0.424150434269331]);
box(axes1,'on');
hold(axes1,'all');
% Create multiple lines using matrix input to plot
plot1 = plot(axes1, I*1e3, real_delta);
% Create xlabel
xlabel({'Current per bunch [mA]'},'FontSize',12);
% Create ylabel
ylabel({'Re(\Omega - \omega_\beta)/\omega_s'},'FontSize',12);
% Create title
title({'Real Tune Shifts'});


% Create axes
axes2 = axes('Parent',figure1,...
    'Position',[0.0697674418604649 0.563326916471794 0.558139534883721 0.405367231638418]);
box(axes2,'on');
hold(axes2,'all');
% Create multiple lines using matrix input to plot
plot2 = plot(axes2, I*1e3, imag_delta*nus*w0*tau);
% Create xlabel
xlabel({'Current per bunch [mA]'},'FontSize',12);
% Create ylabel
ylabel({'\tau_{damp}/\tau_g'},'FontSize',12);
% Create title
title({'Growth Rates'});


% Create textbox
string = {};
if strcmp(plane,'v'), 
    string = [string, {'Plane: Vertical'},{' '}]; 
else
    string = [string, {'Plane: Horizontal'},{' '}];
end;
string = [string , {'Impedances used:'}];
for i=imped
    string = [string, {sprintf('- %s', budget{i}.name)}];
end
string = [string ,{' '}, {'Stage of the Machine:'}, {stage},{' '}];
% string = [string ,{' '},{' '}];
string = [string , {sprintf('Chromaticity:  %3.2f', chrom)},{' '}];
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
    saveas(figure1,['tmci_' plane '_' ringdata.stage '.fig']);
end
