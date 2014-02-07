function machine = correct_coupling(r, selection, sv_list, nr_iterations)

global THERING;

fprintf(['--- correct_coupling [' datestr(now) '] ---\n']);

machine = r.machine;

if ischar(sv_list) && strcmpi(sv_list, 'all')
    sv_list = min(size(r.params.coup_respm.M));
end

for i=selection
        THERING = machine{i};
        [Tilt, Eta, EpsX, EpsY, Ratio, ENV, DP, DL, sigmas] = calccoupling;
        Ratio_lnls = lnls_calc_emittance_coupling(machine{i});
        init_fm = calc_residue_coupling(THERING, r.params.bpm_idx, r.params.hcm_idx, r.params.vcm_idx);
        %init_fm = init_fm(r.params.ele_idx);
        init_fm = sqrt(sum(init_fm.^2)/length(init_fm));
        best_fm = init_fm;
        for s=sv_list
            [machine{i} skewstr coup_vec] = coup_sg(r, s, machine{i}, nr_iterations);
            fm = sqrt(sum(coup_vec.^2)/length(coup_vec));
            if (fm < best_fm)
                best_fm       = fm;
                best_skewstr  = skewstr;
                best_machine  = machine{i};
                best_coupvec  = coup_vec;
            else
                machine{i} = best_machine;
            end
        end 
        % restores best config of orbit correction singular values
        machine{i} = best_machine;
        coup_vec   = best_coupvec;
        skewstr    = best_skewstr;
        THERING = machine{i};
        Ratio2_lnls = lnls_calc_emittance_coupling(machine{i});
        [Tilt2, Eta2, EpsX2, EpsY2, Ratio2, ENV2, DP2, DL2, sigmas2] = calccoupling;
        %fprintf('%03i| skewstr[1/m^2] %+6.4f(max) %6.4f(std) | coup %8.5f (std) | tilt[deg] %5.2f -> %5.2f (std), k[%%] %5.2f -> %5.2f (std)\n', i, max(abs(skewstr)), std(skewstr), best_fm, std(Tilt)*180/pi, std(Tilt2)*180/pi, 100*Ratio, 100*Ratio2);
        fprintf('%03i| skewstr[1/m^2] %+6.4f(max) | chi2: %8.5f -> %8.5f | tilt[deg]: %8.5f -> %8.5f | coup[%%]: %8.5f -> %8.5f | coup_lnls[%%]: %8.5f -> %8.5f\n', i, max(abs(skewstr)), init_fm, best_fm, std(Tilt)*180/pi, std(Tilt2)*180/pi,  100*Ratio, 100*Ratio2,  100*Ratio_lnls, 100*Ratio2_lnls);
        
end

% hkicks = zeros(length(machine), length(r.params.the_ring));
% vkicks = zeros(length(machine), length(r.params.the_ring));
% for i=selection
%     hkicks(i,r.params.hcm_idx) = getcellstruct(machine{i}, 'KickAngle', r.params.hcm_idx, 1, 1);
%     vkicks(i,r.params.vcm_idx) = getcellstruct(machine{i}, 'KickAngle', r.params.vcm_idx, 1, 2);
% end
% dlmwrite([r.config.label '_cor_codx.dat'],    1e6*codx,   'precision', '%+8.2f', 'newline', 'pc', 'delimiter', ' ');
% dlmwrite([r.config.label '_cor_cody.dat'],    1e6*cody,   'precision', '%+8.2f', 'newline', 'pc', 'delimiter', ' ');
% dlmwrite([r.config.label '_hkicks.dat'],      1e3*hkicks, 'precision', '%+8.5f', 'newline', 'pc', 'delimiter', ' ');
% dlmwrite([r.config.label '_vkicks.dat'],      1e3*vkicks, 'precision', '%+8.5f', 'newline', 'pc', 'delimiter', ' ');
    
fprintf('\n');


function [the_ring skewstr coup_vec] = coup_sg(r, nr_sing_values, the_ring0, nr_iterations)

the_ring = the_ring0;

[U,S,V] = svd(r.params.coup_respm.M, 'econ');

% selection of singular values
iS = diag(1./diag(S));
diS = diag(iS);
diS(nr_sing_values+1:end) = 0;
iS = diag(diS);
CM = -(V*iS*U');

for k=1:nr_iterations
    % calcs kicks
    coup_vec = calc_residue_coupling(the_ring, r.params.bpm_idx, r.params.hcm_idx, r.params.vcm_idx);
    delta_kicks = CM * coup_vec;
    
    % sets kicks
    init_kicks = getcellstruct(the_ring, 'PolynomA', r.params.scm_idx, 1, 2);
    tota_kicks = init_kicks + delta_kicks;
    the_ring   = setcellstruct(the_ring, 'PolynomA', r.params.scm_idx, tota_kicks, 1, 2);
end
skewstr = getcellstruct(the_ring, 'PolynomA', r.params.scm_idx, 1, 2);
coup_vec = calc_residue_coupling(the_ring, r.params.bpm_idx, r.params.hcm_idx, r.params.vcm_idx);


