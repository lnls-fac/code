function study_residual_dispersion_and_beamsize

%clc; close('all'); drawnow;
filename = fullfile('CONFIG_V403_AC10_5','CONFIG_V403_AC10_5.mat');
load(filename);

coupling = 1.0 / 100;


% nominal lattices
the_ring = r.params.the_ring;
[~,the_ring] = setcavity('on', the_ring);
[~,~,~,~,~,~,the_ring] = setradiation('on', the_ring);
twiss = twissring(the_ring, 0, 1:length(the_ring), 'chrom');
s    = [twiss.SPos];
eta  = [twiss.Dispersion];
beta = reshape([twiss.beta],2,[]); 
ats = atsummary(the_ring);
sigmay0(1,:) = sqrt(ats.naturalEmittance * beta(2,:) * coupling + (eta(3,:) * ats.naturalEnergySpread).^2);

mia   = findcells(the_ring, 'FamName', 'mia');
mib   = findcells(the_ring, 'FamName', 'mib');
mc    = findcells(the_ring, 'FamName', 'mc');
rspls = sort([mia mib mc]); 

% random lattices
for i=1:length(r.machine)
    the_ring = r.machine{i};
    [~,the_ring] = setcavity('on', the_ring);
    [~,~,~,~,~,~,the_ring] = setradiation('on', the_ring);
    twiss = twissring(the_ring, 0, 1:length(the_ring), 'chrom');
    eta  = [twiss.Dispersion];
    beta = reshape([twiss.beta],2,[]);
    ats = atsummary(the_ring);
    sigmay(i,:)     = sqrt(ats.naturalEmittance * beta(2,:) * coupling);
    sigmay_eta(i,:) = sqrt(ats.naturalEmittance * beta(2,:) * coupling + (eta(3,:) * ats.naturalEnergySpread).^2);
end

sigmay0    = repmat(sigmay0, length(r.machine), 1);
increase     = 100 * (sigmay ./ sigmay0 - 1);
increase_eta = 100 * (sigmay_eta ./ sigmay0 - 1);

increase_avg     = mean(increase);
increase_std     = std(increase);
increase_eta_avg = mean(increase_eta);
increase_eta_std = std(increase_eta);



% results
figure; hold all;
plot(s,increase_avg);
plot(s(rspls),increase_avg(rspls), 'o');
xlabel('pos [m]'); ylabel('increase in \sigma_y(s) [%]');
title('Vertical Beam Size Increase from BetaBeating');

figure; hold all;
plot(s,increase_eta_avg);
plot(s(rspls),increase_eta_avg(rspls), 'o');
xlabel('pos [m]'); ylabel('increase in \sigma_y(s) [%]');
title('Vertical Beam Size Increase from BetaBeating + Residual Dispersion');

fprintf('Reference coupling: %f %%\n', coupling * 100);
fprintf('INCREASE - BETA BEATING\n');
fprintf('increase[%%] @ MIA      : %f\n', mean(increase_avg(mia)));
fprintf('increase[%%] @ MIB      : %f\n', mean(increase_avg(mib)));
fprintf('increase[%%] @ MC       : %f\n', mean(increase_avg(mc)));
fprintf('increase[%%] @ ALL_RING : %f\n', mean(increase_avg));
fprintf('INCREASE - BETA BEATING + ETA\n');
fprintf('increase[%%] @ MIA      : %f\n', mean(increase_eta_avg(mia)));
fprintf('increase[%%] @ MIB      : %f\n', mean(increase_eta_avg(mib)));
fprintf('increase[%%] @ MC       : %f\n', mean(increase_eta_avg(mc)));
fprintf('increase[%%] @ ALL_RING : %f\n', mean(increase_eta_avg));

% fprintf('Reference coupling: %f %%\n', coupling * 100);
% fprintf('INCREASE - BETA BEATING\n');
% fprintf('increase[%%] @ MIA      : %f +/- %f\n', mean(increase_avg(mia)), mean(increase_std(mia)));
% fprintf('increase[%%] @ MIB      : %f +/- %f\n', mean(increase_avg(mib)), mean(increase_std(mib)));
% fprintf('increase[%%] @ MC       : %f +/- %f\n', mean(increase_avg(mc)), mean(increase_std(mc)));
% fprintf('increase[%%] @ ALL_RING : %f +/- %f\n', mean(increase_avg), mean(increase_std));
% fprintf('INCREASE - BETA BEATING + ETA\n');
% fprintf('increase[%%] @ MIA      : %f +/- %f\n', mean(increase_eta_avg(mia)), mean(increase_eta_std(mia)));
% fprintf('increase[%%] @ MIB      : %f +/- %f\n', mean(increase_eta_avg(mib)), mean(increase_eta_std(mib)));
% fprintf('increase[%%] @ MC       : %f +/- %f\n', mean(increase_eta_avg(mc)), mean(increase_eta_std(mc)));
% fprintf('increase[%%] @ ALL_RING : %f +/- %f\n', mean(increase_eta_avg), mean(increase_eta_std));

