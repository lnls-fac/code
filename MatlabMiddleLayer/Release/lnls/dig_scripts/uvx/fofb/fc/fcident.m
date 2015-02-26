function varargout = fcident(varargin)

siso2mimo_derate_factor = 1/3;

if ischar(varargin{1}) && strcmpi(varargin{1}, 'init')
    npts_packet = varargin{2};
    expinfo = varargin{3};
    expout = [];
    if strcmpi(expinfo.excitation, 'step')
        step_duration = expinfo.duration/2;
        fcdata = [-ones(npts_packet*floor(step_duration), expinfo.ncols); ones(npts_packet*ceil(step_duration), expinfo.ncols)];
    elseif strcmpi(expinfo.excitation, 'ramp')
        ramp_duration = expinfo.duration/2;
        fcdata = [repmat(linspace(0,1,npts_packet*floor(ramp_duration))', 1, expinfo.ncols); repmat(linspace(1,0,npts_packet*floor(ramp_duration))', 1, expinfo.ncols);];
    elseif strcmpi(expinfo.excitation, 'sine')
        [fcdata, expout.freqs] = idinput([npts_packet*expinfo.duration expinfo.ncols expinfo.nperiods], 'sine', expinfo.band, [-1 1], expinfo.sinedata);
    else
        fcdata = idinput([expinfo.prbsperiod expinfo.ncols floor(expinfo.duration*npts_packet/expinfo.prbsperiod)], expinfo.excitation, expinfo.band, [-1 1]); % FIXME
        if strcmpi(expinfo.excitation, 'prbs')
            fcdata = fcdata(1:floor(npts_packet*expinfo.duration/expinfo.prbsperiod)*expinfo.prbsperiod,:);
        end
        fcdata = [fcdata; zeros(npts_packet*expinfo.duration - size(fcdata,1), size(fcdata,2))];
    end
    fcdata = [fcdata; zeros(npts_packet*expinfo.duration - size(fcdata,1), size(fcdata,2))];

    varargout = {fcdata, expout};
else
    i = varargin{1};
    npts_packet = varargin{2};
    expinfo = varargin{3};
    fprintf('packet #%d: ', i+1);

    expnumber = floor(i/(expinfo.duration + expinfo.pauselength));

    i_ = rem(i,(expinfo.duration + expinfo.pauselength));
    repeatprofiles_after = size(expinfo.profiles,1) + 1;
    profile_number = rem(expnumber, repeatprofiles_after);

    if i_ < expinfo.pauselength || (~expinfo.uncorrelated && (profile_number == 0))
        packet = zeros(npts_packet, expinfo.ncols);
        expinterval = true;
        fprintf('pause');

    else
        if profile_number == 0
            profile = diag(ones(1, size(expinfo.profiles,2)))*siso2mimo_derate_factor;
        else
            profile = expinfo.profiles(profile_number,:);
        end
        fprintf('profile #%d', profile_number);
        fcdata = varargin{4};
        indices1 = ((i_ - expinfo.pauselength)*npts_packet+(1:npts_packet));
        %indices2 = ((i - expinfo.pauselength)*npts_packet+(1:npts_packet));
        %t = ((indices2-1)*expinfo.Ts)';
        if profile_number ~= 0
            cols = 1;
        else
            cols = 1:size(profile,2);
        end
        packet = expinfo.amplitude*fcdata(indices1,cols)*profile;

        % Zero-padding
        packet = [packet zeros(npts_packet, expinfo.ncols-size(packet,2))];
        expinterval = false;
    end
    fprintf('\n');
    varargout{1} = packet;
    varargout{2} = expinterval;
end
