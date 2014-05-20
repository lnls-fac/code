function errors = generate_errors(r,varargin)

errors.errors_x      = zeros(r.config.nr_machines, length(r.params.the_ring));
errors.errors_y      = zeros(r.config.nr_machines, length(r.params.the_ring));
errors.errors_roll   = zeros(r.config.nr_machines, length(r.params.the_ring));
errors.errors_yaw    = zeros(r.config.nr_machines, length(r.params.the_ring));
errors.errors_pitch  = zeros(r.config.nr_machines, length(r.params.the_ring));
errors.errors_e      = zeros(r.config.nr_machines, length(r.params.the_ring));
errors.errors_e_kdip = zeros(r.config.nr_machines, length(r.params.the_ring));
% errors.errors_ripple = zeros(r.config.nr_machines, length(r.params.the_ring));

bpm_idx = [];
if exist('varargin','var') && strcmp(varargin{1},'static')
    fprintf(['--- generate_static_errors [' datestr(now) '] ---\n']);
    config = r.config.static;
    if r.params.correct2bba_orbit
        bpm_idx = findcells(r.params.the_ring,'FamName','BPM');
    end
elseif exist('varargin','var') && strcmp(varargin{1},'dynamic')
    fprintf(['--- generate_dynamic_errors [' datestr(now) '] ---\n']);
    config = r.config.dynamic;
else
    fprintf(['--- generate_errors [' datestr(now) '] ---\n']);
    config = r.config;
end


if ~isfield(config, 'cutoff_errors'), config.cutoff_errors = []; end
if ~isfield(config, 'rndtype'), config.rndtype = 'gaussian'; end;

families = fieldnames(config.families);
fam_idx = findcells(r.params.the_ring, 'FamName');
fam_list = getcellstruct(r.params.the_ring,'FamName',fam_idx);
for k=1:r.config.nr_machines
    for i=1:length(families)
        family = config.families.(families{i});
        if ischar(family.labels)
            % GIRDERS!!!
            label = family.labels;
            idx = fam_idx(ismember(fam_list,label));
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
                errors = get_fam_random_errors(errors, family, k, indcs, nrels, nrsgs, config.cutoff_errors, config.rndtype);
            end
            
        elseif iscell(family.labels{1})
            indcs = [];
            for j=1:length(family.labels{1})
                indcs = [indcs fam_idx(ismember(fam_list,family.labels{1}{j}))];
            end
            nrels = 1;
            nrsgs = length(indcs);
            
            errors = get_fam_random_errors(errors, family, k, indcs, nrels, nrsgs, config.cutoff_errors, config.rndtype);
            
        else
            for j=1:length(family.labels)
                
                label = family.labels{j};
                nrsgs = family.nrsegs(j);
                indcs = fam_idx(ismember(fam_list,label));
                nrels = length(indcs) / nrsgs;
                
                errors = get_fam_random_errors(errors, family, k, indcs, nrels, nrsgs, config.cutoff_errors, config.rndtype);
            end
        end
    end
end

if (config.girder.girder_error_flag)
    girders_idx = findcells(r.params.the_ring,'Girder');
    girders_list = getcellstruct(r.params.the_ring,'Girder',girders_idx);
    [fam_girders, fam_idx, ~] = unique(girders_list);
    [~, idx_fam] = sort(girders_idx(fam_idx));
    fam_girders = fam_girders(idx_fam);
    
    girder = config.girder;
    
    if ~girder.correlated_errors
        nrels = length(fam_girders);
        indcs = ones(1,length(r.params.the_ring));
        for ii=1:nrels
            label = fam_girders{ii};
            idx = girders_idx(ismember(girders_list,label));
            idx = setdiff(idx,bpm_idx); % retira bpms dos erros de girders
            indcs(idx) = indcs(idx) + ii;
        end
        
        for k=1:r.config.nr_machines
            errors = get_gir_random_errors(errors, girder, k,indcs, nrels, config.cutoff_errors, config.rndtype);
        end
    else
        dip_idx = findcells(r.params.the_ring,'BendingAngle');
        dip_girder = unique(girders_list(ismember(girders_idx,dip_idx)));
        nrels = length(dip_girder);
        indcs  = ones(1,length(r.params.the_ring));
        indcs2 = ones(2,length(r.params.the_ring));
        for ii=1:nrels
            label = dip_girder{ii};
            idx = girders_idx(ismember(girders_list,label));
            idx = setdiff(idx,bpm_idx); % retira bpms dos erros de girders
            indcs(idx) = indcs(idx) + ii;
            [~,id] = ismember(label,fam_girders);
            idx = girders_idx(ismember(girders_list,fam_girders{id-1}));
            idx = setdiff(idx,bpm_idx); % retira bpms dos erros de girders
            indcs2(1,idx) = indcs2(1,idx) + ii;
            idx = girders_idx(ismember(girders_list,fam_girders{id+1}));
            idx = setdiff(idx,bpm_idx); % retira bpms dos erros de girders
            indcs2(2,idx) = indcs2(2,idx) + ii;
        end
        
        for k=1:r.config.nr_machines
            errors = get_gir_random_errors(errors, girder, k,indcs, nrels, config.cutoff_errors, config.rndtype, indcs2);
        end
    end
end

% dlmwrite([config.label '_errors_x.dat'],      1e6*errors.errors_x, 'precision',    '%+8.3f', 'newline', 'pc', 'delimiter', ' ');
fprintf('\n');


function errors = get_fam_random_errors(errors, family, k, indcs, nrels, nrsgs, cutoff_errors, rndtype)

type_err = {'x','y','roll','yaw','pitch','e','e_kdip'};
for ii=type_err
    try
        rndnr1 = get_random_numbers(family.(['sigma_' ii{:}]), nrels, cutoff_errors, rndtype);
        rndnr1 = repmat(rndnr1', nrsgs, 1); rndnr1 = rndnr1(:);
        errors.(['errors_' ii{:}])(k,indcs) = errors.(['errors_' ii{:}])(k,indcs) + rndnr1';
    catch
    end
end


function errors = get_gir_random_errors(errors, girder, k, indcs, nrels, cutoff_errors, rndtype, indcs2)

if ~exist('indcs2','var')
    indcs2 = ones(2,length(errors.errors_x));
end

type_err = {'x','y','roll','yaw','pitch'};
for ii=type_err
    try
        rndn1 = get_random_numbers(girder.(['sigma_' ii{:}]), nrels, cutoff_errors, rndtype); rndn1 = [0, rndn1'];
        errors.(['errors_' ii{:}])(k,:) = errors.(['errors_' ii{:}])(k,:) + rndn1(indcs) + (rndn1(indcs2(1,:))+rndn1(indcs2(2,:)))/2;
    catch
    end
end


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


