function lnls_at2flatfile(lattice, filename)
%lnls_at2flatfile(lattice, filename) gera um arquivo flatfile 
%com nome 'filename' a partir do modelo do 'lattice' do AT.
%
%
%Ximenes - 2014-08-27

fp = fopen(filename, 'w');

column_format = '%-20s ';
double_format = '%+.15E';
for i=1:length(lattice)
    fprintf(fp, column_format, 'index'); fprintf(fp, '%04i\n', i);
    fprintf(fp, column_format, 'fam_name'); fprintf(fp, '%s\n', lattice{i}.FamName);
    fprintf(fp, column_format, 'length'); fprintf(fp, [double_format, '\n'], lattice{i}.Length);
    if isfield(lattice{i}, 'NumIntSteps'), fprintf(fp, column_format, 'nr_steps'); fprintf(fp, '%i\n', lattice{i}.NumIntSteps); end;
    if isfield(lattice{i}, 'PolynomA')
        [PolyA, PolyB] = calc_polynoms(lattice{i});
        if (~isempty(PolyA) && any(PolyA ~= 0)), fprintf(fp, column_format, 'polynom_a'); print_polynom(fp, PolyA, double_format); end;
        if (~isempty(PolyB) && any(PolyB ~= 0)), fprintf(fp, column_format, 'polynom_b'); print_polynom(fp, PolyB, double_format); end;
    end
    fprintf(fp, '\n');
end

fclose(fp);


function print_polynom(fp, polynom, double_format)

for i=1:length(polynom)
    if polynom(i) ~= 0
        fprintf(fp, ['%i ', double_format], i-1, polynom(i));
    end
end
fprintf(fp, '\n');

function [PolynomA, PolynomB] = calc_polynoms(element)

selA = (element.PolynomA ~= 0);
selB = (element.PolynomB ~= 0);
order = max([find(selB, 1, 'last') find(selA, 1, 'last')]);
PolynomA = zeros(1,order);
PolynomB = zeros(1,order);
PolynomA(selA) = element.PolynomA(selA);
PolynomB(selB) = element.PolynomB(selB);

