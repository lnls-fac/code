function machine = correct_optics(r, selection, sing_vals, max_nr_iters, tolerancia)

if ischar(sing_vals) && strcmpi(sing_vals, 'all')
    sing_vals = min(size(r.params.static.opt_respm.M));
end

fprintf(['--- correct_optics [' datestr(now) '] ---\n']);
fprintf('\nNumber Of Singular Values : %4d\n',sing_vals);
fprintf('Max Number of Orbit Correction iterations : %4d\n',max_nr_iters);
fprintf('Tolerância : %7.2e\n\n', tolerancia);
machine = r.machine;

fprintf('mac | Max Kl |  chi2  | dtunes | Betbeat  | eta @ss | NIters | NRedStr\n');
fprintf('    | [1/mm] |        |  x1000 | rms[%%]   | Max[mm] |        |\n');
fprintf('%s',repmat('-',1,69));

indcs = r.params.static.bpm_idx;
indcs = indcs(logical(repmat([1,0,0,0,0,0,0,0,1],1,20)));
[bx0,by0,tune0] = calcbetas(r.params.the_ring);
eta0 = calc_dispersion(r.params.the_ring,0, indcs);
for i=selection
        [bxi,byi,tunei] = calcbetas(machine{i});
        etai = calc_dispersion(machine{i},0, indcs);
        
        [machine{i}, quadstr, iniFM, bestFM, iter, n_times] = optics_sg(r, ...
                                sing_vals, machine{i}, max_nr_iters,tolerancia);
                            
        [bxf,byf,tunef]  = calcbetas(machine{i});
        etaf = calc_dispersion(machine{i},0, indcs);

        dtune = sqrt(sum((tune0-tunei).^2))*1000;
        dbx = sqrt(lnls_meansqr((bx0-bxi)./bx0));
        dby = sqrt(lnls_meansqr((by0-byi)./by0));
        fprintf('\n%03d | %6s | %6.1f | %6.3f | %5.2f / %5.2f |  %5.3f  |  %4s  |  %4s \n',...
            i, ' ', iniFM, dtune,  100*[dbx, dby],max(etai(1,:))*1000,' ',' ');
        dtune = sqrt(sum((tune0-tunef).^2))*1000;
        dbx = sqrt(lnls_meansqr((bx0-bxf)./bx0));
        dby = sqrt(lnls_meansqr((by0-byf)./by0));
        fprintf('%3s | %6.2f | %6.3f | %6.3f | %5.2f / %5.2f |  %5.3f  |  %4d  |  %4d \n',...
            ' ', 1000*max(abs(quadstr)), bestFM, dtune,  100*[dbx, dby],max(etaf(1,:))*1000, iter, n_times);
        fprintf('%s',repmat('-',1,69));
end
fprintf('\n');


function [betax, betay, tune] = calcbetas(the_ring)

[TD, tune] = twissring(the_ring,0,1:length(the_ring));
beta = cat(1, TD.beta);
betax = beta(:,1);
betay = beta(:,2);

function dispersion = calc_dispersion(the_ring,dp, idx)

ddp = 1e-8;

orbn = findorbit4(the_ring,dp-ddp,idx);
orbp = findorbit4(the_ring,dp+ddp,idx);
dispersion = (orbp - orbn) / (2*ddp);


function [the_ring, quadstr, init_fm,best_fm, iter, n_times] = optics_sg(r, nr_sing_values,...
                                                the_ring, max_nr_iters, tolerancia)

if ~exist('tolerancia','var'), tolerancia = 1e-5; end
tolerancia = abs(tolerancia);

quad_lst = r.params.static.kbs_idx;
tune = r.params.static.tune_goal;

respm = r.params.static.opt_respm;
U = respm.U;
V = respm.V;
S = respm.S;
% selection of singular values
iS = diag(1./diag(S));
diS = diag(iS);
diS(nr_sing_values+1:end) = 0;
iS = diag(diS);
CM = -(V*iS*U');

best_optvec = calc_residue_optics(the_ring, tune, r.params.static.bpm_idx,...
                    r.params.static.hcm_idx, r.params.static.vcm_idx);
best_quad    = the_ring(quad_lst);
best_fm = sqrt(lnls_meansqr(best_optvec));
init_fm = best_fm;
init_kicks = getcellstruct(the_ring, 'PolynomB', quad_lst, 1, 2);
factor = 1;
n_times = 0;
for iter = 1:max_nr_iters
    % calcs kicks
    delta_kicks = factor*CM * best_optvec;
    
    % sets kicks
    tota_kicks = getcellstruct(the_ring, 'PolynomB', quad_lst, 1, 2);
    tota_kicks = tota_kicks + delta_kicks;
    the_ring   = setcellstruct(the_ring, 'PolynomB', quad_lst, tota_kicks, 1, 2);

    opt_vec = calc_residue_optics(the_ring, tune, r.params.static.bpm_idx, ...
                      r.params.static.hcm_idx, r.params.static.vcm_idx);
    fm = sqrt(lnls_meansqr(opt_vec));
    residue = abs(best_fm-fm)/best_fm;
    if (fm < best_fm)
        best_fm      = fm;
        best_quad    = the_ring(quad_lst);
        factor = 1; % reset the correction strength to 1
        best_optvec  = opt_vec;
    else
        the_ring(quad_lst) = best_quad;
        factor = factor * 0.75; % reduces the strength of the correction
        n_times = n_times + 1; % to check how many times it passed here;
    end
    % breaks the loop in case convergence is reached
    if residue < tolerancia
        break;
    end
end
quadstr = getcellstruct(the_ring, 'PolynomB', r.params.static.kbs_idx, 1, 2);
quadstr = (quadstr-init_kicks).*getcellstruct(the_ring, 'Length', r.params.static.kbs_idx);



    

