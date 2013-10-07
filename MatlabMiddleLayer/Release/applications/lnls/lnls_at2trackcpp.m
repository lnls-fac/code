function lnls_at2trackcpp(the_ring, filename)


if ~exist('filename', 'var')
    [filename, PathName, FilterIndex] = uigetfile('*.txt','Select file to save lattice to','lattice.txt');
    if isnumeric(filename) && filename ==0, return; end
    filename = fullfile(PathName,filename);
end
    
field_sep = ' ';

fp = fopen(filename, 'w');
for i=1:length(the_ring)
    
    i_str           = [num2str(i, '%05i') field_sep];
    type_str        = [get_element_type(the_ring{i}) field_sep];
    fam_name_str    = [get_element_fam_name(the_ring{i}) field_sep];
    length_str      = [get_element_length(the_ring{i}) field_sep];  
    pass_method_str = [get_element_pass_method(the_ring{i}) field_sep]; 
    nr_steps_str    = [get_element_nr_steps(the_ring{i}) field_sep];
    angle_str       = [get_element_angle(the_ring{i}) field_sep];
    angle_in_str    = [get_element_angle_in(the_ring{i}) field_sep];
    angle_out_str   = [get_element_angle_out(the_ring{i}) field_sep];
    gap_str         = [get_element_gap(the_ring{i}) field_sep];
    fint1_str       = [get_element_fint1(the_ring{i}) field_sep];
    fint2_str       = [get_element_fint2(the_ring{i}) field_sep];
    ellip_str       = [get_element_ellip(the_ring{i}) field_sep];
    ax_str          = [get_element_ax(the_ring{i}) field_sep];
    ay_str          = [get_element_ay(the_ring{i}) field_sep];
    err_dx_str      = [get_element_err_dx(the_ring{i}) field_sep];
    err_dy_str      = [get_element_err_dy(the_ring{i}) field_sep];
    err_excit_str   = [get_element_err_excit(the_ring{i}) field_sep];
    err_roll_str    = [get_element_err_roll(the_ring{i}) field_sep];
    err_pitch_str   = [get_element_err_pitch(the_ring{i}) field_sep];
    err_yaw_str     = [get_element_err_yaw(the_ring{i}) field_sep];
%     hkick_str       = [get_element_hkick(the_ring{i}) field_sep];
%     vkick_str       = [get_element_vkick(the_ring{i}) field_sep];
%     thin_KL_str     = [get_element_thin_KL(the_ring{i}) field_sep];
%     thin_SL_str     = [get_element_thin_SL(the_ring{i}) field_sep];
%     polynomA_str    = [get_element_polynomA(the_ring{i}) field_sep];
%     polynomB_str    = [get_element_polynomB(the_ring{i}) field_sep];
    
    fprintf(fp, i_str);
    fprintf(fp, type_str);
    fprintf(fp, fam_name_str);
    fprintf(fp, length_str);
    fprintf(fp, pass_method_str);
    fprintf(fp, nr_steps_str);
    fprintf(fp, angle_str);
    fprintf(fp, angle_in_str);
    fprintf(fp, angle_out_str);
    fprintf(fp, gap_str);
    fprintf(fp, fint1_str);
    fprintf(fp, fint2_str);
    fprintf(fp, ellip_str);
    fprintf(fp, ax_str);
    fprintf(fp, ay_str);
    fprintf(fp, err_dx_str);
    fprintf(fp, err_dy_str);
    fprintf(fp, err_excit_str);
    fprintf(fp, err_roll_str);
    fprintf(fp, err_pitch_str);
    fprintf(fp, err_yaw_str);
%     fprintf(fp, hkick_str);
%     fprintf(fp, vkick_str);
%     fprintf(fp, thin_KL_str);
%     fprintf(fp, thin_SL_str);
%     fprintf(fp, polynomA_str);
%     fprintf(fp, polynomB_str);
    
    fprintf(fp, '\r\n');
    
%         fprintf(fp, "%05i ",     i);
% 		fprintf(fp, "%02i ",     element.type);
% 		fprintf(fp, "%20s ",     element.fam_name.c_str());
% 		fprintf(fp, "%24.16e ",  element.length);
% 		fprintf(fp, "%03i ",     element.pass_method);
% 		fprintf(fp, "%03i ",     element.nr_steps);
% 		fprintf(fp, "%+24.16e ", element.angle);
% 		fprintf(fp, "%+24.16e ", element.angle_in);
% 		fprintf(fp, "%+24.16e ", element.angle_out);
% 		fprintf(fp, "%24.16e ",  element.gap);
% 		fprintf(fp, "%+24.16e ", element.fint1);
% 		fprintf(fp, "%+24.16e ", element.fint2);
% 		fprintf(fp, "%1i ",      element.ellip_chamber);
% 		fprintf(fp, "%24.16e ",  element.ax);
% 		fprintf(fp, "%24.16e ",  element.ay);
% 		fprintf(fp, "%+24.16e ", element.err_dx);
% 		fprintf(fp, "%+24.16e ", element.err_dy);
% 		fprintf(fp, "%+24.16e ", element.err_excit);
% 		fprintf(fp, "%+24.16e ", element.err_roll);
% 		fprintf(fp, "%+24.16e ", element.err_pitch);
% 		fprintf(fp, "%+24.16e ", element.err_yaw);
% 		fprintf(fp, "%+24.16e ", element.hkick);
% 		fprintf(fp, "%+24.16e ", element.vkick);
% 		fprintf(fp, "%+24.16e ", element.thin_KL);
% 		fprintf(fp, "%+24.16e ", element.thin_SL);
% 		fprintf(fp, "%02i ",(int)element.polynom_a.size());
% 		for(int j=0; j<element.polynom_a.size(); ++j) {
% 			fprintf(fp, "%+24.16e ", element.polynom_a[j]);
% 		}
% 		fprintf(fp, "%02i ",(int)element.polynom_b.size());
% 		for(int j=0; j<element.polynom_b.size(); ++j) {
% 			fprintf(fp, "%+24.16e ", element.polynom_b[j]);
% 		}
% 		fprintf(fp, "\n");

end
fclose(fp);


function str = get_element_err_pitch(element)

fmt = '%+24.16e';
if isfield(element, 'T1')
    pitch = element.T1(4);
    str = num2str(roll, fmt);
else
    str = num2str(0, fmt);
end

function str = get_element_err_roll(element)

fmt = '%+24.16e';
if isfield(element, 'R1')
    roll = asin(element.R1(1,3));
    str = num2str(roll, fmt);
else
    str = num2str(0, fmt);
end

function str = get_element_err_excit(element)

fmt = '%+24.16e';
str = num2str(0, fmt);

function str = get_element_err_dy(element)

fmt = '%+24.16e';

if isfield(element, 'T1')
    pitch = element.T1(4);
    dy  = -(element.T1(3) + (element.Length/2) * pitch);
    str = num2str(dy, fmt);
else
    str = num2str(0, fmt);
end

function str = get_element_err_dx(element)

fmt = '%+24.16e';

if isfield(element, 'T1')
    yaw = element.T1(2);
    dx  = -(element.T1(1) + (element.Length/2) * yaw);
    str = num2str(dx, fmt);
else
    str = num2str(0, fmt);
end


function str = get_element_ay(element)

fmt = '%24.16e';
max_float = '1.7976931348623157e+308';

if isfield(element, 'VChamber')
    str = num2str(element.VChamber(2), fmt);
else
    str = max_float;
end

function str = get_element_ax(element)

fmt = '%24.16e';
max_float = '1.7976931348623157e+308';

if isfield(element, 'VChamber')
    str = num2str(element.VChamber(1), fmt);
else
    str = max_float;
end

function str = get_element_ellip(element)

fmt = '%1i';
if isfield(element, 'VChamber') && (element.VChamber(3) == 2)
    str = num2str(1, fmt);
else
    str = num2str(0, fmt);
end

function str = get_element_fint2(element)

fmt = '%+24.16e';
if isfield(element, 'FringeInt2')
    str = num2str(element.FringeInt2, fmt);
else
    str = num2str(0, fmt);
end

function str = get_element_fint1(element)

fmt = '%+24.16e';
if isfield(element, 'FringeInt1')
    str = num2str(element.FringeInt1, fmt);
else
    str = num2str(0, fmt);
end

function str = get_element_gap(element)

fmt = '%24.16e';
if isfield(element, 'FullGap')
    str = num2str(element.FullGap, fmt);
else
    str = num2str(0, fmt);
end

function str = get_element_angle_out(element)

fmt = '%+24.16e';
if isfield(element, 'ExitAngle')
    str = num2str(element.ExitAngle, fmt);
else
    str = num2str(0, fmt);
end

function str = get_element_angle_in(element)

fmt = '%+24.16e';
if isfield(element, 'EntranceAngle')
    str = num2str(element.EntranceAngle, fmt);
else
    str = num2str(0, fmt);
end

function str = get_element_angle(element)

fmt = '%+24.16e';
if isfield(element, 'BendingAngle')
    str = num2str(element.BendingAngle, fmt);
else
    str = num2str(0, fmt);
end

function str = get_element_nr_steps(element)

fmt = '%03i';
if isfield(element, 'NumIntSteps')
    str = num2str(element.NumIntSteps, fmt);
else
    str = num2str(1, fmt);
end


function str = get_element_length(element)

fmt = '%24.16e';
str = num2str(element.Length, fmt);

function str = get_element_pass_method(element)

fmt = '%03i';

pm_identity = 0;
pm_drift = 1;
pm_thinquad = 2;
pm_thickquad = 3;
pm_thinsext = 4;
pm_strmpolesymplectic4pass = 5;
pm_bndmpolesymplectic4pass = 6;
pm_correctorpass = 7;

if strcmpi(element.PassMethod, 'CorrectorPass')
    str = num2str(pm_correctorpass, fmt);
    return;
end

if strcmpi(element.PassMethod, 'DriftPass')
    str = num2str(pm_drift, fmt);
    return;
end

if strcmpi(element.PassMethod, 'BndMPoleSymplectic4Pass')
    str = num2str(pm_bndmpolesymplectic4pass, fmt);
    return;
end

if strcmpi(element.PassMethod, 'StrMPoleSymplectic4Pass')
    str = num2str(pm_strmpolesymplectic4pass, fmt);
    return;
end

if strcmpi(element.PassMethod, 'IdentityPass')
    str = num2str(pm_identity, fmt);
    return;
end

error('problem converting at2trackpp: pass_method not defined!');

    
function str = get_element_fam_name(element)

fmt = '%20s';
str = sprintf(fmt, element.FamName);
    
function str = get_element_type(element)

% enum enum_pm        { pm_identity, pm_drift, pm_thinquad, pm_thickquad, pm_thinsext, pm_strmpolesymplectic4pass, pm_bndmpolesymplectic4pass, pm_correctorpass };
% enum enum_type      { tp_marker, tp_drift, tp_quadrupole, tp_sextupole, tp_bend, tp_bpm, tp_hcorrector, tp_vcorrector, tp_scorrector };

fmt = '%02i';

tp_marker = 0;
tp_drift  = 1;
tp_quadrupole = 2;
tp_sextupole = 3;
tp_bend = 4;
tp_bpm = 5;
tp_hcorrector = 6;
tp_vcorrector = 7;
tp_scorrector = 8;

% tp_hcorrector and tp_vcorrector
if strcmpi(element.PassMethod, 'CorrectorPass')
    if strcmpi(element.FamName, 'hcm')
        str = num2str(tp_hcorrector, fmt);
    elseif strcmpi(element.FamName, 'vcm')
        str = num2str(tp_vcorrector, fmt);
    elseif abs(element.KickAngle(2)) > abs(element.KickAngle(1))
        str = num2str(tp_hcorrector, fmt);
    else
        str = num2str(tp_vcorrector, fmt);
    end
    return;
end

% tp_bpm
if any(strcmpi(element.FamName, {'bpm','bpmx','bpmy'})) && strcmpi(element.PassMethod, 'IdentityPass')
    str = num2str(tp_bpm, fmt);
    return;
end

% tp_drift
if strcmpi(element.PassMethod, 'DriftPass')
    str = num2str(tp_drift, fmt);
    return;
end

% tp_bend      
if strcmpi(element.PassMethod, 'BndMPoleSymplectic4Pass')
    str = num2str(tp_bend, fmt);
    return;
end

% tp_quadrupole, tp_scorrector
if strcmpi(element.PassMethod, 'StrMPoleSymplectic4Pass') && isfield(element, 'K')
    if abs(element.PolynomA(2)) > abs(element.PolynomB(2))
        str = num2str(tp_scorrector, fmt);
    else
        str = num2str(tp_quadrupole, fmt);
    end
    return;
end

% tp_sextupole
if strcmpi(element.PassMethod, 'StrMPoleSymplectic4Pass')
    str = num2str(tp_sextupole, fmt);
    return;
end

% tp_marker
if strcmpi(element.PassMethod, 'IdentityPass')
    str = num2str(tp_marker, fmt);
    return;
end


error('problem converting at2trackpp: type not defined!');
