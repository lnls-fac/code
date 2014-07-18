function print_orbit

global THERING;

setcavity('on');
setradiation('on');

o = linepass(THERING, [0.001, 0, 0.0001, 0, 0, 0]', 1:length(THERING)+1);
fp = fopen('orbit_matlab.txt', 'w');
for i=1:size(o,2)
    pos = o(:,i);
    fprintf(fp, '%+23.16E %+23.16E %+23.16E %+23.16E %+23.16E %+23.16E \n', pos);
end
fclose(fp);