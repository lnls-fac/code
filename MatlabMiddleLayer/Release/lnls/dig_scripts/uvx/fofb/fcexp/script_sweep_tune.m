deltarf = 1e-3; % MHz
tunematrixfile = 'TuneRespMat_online_2010-06-19_21-47-43.mat';

n = 11;
nu1 = ones(n,1);
nuvar = linspace(0.99,1.01,n)';

tunes = [nu1 nuvar; nuvar nu1];

switch2online;

nu0 = gettune;
nu = zeros(size(tunes,1), 2);

TuneMatrix = gettuneresp('FileName',fullfile('C:\Arq\fac_files\code\MatlabMiddleLayer\Release\machine\LNLS1\StorageRingData\User\Response\Tune', tunematrixfile));

lnls1_fast_orbcorr_enable_excitation;

for i=1:length(tunes)
    for j=1:5
        settune(nu0.*(tunes(1,i)'),0)
        pause(0.5);
    end
    
    % Turn FOFB temporarily on to correct orbit to reference
    lnls1_fast_orbcorr_on;
    pause(1);
    lnls1_fast_orbcorr_off;
    pause(2);
    
    nu(i,:) = gettune;
    
    % Perform response matrix measurement via FOFB Fast Command
    fcexprespm;
end

settune(nu0);

lnls1_fast_orbcorr_disable_excitation;