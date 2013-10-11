function machine = correct_optics(r, selection, sv_list, nr_iterations)

fprintf(['--- correct_optics [' datestr(now) '] ---\n']);

machine = r.machine;

for i=selection
    v = calc_residue_optics(machine{i}, r.params.the_ring); init_fm = sqrt(sum(v.^2) / length(v));
    best_fm = Inf;
    for s=sv_list
        [machine{i} v] = optics_sg(r, s, machine{i}, nr_iterations);
        fm = sqrt(sum(v.^2) / length(v));
        if (fm < best_fm)
            best_fm      = fm;
            best_machine = machine{i};
            best_v       = v;
        else
            machine{i} = best_machine;
        end
    end
    % restores best config of orbit correction singular values
    machine{i} = best_machine;
    v          = best_v;
    fm         = best_fm;
    fprintf('%03i| asymm %f -> %f\n', i, init_fm, best_fm);
end

fprintf('\n');


function [the_ring v] = optics_sg(r, nr_sing_values, the_ring0, nr_iterations)


the_ring = the_ring0;

S = r.params.opt_respm.S;
U = r.params.opt_respm.U;
V = r.params.opt_respm.V;

% selection of singular values
iS = diag(1./diag(S));
diS = diag(iS);
diS(nr_sing_values+1:end) = 0;
iS = diag(diS);
CM = -(V*iS*U');

for i=1:nr_iterations
    v = calc_residue_optics(the_ring, r.params.the_ring);
    %disp([std(v) max(abs(v))]);
    dk = CM * v;
    k_init  = getcellstruct(the_ring, 'K', r.params.kbs_idx);
    k_final = k_init + dk;
    the_ring = setcellstruct(the_ring, 'K', r.params.kbs_idx, k_final);
    the_ring = setcellstruct(the_ring, 'PolynomB', r.params.kbs_idx, k_final, 1, 2);
end



    
    

