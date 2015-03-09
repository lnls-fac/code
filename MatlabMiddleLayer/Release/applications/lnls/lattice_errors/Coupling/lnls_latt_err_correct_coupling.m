function machine = correct_coupling(machine, coup)

nr_machines = length(machine);

calc_respm = false;
if ~isfield(coup,'respm'), calc_respm = true; end

save([name,'_correct_coup_input.mat'], 'coup');

fprintf(['--- correct_coupling [' datestr(now) '] ---\n']);
if isnumeric(coup.svs), svs = num2str(coup.svs);else svs = coup.svs;end
fprintf('\nNumber Of Singular Values : %4s\n',svs);
fprintf('Max Number of Correction iterations : %4d\n',coup.max_nr_iter);
fprintf('Tolerância : %7.2e\n\n', coup.tolerance);

fprintf('mac | Max Kl |  chi2  | Tilt  |      Coup[%%]      | NIters | NRedStr\n');
fprintf('    | [1/km] |        | [deg] |  Ey/Ex  | Tracking|        |\n');
fprintf('%s',repmat('-',1,69));
for i=1:nr_machines
        R=0;
        T = 0;
        try
            [T, ~, ~, ~, R, ~, ~, ~, ~] = calccoupling(machine{i});
        end
        
        if calc_respm
            [respm, ~] = calc_respm_coupling(machine{i}, coup);
            coup.respm = respm;
        end
        
        RTr = mean(lnls_calc_emittance_coupling(machine{i}));
        [machine{i}, skewstr, iniFM, bestFM, iter, n_times] = coup_sg(machine{i}, coup);
        RTr2 = mean(lnls_calc_emittance_coupling(machine{i}));
        R2=0;
        T2 = 0;
        try
            [T2, ~, ~, ~, R2, ~, ~, ~, ~] = calccoupling(machine{i});
        end
        %fprintf('%03i| skewstr[1/m^2] %+6.4f(max) %6.4f(std) | coup %8.5f (std) | tilt[deg] %5.2f -> %5.2f (std), k[%%] %5.2f -> %5.2f (std)\n', i, max(abs(skewstr)), std(skewstr), best_fm, std(Tilt)*180/pi, std(Tilt2)*180/pi, 100*Ratio, 100*Ratio2);
        fprintf('\n%03d | %6s | %6.3f | %5.2f | %7.3f | %7.3f |  %4s  |  %4s \n',...
            i, ' ', iniFM, std(T)*180/pi,  100*[R, RTr],' ',' ');  
        fprintf('%3s | %6.2f | %6.3f | %5.2f | %7.4f | %7.4f |  %4d  |  %4d \n',...
            ' ', 1000*max(abs(skewstr)), bestFM, std(T2)*180/pi,  100*[R2, RTr2], iter, n_times);
        fprintf('%s',repmat('-',1,69));
end
fprintf('\n');