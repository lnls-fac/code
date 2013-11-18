function impedance_budget_summary(ringdata, budget, save)

w = ringdata.w;
h = ringdata.nb;
I = ringdata.I_tot;
T0 = 2*pi/ringdata.w0;
lf = zeros(1,length(budget));
Pl = lf; TPl = lf; Tlf = lf; Tkfx = lf; Tkfy = lf;

fprintf('%-26s: %-20s\n','Lattice', ringdata.lattice_version);
fprintf('%-26s: %-20s\n','Stage', ringdata.stage);
fprintf('%-26s: %-20d\n','Number of Bunches', ringdata.nb);
fprintf('%-26s: %-20.4g\n','Revolution Frequency [Mhz]', ringdata.w0*1e-6/2/pi);
fprintf('%-26s: %-20.4g\n','Total Current [mA]', ringdata.I_tot*1e3);
fprintf('%-26s: %-20.4g\n','Bunch Lengh [mm]', ringdata.sigma*1e3); fprintf('\n');
fprintf('Model                     Number     Kl      Power     sum(Kl)  sum(Power)   bx*Kh        by*Kv  \n');
fprintf('                            #      [mV/pC]    [mW]     [V/pC]     [W]       [kV/pC]      [kV/pC] \n');
for i=1:length(budget)
    lf(i) = lnls_calc_loss_factor(w,budget{i}.Zl,ringdata.sigma, ringdata.w0,ringdata.nb);
    Pl(i) = I^2/h*T0*lf(i);
    Tlf(i) = budget{i}.quantity*lf(i);
    TPl(i) = Pl(i)*budget{i}.quantity;
    Tkfx(i)= budget{i}.betax*budget{i}.quantity*lnls_calc_kick_factor(w,budget{i}.Zh,ringdata.sigma, ringdata.w0,ringdata.nb);
    Tkfy(i)= budget{i}.betay*budget{i}.quantity*lnls_calc_kick_factor(w,budget{i}.Zv,ringdata.sigma, ringdata.w0,ringdata.nb);
    if budget{i}.quantity == 1
        fprintf('%-27s %-7d %-9s %-9s %-9.3g %-9.3g %-12.3g %-12.3g\n', budget{i}.name, budget{i}.quantity, ...
            '-', '-', Tlf(i)*1e-12, TPl(i), Tkfx(i)*1e-15 ,Tkfy(i)*1e-15);
    else
        fprintf('%-27s %-7d %-9.3g %-9.3g %-9.3g %-9.3g %-12.3g %-12.3g\n', budget{i}.name, budget{i}.quantity, ...
            lf(i)*1e-9, Pl(i)*1e3, Tlf(i)*1e-12, TPl(i), Tkfx(i)*1e-15 ,Tkfy(i)*1e-15);
    end
end

fprintf('%-27s %-7s %-9s %-9s %-9.3g %-9.3g %-12.3g %-12.3g\n\n\n', 'Total', '-', '-', '-', ...
    sum(Tlf)*1e-12, sum(TPl), sum(Tkfx)*1e-15 ,sum(Tkfy)*1e-15);

if save
    fp = fopen(['impedance_summary_' ringdata.stage '.txt'],'w');
    
    fprintf(fp,'%-26s: %-20s\n','Lattice', ringdata.lattice_version);
    fprintf(fp,'%-26s: %-20s\n','Stage', ringdata.stage);
    fprintf(fp,'%-26s: %-20d\n','Number of Bunches', ringdata.nb);
    fprintf(fp,'%-26s: %-20.4g\n','Revolution Frequency [Mhz]', ringdata.w0*1e-6/2/pi);
    fprintf(fp,'%-26s: %-20.4g\n','Total Current [mA]', ringdata.I_tot*1e3);
    fprintf(fp,'%-26s: %-20.4g\n','Bunch Lengh [mm]', ringdata.sigma*1e3); fprintf('\n');
    fprintf(fp,'Model                     Number     Kl      Power     sum(Kl)  sum(Power)   bx*Kh        by*Kv  \n');
    fprintf(fp,'                            #      [mV/pC]    [mW]     [V/pC]     [W]       [kV/pC]      [kV/pC] \n');
    for i=1:length(budget)
        if budget{i}.quantity == 1
            fprintf(fp,'%-27s %-7d %-9s %-9s %-9.3g %-9.3g %-12.3g %-12.3g\n', budget{i}.name, budget{i}.quantity, ...
                '-', '-', Tlf(i)*1e-12, TPl(i), Tkfx(i)*1e-15 ,Tkfy(i)*1e-15);
        else
            fprintf(fp,'%-27s %-7d %-9.3g %-9.3g %-9.3g %-9.3g %-12.3g %-12.3g\n', budget{i}.name, budget{i}.quantity, ...
                lf(i)*1e-9, Pl(i)*1e3, Tlf(i)*1e-12, TPl(i), Tkfx(i)*1e-15 ,Tkfy(i)*1e-15);
        end
    end
    
    fprintf(fp,'%-27s %-7s %-9s %-9s %-9.3g %-9.3g %-12.3g %-12.3g\n', 'Total', '-', '-', '-', ...
        sum(Tlf)*1e-12, sum(TPl), sum(Tkfx)*1e-15 ,sum(Tkfy)*1e-15);
    
    fclose(fp);
end