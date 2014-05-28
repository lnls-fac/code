function dynapt = tracy3_load_fmap_data(pathname)

fname = fullfile(pathname, 'fmap.out');

[~, fmap] = hdrload(fname);

% Agora, eu tenho que encontrar a DA
%primeiro eu identifico quantos x e y existem
npx = length(unique(fmap(:,1)));
npy = size(fmap,1)/npx;
%agora eu pego a coluna da frequencia x
x = fmap(:,1);
y = fmap(:,2);
fx = fmap(:,3);
% e a redimensiono para que todos os valores calculados para x iguais
%fiquem na mesma coluna:
x = reshape(x,npy,npx);
y = reshape(y,npy,npx);
fx = reshape(fx,npy,npx);
% e vejo qual o primeiro valor nulo dessa frequencia, para identificar
% a borda da DA
y  = flipud(y);
fx = flipud(fx);
[~,ind] = min(fx,[],1);

% por fim, defino a DA
x = x(1,:);
y = unique(y(ind,:)','rows');

dynapt = [x', y'];


% % loads raw data
% [~, raw_data] = hdrload(fname);
% 
% % finds number of x points (nx) and y points (ny) in 'fmap.out'
% nx = find(raw_data(2:end,1) ~= raw_data(1,1), 1);
% ny = size(raw_data,1)/nx;
% 
% % loads data into 'dynapt' matrix
% dynapt = zeros(size(raw_data));
% idx = 1;
% for j=0:(ny-1)
%     m=nx;
%     controle=0;
%     while ((controle < 1) && (m>=1))
%         if (raw_data(j*nx+m,3)==0)
%             controle=controle+1;
%         end
%         m=m-1;
%     end
%     dynapt(idx,:) = raw_data(j*nx+m+1,:); idx = idx + 1;
% end