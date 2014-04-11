function ref_cod = get_reference_orbit(r,selection)

ref_cod.codx = zeros(r.config.nr_machines, length(r.params.the_ring));
ref_cod.cody = zeros(r.config.nr_machines, length(r.params.the_ring));

if isfield(r,'machine')
    for i=selection
        [codx cody] = calc_cod(r.machine{i});
        ref_cod.codx(i,:) = codx;
        ref_cod.cody(i,:) = cody;
    end
else
    [codx cody] = calc_cod(r.params.the_ring);
    ref_cod.codx(selection,:) = repmat(codx,length(selection),1);
    ref_cod.cody(selection,:) = repmat(cody,length(selection),1);
end