function generate_tracy_folders

clc;

if strcmpi(computer, 'PCWIN')
    editor = 'C:\Progra~1\Notepad++\notepad++ ';
else
    editor = 'gedit ';
end

% tracy folder
r.tracy_dir = uigetdir('../', 'Select tracy folder');
if isnumeric(r.tracy_dir)
    r.tracy_dir = getappdata(0, 'tracy_dir');
    fprintf('using tracy_dir = %s\n', r.tracy_dir);
else
    setappdata(0, 'tracy_dir', r.tracy_dir);
end

% *.mat file with machines
[FileName,PathName,FilterIndex] = uigetfile('*.mat','Select mat file with machines','');
if isnumeric(FileName)
    r.mat_file = getappdata(0, 'mat_file');
    fprintf('using mat_file = %s\n', r.mat_file);
else
    r.mat_file = fullfile(PathName, FileName);
    setappdata(0, 'mat_file', r.mat_file);
end


% edita input.prm
[FileName,PathName,FilterIndex] = uigetfile('*.prm','Select tracy INPUT file','');
if isnumeric(FileName)
    r.tracy_input_file = getappdata(0, 'tracy_input_file');
    fprintf('using tracy_input_file = %s\n', r.tracy_input_file);
else
    r.tracy_input_file = fullfile(PathName, FileName);
    system([editor r.tracy_input_file]);
    setappdata(0, 'tracy_input_file', r.tracy_input_file);
end


% edita multipolos
[FileName,PathName,FilterIndex] = uigetfile('*.dat','Select tracy MULTIPOLES file','');
if isnumeric(FileName)
    r.tracy_multipoles_file = getappdata(0, 'tracy_multipoles_file');
    fprintf('using tracy_multipoles_file = %s\n', r.tracy_multipoles_file);
else
    r.tracy_multipoles_file = fullfile(PathName, FileName);
    system([editor r.tracy_multipoles_file]);
    setappdata(0, 'tracy_multipoles_file', r.tracy_multipoles_file);
end

% edita chamber
[FileName,PathName,FilterIndex] = uigetfile('*.dat','Select tracy CHAMBER file','');
if isnumeric(FileName)
    r.tracy_chamber_file = getappdata(0, 'tracy_chamber_file');
    fprintf('using tracy_chamber_file = %s\n', r.tracy_chamber_file);
else
    r.tracy_chamber_file = fullfile(PathName, FileName);
    system([editor r.tracy_chamber_file]);
    setappdata(0, 'tracy_chamber_file', r.tracy_chamber_file);
end

% initialization
try
    rmdir(fullfile(r.tracy_dir, 'rms*'));
catch
end
data = load(r.mat_file, 'machine'); 
r.machines = data.machine;


% loop principal, gera flat_files
lnls_create_waitbar('Generating flat files', 1.0, length(r.machines));
for i=1:length(r.machines)
    
    % cria rms dir
    rms_dir = fullfile(r.tracy_dir, ['rms' num2str(i, '%02i')]);
    if ~exist(rms_dir, 'dir')
        mkdir(rms_dir);
    end
    
    [pathstr, fname_input, ext] = fileparts(r.tracy_input_file); fname_input = strrep([fname_input ext], '_template', '');
    [pathstr, fname_chamber, ext] = fileparts(r.tracy_chamber_file); fname_chamber =  strrep([fname_chamber ext], '_template', '');
    [pathstr, fname_multipoles, ext] = fileparts(r.tracy_multipoles_file); fname_multipoles =  strrep([fname_multipoles ext], '_template', '');
    
    % copia arquivo input.prm
    str_replace = {
        {'FLAT_FILENAME', ['flat_file_rms', num2str(i,'%02i'), '.dat']}, ...
        {'MULTIPOLES_FILENAME', fname_multipoles}, ...
        {'CHAMBER_FILENAME', fname_chamber}, ...
        };
    copyfile_with_str_replacement(r.tracy_input_file, fullfile(rms_dir, fname_input), str_replace); 
    
    % copia chamber
    str_replace = {};
    if exist(r.tracy_chamber_file, 'file')
        copyfile_with_str_replacement(r.tracy_chamber_file, fullfile(rms_dir, fname_chamber), str_replace);
    end
    
    % copia multipolos
    str_replace = {{'SEED_VALUE', num2str(i*100, '%03i')}};
    if exist(r.tracy_multipoles_file, 'file')
       copyfile_with_str_replacement(r.tracy_multipoles_file, fullfile(rms_dir, fname_multipoles), str_replace);
    end
    
    % gera flat_file
    this_dir = pwd(); cd(rms_dir);
    lnls_at2tracyflat(r.machines{i},  fullfile(rms_dir, ['rms' ,num2str(i, '%02i'), '.dat']));
    cd(this_dir);
    lnls_update_waitbar(i);
    
end
lnls_delete_waitbar();



function copyfile_with_str_replacement(file_src, file_des, str_replace)

fp_src = fopen(file_src, 'r');
fp_des = fopen(file_des, 'w');

while ~feof(fp_src)
    line = fgetl(fp_src);
    for i=1:length(str_replace)
        line = strrep(line, str_replace{i}{1}, str_replace{i}{2});
    end
    fprintf(fp_des, '%s\n', line);
end

fclose(fp_src);
fclose(fp_des);

