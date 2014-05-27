function dynapt = tracy3_load_daxy_data(pathname)

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
%turn = data(:,4);
%pos  = data(:,5);
% e a redimensiono para que todos os valores calculados para x iguais
%fiquem na mesma coluna:
x = reshape(x,npy,npx);
y = reshape(y,npy,npx);
plane = reshape(plane,npy,npx);
% e vejo qual o primeiro valor nulo dessa frequencia, para identificar
% a borda da DA
y  = flipud(y);
plane = flipud(plane);
[~,ind] = min(plane,[],1);

% por fim, defino a DA
x = x(1,:);
y = unique(y(ind,:)','rows');

dynapt = [x', y'];