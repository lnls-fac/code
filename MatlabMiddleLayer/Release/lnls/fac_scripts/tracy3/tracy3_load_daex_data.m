function dynapt = tracy3_load_daex_data(pathname)

fname = fullfile(pathname, 'fmapdp.out');

[~, data] = hdrload(fname);

% Agora, eu tenho que encontrar a DA
%primeiro eu identifico quantos x e y existem
npe = length(unique(data(:,1)));
npx = size(data,1)/npe;
%agora eu pego a coluna da frequencia x
en = data(:,1);
x = data(:,2);
plane = data(:,3);
%turn = data(:,4);
%pos  = data(:,5);
% e a redimensiono para que todos os valores calculados para x iguais
%fiquem na mesma coluna:
en = reshape(en,npx,npe);
x = reshape(x,npx,npe);
plane = reshape(plane,npx,npe);
% e vejo qual o primeiro valor nulo dessa frequencia, para identificar
% a borda da DA
[~,ind] = min(plane,[],1);

% por fim, defino a DA
en = en(1,:);
x = unique(x(ind,:)','rows');

dynapt = [en', x'];