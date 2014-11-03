function r = lattice_errors(varargin)

%clc; % close('all'); fclose('all'); drawnow;
current_dir = pwd;
% apaga variaveis temporarias criadas em appdata por calculos anteriores
clear_appdata();
p = mfilename('fullpath');
[pathstr, ~, ~] = fileparts(p); 
cd(pathstr);

% testa se input e uma estrutura ou string
if ~isempty(varargin)
    if isstruct(varargin{1})
        r = varargin{1};
        config_folder = current_dir;
    elseif ischar(varargin{1})
        config_folder = varargin{1};
    end
    
    % inicializacoes basicas
else
    % files = dir(); if ~any(strcmpi('lattice_errors.m', {files.name})), cd('../'); end
    % config_folder = fullfile(lnls_get_root_folder(), 'data', 'sirius_mml', 'lattice_errors','CONFIG_V500_AC10_5_40ums_IDs_new_order_symm_coup');
    %config_folder = fullfile(lnls_get_root_folder(), 'data', 'sirius_mml', 'lattice_errors','BOOSTER_V810');
    %config_folder = fullfile(lnls_get_root_folder(), 'data', 'sirius', 'bo', 'beam_dynamics', 'oficial', 'v900', 'multi.cod.physap', 'cod_matlab');
    %config_folder = fullfile(lnls_get_root_folder(), 'data', 'sirius', 'bo', 'beam_dynamics', 'calcs', 'v900', 'multi.cod.physap.bpm.error.free', 'cod_matlab');
    %config_folder = fullfile(lnls_get_root_folder(), 'data', 'sirius', 'bo', 'beam_dynamics', 'calcs', 'v900', 'multi.cod.physap.chroms.corrected', 'cod_matlab');
    %config_folder = fullfile(lnls_get_root_folder(), 'data', 'sirius', 'bo', 'beam_dynamics','calcs','v901','multi.cod.physap.prev.bend.sys.multipoles','cod_matlab');
    config_folder = fullfile(lnls_get_root_folder(), 'data', 'sirius', 'bo', 'beam_dynamics','calcs','v901','multi.cod.physap.new.qf.multipoles','cod_matlab');
    %config_folder = fullfile(lnls_get_root_folder(), 'data', 'sirius', 'bo', 'beam_dynamics', 'oficial', 'v810', 'multi.cod.physap', 'cod_matlab');                     
    %config_folder = fullfile(lnls_get_root_folder(), 'data', 'sirius', 'bo', 'beam_dynamics', 'oficial', 'v810', 'multi.cod.physap.corr.mult.off', 'cod_matlab');                     
end

cd(config_folder);

% carrega configuracaoo com parametros do calculo
fprintf('< loading configuration parameters... > \n\n');
if ~exist('r','var')
    mfiles = dir('CONFIG*.m'); config_label = strrep(mfiles(1).name,'.m','');
    r = eval(config_label);
end
selection = 1:r.config.nr_machines;
%selection = 4;
fprintf('\n');

if ~isfield(r,'questiona') || r.questiona
    % cria um dialogo que questão para informar sobre as mudancas no código
    texto = sprintf(['O código lattice_errors foi alterado no dia 10/07/2014 para ' ...
        'incluir a opcao de adicionar erros multipolares nos modelos do anel. Isso ' ...
        'implicou mudanças no script de configuração. Há uma versão atual desse '...
        'script na pasta em que está o lattice_errors. \n Você deseja continuar?\n'...
        '\n Ps.:Se você não quer mais ver essa mensagem, crie uma variavel '...
        '''r.questiona = false'' no arquivo de configuração.']);
    choice = questdlg(texto, 'Alteração de programa', 'Continuar', 'Parar','Parar');
    switch choice
        case 'Continuar'
        otherwise
            cd(current_dir);
            return;
    end
end


% calcula estruturas auxiliares baseadas nos par??metros de configura????o
fprintf('< initializing data structures... > \n\n');
r.params = initialization(r, 'ReadCODRespM', 'ReadCoupRespM', 'ReadOptRespM');

% gera vetores com erros
fprintf('< generating random errors... > \n\n');
if r.config.simulate_static
    r.errors.static  = generate_errors(r,'static');
end
if r.config.simulate_multipoles
    r.errors.multipoles  = generate_multipoles_errors(r);
end
if r.config.simulate_dynamic
    r.errors.dynamic = generate_errors(r,'dynamic');
end

name_saved_machines = 'machines';
if r.config.simulate_static
    
    % aplica erros a otica nominal e retorna estrutura com as maquinas aleatorias
    fprintf('< applying random errors to bare lattice ... > \n\n');
    
    for i=1:length(r.config.static.errors_delta)
        
        r.machine = apply_errors(r, r.config.static.errors_delta(i),'static');
        
        % desliga IDS para eliminar restrição física
        if (i == 1)
%             for m=selection
%                 r.machine{m} = set_ids(r.machine{m}, 'off');
%             end
            % faz calculo da trajetoria distorcida (com sextupolos e IDs zerados)
            fprintf('< calculating COD with sextupoles off... > \n\n');
            r.init_cod = calc_init_cod(r, selection);
        end
        
%         % liga IDS para eliminar restrição física
%         if (i == length(r.config.static.errors_delta))
%             for m=selection
%                 r.machine{m} = set_ids(r.machine{m}, 'on');
%             end
%         end
%         
        if r.params.static.cod_correction_flag    
            % faz correcao de orbita ligando gradualmente os campos dos
            % sextupolos e os IDs (apos 1a iteracao da correcao)
            fprintf('< correcting COD ... > \n\n');
            r=correct_cod_slow(r,selection,r.params.static.cod_sextupoles_ramp, ...
                          r.params.static.cod_svs, r.params.static.cod_nr_iter);
        end
    end
    if r.params.static.cod_correction_flag
        name_saved_machines = [name_saved_machines '_cod_corrected'];
    else
        name_saved_machines = [name_saved_machines '_cod'];
    end
    r = archive_machines(r, 'save', name_saved_machines);
    
    if r.params.static.optics_correction_flag
        % faz simetrizacao da rede
        fprintf('< symmetrizing optics of random machines... > \n\n');
        r.machine = correct_optics(r, selection, r.params.static.optics_svs, ...
                                   r.params.static.optics_nr_iter);
        name_saved_machines = [name_saved_machines '_symm'];
        r = archive_machines(r, 'save', name_saved_machines); % liga IDs antes de salvar
    end
    
    if r.params.static.coup_correction_flag
        % faz correcao de acoplamento
        fprintf('< correcting coupling... > \n\n');
        r.machine = correct_coupling(r, selection, r.params.static.coup_svs, ...
                                     r.params.static.coup_nr_iter);
        name_saved_machines = [name_saved_machines '_coup'];
        r = archive_machines(r, 'save', name_saved_machines);
    end
    
    if r.params.static.tune_correction_flag
        % faz correcao de tune
        r.machine = correct_tune_machines(r, selection);
        name_saved_machines = [name_saved_machines '_tune'];
        r = archive_machines(r, 'save', name_saved_machines);
    end
end

if r.config.simulate_multipoles
    fprintf('< applying multipole errors to bare lattice ... > \n\n');
    r.machine = apply_multipoles_errors(r);
    name_saved_machines = [name_saved_machines '_multi'];
    r = archive_machines(r, 'save', name_saved_machines);
end

if r.config.simulate_dynamic
    
    r.params.dynamic.ref_cod = get_reference_orbit(r, selection);
    
    fprintf('< applying dynamic random errors to lattices ... > \n\n');

    r.machine = apply_errors(r,1,'dynamic');
    
    name_saved_machines = [name_saved_machines '_dyn_cod'];
 
    if r.params.dynamic.cod_correction_flag
        fprintf('< correcting COD > \n\n');
        r = correct_cod_fast(r, selection, r.params.dynamic.cod_svs, ...
                             r.params.dynamic.cod_nr_iter);
        name_saved_machines = [name_saved_machines '_corrected'];
    end
    r = archive_machines(r, 'save', name_saved_machines);    
end

% salva estruturas de dados
save([r.config.label '.mat'], 'r');

% finalizacoes
fclose('all');
cd('../');
