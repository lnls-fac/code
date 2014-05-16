% function machine = apply_errors(r, fraction, excitation_flag)
function machine = apply_errors(r, fraction, type)

% if ~exist('excitation_flag')
%     excitation_flag = 'all';
% end

if exist('type','var') && strcmp(type,'static')
    errors = r.errors.static;
elseif exist('type','var') && strcmp(type,'dynamic')
    errors = r.errors.dynamic;
else
    errors = r.errors;
end


for i=1:r.config.nr_machines
    
    if ~isfield(r, 'machine') || (length(r.machine) < i)
        machine{i}    = apply_errors_one_machine(r.params.the_ring, errors, i, fraction);
    else
        machine{i}    = apply_errors_one_machine(r.machine{i}, errors, i, fraction);
    end
%     if any(strcmpi(excitation_flag, {'ripple'}))
%         machine{i}    = apply_errors_one_machine(r.machine{i}, r.errors, i, excitation_flag, fraction);
%     else
%         machine{i}    = apply_errors_one_machine(r.params.the_ring, r.errors, i, excitation_flag, fraction);
%     end
end


% function the_ring = apply_errors_one_machine(the_ring0, errors, machine, excitation_flag, fraction)
function the_ring = apply_errors_one_machine(the_ring0, errors, machine, fraction)

the_ring  = the_ring0;

% if any(strcmpi(excitation_flag, {'ripple'}))
%
%     err = fraction * errors.errors_ripple(machine,:);
%     idx = find(err ~= 0)';
%     the_ring  = lnls_set_excitation(err(idx), idx, the_ring);
%
% else

err = fraction * errors.errors_x(machine,:);
idx = find(err ~= 0)';
the_ring  = lnls_set_misalignmentX(err(idx), idx, the_ring);

err = fraction * errors.errors_y(machine,:);
idx = find(err ~= 0)';
the_ring  = lnls_set_misalignmentY(err(idx), idx, the_ring);

err = fraction * errors.errors_roll(machine,:);
idx = find(err ~= 0)';
the_ring  = lnls_set_rotation_ROLL(err(idx), idx, the_ring);

err = fraction * errors.errors_yaw(machine,:);
idx = find(err ~= 0)';
the_ring  = lnls_set_rotation_YAW(err(idx), idx, the_ring);

err = fraction * errors.errors_pitch(machine,:);
idx = find(err ~= 0)';
the_ring  = lnls_set_rotation_PITCH(err(idx), idx, the_ring);

err = fraction * errors.errors_e(machine,:);
idx = find(err ~= 0)';
the_ring  = lnls_set_excitation(err(idx), idx, the_ring);

err = fraction * errors.errors_e_kdip(machine,:);
idx = find(err ~= 0)';
the_ring  = lnls_set_excitation_Kdip(err(idx), idx, the_ring);

% end

