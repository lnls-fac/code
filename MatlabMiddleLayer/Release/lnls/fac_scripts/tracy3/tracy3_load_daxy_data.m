function [dynapt, dados] = tracy3_load_daxy_data(pathname,var_plane)

fname = fullfile(pathname, 'daxy.out');

%variável para determinar o tipo de varredura no calculo da abertura;
if ~exist('var_plane','var');
     var_plane = 1;  % 1 = varredura em y; 0 = varredura em x;
end

[~, data] = hdrload(fname);

% Agora, eu tenho que encontrar a DA
%primeiro eu identifico quantos x e y existem
npx = length(unique(data(:,1)));
npy = size(data,1)/npx;
%agora eu pego a coluna da frequencia x
x = data(:,1);
y = data(:,2);
plane = data(:,3);
turn = data(:,4);
pos  = data(:,5);
% e a redimensiono para que todos os valores calculados para x iguais
%fiquem na mesma coluna:
x = reshape(x,npy,npx); dados.x = x;
y = reshape(y,npy,npx); dados.y = y;
plane = reshape(plane,npy,npx); dados.plane = plane;
turn = reshape(turn,npy,npx); dados.turn = turn;
pos = reshape(pos,npy,npx); dados.pos = pos;
% e vejo qual o primeiro valor nulo dessa frequencia, para identificar
% a borda da DA
if var_plane
    y  = flipud(y);
    plane = flipud(plane);
    [~,ind] = min(plane == -1,[],1);
    % por fim, defino a DA
    x = x(1,:);
    y = unique(y(ind,:)','rows');
    dynapt = [x', y'];
else
    idx = x(1,:) > 0;
    x_ma = x(1,idx);
    [~,ind_pos] = min(plane(:,idx) == - 1,[],2);
    dynapt = [x_ma(ind_pos)' y(:,1)];
    x_mi = fliplr(x(1,~idx));
    [~,ind_neg] = min(fliplr(plane(:,~idx)) == - 1,[],2);
    dynapt = [[fliplr(x_mi(ind_neg))' flipud(y(:,1))]; dynapt];
end