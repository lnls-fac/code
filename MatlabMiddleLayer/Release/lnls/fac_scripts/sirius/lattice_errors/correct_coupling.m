function machine = correct_coupling(r, selection, sing_vals, max_nr_iters, tolerancia)

if ischar(sing_vals) && strcmpi(sing_vals, 'all')
    sing_vals = min(size(r.params.static.coup_respm.M));
end

fprintf(['--- correct_coupling [' datestr(now) '] ---\n']);
fprintf('\nNumber Of Singular Values : %4d\n',sing_vals);
fprintf('Max Number of Orbit Correction iterations : %4d\n',max_nr_iters);
fprintf('Tolerância : %7.2e\n\n', tolerancia);
machine = r.machine;

fprintf('mac | Max Kl |  chi2  | Tilt  |      Coup[%%]      | NIters | NRedStr\n');
fprintf('    | [1/Km] |        | [deg] |  Ey/Ex  | Tracking|        |\n');
fprintf('%s',repmat('-',1,69));
for i=selection
        R=0;
        T = 0;
        try
            [T, ~, ~, ~, R, ~, ~, ~, ~] = calccoupling(machine{i});
        catch
        end
        RTr = mean(lnls_calc_emittance_coupling(machine{i}));
        [machine{i}, skewstr, iniFM, bestFM, iter, n_times] = coup_sg(r, ...
                                sing_vals, machine{i}, max_nr_iters,tolerancia);
        RTr2 = mean(lnls_calc_emittance_coupling(machine{i}));
        R2=0;
        T2 = 0;
        try
            [T2, ~, ~, ~, R2, ~, ~, ~, ~] = calccoupling(machine{i});
        catch
        end
        %fprintf('%03i| skewstr[1/m^2] %+6.4f(max) %6.4f(std) | coup %8.5f (std) | tilt[deg] %5.2f -> %5.2f (std), k[%%] %5.2f -> %5.2f (std)\n', i, max(abs(skewstr)), std(skewstr), best_fm, std(Tilt)*180/pi, std(Tilt2)*180/pi, 100*Ratio, 100*Ratio2);
        fprintf('\n%03d | %6s | %6.3f | %5.2f | %7.3f | %7.3f |  %4s  |  %4s \n',...
            i, ' ', iniFM, std(T)*180/pi,  100*[R, RTr],' ',' ');  
        fprintf('%3s | %6.2f | %6.3f | %5.2f | %7.4f | %7.4f |  %4d  |  %4d \n',...
            ' ', 1000*max(abs(skewstr)), bestFM, std(T2)*180/pi,  100*[R2, RTr2], iter, n_times);
        fprintf('%s',repmat('-',1,69));
end
fprintf('\n\n');


function [the_ring, skewstr, init_fm,best_fm, iter, n_times] = coup_sg(r, nr_sing_values,...
                                                the_ring, max_nr_iters, tolerancia)

if ~exist('tolerancia','var'), tolerancia = 1e-5; end
tolerancia = abs(tolerancia);

skew_lst = r.params.static.scm_idx;

respm = r.params.static.coup_respm;
U = respm.U;
V = respm.V;
S = respm.S;
% selection of singular values
iS = diag(1./diag(S));
diS = diag(iS);
diS(nr_sing_values+1:end) = 0;
iS = diag(diS);
CM = -(V*iS*U');

best_coupvec = calc_residue_coupling(the_ring, r.params.static.bpm_idx,...
                    r.params.static.hcm_idx, r.params.static.vcm_idx);
best_skew    = the_ring(skew_lst);
best_fm = sqrt(lnls_meansqr(best_coupvec));
init_fm = best_fm;
factor = 1;
n_times = 0;
for iter = 1:max_nr_iters
    % calcs kicks
    delta_kicks = factor*CM * best_coupvec;
    
    % sets kicks
    init_kicks = getcellstruct(the_ring, 'PolynomA', skew_lst, 1, 2);
    tota_kicks = init_kicks + delta_kicks;
    the_ring   = setcellstruct(the_ring, 'PolynomA', skew_lst, tota_kicks, 1, 2);

    coup_vec = calc_residue_coupling(the_ring, r.params.static.bpm_idx, ...
                      r.params.static.hcm_idx, r.params.static.vcm_idx);
    fm = sqrt(lnls_meansqr(coup_vec));
    residue = abs(best_fm-fm)/best_fm;
    if (fm < best_fm)
        best_fm      = fm;
        best_skew    = the_ring(skew_lst);
        factor = 1; % reset the correction strength to 1
        best_coupvec  = coup_vec;
    else
        the_ring(skew_lst) = best_skew;
        factor = factor * 0.75; % reduces the strength of the correction
        n_times = n_times + 1; % to check how many times it passed here;
    end
    % breaks the loop in case convergence is reached
    if residue < tolerancia
        break;
    end
end
skewstr = getcellstruct(the_ring, 'PolynomA', r.params.static.scm_idx, 1, 2);
skewstr = skewstr.*getcellstruct(the_ring, 'Length', r.params.static.scm_idx);


