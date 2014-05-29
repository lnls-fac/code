function [dynapt, dados] = tracy3_load_daxy_data(pathname)

fname = fullfile(pathname, 'daxy.out');

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
y  = flipud(y);
plane = flipud(plane);
[~,ind] = min(plane == -1,[],1);

% por fim, defino a DA
x = x(1,:);
y = unique(y(ind,:)','rows');

dynapt = [x', y'];