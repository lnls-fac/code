function tracking_test()


nb = 864;
n_turn = 100000;

part = rand(2,nb,n_turn);

nu = 0.1472;
Mat = [cos(2*pi*nu), sin(2*pi*nu); -sin(2*pi*nu), cos(2*pi*nu)];


tic
for ii=2:n_turn
    part(:,:,ii) = Mat*squeeze(part(:,:,ii-1));
end

% for ii=2:n_turn
%     for jj =1:nb
%         part(:,jj,ii) = Mat*squeeze(part(:,jj,ii-1));
%     end
% end


toc