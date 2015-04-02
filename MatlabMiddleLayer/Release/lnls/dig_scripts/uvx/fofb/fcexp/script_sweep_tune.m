deltarf = 1e3;
gap_vel = 300;
phase_vel = 300;

n = 11;
nu1 = ones(n,1);
nuvar = linspace(0.99,1.01,n)';

tunes = [nu1 nuvar; nuvar nu1];

nu0 = gettune;
nu = zeros(size(tunes,1), 2);

setpv('AON11VGAP_SP', gap_vel);
setpv('AON11VFASE_SP', phase_vel);

lnls1_fast_orbcorr_enable_excitation;

for i=1:length(tunes)
    settune(nu0.*(tunes(1,i)'), 0);
    pause(10);
    
    % Turn FOFB temporarily on to correct orbit to reference
    lnls1_fast_orbcorr_on;
    pause(1);
    lnls1_fast_orbcorr_off;
    pause(2);
    
    nu(i,:) = gettune;
    
    % Perform response matrix measurement via FOFB Fast Command
    fcexprespm;
end

lnls1_fast_orbcorr_disable_excitation;