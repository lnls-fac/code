function errors = generate_multipole_errors(name, the_ring, multi, nr_machines, cutoff)

fprintf(['--- generate_multipole_errors [' datestr(now) '] ---\n']);

if ~exist('cutoff_errors', 'var'), cutoff = []; end

save([name,'_generate_multipole_errors_input.mat'], 'multi', 'nr_machines', 'cutoff');

families = fieldnames(multi);
fam_idx = findcells(the_ring, 'FamName');
fam_list = getcellstruct(the_ring,'FamName',fam_idx);
for k=1:nr_machines
    for i=1:length(families)
        family = multi.(families{i});
        errors.(families{i}).indcs = [];
        Bn_norm = [];
        An_norm = [];
        for j=1:length(family.labels)
            label = family.labels{j};
            nrsgs = family.nrsegs(j);
            indcs = fam_idx(ismember(fam_list,label));
            errors.(families{i}).indcs = [errors.(families{i}).indcs indcs];
            nrels = length(indcs) / nrsgs;
            [Bn, An]= get_random_errors(family, nrels, nrsgs, cutoff);
            Bn_norm = [Bn_norm Bn];
            An_norm = [An_norm An];
        end
        errors.(families{i}).Bn_norm(k,:,:) = Bn_norm;
        errors.(families{i}).An_norm(k,:,:) = An_norm;
    end
end
fprintf('\n');


function [rndnr1, rndnr2] = get_random_errors(family, nrels, nrsgs, cutoff_errors)
%Componentes normais
num_orders = length(family.main_vals);
rndnr = zeros(1,nrels*num_orders);
sel = 1:nrels*num_orders;
while ~isempty(sel)
    rndnr(sel) = randn(1,length(sel));
    sel = find(abs(rndnr) > cutoff_errors);
end
rndnr = reshape(rndnr,num_orders,nrels);
rndnr = repmat(family.main_vals',1,nrels) .* rndnr;
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
rndnr = repmat(family.skew_vals',1,nrels) .* rndnr;
rndnr = repmat(rndnr, nrsgs, 1);
rndnr2 = reshape(rndnr,num_orders,nrels*nrsgs);

