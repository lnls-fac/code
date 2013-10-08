clear all;
RandStream.setGlobalStream(RandStream('mt19937ar','seed', 131071));
% first, we load the lattice
storage_ring_ref = sirius_lattice('AC10_3');
lattice_errors([pwd '/cod_matlab']);
machines = load([pwd '/cod_matlab/CONFIG_machines_cod_corrected.mat']);
storage_ring = machines.machine{1};

% now, we define which families will be used to optimize the phase space
% and which will be used to correct chromaticity;
opt.fam = {'sa1','sa2','sb1','sb2','sd2','sd3','sf2'};
chr.fam = {'sd1','sf1'};

%what is our target chromaticity?
chr.value = [0,0];

% now we find the indexes of the elements in the ring:
opt.ind = cell(1,length(opt.fam));
opt.size = zeros(length(opt.fam),1);
chr.ind = cell(1,length(chr.fam));
for ii=1:length(opt.fam)
    opt.ind{ii} = findcells(storage_ring,'FamName',opt.fam{ii});
    opt.size(ii) = length(opt.ind{ii}); % get the number of elements in each family
end
for ii=1:length(chr.fam)
    chr.ind{ii} = findcells(storage_ring,'FamName',chr.fam{ii});
end
opt.ind = cell2mat(opt.ind); % transform to vector;


% Lets define our initial point:
% vec = [-115.7829759411277/2,  49.50386128829739/2, -214.5386552515188/2,...
%     133.1252391065637/2, -164.3042864671946/2, -289.9270429064217/2,...
%     333.7039740852999/2];

% vec = [-67.6329   18.4370 -130.5790   59.2409  -85.2405 -139.4236  169.3679];
vec = [-58.9405   25.1813 -107.7365   65.8960  -80.1791 -143.6776  162.9090];

% vec = [-60.239229   19.517471 -134.941867   62.009293  -83.880300 -171.306748  203.282027];


% what will be our error level:
err_level = 10/100;

%% now we begin the optimization:

% first we calculate the initial parameters 
[res chr.val] = optimize_fun(storage_ring, storage_ring_ref, vec, opt, chr);

% and begin the main loop
for ii=1:1000000
    err = lnls_generate_random_numbers(err_level, length(opt.fam),'uniform',1,0);
    newvec = vec.*(1+err);
    [newres newval] = optimize_fun(storage_ring, storage_ring_ref, newvec, opt, chr);
    if newres < res
        res = newres;
        vec = newvec;
        chr.val = newval;
        fprintf('%d: %10.6f  vec =  ',ii,res);
        fprintf('%12.6f',vec);
        fprintf('\n');
        for jj = 1:length(opt.fam)
            fprintf('    %3s_strength       = %10.4f;\n',opt.fam{jj}, vec(jj));
        end
        for jj = 1:length(chr.fam)
            fprintf('    %3s_strength       = %10.4f;\n',chr.fam{jj}, chr.val(jj));
        end
    end
end
    