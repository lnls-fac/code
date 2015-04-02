deltarf = 1e3;
gap_vel = 300;
phase_vel = 300;

aon11_gaps = [repmat(22,5,1); repmat(26,5,1); repmat(29,5,1); repmat(33, 5,1)];
aon11_phases = repmat([-25; -15; -10; -5; 0; 5; 10; 15; 25], 4,1);
    
aon11_gap0 = getpv('AON11GAP_SP');
aon11_phase0 = getpv('AON11FASE_SP');

setpv('AON11VGAP_SP', gap_vel);
setpv('AON11VFASE_SP', phase_vel);

nu = zeros(length(aon11_gaps), 2);

lnls1_fast_orbcorr_enable_excitation;

for i=1:length(aon11_gaps)
    if getpv('AON11GAP_SP') ~= aon11_gaps(i)
        setpv('AON11GAP_SP', aon11_gaps(i));
    end
    pause(10);
    
    if getpv('AON11FASE_SP') ~= aon11_phases(i)
        setpv('AON11FASE_SP', aon11_phases(i));
    end
    pause(10);
    
    % Turn FOFB temporarily on to correct orbit to reference
    lnls1_fast_orbcorr_on;
    pause(1);
    lnls1_fast_orbcorr_off;
    pause(2);
    
    % Perform response matrix measurement via FOFB Fast Command
    fcexprespm;
    
    % Change RF frequency to measure dispersion orbit
    pause(1);
    frf = getrf;
    setrf(frf-deltarf/2);
    pause(2);
    setrf(frf+deltarf/2);
    pause(2);
    setrf(frf);
    pause(1);
    
    nu(i,:) = gettune;
end

lnls1_fast_orbcorr_disable_excitation;

data_header = {'AON11_GAP','AON11_FASE','TUNEX','TUNEY'};
data = [aon11_gaps aon11_phases nu];