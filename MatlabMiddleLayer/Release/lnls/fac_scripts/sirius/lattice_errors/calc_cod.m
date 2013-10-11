function [codx cody] = calc_cod(the_ring, dim)

global THERING

if ~exist('dim', 'var')
    dim = '4d';
end

THERING = the_ring;
if strcmpi(dim, '6d')
    setcavity('on');
    setradiation('off');
    orb = findorbit6(THERING, 1:length(the_ring));
else
    orb = findorbit4(the_ring, 0, 1:length(the_ring));
end

codx = orb(1,:);
cody = orb(3,:);
