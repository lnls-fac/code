function mode = sirius_get_mode_number(mode_label)

if strcmpi(mode_label, {'a'})
    mode = 1;
elseif strcmpi(mode_label, {'b'})
    mode = 2;
end