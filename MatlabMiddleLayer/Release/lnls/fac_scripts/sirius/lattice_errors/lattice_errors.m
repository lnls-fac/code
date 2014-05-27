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
    config_folder = fullfile(lnls_get_root_folder(), 'data', 'sirius_mml', 'lattice_errors','CONFIG_V500_AC10_5_40ums_IDs_phase2');
end

cd(config_folder);

% carrega configuracaoo com parametros do calculo
fprintf('< loading configuration parameters... > \n\n');
if ~exist('r','var')
    mfiles = dir('*.m'); config_label = strrep(mfiles(1).name,'.m','');
    r = eval(config_label);
end
selection = 1:r.config.nr_machines;
%selection = 4;
fprintf('\n');

if ~isfield(r,'question') || r.question
    % cria um dialogo que questão para informar sobre as mudancas no código
    texto = sprintf(['O código lattice_errors foi alterado no dia 03/04/2014 para ' ...
        'separar o estudo dos erros lentos e dos rápidos. Isso implicou mudanças ' ...
        'no script de configuração. Há uma versão atual desse script na pasta em '...
        'que está o lattice_errors. \n Você deseja continuar?\n\n Ps.:Se você '...
        'não quer mais ver essa mensagem, crie uma variavel ''r.question = false'' '...
        'no arquivo de configuração.']);
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
if r.config.simulate_dynamic
    r.errors.dynamic = generate_errors(r,'dynamic');
end


if r.config.simulate_static
    
    % aplica erros a otica nominal e retorna estrutura com as maquinas aleatorias
    fprintf('< applying random errors to bare lattice (ramping up) ... > \n\n');
    
    for i=1:length(r.config.static.errors_delta)
        
        r.machine = apply_errors(r, r.config.static.errors_delta(i),'static');
        
        if (i == 1)
            sext_idx = getappdata(0, 'Sextupole_Idx');
            % desliga IDS para eliminar restrição física
            for m=selection
                r.machine{m} = set_ids(r.machine{m}, 'off');
                sext_str{m}  = getcellstruct(r.machine{m}, 'PolynomB', sext_idx, 1, 3);
                r.machine{m} = set_sextupoles(r.machine{m}, 0, sext_str{m});
            end
            % faz calculo da trajetoria distorcida (com sextupolos e IDs zerados)
            fprintf('< calculating COD with sextupoles off... > \n\n');
            r.init_cod = calc_init_cod(r, selection);
        elseif (i == length(r.config.static.errors_delta))
            % liga IDS para eliminar restrição física
            for m=selection
                r.machine{m} = set_ids(r.machine{m}, 'on');
                r.machine{m} = set_sextupoles(r.machine{m}, 1, sext_str{m});
            end
        end
        
        if r.params.static.cod_correction_flag    
            % faz correcao de orbita ligando gradualmente os campos dos
            % sextupolos e os IDs (apos 1a iteracao da correcao)
            fprintf('< correcting COD ... > \n\n');
            r = correct_cod_slow(r, selection, r.params.static.cod_sextupoles_ramp, r.params.static.cod_svs, r.params.static.cod_nr_iter);
        end
    end
    r = archive_machines(r, 'save', 'machines_cod_corrected');
    
    if r.params.static.optics_correction_flag
        % faz simetrizacao da rede
        fprintf('< symmetrizing optics of random machines... > \n\n');
        r.machine = correct_optics(r, selection, r.params.static.optics_svs, r.params.static.optics_nr_iter);
        r = archive_machines(r, 'save', 'machines_cod_symm_corrected'); % liga IDs antes de salvar
    end
    
    if r.params.static.coup_correction_flag
        % faz correcao de acoplamento
        fprintf('< correcting coupling... > \n\n');
        r.machine = correct_coupling(r, selection, r.params.static.coup_svs, r.params.static.coup_nr_iter);
        r = archive_machines(r, 'save', 'machines_cod_symm_coup_corrected'); % liga IDs antes de salvar
    end
end


if r.config.simulate_dynamic
    
    r.params.dynamic.ref_cod = get_reference_orbit(r, selection);
    
    fprintf('< applying dynamic random errors to lattices ... > \n\n');

    r.machine = apply_errors(r,1,'dynamic');
 
    if r.params.dynamic.cod_correction_flag
        fprintf('< correcting COD > \n\n');
        r = correct_cod_fast(r, selection, r.params.dynamic.cod_svs, r.params.dynamic.cod_nr_iter);
    end
r = archive_machines(r, 'save', 'machines_cod_corrected');
end

% salva estruturas de dados
save([r.config.label '.mat'], 'r');

% finalizacoes
fclose('all');
cd('../');
