function machine = apply_multipoles_errors(r)

errors = r.errors.multipoles;
config = r.config.multipoles.families;

machine = cell(1,r.config.nr_machines);
for i=1:r.config.nr_machines
    
    if ~isfield(r, 'machine') || (length(r.machine) < i)
        machine{i}    = apply_multipoles_errors_one_machine(r.params.the_ring, errors, config, i);
    else
        machine{i}    = apply_multipoles_errors_one_machine(r.machine{i}, errors, config, i);
    end
end


function the_ring = apply_multipoles_errors_one_machine(the_ring0, errors, config, machine)

the_ring  = the_ring0;

families = fieldnames(errors);
for ii =1:length(families);
    errors_fam = errors.(families{ii});
    config_fam = config.(families{ii});
    
    rms_monomials = config_fam.rms.order;
    sys_monomials = config_fam.sys.order;
    r0 = config_fam.r0;
    main_monomial = config_fam.main_multipole;
    idx = errors.(families{ii}).indcs;
    
    Bn_norm = zeros(max([rms_monomials, sys_monomials]),length(idx));
    An_norm = Bn_norm;
    Bn_norm(rms_monomials,:) = squeeze(errors_fam.rms.Bn_norm(machine,:,:));
    An_norm(rms_monomials,:) = squeeze(errors_fam.rms.An_norm(machine,:,:));
    Bn_norm(sys_monomials,:) = Bn_norm(sys_monomials,:) + repmat(config_fam.sys.main_values',1,length(idx));
    An_norm(sys_monomials,:) = An_norm(sys_monomials,:) + repmat(config_fam.sys.skew_values',1,length(idx));
    
    the_ring  = lnls_set_multipoles(the_ring, Bn_norm, An_norm, main_monomial, r0, idx);
end
