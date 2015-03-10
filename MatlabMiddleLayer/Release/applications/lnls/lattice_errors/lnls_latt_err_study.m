function machine = lnls_latt_err_study()

fprintf('\n')
fprintf('Lattice Errors Run\n');
fprintf('==================\n');

% first step is to initialize global auxiliary structures
name = 'CONFIG'; name_saved_machines = name;
initializations();

% next a nominal model is chosen for the study 
the_ring = create_nominal_model();

% application of errors to the nominal model
machine  = create_apply_errors(the_ring);

% orbit correction is performed
machine  = correct_orbit(machine);

% next, coupling correction
machine  = correct_coupling(machine);

% tune correction
machine  = correct_tune(machine);

% at last, multipole errors are applied
machine  = create_apply_multipoles(machine);

% finalizations are done
finalizations()


%% Initializations
    function initializations()
        
        fprintf('\n<initializations> [%s]\n\n', datestr(now));
        
        % seed for random number generator
        seed = 131071;
        fprintf('-  initializing random number generator with seed = %i ...\n', seed);
        RandStream.setGlobalStream(RandStream('mt19937ar','seed', seed));
        
        % sends copy of all output to a diary in a file
        fprintf('-  creating diary file ...\n');
        diary([name, '_summary.txt']);
        
    end

%% finalizations
    function finalizations()
        
        % closes diary and all open plots
        diary 'off'; fclose('all');
        
    end

%% Definition of the nominal AT model
    function the_ring = create_nominal_model()
        
        fprintf('\n<nominal model> [%s]\n\n', datestr(now));
        
        % loads nominal ring as the default lattice for a particular
        % lattice version. It is assumed that sirius MML structure has been
        % loaded with 'sirius' command the appropriate lattice version.
        fprintf('-  loading model ...\n');
        fprintf('   file: %s\n', which('sirius_si_lattice'));
        the_ring = sirius_si_lattice();
        
        % sets cavity and radiation off for 4D trackings
        fprintf('-  turning radiation and cavity off ...\n');
        the_ring = setcavity('off', the_ring);
        the_ring = setradiation('off', the_ring);
        
        % saves nominal lattice to file
        save([name,'_the_ring.mat'], 'the_ring');
        
    end

%% Magnet Errors:
    function machine = create_apply_errors(the_ring)
        
        fprintf('\n<error generation and random machines creation> [%s]\n\n', datestr(now));
        
        % constants
        um = 1e-6; mrad = 0.001; percent = 0.01;

        % <quadrupoles> alignment, rotation and excitation errors
        config.fams.quads.labels     = {'qfa','qdb2','qfb','qdb1','qda','qf1','qf2','qf3','qf4'};
        config.fams.quads.nrsegs     = [1,1,1,1,1,1,1,1,1]; % number of segments for each magnet in the corresponding family
        config.fams.quads.sigma_x    = 40 * um * 1;
        config.fams.quads.sigma_y    = 40 * um * 1;
        config.fams.quads.sigma_roll = 0.20 * mrad * 1;
        config.fams.quads.sigma_e    = 0.05 * percent * 1;
        
        % <sextupoles> alignment, rotation and excitation errors
        config.fams.sexts.labels     = {'sda','sfa','sd1','sf1','sd2','sd3','sf2','sf3','sd4','sd5','sf4','sd6','sdb','sfb'};
        config.fams.sexts.nrsegs     = [1,1,1,1,1,1,1,1,1,1,1,1,1,1]; % number of segments for each magnet in the corresponding family
        config.fams.sexts.sigma_x    = 40 * um * 1;
        config.fams.sexts.sigma_y    = 40 * um * 1;
        config.fams.sexts.sigma_roll = 0.20 * mrad * 1;
        config.fams.sexts.sigma_e    = 0.05 * percent * 1;
        
        % <electromagnetic dipoles> alignment, rotation and excitation errors
        config.fams.bends.labels       = {'b1','b2','b3'};
        config.fams.bends.nrsegs       = [2,2,2]; % number of segments for each magnet in the corresponding family
        config.fams.bends.sigma_x      = 40 * um * 1;
        config.fams.bends.sigma_y      = 40 * um * 1;
        config.fams.bends.sigma_roll   = 0.20 * mrad * 1;
        config.fams.bends.sigma_e      = 0.05 * percent * 1;
        config.fams.bends.sigma_e_kdip = 0.10 * percent * 1;  % quadrupole errors due to pole variations
        
        % <permanent magnet dipoles> alignment, rotation and excitation errors
        config.fams.cbend.labels     = {'bc'};
        config.fams.cbend.nrsegs     = 2;
        config.fams.cbend.sigma_y    = 40 * um * 1;
        config.fams.cbend.sigma_x    = 40 * um * 1;
        config.fams.cbend.sigma_roll = 0.20 * mrad * 1;
        config.fams.cbend.sigma_e    = 0.05 * percent * 1;
        
        % <girders> alignment and rotation
        config.girder.girder_error_flag = false;
        config.girder.correlated_errors = false;
        config.girder.sigma_x     = 100 * um * 1;
        config.girder.sigma_y     = 100 * um * 1;
        config.girder.sigma_roll  = 0.20 * mrad * 1;
        
        % generates error vectors
        nr_machines   = 2;
        rndtype       = 'gaussian';
        cutoff_errors = 1;
        fprintf('-  generating errors ...\n');
        errors        = lnls_latt_err_generate_errors(name, the_ring, config, nr_machines, cutoff_errors, rndtype);
        
        % applies errors to machines
        fractional_delta = 1;
        fprintf('-  creating %i random machines and applying errors ...\n', nr_machines);
        fprintf('-  finding closed-orbit distortions with sextupoles off ...\n\n');
        machine = lnls_latt_err_apply_errors(name, the_ring, errors, fractional_delta);
        
    end

%% Cod Correction
    function machine = correct_orbit(machine)
        
        fprintf('\n<closed-orbit distortions correction> [%s]\n\n', datestr(now));
        
        % parameters for slow correction algorithms
        orbit.bpm_idx = sirius_si_bpm_indices(the_ring);
        orbit.hcm_idx = sirius_si_chs_indices(the_ring);
        orbit.vcm_idx = sirius_si_cvs_indices(the_ring);
        
        % parameters for SVD correction
        orbit.sext_ramp         = [0 1];
        orbit.svs               = 'all';
        orbit.max_nr_iter       = 50;
        orbit.tolerance         = 1e-5;
        orbit.correct2bba_orbit = false;
        orbit.simul_bpm_err     = false;
        
        % calcs nominal cod response matrix, if chosen
        use_respm_from_nominal_lattice = true; 
        if use_respm_from_nominal_lattice
            fprintf('-  calculating orbit response matrix from nominal machine ...\n');
            lattice_symmetry = 10;  
            orbit.respm = calc_respm_cod(the_ring, orbit.bpm_idx, orbit.hcm_idx, orbit.vcm_idx, lattice_symmetry, true); 
            orbit.respm = orbit.respm.respm;
        end 
        
        % loops over random machine, correcting COD...
        machine = lnls_latt_err_correct_cod(name, machine, orbit);
        
        % saves results to file
        name_saved_machines = [name_saved_machines,'_machines_cod_corrected'];
        save([name_saved_machines '.mat'], 'machine');
        
    end

%% Coupling Correction
    function machine = correct_coupling(machine)
        
        fprintf('\n<coupling correction> [%s]\n\n', datestr(now));
        
        coup.scm_idx = sirius_si_qs_indices(the_ring);
        coup.bpm_idx = sirius_si_bpm_indices(the_ring);
        coup.hcm_idx = sirius_si_chs_indices(the_ring);
        coup.vcm_idx = sirius_si_cvs_indices(the_ring);
        coup.svs           = 'all';
        coup.max_nr_iter   = 50;
        coup.tolerance     = 1e-5;
        coup.simul_bpm_corr_err = false;
        
        % calcs coupling symmetrization matrix
        fname = [name '_info_coup.mat'];
        lattice_symmetry = 10;
        if ~exist(fname, 'file')
            [respm, info] = calc_respm_coupling(the_ring, coup, lattice_symmetry);
            coup.respm = respm;
            save(fname, 'info');
        else
            data = load(fname);
            [respm, ~] = calc_respm_coupling(the_ring, coup, lattice_symmetry, data.info);
            coup.respm = respm;
        end
        machine = lnls_latt_err_correct_coupling(name, machine, coup);
        
        name_saved_machines = [name_saved_machines '_coup'];
        save([name_saved_machines '.mat'], 'machine');
    end

%% Tune Correction
    function machine = correct_tune(machine)
        tune.correction_flag = false;
        tune.families        = {'qfa','qdb2','qfb','qdb1','qda'};
        [~, tune.goal]       = twissring(the_ring,0,1:length(the_ring)+1);
        tune.max_iter        = 10;
        tune.tolerance       = 1e-6;
        
        % faz correcao de tune
        machine = lnls_latt_err_correct_tune_machines(tune, machine);
        
        name_saved_machines = [name_saved_machines '_tune'];
        save([name_saved_machines '.mat'], 'machine');
    end

%% Multipoles insertion
    function machine = create_apply_multipoles(machine)
        % QUADRUPOLES
        % quadM multipoles from model3 fieldmap '2015-02-05 Quadrupolo_Anel_QM_Modelo 3_-12_12mm_-500_500mm_156.92A.txt'
        multi.quadsM.labels = {'qfa','qfb','qdb2','qf1','qf2','qf3','qf4'};
        multi.quadsM.nrsegs = ones(1,7);
        multi.quadsM.main_multipole = 2;% positive for normal negative for skew
        multi.quadsM.r0 = 11.7e-3;
        multi.quadsM.order       = [ 3   4   5   6   7   8   9   10]; % 1 for dipole
        multi.quadsM.main_vals = 1*ones(1,8)*4e-5;
        multi.quadsM.skew_vals = 1*ones(1,8)*1e-5;
        
        % quadC multipoles from model2 fielmap '2015-01-27 Quadrupolo_Anel_QC_Modelo 2_-12_12mm_-500_500mm.txt'
        multi.quadsC.labels = {'qdb1','qda'};
        multi.quadsC.nrsegs = ones(1,2);
        multi.quadsC.main_multipole = 2;% positive for normal negative for skew
        multi.quadsC.r0 = 11.7e-3;
        multi.quadsC.order       = [ 3   4   5   6   7   8   9   10]; % 1 for dipole
        multi.quadsC.main_vals = 1*ones(1,8)*4e-5;
        multi.quadsC.skew_vals = 1*ones(1,8)*1e-5;
        
        
        % SEXTUPOLES
        % multipoles from model1 fieldmap 'Sextupolo_Anel_S_Modelo 1_-12_12mm_-500_500mm.txt'
        multi.sexts.labels = {'sda','sfa','sd1','sf1','sd2','sd3','sf2','sf3','sd4','sd5','sf4','sd6','sdb','sfb'};
        multi.sexts.nrsegs = ones(1, 14);
        multi.sexts.main_multipole = 3;% positive for normal negative for skew
        multi.sexts.r0 = 11.7e-3;
        multi.sexts.order       = [4   5   6   7   8   9   10  11]; % 1 for dipole
        multi.sexts.main_vals = 1*ones(1,8)*4e-5;
        multi.sexts.skew_vals = 1*ones(1,8)*1e-5;
        
        % DIPOLES
        %The default systematic multipoles for the dipoles were changed.
        %Now we are using the values of a standard pole dipole which Ricardo
        %optimized (2015/02/02) as base for comparison with the other alternative with
        %incrusted coils in the poles for independent control of que gradient.
        multi.bends.labels = {'b1','b2','b3', 'bc'};
        multi.bends.nrsegs = [2 3 2 2];
        multi.bends.main_multipole = 1;% positive for normal negative for skew
        multi.bends.r0 = 11.7e-3;
        multi.bends.order       = [ 3   4   5   6   7   8   9 ]; % 1 for dipole
        multi.bends.main_vals = 1*ones(1,7)*4e-5;
        multi.bends.skew_vals = 1*ones(1,7)*1e-5;
        
        cutoff_errors = 2;
        nr_machines = 20;
        multi_errors  = lnls_latt_err_generate_multipole_errors(name, the_ring, multi, nr_machines, cutoff_errors);
        machine = lnls_latt_err_apply_multipole_errors(name, machine, multi_errors, multi);
        
        name_saved_machines = [name_saved_machines '_multi'];
        save([name_saved_machines '.mat'], 'machine');
    end
end
