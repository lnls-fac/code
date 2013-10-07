function save_tracy_flatfiles(fname)

if ~exist('fname', 'var')
    [FileName,PathName] = uigetfile('*.mat','Select mat file with machines','selection');
    if isnumeric(FileName)
        return;
    end
    fname = fullfile(PathName, FileName);
end

data = load(fname);
machine = data.machine;

for i=1:length(machine)
    fprintf(['machine #' num2str(i,'%02i') '...']);
    lnls_at2tracyflat(machine{i}, fullfile(PathName, ['rms' num2str(i,'%02i') '.dat']));
    fprintf('ok\n');
end