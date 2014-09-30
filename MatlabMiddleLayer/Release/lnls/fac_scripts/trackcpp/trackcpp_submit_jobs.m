function trackcpp_submit_jobs(path, inpfile, exec_scpt, description, possible_hosts)
cur_dir = pwd;

if ~exist('path','var'), path = pwd; end
if ~exist('inpfile','var'), inpfile = 'input.py'; end
if ~exist('exec_scpt','var'), exec_scpt = '../runjob.sh'; end
if ~exist('description','var'), description = ''; end
if ~exist('possible_hosts','var'), possible_hosts = 'all'; end
if ~exist(fullfile(path,inpfile),'file'), error('input file does not exist');end

pyjob = 'pyjob_qsub.py ';

SCRIPT = '#!/bin/bash\n\nsource ~/.bashrc\n\n%s\n';

cd(path);

[~, result] = system('ls | grep rms | wc -l');
nfolder = str2double(result);

for ii = 1:nfolder
    cd(sprintf('rms%02d',ii));
    comm = [pyjob, ' --description ', sprintf('"trcpp: rms%02d - ',ii), description,'"'];
    comm = [comm, ' --exec ', exec_scpt, ' --possibleHosts ', possible_hosts];
    [~, res] = system('ls | grep flatfile');
    comm = [comm, ' --inputFiles ', inpfile, ',',res];
    fh = fopen('tjoaieh.sh','w');
    fprintf(fh,SCRIPT,comm);
    fclose(fh);
    system('chmod gu+x tjoaieh.sh');
    unix('./tjoaieh.sh');
    system('rm tjoaieh.sh');
    cd('..');
end
cd(cur_dir);