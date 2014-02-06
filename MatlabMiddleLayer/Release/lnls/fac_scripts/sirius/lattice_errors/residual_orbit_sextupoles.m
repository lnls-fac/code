function residual_orbit_sextupoles()

file = 'CONFIG_V500_AC10_6_40ums';


r = load([file '_machines_cod_corrected.mat']);
nr_machines = length(r.machine);

bare_ring = load([file '_the_ring.mat']);
[baretune barechrom] = tunechrom(bare_ring.the_ring,0,[0.40 0.27],'chrom','coup');

sext_idx = findcells(bare_ring.the_ring, 'PolynomB');
sext_str = getcellstruct(bare_ring.the_ring, 'PolynomB', sext_idx, 1, 3);
sext_idx2 = (sext_str ~= 0);
sext_str  = sext_str(sext_idx2);
sext_str  = repmat(sext_str,1,nr_machines);
sext_idx  = sext_idx(sext_idx2);
sext_len  = getcellstruct(bare_ring.the_ring,'Length',sext_idx);
sext_len  = repmat(sext_len,1,nr_machines);


codx = zeros(nr_machines,length(r.machine{1}));
cody = codx;
for ii=1:nr_machines
    the_ring0 = r.machine{ii};
    cod = findorbit4(the_ring0,0,1:length(the_ring0));
    codx(ii,:) = cod(1,:);
    cody(ii,:) = cod(3,:);
end

% codx       = load([file '_codx_corrected.dat']);
codx       = 1e6*codx(:,sext_idx)';
std_codx   = std(codx);
max_codx   = max(abs(codx));

% cody      = load([file '_cody_corrected.dat']);
cody       = 1e6*cody(:,sext_idx)';
std_cody   = std(cody);
max_cody   = max(abs(cody));

xpos  = load([file '_errors_x.dat']);
ypos  = load([file '_errors_y.dat']);
xpos  = xpos(:,sext_idx)';
ypos  = ypos(:,sext_idx)';


xdist = xpos + codx;
ydist = ypos + cody;

mean_xdist = mean(xdist);
std_xdist   = std(xdist);
max_xdist   = max(abs(xdist));

std_ydist   = std(ydist);
max_ydist   = max(abs(ydist));

deltak      = 2*sext_len.*sext_str.*xdist*1e-6;
deltakac    = 2*sext_len.*sext_str.*ydist*1e-6;

sum_deltak   = sum(abs(deltak));
max_deltak   = max(abs(deltak));
sum_deltakac = sum(abs(deltakac));
max_deltakac = max(abs(deltakac));

    fprintf(['\ncod: closed orbit distortion at sextupoles'...
            '\ndist: distance of the cod to the center of the sextupoles'...
            '\ndeltak: for�a quadrupolar normal introduzida pelos sextupolos'...
            '\ndeltakac: for�a quadrupolar skew introduzida pelos sextupolos\n\n']);
    fprintf('machine|   codx[um]   |   cody[um]   |   xdist[um]   |   ydist[um]   |   deltak[1/m]  | deltakac[1/m] |    dtune     |    dchrom    \n');
    fprintf('       |  max    std  |  max    std  |  max     std  |  max     std  |  sum     max   |  sum     max  |  x      y    |  x      y    \n');
for i=1:length(mean_xdist)
    [tune chrom] = tunechrom(r.machine{i},0,[0.40 0.27],'chrom','coup');
    dtune = tune - baretune; dchrom = chrom - barechrom;
    fprintf('   %03i |%6.2f %6.2f |%6.2f %6.2f |%6.2f  %6.2f |%6.2f  %6.2f | %6.4f  %6.4f | %6.4f  %6.4f | %6.4f  %6.4f | %6.4f  %6.4f \n',...
        i, max_codx(i), std_codx(i), max_cody(i), std_cody(i), max_xdist(i), std_xdist(i), max_ydist(i), std_ydist(i),...
        sum_deltak(i), max_deltak(i), sum_deltakac(i), max_deltakac(i), dtune(1), dtune(2), dchrom(1), dchrom(2));
end