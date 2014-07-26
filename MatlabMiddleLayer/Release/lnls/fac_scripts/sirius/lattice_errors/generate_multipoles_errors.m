function errors = generate_multipoles_errors(r,varargin)

fprintf(['--- generate_multipole_errors [' datestr(now) '] ---\n']);
config = r.config.multipoles;

if ~isfield(config, 'cutoff_errors'), config.cutoff_errors = []; end
if ~isfield(config, 'rndtype'), config.rndtype = 'gaussian'; end;

families = fieldnames(config.families);
fam_idx = findcells(r.params.the_ring, 'FamName');
fam_list = getcellstruct(r.params.the_ring,'FamName',fam_idx);
for k=1:r.config.nr_machines
    for i=1:length(families)
        family = config.families.(families{i});
        if isfield(family,'rms')
            errors.(families{i}).indcs = [];
            Bn_norm = [];
            An_norm = [];
            for j=1:length(family.labels)
                label = family.labels{j};
                nrsgs = family.nrsegs(j);
                indcs = fam_idx(ismember(fam_list,label));
                errors.(families{i}).indcs = [errors.(families{i}).indcs indcs];
                nrels = length(indcs) / nrsgs;
                [Bn, An]= get_random_errors(family, nrels, nrsgs, config.cutoff_errors);%, config.rndtype);
                Bn_norm = [Bn_norm Bn];
                An_norm = [An_norm An];
            end
        errors.(families{i}).rms.Bn_norm(k,:,:) = Bn_norm;
        errors.(families{i}).rms.An_norm(k,:,:) = An_norm;    
        end
    end
end
fprintf('\n');


function [rndnr1, rndnr2] = get_random_errors(family, nrels, nrsgs, cutoff_errors)
%Componentes normais
num_orders = length(family.rms.main_values);
rndnr = zeros(1,nrels*num_orders);
sel = 1:nrels*num_orders;
while ~isempty(sel)
    rndnr(sel) = randn(1,length(sel));
    sel = find(abs(rndnr) > cutoff_errors);
end
rndnr = reshape(rndnr,num_orders,nrels);
rndnr = repmat(family.rms.main_values',1,nrels) .* rndnr;
rndnr = repmat(rndnr, nrsgs, 1);
rndnr1 = reshape(rndnr,num_orders,nrels*nrsgs);

%Componentes skew
rndnr = zeros(1,nrels*num_orders);
sel = 1:nrels*num_orders;
while ~isempty(sel)
    rndnr(sel) = randn(1,length(sel));
    sel = find(abs(rndnr) > cutoff_errors);
end
rndnr = reshape(rndnr,num_orders,nrels);
rndnr = repmat(family.rms.skew_values',1,nrels) .* rndnr;
rndnr = repmat(rndnr, nrsgs, 1);
rndnr2 = reshape(rndnr,num_orders,nrels*nrsgs);

