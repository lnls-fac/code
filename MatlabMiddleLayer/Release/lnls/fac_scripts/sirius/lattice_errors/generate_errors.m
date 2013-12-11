function errors = generate_errors(r)




fprintf(['--- generate_errors [' datestr(now) '] ---\n']);
errors_x      = zeros(r.config.nr_machines, length(r.params.the_ring));
errors_y      = zeros(r.config.nr_machines, length(r.params.the_ring));
errors_roll   = zeros(r.config.nr_machines, length(r.params.the_ring));
errors_yaw    = zeros(r.config.nr_machines, length(r.params.the_ring));
errors_pitch  = zeros(r.config.nr_machines, length(r.params.the_ring));
errors_e      = zeros(r.config.nr_machines, length(r.params.the_ring));
errors_e_kdip = zeros(r.config.nr_machines, length(r.params.the_ring));
errors_ripple = zeros(r.config.nr_machines, length(r.params.the_ring));

if ~isfield(r.config, 'cutoff_errors'), r.config.cutoff_errors = []; end
if ~isfield(r.config, 'rndtype'), r.config.rndtype = 'gaussian'; end;
    
families = fieldnames(r.config.families);
for k=1:r.config.nr_machines
    for i=1:length(families)
        family = r.config.families.(families{i});
        if ischar(family.labels)
            % GIRDERS!!!
            label = family.labels;
            idx   = findcells(r.params.the_ring, 'FamName', label);
            idx   = idx(:)';
            idx   = [idx; idx(2:end) idx(1)]';
            for j=1:size(idx, 1)
                if idx(j,2) < idx(j,1)
                    indcs = [idx(j,1)+1:length(r.params.the_ring) 1:idx(j,2)-1];
                else
                    indcs = idx(j,1)+1:idx(j,2)-1;
                end
                nrsgs = length(indcs);
                nrels = length(indcs) / nrsgs;
                try 
                    rndnr1 = get_random_numbers(family.sigma_x, nrels, r.config.cutoff_errors, r.config.rndtype); rndnr1 = repmat(rndnr1', nrsgs, 1); rndnr1 = rndnr1(:); errors_x(k,indcs) = errors_x(k,indcs) + rndnr1';
                catch
                end
                try
                    rndnr2 = get_random_numbers(family.sigma_y, nrels, r.config.cutoff_errors, r.config.rndtype); rndnr2 = repmat(rndnr2', nrsgs, 1); rndnr2 = rndnr2(:); errors_y(k,indcs) = errors_y(k,indcs) + rndnr2';
                catch
                end
                try
                    rndnr3 = get_random_numbers(family.sigma_roll, nrels, r.config.cutoff_errors, r.config.rndtype); rndnr3 = repmat(rndnr3', nrsgs, 1); rndnr3 = rndnr3(:); errors_roll(k,indcs)  = errors_roll(k,indcs) + rndnr3';
                catch
                end
                try
                    rndnr4 = get_random_numbers(family.sigma_yaw, nrels, r.config.cutoff_errors, r.config.rndtype); rndnr4 = repmat(rndnr4', nrsgs, 1); rndnr4 = rndnr4(:); errors_yaw(k,indcs)   = errors_yaw(k,indcs) + rndnr4';
                catch
                end
                try
                    rndnr5 = get_random_numbers(family.sigma_pitch, nrels, r.config.cutoff_errors, r.config.rndtype); rndnr5 = repmat(rndnr5', nrsgs, 1); rndnr5 = rndnr5(:); errors_pitch(k,indcs) = errors_pitch(k,indcs) + rndnr5';
                catch
                end
                try
                    rndnr6 = get_random_numbers(family.sigma_e, nrels, r.config.cutoff_errors, r.config.rndtype);  rndnr6 = repmat(rndnr6', nrsgs, 1); rndnr6 = rndnr6(:); errors_e(k,indcs)     = errors_e(k,indcs) + rndnr6';
                catch
                end
                try
                    rndnr7 = get_random_numbers(family.sigma_e_kdip, nrels, r.config.cutoff_errors, r.config.rndtype); rndnr7 = repmat(rndnr7', nrsgs, 1); rndnr7 = rndnr7(:); errors_e_kdip(k,indcs)= errors_e_kdip(k,indcs) + rndnr7';
                catch
                end
                try
                    rndnr8 = get_random_numbers(family.sigma_ripple, nrels, 100*r.config.cutoff_errors, r.config.rndtype); rndnr8 = repmat(rndnr8', nrsgs, 1); rndnr8 = rndnr8(:); errors_ripple(k,indcs)= errors_ripple(k,indcs) + rndnr8';
                catch
                end
            end
            
        elseif iscell(family.labels{1})
            indcs = [];
            for j=1:length(family.labels{1})
                indcs = [indcs findcells(r.params.the_ring, 'FamName', family.labels{1}{j})];
            end
            nrels = 1;
            nrsgs = length(indcs);
         
            try
                rndnr8 = get_random_numbers(family.sigma_ripple, nrels, r.config.cutoff_errors, r.config.rndtype); 
                rndnr8 = repmat(rndnr8', nrsgs, 1); 
                rndnr8 = rndnr8(:); 
                errors_ripple(k,indcs)= rndnr8';
            catch
            end
            
        else
            for j=1:length(family.labels)
                
                label = family.labels{j};
                nrsgs = family.nrsegs(j);
                indcs = findcells(r.params.the_ring, 'FamName', label);
                nrels = length(indcs) / nrsgs;
                
                try
                    rndnr1 = get_random_numbers(family.sigma_x, nrels, r.config.cutoff_errors, r.config.rndtype); rndnr1 = repmat(rndnr1', nrsgs, 1); rndnr1 = rndnr1(:); errors_x(k,indcs) = errors_x(k,indcs) + rndnr1';
                catch
                end
                try
                    rndnr2 = get_random_numbers(family.sigma_y, nrels, r.config.cutoff_errors, r.config.rndtype); rndnr2 = repmat(rndnr2', nrsgs, 1); rndnr2 = rndnr2(:); errors_y(k,indcs) = errors_y(k,indcs) + rndnr2';
                catch
                end
                try
                    rndnr3 = get_random_numbers(family.sigma_roll, nrels, r.config.cutoff_errors, r.config.rndtype); rndnr3 = repmat(rndnr3', nrsgs, 1); rndnr3 = rndnr3(:); errors_roll(k,indcs)  = errors_roll(k,indcs) + rndnr3';
                catch
                end
                try
                    rndnr4 = get_random_numbers(family.sigma_yaw, nrels, r.config.cutoff_errors, r.config.rndtype); rndnr4 = repmat(rndnr4', nrsgs, 1); rndnr4 = rndnr4(:); errors_yaw(k,indcs)   = errors_yaw(k,indcs) + rndnr4';
                catch
                end
                try
                    rndnr5 = get_random_numbers(family.sigma_pitch, nrels, r.config.cutoff_errors, r.config.rndtype); rndnr5 = repmat(rndnr5', nrsgs, 1); rndnr5 = rndnr5(:); errors_pitch(k,indcs) = errors_pitch(k,indcs) + rndnr5';
                catch
                end
                try
                    rndnr6 = get_random_numbers(family.sigma_e, nrels, r.config.cutoff_errors, r.config.rndtype);  rndnr6 = repmat(rndnr6', nrsgs, 1); rndnr6 = rndnr6(:); errors_e(k,indcs)     = errors_e(k,indcs) + rndnr6';
                catch
                end
                try
                    rndnr7 = get_random_numbers(family.sigma_e_kdip, nrels, r.config.cutoff_errors, r.config.rndtype); rndnr7 = repmat(rndnr7', nrsgs, 1); rndnr7 = rndnr7(:); errors_e_kdip(k,indcs)= errors_e_kdip(k,indcs) + rndnr7';
                catch
                end
                try
                    rndnr8 = get_random_numbers(family.sigma_ripple, nrels, 100*r.config.cutoff_errors, r.config.rndtype); rndnr8 = repmat(rndnr8', nrsgs, 1); rndnr8 = rndnr8(:); errors_ripple(k,indcs)= errors_ripple(k,indcs) + rndnr8';
                catch
                end
                
            end
            
        end
        
    end
end


errors.errors_x      = 1*errors_x;
errors.errors_y      = 1*errors_y;
errors.errors_roll   = 1*errors_roll;
errors.errors_yaw    = 1*errors_yaw;
errors.errors_pitch  = 1*errors_pitch;
errors.errors_e      = 1*errors_e;
errors.errors_e_kdip = 1*errors_e_kdip;
errors.errors_ripple = 1*errors_ripple;


dlmwrite([r.config.label '_errors_x.dat'],      1e6*errors_x, 'precision',    '%+8.3f', 'newline', 'pc', 'delimiter', ' ');
dlmwrite([r.config.label '_errors_y.dat'],      1e6*errors_y, 'precision',    '%+8.3f', 'newline', 'pc', 'delimiter', ' ');
dlmwrite([r.config.label '_errors_roll.dat'],   1e3*errors_roll,  'precision', '%+8.5f', 'newline', 'pc', 'delimiter', ' ');
dlmwrite([r.config.label '_errors_yaw.dat'],    1e3*errors_yaw,   'precision', '%+8.5f', 'newline', 'pc', 'delimiter', ' ');
dlmwrite([r.config.label '_errors_pitch.dat'],  1e3*errors_pitch, 'precision', '%+8.5f', 'newline', 'pc', 'delimiter', ' ');
dlmwrite([r.config.label '_errors_e.dat'],      1e2*errors_e, 'precision', '%+8.5f', 'newline', 'pc', 'delimiter', ' ');
dlmwrite([r.config.label '_errors_e_kdip.dat'], 1e2*errors_e_kdip, 'precision', '%+8.5f', 'newline', 'pc', 'delimiter', ' ');
dlmwrite([r.config.label '_errors_ripple.dat'], 2^16*errors_ripple, 'precision', '%+8.5f', 'newline', 'pc', 'delimiter', ' ');
fprintf('\n');




function rndnr = get_random_numbers(sigma, nrels, cutoff, type)

% erro gaussiano truncado em 1 sigma: decidido apos conversa com o Ricardo
% sobre erros de alinhamento em 17/09/2012.
max_value = cutoff;

rndnr = zeros(nrels,1);
sel = 1:nrels;
if any(strcmpi(type, {'gaussian','gauss','norm', 'normal'}))
    while ~isempty(sel)
        rndnr(sel) = randn(1,length(sel));
        sel = find(abs(rndnr) > max_value);
        %     sel = []; % abri mão da truncagem para para tornar os erros repetitivos.
    end
elseif any(strcmpi(type, {'sin','vibration','ripple', 'cos','time-average'}))
    rndnr(sel) = gen_random_from_sin(length(sel));
end
rndnr = sigma * rndnr;




function rndnr = gen_random_from_sin(nrnrs)

rndnr = sin(2*pi*rand(1,nrnrs));


