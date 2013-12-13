function r = track_through_fieldmap(ref_traj, track, runge_kutta_flags)

% initial conditions
pts0 = zeros(length(track.px)*length(track.rx),6);
for i=1:length(track.px)
    for j=1:length(track.rx)
       pts0((i-1)*length(track.rx)+j,:) = [track.rx(j) track.px(i) 0 0 0 0];
    end
end

% entrance and exit reference systems
sf_in  = get_local_SerretFrenet_coord_system(ref_traj, ref_traj.s(1));
sf_out = get_local_SerretFrenet_coord_system(ref_traj, ref_traj.s(end));

s_length = ref_traj.s(end) + 0.1; % 100 mm should be enough
pts1 = zeros(size(pts0));
for i=1:size(pts0,1)
    pos = sf_in.r + sf_in.n * pts0(i,1);
    if pos(1) == 0
        disp('ok');
    end
    beta_x = sf_in.t(1) + pts0(i,2);
    beta_z = sqrt(1-beta_x^2); % beta = constant
    p = [beta_x; 0; beta_z];
    traj = calc_trajectory(s_length, [pos; p], runge_kutta_flags);
    [s_intersection x_perp] = find_intersection_point(traj, sf_out);

%     beta_x1 = interp1q(traj.s, traj.beta_x, s_intersection);
%     dbeta_x = beta_x1 - sf_out.p(1);
%     pts1(i,:) = [x_perp dbeta_x 0 0 0 s_intersection - ref_traj.s(end)];
    p1(1,1) = interp1q(traj.s, traj.beta_x, s_intersection);
    p1(2,1) = interp1q(traj.s, traj.beta_y, s_intersection);
    p1(3,1) = interp1q(traj.s, traj.beta_z, s_intersection);
    dp = (p1 - sf_out.t)'*sf_out.n;
    pts1(i,:) = [x_perp dp 0 0 0 s_intersection - ref_traj.s(end)];

    fprintf('rx = %+7.2f [mm] -> px = %+7.4f [mrad] \n', 1e3*pts0(i,1), 1e3*pts1(i,2));
    
end
r.rx = track.rx;
r.px = track.px;
r.in_pts  = pts0;
r.out_pts = pts1;



function sf = get_local_SerretFrenet_coord_system(traj, s)
% function sf = get_local_SerretFrenet_coord_system(traj, s)
%
% History:
%   2011-11-25: versao revisada e comentada (Ximenes).

x = interp1q(traj.s, traj.x, s);
y = interp1q(traj.s, traj.y, s);
z = interp1q(traj.s, traj.z, s);
beta_x = interp1(traj.s, traj.beta_x, s);
beta_y = interp1(traj.s, traj.beta_y, s);
beta_z = interp1(traj.s, traj.beta_z, s);

sf.s = s;
sf.r = [x; y; z];                                                 % coordenadas na posicaoo s da trajet?ria
% sf.p = [beta_x; beta_y; beta_z];                                  % velocidades na posicaoo s da trajet?ria
sf.t = [beta_x; beta_y; beta_z] / norm([beta_x; beta_y; beta_z]); % versor tangente
sf.n = [0 0 1; 0 1 0; -1 0 0] * sf.t;                             % versor normal
sf.k = cross(sf.t, sf.n);                                         % versor torsao



function [s_intersection x_perp] = find_intersection_point(traj, sf_coord)
% function s_intersection = find_intersection_point(traj, sf_coord)
%
% finds s position in 'traj' at which normal line defined in 'sf_coord' intersects the trajectory
%
% Obs:
%   O algortimo funciona da seguinte maneira: a trajet?ria ? composta por uma sequencia ordenada em s de pontos:
%   p_1, p_2, ..., p_n. Para cada par de pontos consecutivos (p_i,p_(i+1)) calcula-se o ponto em que a reta que os
%   une cruza a reta definida pela dire??o normal (versor 'sf_coord.n'). Para isto calculam-se os par?metros 
%   (alpha,beta) de forma a garantir que
%                                       sf_coord.r + alpha * sf_coord.n = p_i + beta * (p_(i+1) - p_i)
%   o par (alpha,beta) define o ponto de interse??o das duas retas.  Se 0 <= beta <= 1 ent?o a reta normal definida
%   por sf_coord.n cruza a trajet?ria em um ponto entre p_i e p_(i+1).
%   
% History:
%   2011-11-25: vers?o revisada e comentada (Ximenes).

p0 = [sf_coord.r(1); sf_coord.r(3)];
n  = [sf_coord.n(1); sf_coord.n(3)];
for i=1:(size(traj.s)-1)
    p1  = [traj.x(i); traj.z(i)];
    p2  = [traj.x(i+1); traj.z(i+1)];
    M   = [n(1) (p1(1)-p2(1)); n(2) (p1(2) - p2(2))];
    b   = [(p1(1) - p0(1)); (p1(2) - p0(2))];
    res = M \ b;
    alpha(i) = res(1);
    beta(i)  = res(2);
end
idx = find((beta >= 0) & (beta <= 1),1);
s1 = traj.s(idx);
s2 = traj.s(idx+1);
x_perp = alpha(idx);
s_intersection  = s1 + beta(idx) * (s2 - s1);