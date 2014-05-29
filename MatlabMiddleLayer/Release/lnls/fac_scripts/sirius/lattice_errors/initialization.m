function params = initialization(r, varargin)

% 2013-05-02: agora script checa consistencia the the_ring antes de aceitar
% matrizes respostas lidas em arquivos.

% argument processing
read_coup_respm = false;
read_cod_respm  = false;
read_opt_respm  = false;
for i=1:length(varargin)
    if ischar(varargin{i}) && strcmpi(varargin{i}, 'ReadCoupRespM')
        read_coup_respm = true;
    elseif ischar(varargin{i}) && strcmpi(varargin{i}, 'ReadCODRespM')
        read_cod_respm = true;
    elseif ischar(varargin{i}) && strcmpi(varargin{i}, 'ReadOptRespM')
        read_opt_respm = true;
    end
end


fprintf(['--- initialization [' datestr(now) '] ---\n']);

params = r.params;

%RandStream.setDefaultStream(RandStream('mt19937ar','seed', 131071));
RandStream.setGlobalStream(RandStream('mt19937ar','seed', 131071));
 
%Warning: The RandStream.setDefaultStream static method will be removed in a future
%release.  Use RandStream.setGlobalStream instead. 

% turn sextupoles off
params.the_ring = turn_longitudinal_dynamics_off(params.the_ring);

% stores index of sextupoles in the ring
sext_idx = findcells(params.the_ring, 'PolynomB');
setappdata(0, 'Sextupole_Idx', sext_idx);
fprintf('\n');

% saves file with nominal optics
% the_ring = params.the_ring; save([r.config.label '_the_ring.mat'], 'the_ring');

if r.config.simulate_static
    % calcs cod response matrix
    fname = [r.config.label '_static_respm_cod.mat'];
    if params.static.cod_correction_flag
        if (read_cod_respm && exist(fname, 'file'))
            data = load(fname);
            params.static.cod_respm = data.cod_respm;
        end
        if (~read_cod_respm || ~exist(fname, 'file') || ~isfield(data, 'the_ring') || ~isequal(data.the_ring,  params.the_ring))
            the_ring = set_ids(params.the_ring, 'off');
            cod_respm = calc_respm_cod(the_ring, params.static.bpm_idx, params.static.hcm_idx, params.static.vcm_idx);
            %cod_respm = calc_respm_cod(params.the_ring, params.static.bpm_idx, params.static.hcm_idx, params.static.vcm_idx);
            params.static.cod_respm = cod_respm.respm;
            the_ring = params.the_ring;
            cod_respm = params.static.cod_respm;
            save(fname, 'cod_respm','the_ring');
        end
    end
    
    % calcs coupling correction matrix
    fname = [r.config.label '_respm_coupling.mat'];
    if params.static.coup_correction_flag
        if (~read_coup_respm || ~exist(fname, 'file'))
            coup_respm = calc_respm_coupling(params.the_ring, params.static.bpm_idx, params.static.hcm_idx, params.static.vcm_idx, params.static.scm_idx);
            params.static.coup_respm = coup_respm;
            save(fname, 'coup_respm');
        else
            data = load(fname);
            params.static.coup_respm = data.coup_respm;
        end
    end
    
    % calcs optics symmetrization matrix
    fname = [r.config.label '_respm_optics.mat'];
    if params.static.optics_correction_flag
        if (~read_opt_respm || ~exist(fname, 'file'))
            opt_respm = calc_respm_optics(params.the_ring, params.static.kbs_idx);
            params.static.opt_respm = opt_respm;
            save(fname, 'opt_respm');
        else
            data = load(fname);
            params.static.opt_respm = data.opt_respm;
        end
    end
end

if r.config.simulate_dynamic
    fname = [r.config.label '_dynamic_respm_cod.mat'];
    if params.dynamic.cod_correction_flag
        if (read_cod_respm && exist(fname, 'file'))
            data = load(fname);
            params.dynamic.cod_respm = data.cod_respm;
        end
        if (~read_cod_respm || ~exist(fname, 'file') || ~isfield(data, 'the_ring') || ~isequal(data.the_ring,  params.the_ring))
            cod_respm = calc_respm_cod(params.the_ring, params.dynamic.bpm_idx, params.dynamic.hcm_idx, params.dynamic.vcm_idx);
            params.dynamic.cod_respm = cod_respm.respm;
            the_ring = params.the_ring;
            cod_respm = params.dynamic.cod_respm;
            save(fname, 'cod_respm','the_ring');
        end
    end
end

function the_ring = turn_longitudinal_dynamics_off(the_ring0)

global THERING;
TR0 = THERING;
THERING = the_ring0;
setcavity('off');
setradiation('off');
the_ring = THERING;
THERING = TR0;





