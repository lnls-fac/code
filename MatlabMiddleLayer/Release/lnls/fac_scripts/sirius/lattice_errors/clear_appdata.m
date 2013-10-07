function clear_appdata()

%remove appdata from previous runs
if ~isempty(getappdata(0,'Sextupole_Idx'))
    rmappdata(0,'Sextupole_Idx');
    rmappdata(0,'Sextupole_Strength');
end
if ~isempty(getappdata(0,'TwissTheRing0'))
    rmappdata(0,'TwissTheRing0');
end
if ~isempty(getappdata(0,'objectiveSigmaY'))
    rmappdata(0, 'objectiveSigmaY');
end
if ~isempty(getappdata(0,'IDs_Idx'))
    rmappdata(0,'IDs_Idx');
    rmappdata(0,'IDs_PassMethods');
end
