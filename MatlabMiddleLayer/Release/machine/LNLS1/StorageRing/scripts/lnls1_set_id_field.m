function lnls1_set_id_field(id, field)

global THERING;

idx = findcells(THERING, 'FamName', id);
energy = getenergymodel;
[beta gamma b_rho] = lnls_beta_gamma(energy);

% se campo � zero os elementos s�o transformados em drifts
if (field == 0)
    for i=1:length(idx)
        
        if ~strcmpi(THERING{idx(i)}.PassMethod, 'DriftPass')
            try
                THERING{idx(i)}.PassMethodOFF = THERING{idx(i)}.PassMethod;
            catch
            end
            THERING = setcellstruct(THERING, 'PassMethod', idx, 'DriftPass');
        end
        
        try
            THERING{idx(i)}.BendingAngleOFF = THERING{idx(i)}.BendingAngle;
            THERING{idx(i)} = rmfield(THERING{idx(i)}, 'BendingAngle');
        catch
        end
        THERING{idx(i)}.Field = 0;
        
    end

    return;
end

if strcmpi(id, 'AWS07')
    try
        ang0     = getcellstruct(THERING, 'BendingAngle', idx);
    catch
        ang0     = getcellstruct(THERING, 'BendingAngleOFF', idx);
    end
    len0     = getcellstruct(THERING, 'Length', idx);
    rho0     = len0 ./ ang0;
    min_rho0 = min(abs(rho0));
    min_rho  = b_rho / field;
    rho      = rho0 * (min_rho / min_rho0);
    ang      = len0 ./ rho;
    THERING  = setcellstruct(THERING, 'BendingAngle', idx, ang);
    try
        pass_methods = getcellstruct(THERING, 'PassMethodOFF', idx);
        THERING  = setcellstruct(THERING, 'PassMethod', idx, pass_methods);
    catch
    end
    THERING  = setcellstruct(THERING, 'Field', idx, field);
    THERING  = setcellstruct(THERING, 'PolynomA', idx, (min_rho0 / min_rho) * getcellstruct(THERING, 'PolynomA', idx));
    THERING  = setcellstruct(THERING, 'PolynomB', idx, (min_rho0 / min_rho) * getcellstruct(THERING, 'PolynomB', idx));
    return;
end

ids_label =  {'AWG01', 'AWG09', 'AON11'};
ids_period = [0.18, 0.06, 0.05];
ids_poles  = {...
    [0.5 repmat([-1 1],1,14) -0.5]; ...
    %[-1/4 3/4 repmat([-1 1],1,7) -1 repmat([1 -1],1,8) 3/4 -1/4]; ...
    [0.5 repmat([-1 1],1,16) -0.5];
    [-0.5 repmat([-1 1],1,56) 0.5] ...
    };


id_idx = strcmpi(ids_label, id);
period = ids_period(id_idx);
poles  = ids_poles{id_idx};
lhe     = 4 * period / pi^2;

idx1 = findcells(THERING, 'FamName', id);
idx2 = [findcells(THERING, 'BendingAngle') findcells(THERING, 'BendingAngleOFF')];
at_idx = intersect(idx1, idx2);
for i=1:length(at_idx)
    rho0       = b_rho / (poles(i)*field);
    rho        = 4 * rho0 / pi;
    this_angle = lhe/rho;
    ldr        = (period/2) - 2*rho*sin(0.5*this_angle);
    try
        THERING{at_idx(i)} = rmfield(THERING{at_idx(i)}, 'BendingAngleOFF');
    catch
    end
    THERING{at_idx(i)}.BendingAngle = this_angle;
    THERING{at_idx(i)}.EntranceAngle = this_angle/2;
    THERING{at_idx(i)}.ExitAngle = this_angle/2;
    try
        THERING{at_idx(i)}.PassMethod = THERING{at_idx(i)}.PassMethodOFF;
        THERING{at_idx(i)} = rmfield(THERING{at_idx(i)}, 'PassMethodOFF');
    catch
    end
    THERING{at_idx(i)-1}.Length = ldr/2;
    THERING{at_idx(i)+1}.Length = ldr/2;
    THERING{at_idx(i)-1}.Field = field;
    THERING{at_idx(i)}.Field = field;
    THERING{at_idx(i)+1}.Field = field;
end


%{
function lnls1_set_id_field(id, field)

global THERING;

idx = findcells(THERING, 'FamName', id);
energy = getenergymodel;
[beta gamma b_rho] = lnls_beta_gamma(energy);

% se campo � zero os elementos s�o transformados em drifts
if (field == 0) field = 1e-16; end;

if strcmpi(id, 'AWS07')
    ang0     = getcellstruct(THERING, 'BendingAngle', idx);
    len0     = getcellstruct(THERING, 'Length', idx);
    rho0     = len0 ./ ang0;
    min_rho0 = min(abs(rho0));
    min_rho  = b_rho / field;
    rho      = rho0 * (min_rho / min_rho0);
    ang      = len0 ./ rho;
    THERING  = setcellstruct(THERING, 'BendingAngle', idx, ang);
    THERING  = setcellstruct(THERING, 'Field', idx, field);
    THERING  = setcellstruct(THERING, 'PolynomA', idx, (min_rho0 / min_rho) * getcellstruct(THERING, 'PolynomA', idx));
    THERING  = setcellstruct(THERING, 'PolynomB', idx, (min_rho0 / min_rho) * getcellstruct(THERING, 'PolynomB', idx));
    return;
end
     
ids_label =  {'AWG01', 'AWG09', 'AON11'};
ids_period = [0.18, 0.06, 0.05];
ids_poles  = {...
    [0.5 repmat([-1 1],1,14) -0.5]; ...
    %[-1/4 3/4 repmat([-1 1],1,7) -1 repmat([1 -1],1,8) 3/4 -1/4]; ...
    [0.5 repmat([-1 1],1,16) -0.5];
    [-0.5 repmat([-1 1],1,56) 0.5] ...
    };


id_idx = strcmpi(ids_label, id);
period = ids_period(id_idx);
poles  = ids_poles{id_idx};
lhe     = 4 * period / pi^2;

idx1 = findcells(THERING, 'FamName', id);
idx2 = findcells(THERING, 'BendingAngle');
at_idx = intersect(idx1, idx2);
for i=1:length(at_idx)
     rho0       = b_rho / (poles(i)*field);
     rho        = 4 * rho0 / pi;
     this_angle = lhe/rho;
     ldr        = (period/2) - 2*rho*sin(0.5*this_angle);
     THERING{at_idx(i)}.BendingAngle = this_angle;
     THERING{at_idx(i)}.EntranceAngle = this_angle/2;
     THERING{at_idx(i)}.ExitAngle = this_angle/2;
     THERING{at_idx(i)-1}.Length = ldr/2;
     THERING{at_idx(i)}.Length   = lhe;
     THERING{at_idx(i)+1}.Length = ldr/2;
     THERING{at_idx(i)-1}.Field = field;
     THERING{at_idx(i)}.Field = field;
     THERING{at_idx(i)+1}.Field = field;
end
%}









