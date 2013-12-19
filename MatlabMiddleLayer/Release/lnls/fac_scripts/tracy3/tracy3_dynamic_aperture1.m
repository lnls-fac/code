function tracy3_dynamic_aperture1(fmapdpFlag)

if ~exist('fmapdpFlag', 'var'), fmapdpFlag = true; end

% selects data folder
default = fullfile(lnls_get_root_folder(), 'data', 'sirius_tracy');
pathname = uigetdir(default,'Em qual pasta estao os dados?');
if (pathname == 0);
    pathname = default;
end

% gets number of random machines (= number of rms folders)
[~, result] = system(['ls ' pathname '| grep rms | wc -l']);
n_pastas = str2double(result);

% creates figures or ploting dynapts
f=figure;
fa = axes('Parent',f,'YGrid','on','XGrid','on'); box(fa,'on'); hold(fa,'all');
xlabel('x [mm]','FontSize',20); ylabel('z [mm]','FontSize',20);
if(fmapdpFlag)
    fdp=figure;
    fdpa = axes('Parent',fdp,'YGrid','on','XGrid','on'); box(fdpa,'on'); hold(fdpa,'all');
    xlabel('dp [%]','FontSize',20); ylabel('x [mm]','FontSize',20);
end


% loops over random machine, loading and plotting data
for i=1:n_pastas
    
    % -- FMAP --
    full_name = fullfile(pathname, ['rms', num2str(i, '%02i')], 'fmap.out');
    dynapt    = tracy3_load_fmap_data(full_name); 
    plot(fa,1000*dynapt(:,1),1000*dynapt(:,2));
    title(fa,{full_name},'Interpreter','none','FontSize',30); drawnow;
    
    if (fmapdpFlag)
        % -- FMAPDP --
        full_name = fullfile(pathname, ['rms', num2str(i, '%02i')], 'fmapdp.out');
        dynapt    = tracy3_load_fmapdp_data(full_name); 
        plot(fdpa,100*dynapt(:,1),1000*dynapt(:,2));
        title(fdpa,{full_name},'Interpreter','none','FontSize',30); drawnow;
    end
    
end
