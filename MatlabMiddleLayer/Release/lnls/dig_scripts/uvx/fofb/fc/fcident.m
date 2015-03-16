function varargout = fcident(varargin)

ncols = 50;

if ischar(varargin{1}) && strcmpi(varargin{1}, 'init')
    npts_packet = varargin{2};
    expinfo = varargin{3};
    expout = [];
    
    if strcmpi(expinfo.excitation, 'prbs') || strcmpi(expinfo.excitation, 'sine')
        nperiods = floor(expinfo.duration*npts_packet/expinfo.period);
    end
    
    if strcmpi(expinfo.excitation, 'step')
        step_duration = expinfo.duration/2;
        fcdata = [-ones(npts_packet*floor(step_duration), 1); ones(npts_packet*ceil(step_duration), 1)];
    elseif strcmpi(expinfo.excitation, 'ramp')
        ramp_duration = expinfo.duration/2;
        fcdata = [repmat(linspace(0,1,npts_packet*floor(ramp_duration))', 1, 1); repmat(linspace(1,0,npts_packet*floor(ramp_duration))', 1, 1);];
    elseif strcmpi(expinfo.excitation, 'sine')
        [fcdata, expout.freqs] = idinput([expinfo.period 1 nperiods], 'sine', expinfo.band, [-1 1], expinfo.sinedata);
    elseif strcmpi(expinfo.excitation, 'prbs')
        fcdata = idinput([expinfo.period 1 nperiods], expinfo.excitation, expinfo.band, [-1 1]);
    end
    fcdata = [fcdata; zeros(npts_packet*expinfo.duration - size(fcdata,1), size(fcdata,2))];
    
    varargout = {fcdata, expout};
else
    i = varargin{1};
    npts_packet = varargin{2};
    expinfo = varargin{3};
    
    fprintf('packet #%d: ', i+1);
    
    profile_number = floor(i/(expinfo.duration + expinfo.pauselength)) + 1;

    i_ = rem(i,(expinfo.duration + expinfo.pauselength));

    if i_ < expinfo.pauselength
        packet = zeros(npts_packet, ncols);
        expinterval = true;
        fprintf('pause');
       
    else
        profile = expinfo.profiles(profile_number,:);

        fprintf('profile #%d', profile_number);
        fcdata = varargin{4};
        indices = ((i_ - expinfo.pauselength)*npts_packet+(1:npts_packet));
        cols = 1:size(profile,2);
        
        % Apply amplitude scaling and profile
        packet = expinfo.amplitude*fcdata(indices)*profile;
        
        % Zero-padding
        packet = [packet zeros(npts_packet, ncols-size(packet,2))];

        expinterval = false;
    end

    % Insert marker
    packet = [packet repmat(typecast(expinfo.marker, 'single'), size(packet,1),1)];
    
    fprintf('\n');
    varargout{1} = packet;
    varargout{2} = expinterval;
end