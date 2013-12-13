function lnls_drawlattice(the_ring, nper)

idx = findcells(the_ring, 'PassMethod', 'IdentityPass');
the_ring(idx) = [];
for i=length(the_ring):-1:2
    if strcmpi(the_ring{i-1}.FamName, the_ring{i}.FamName)
        the_ring{i-1}.Length = the_ring{i-1}.Length + the_ring{i}.Length;
        the_ring(i) = [];
    end
end

pos = findspos(the_ring, 1:(length(the_ring)+1));
max_pos = pos(end) / (nper - 0.001);



s = 0;
for i=1:(length(pos)-1)
    len = pos(i+1) - pos(i);
    if isfield(the_ring{i}, 'BendingAngle')
        rectangle('Position',[s,-1,len,2], 'FaceColor', [0 0 1], 'EdgeColor', [0 0 1]);
        text(s+len/2, 1.9, the_ring{i}.FamName, 'HorizontalAlignment', 'center', 'FontWeight', 'bold');
    elseif isfield(the_ring{i}, 'K')
        rectangle('Position',[s,-1,len,2], 'FaceColor', [1 0 0], 'EdgeColor', [1 0 0]);
        text(s+len/2, 1.9, the_ring{i}.FamName, 'HorizontalAlignment', 'center', 'FontWeight', 'bold');
    elseif isfield(the_ring{i}, 'PolynomB')
        rectangle('Position',[s,-1,len,2], 'FaceColor', [0 0.8 0], 'EdgeColor', [0 0.8 0]);
        text(s+len/2, -1.9, the_ring{i}.FamName, 'HorizontalAlignment', 'center', 'FontWeight', 'bold');
    else
        line([s s+len], [0 0], 'Color', [0 0 0]);
    end
    s = s + len;
    if (s > max_pos), break; end;
end
axis([0 max_pos -10 10]);

h = gcf;
axis off;
set(h, 'Color', [1 1 1]);
