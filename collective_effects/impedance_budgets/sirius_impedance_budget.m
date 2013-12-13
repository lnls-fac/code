function budget = sirius_impedance_budget(w, select)

% beta values are estimated based on mode AC10.

mu0 = 4*pi*1e-7;
c   = 299792458;
ep0 = 1/c^2/mu0;
E = 3;

i=1;
%% Resistive wall form cilindrical vaccum chamber;
if (any(strcmp(select,'resistive_wall')) )%|| strcmp(select,'all'))
    budget{i}.name = 'Resistive Wall';
    budget{i}.type = 'rw';
    budget{i}.quantity = 1;
    budget{i}.betax = 7;
    budget{i}.betay = 11;
    epb     = [1 1];
    mub     = [1 1];
    ange    = [0 0];
    angm    = [0 0];
    sigmadc = [0 5.9e7];
    tau     = [0 0]*27e-15;
    b       = 12.00*1e-3;
    L       = 4800;
    budget{i}.mub = mub;
    budget{i}.ange = ange;
    budget{i}.angm = angm;
    budget{i}.tau   = tau;
    budget{i}.sigmadc = sigmadc;
    budget{i}.epb = epb;
    budget{i}.b = b;
    budget{i}.L = L;
    
    for j = 1: length(epb)
        epr(j,:) = epb(j)*(1-1i.*sign(w).*tan(ange(j))) + sigmadc(j)./(1+1i*w*tau(j))./(1i*w*ep0);
        mur(j,:) = mub(j)*(1-1i.*sign(w).*tan(angm(j)));
    end
    [Zl Zv Zh] = lnls_calc_impedance_multilayer_round_pipe(w, epr, mur, b, L,E, false, 0, 0);
    budget{i}.Zv = Zv;
    budget{i}.Zh = Zh;
    budget{i}.Zl = Zl;
    budget{i}.escala = 'log';
    i=i+1;
end

if (any(strcmp(select,'resistive_wall_with_coating')) || strcmp(select,'all') || strcmp(select,'ring'))
    budget{i}.name = 'Wall With Coating';
    budget{i}.type = 'rw';
    budget{i}.quantity = 1;
    budget{i}.betax = 7;
    budget{i}.betay = 11;
    epb     = [1 1 1];
    mub     = [1 1 1];
    ange    = [0 0 0];
    angm    = [0 0 0];
    sigmadc = [0 4e6 5.9e7]; % Not sure about NEG resistivity
    tau     = [0 0 0]*27e-15;
    b       = [12.000 12.001]*1e-3;
    L       = 480;
    budget{i}.mub = mub;
    budget{i}.ange = ange;
    budget{i}.angm = angm;
    budget{i}.tau   = tau;
    budget{i}.sigmadc = sigmadc;
    budget{i}.epb = epb;
    budget{i}.b = b;
    budget{i}.L = L;
    for j = 1: length(epb)
        epr(j,:) = epb(j)*(1-1i.*sign(w).*tan(ange(j))) + sigmadc(j)./(1+1i*w*tau(j))./(1i*w*ep0);
        mur(j,:) = mub(j)*(1-1i.*sign(w).*tan(angm(j)));
    end
    [Zl Zv Zh] = lnls_calc_impedance_multilayer_round_pipe(w, epr, mur, b, L, E, false, 0, 0);
    budget{i}.Zv = Zv;
    budget{i}.Zh = Zh;
    budget{i}.Zl = Zl;
    budget{i}.escala = 'log';
    i=i+1;
end


%% Resistive wall from in-vaccum ondulators;
if (any(strcmp(select,'in_vacuum_undulators')) || strcmp(select,'all') || strcmp(select,'ring'))
    budget{i}.name = 'In-vac. Und. @ low betax';
    budget{i}.type = 'rw';
    budget{i}.quantity = 4;
    budget{i}.betax = 4.1;
    budget{i}.betay = 1.5;
  
    epb     = [1 1 1];
    mub     = [1 1 10];
    ange    = [0 0 0];
    angm    = [0 0 0];
    sigmadc = [0 5.9e7 6.25e5]; % Copper Sheet
    tau     = [0 1 0]*27e-15;
    b       = [4/2 4.1/2]*1e-3;
    L       = 2.0;
    budget{i}.mub = mub;
    budget{i}.ange = ange;
    budget{i}.angm = angm;
    budget{i}.tau   = tau;
    budget{i}.sigmadc = sigmadc;
    budget{i}.epb = epb;
    budget{i}.b = b;
    budget{i}.L = L;
    
    for j = 1: length(epb)
        epr(j,:) = epb(j)*(1-1i.*sign(w).*tan(ange(j))) + sigmadc(j)./(1+1i*w*tau(j))./(1i*w*ep0);
        mur(j,:) = mub(j)*(1-1i.*sign(w).*tan(angm(j)));
    end
    
    [Zl Zv Zh] = lnls_calc_impedance_multilayer_round_pipe(w, epr, mur, b, L, E, false, 0, 0);
    Zv = pi^2/12*Zv;
    Zh = pi^2/24*Zh;
    budget{i}.Zv = Zv;
    budget{i}.Zh = Zh;
    budget{i}.Zl = Zl;
    budget{i}.escala = 'log';
    i=i+1;
end

% if (any(strcmp(select,'in_vacuum_undulators')) || strcmp(select,'all') || strcmp(select,'ring'))
%     budget{i}.name = 'In-vac. Und. @ high betax';
%     budget{i}.type = 'rw';
%     budget{i}.quantity = 1;
%     budget{i}.betax = 16;
%     budget{i}.betay = 4.0;
%     epb     = [1 1 1];
%     mub     = [1 1 10];
%     ange    = [0 0 0];
%     angm    = [0 0 0];
%     sigmadc = [0 5.9e7 6.25e5]; % Copper Sheet
%     tau     = [0 1 0]*27e-15;
%     b       = [5.3/2 (5.3+0.1)/2]*1e-3;
%     L       = 2.0;
%     budget{i}.mub = mub;
%     budget{i}.ange = ange;
%     budget{i}.angm = angm;
%     budget{i}.tau   = tau;
%     budget{i}.sigmadc = sigmadc;
%     budget{i}.epb = epb;
%     budget{i}.b = b;
%     budget{i}.L = L;
%     
%     for j = 1: length(epb)
%         epr(j,:) = epb(j)*(1-1i.*sign(w).*tan(ange(j))) + sigmadc(j)./(1+1i*w*tau(j))./(1i*w*ep0);
%         mur(j,:) = mub(j)*(1-1i.*sign(w).*tan(angm(j)));
%     end
%     
%     [Zl Zv Zh] = lnls_calc_impedance_multilayer_round_pipe(w, epr, mur, b, L, E, false, 0, 0);
%     Zv = pi^2/12*Zv;
%     Zh = pi^2/24*Zh;
%     budget{i}.Zv = Zv;
%     budget{i}.Zh = Zh;
%     budget{i}.Zl = Zl;
%     budget{i}.escala = 'log';
%     i=i+1;
% end


%% Resistive wall from smallgap vacuum chambers;
if (any(strcmp(select,'smallgap_undulators')) || strcmp(select,'all') || strcmp(select,'ring'))
    budget{i}.name = 'Small Gap Undulators';
    budget{i}.type = 'rw';
    budget{i}.quantity = 3;
    budget{i}.betax = 16.9;
    budget{i}.betay = 5;
    budget{i}.thick = 0.2e-3;
    budget{i}.cond = 5.94e7;
    budget{i}.perm = 1;
    budget{i}.h = 10e-3;
    budget{i}.L = 2;
    [Zv Zh Zl w_val] = lnls_calc_impedance_flat_chamber(budget{i}.thick, ...
        budget{i}.cond, budget{i}.perm, budget{i}.h, budget{i}.L, 0, w);
    
    budget{i}.Zv = Zv;
    budget{i}.Zh = Zh;
    budget{i}.Zl = Zl;
    budget{i}.escala = 'log';
    i=i+1;
end

%% Ferrite Kickers for injection
if (any(strcmp(select,'kicker')) || strcmp(select,'all') )%|| strcmp(select,'ring') )
    budget{i}.name = 'Ferrite Kickers';
    budget{i}.type = 'misto';
    budget{i}.quantity = 4;
    budget{i}.betax = 17;
    budget{i}.betay = 4;
% Valores que peguei com o F??bio.
    a = 63/2*1e-3;
    b = (10+7.5)*1e-3;
    d = b + 20e-3;
    L = 0.6;
    % Ferrite CMD5005
    epl = 12;
    rho = 1e6;
    epr = epl - 1i./w/ep0/rho*0;
    mui = 1600;
    ws = 20e6;
    mur = 1 + mui./(1+1i*w/ws);
    Zg = (1/50 + 1i*w*30e-12).^-1;
    % mean case
    [Zlw Zhw Zvw] = lnls_calc_ferrite_kicker_impedance(w,a,b,d,L,epr,mur,Zg,'pior');
    [Zlb Zhb Zvb] = lnls_calc_ferrite_kicker_impedance(w,a,b,d,L,epr,mur,Zg,'melhor');
    theta = atan(b/a);
    Zl = (theta*Zlb + (pi/2-theta)*Zlw)/(pi/2);
    Zv = (theta*Zvb + (pi/2-theta)*Zvw)/(pi/2);
    Zh = (theta*Zhb + (pi/2-theta)*Zhw)/(pi/2);
        
    budget{i}.L = L;
    budget{i}.Zv = Zv;
    budget{i}.Zh = Zh;
    budget{i}.Zl = Zl;
    budget{i}.escala = 'log';
    i=i+1;
end

%% Coherente Synchrotron Radiation Impedance: Not implemented yet;
if (any(strcmp(select,'coherent_synchrotron_radiation')))
    budget{i}.name = 'Cohererent Synchrotron Radiation';
    budget{i}.type = 'geo';
    budget{i}.quantity = 120;
    budget{i}.betax = 3;
    budget{i}.betay = 20;
    budget{i}.rho = 16.7;
    budget{i}.L = 6;
    Zl = lnls_calc_impedance_csr(budget{i}.rho, budget{i}.L);
    
    budget{i}.Zv = Zl*0;
    budget{i}.Zh = Zl*0;
    budget{i}.Zl = Zl;
    budget{i}.escala = 'log';
    i=i+1;
end


%% BPMs;
if (any(strcmp(select,'bpm')) || strcmp(select,'all') )%|| strcmp(select,'ring') )
    budget{i}.name = 'BPM-3-BNcernew';
    budget{i}.type = 'geo';
    budget{i}.quantity = 180;
    budget{i}.betax = 7;
    budget{i}.betay = 11;
    % Fiz uma mescla entre impedancia fittada por ressonadores e a impedancia
    % interpolada a partir da original. Usei a fittada para reproduzir o
    % broad-band e a interpolada para os picos narrow-band.
    Zlf = lnls_load_fitted_impedance(w, ...
        '/home/fac_files/data/sirius_col_effec/impedance_simulations/BPM/004-BPM_buttons/3/BNcernew', ...
        'Longitudinal','GdfidL');
    [Zlor wor] = lnls_load_impedance(...
        '/home/fac_files/data/sirius_col_effec/impedance_simulations/BPM/004-BPM_buttons/3/BNcernew', ...
        'Longitudinal','GdfidL');
    Zlint = interp1(wor,Zlor,w,'linear',0);
    Zl = Zlint;
    ind = (Zlint ==0);
    Zl(ind) = Zlf(ind);
    % Zl = Zlf;
    
    % Zxf = lnls_load_fitted_impedance(w, ...
    %     '/home/ABTLUS/fernando.sa/MATLAB/Impedancias/Simulacoes/Masks/_results/Ridge/w10/SOFT_HARD/h2', ...
    %     'Horizontal','GdfidL');
    % [Zxor wor] = lnls_load_impedance(...
    %     '/home/ABTLUS/fernando.sa/MATLAB/Impedancias/Simulacoes/Masks/_results/Ridge/w10/SOFT_HARD/h2', ...
    %     'Horizontal','GdfidL');
    % Zxint = interp1(wor,Zxor,w,'linear',0);
    % ind = (Zxint ==0) | abs(w)<1e10;
    % Zxint(ind) = Zxf(ind);
    
    budget{i}.Zv = Zl*0;
    budget{i}.Zh = Zl*0;
    budget{i}.Zl = Zl;
    budget{i}.escala = 'linear';
    i=i+1;
end

%% Masks
if (any(strcmp(select,'masks')) || strcmp(select,'all') )%|| strcmp(select,'ring') )
    budget{i}.name = 'Masks-ridge-softhard-h2';
    budget{i}.type = 'geo';
    budget{i}.quantity = 350;
    budget{i}.betax = 7;
    budget{i}.betay = 11;
    % Fiz uma mescla entre impedancia fittada por ressonadores e a imped??ncia
    % interpolada a partir da original. Usei a fittada para reproduzir o
    % broad-band e a interpolada para os picos narrow-band.
    Zlf = lnls_load_fitted_impedance(w, ...
        '/home/fac_files/data/sirius_col_effec/impedance_simulations/Masks/_results/Ridge/w10/SOFT_HARD/h2', ...
        'Longitudinal','GdfidL');
    [Zlor wor] = lnls_load_impedance(...
        '/home/fac_files/data/sirius_col_effec/impedance_simulations/Masks/_results/Ridge/w10/SOFT_HARD/h2', ...
        'Longitudinal','GdfidL');
    Zlint = interp1(wor,Zlor,w,'linear',0);
    ind = (Zlint ==0);
    Zlint(ind) = Zlf(ind);
    
    Zxf = lnls_load_fitted_impedance(w, ...
        '/home/fac_files/data/sirius_col_effec/impedance_simulations/Masks/_results/Ridge/w10/SOFT_HARD/h2', ...
        'Horizontal','GdfidL');
    [Zxor wor] = lnls_load_impedance(...
        '/home/fac_files/data/sirius_col_effec/impedance_simulations/Masks/_results/Ridge/w10/SOFT_HARD/h2', ...
        'Horizontal','GdfidL');
    Zxint = interp1(wor,Zxor,w,'linear',0);
    ind = (Zxint ==0) | abs(w)<1e10;
    Zxint(ind) = Zxf(ind);
    
    budget{i}.Zv = Zlint*0;
    budget{i}.Zh = Zxint;
    budget{i}.Zl = Zlint;
    budget{i}.escala = 'linear';
    i=i+1;
end

%% RF Cavity's tapers
if (any(strcmp(select,'taper_cv')) || strcmp(select,'all') )%|| strcmp(select,'ring') )
    budget{i}.name = 'Taper-Cav-SC-compL800';
    budget{i}.type = 'geo';
    budget{i}.quantity = 1;
    budget{i}.betax = 16;
    budget{i}.betay = 4;
    % Fiz uma mescla entre impedancia fittada por ressonadores e a impedancia
    % interpolada a partir da original. Usei a fittada para reproduzir o
    % broad-band e a interpolada para os picos narrow-band.
    Zlf = lnls_load_fitted_impedance(w, ...
        '/home/fac_files/data/sirius_col_effec/impedance_simulations/RF_cav/_results/Tapers/SC/Long/completeL800/sig0.75', ...
        'Longitudinal','ECHO');
    [Zlor wor] = lnls_load_impedance(...
        '/home/fac_files/data/sirius_col_effec/impedance_simulations/RF_cav/_results/Tapers/SC/Long/completeL800/sig0.75', ...
        'Longitudinal','ECHO');
    Zlint = interp1(wor,Zlor,w,'linear',0);
    Zl = Zlint;
    ind = (Zlint ==0);
    Zl(ind) = Zlf(ind);
    % Zl = Zlf;
    
    Zyf = lnls_load_fitted_impedance(w, ...
        '/home/fac_files/data/sirius_col_effec/impedance_simulations/RF_cav/_results/Tapers/SC/Trans/completeL800/sig1', ...
        'Vertical','ECHO');
    [Zyor wor] = lnls_load_impedance(...
        '/home/fac_files/data/sirius_col_effec/impedance_simulations/RF_cav/_results/Tapers/SC/Trans/completeL800/sig1', ...
        'Vertical','ECHO');
    Zyint = interp1(wor,Zyor,w,'linear',0);
    Zy  = Zyint;
    ind = (Zyint ==0);
    Zy(ind) = Zyf(ind);
    
    budget{i}.Zv = Zy; % simetria cilindrica
    budget{i}.Zh = Zy;
    budget{i}.Zl = Zl;
    budget{i}.escala = 'linear';
    i=i+1;
end


%% Broad-band impedance;
% if (any(strcmp(select,'broad_band')) || strcmp(select,'all'))
%     budget{i}.name = 'Broad Band ESRF';
%     budget{i}.type = 'geo';
%     budget{i}.quantity = 1;
%     budget{i}.betax = 6.8;
%     budget{i}.betay = 11;      %     valores do ESRF
%     budget{i}.Rsx = [2.0  3.5  12   2.0]*1e6/budget{i}.betax; 
%     budget{i}.wrx = [2.5  5.0  7.0  12.5]*1e9*2*pi; 
%     budget{i}.Qx =  [1    1    1    1]*10;                         
%     budget{i}.Rsy = [12   6.5  11   4.0]*1e6/budget{i}.betay; 
%     budget{i}.wry = [2.0  4.0  6.5  10]*1e9*2*pi;               
%     budget{i}.Qy =  [1    1    1    1]*10;                         
%     budget{i}.Rsl = 5.3e3; % = 3.6*518.25/354.0*1e3;
%     budget{i}.wrl = 20*1e9*2*pi;
%     budget{i}.Ql =  1;
%     Zv = lnls_calc_impedance_transverse_resonator(budget{i}.Rsy, budget{i}.Qy, budget{i}.wry, w);
%     Zh = lnls_calc_impedance_transverse_resonator(budget{i}.Rsx, budget{i}.Qx, budget{i}.wrx, w);
%     Zl = lnls_calc_impedance_longitudinal_resonator(budget{i}.Rsl, budget{i}.Ql, budget{i}.wrl, w);
%     
%     budget{i}.Zv = Zv;
%     budget{i}.Zh = Zh;
%     budget{i}.Zl = Zl;
%     
%     budget{i}.w = w;
%     budget{i}.escala = 'linear';
%     i=i+1;
% end
if (any(strcmp(select,'broad_band')) || strcmp(select,'all') || strcmp(select,'ring'))
    budget{i}.name = 'Broad Band';
    budget{i}.type = 'geo';
    budget{i}.quantity = 1;
    budget{i}.betax = 6.8;
    budget{i}.betay = 11;  
    Zovern = 0.2;
    fr  = 2.4* 299792458/12e-3/2/pi; % 2.4 c/b/2/pi;
    budget{i}.Rsl = Zovern*fr/0.578e6; % = 3.6*518.25/354.0*1e3;
    budget{i}.wrl = fr*2*pi;
    budget{i}.Ql =  1;
    budget{i}.Rsx =  budget{i}.Rsl/12e-3;%0.42e6/2; % = 13.5*1e6*518.25/845/20;
    budget{i}.wrx =  fr*2*pi;
    budget{i}.Qx =   1;                        
    budget{i}.Rsy =  budget{i}.Rsl/12e-3;%0.42e6/2; % = 13.5*1e6*518.25/845/20;
    budget{i}.wry =  fr*2*pi;              
    budget{i}.Qy =   1;                        
    Zv = lnls_calc_impedance_transverse_resonator(budget{i}.Rsy, budget{i}.Qy, budget{i}.wry, w);
    Zh = lnls_calc_impedance_transverse_resonator(budget{i}.Rsx, budget{i}.Qx, budget{i}.wrx, w);
    Zl = lnls_calc_impedance_longitudinal_resonator(budget{i}.Rsl, budget{i}.Ql, budget{i}.wrl, w);
    
    budget{i}.Zv = Zv;
    budget{i}.Zh = Zh;
    budget{i}.Zl = Zl;
    
    budget{i}.escala = 'linear';
    i=i+1;
end