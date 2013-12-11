function r = archive_machines(r0, save_load, label)

r = r0;
if strcmpi(save_load, 'save')
    machine = r.machine;
    save([r.config.label '_' label '.mat'], 'machine');
elseif strcmpi(save_load, 'load')
    data = load([r.config.label '_' label '.mat']);
    r.machine = data.machine;
end