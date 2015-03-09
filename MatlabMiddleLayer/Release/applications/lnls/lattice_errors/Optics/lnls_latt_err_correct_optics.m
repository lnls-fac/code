function machine = correct_optics(name, machine, optics, the_ring)

nr_machines = length(machine);

calc_respm = false;
if ~isfield(optics,'respm'), calc_respm = true; end

save([name,'_correct_optics_input.mat'], 'optics');

fprintf(['Correcting Optics [' datestr(now) ']:\n']);
if isnumeric(optics.svs), svs = num2str(optics.svs);else svs = optics.svs;end
fprintf('\nNumber Of Singular Values : %4s\n',svs);
fprintf('Max Number of Correction iterations : %4d\n',optics.max_nr_iter);
fprintf('Tolerância : %7.2e\n\n', optics.tolerance);

fprintf('mac | Max Kl |  chi2  | dtunes | Betbeat  | eta @ss | NIters | NRedStr\n');
fprintf('    | [1/km] |        |  x1000 | rms[%%]   | Max[mm] |        |\n');
fprintf('%s',repmat('-',1,69));

indcs = optics.bpm_idx;
indcs = indcs(logical(repmat([1,0,0,0,0,0,0,0,1],1,20)));
[bx0,by0,tune0] = calcbetas(the_ring);
for i=1:nr_machines
        [bxi,byi,tunei] = calcbetas(machine{i});
        etai = calc_dispersion(machine{i}, indcs)*1000;
        
        if calc_respm
            [respm, ~] = calc_respm_optics(machine{i}, optics);
            optics.respm = respm;
        end
        
        [machine{i}, quadstr, iniFM, bestFM, iter, n_times] = optics_sg(machine{i}, optics);
                            
        [bxf,byf,tunef]  = calcbetas(machine{i});
        etaf = calc_dispersion(machine{i}, indcs)*1000;

        dtune = sqrt(sum((tune0-tunei).^2))*1000;
        dbx = 100*sqrt(lnls_meansqr((bx0-bxi)./bx0));
        dby = 100*sqrt(lnls_meansqr((by0-byi)./by0));
        fprintf('\n%03d | %6s | %6.1f | %6.3f | %5.2f / %5.2f |  %5.3f  |  %4s  |  %4s \n',...
            i, ' ', iniFM, dtune, [dbx, dby],max(etai(1,:)),' ',' ');
        dtune = sqrt(sum((tune0-tunef).^2))*1000;
        dbx = 100*sqrt(lnls_meansqr((bx0-bxf)./bx0));
        dby = 100*sqrt(lnls_meansqr((by0-byf)./by0));
        fprintf('%3s | %6.2f | %6.3f | %6.3f | %5.2f / %5.2f |  %5.3f  |  %4d  |  %4d \n',...
            ' ', 1000*max(abs(quadstr)), bestFM, dtune, [dbx,dby], max(etaf(1,:)), iter, n_times);
        fprintf('%s',repmat('-',1,69));
end
fprintf('\n');


function [betax, betay, tune] = calcbetas(the_ring)

[TD, tune] = twissring(the_ring,0,1:length(the_ring));
beta = cat(1, TD.beta);
betax = beta(:,1);
betay = beta(:,2);