/*
 a Última alteração 	$ReadfeFile: Corrigi a aplicação de erros de excitação de dipolos$
 Data				 $25/11/2011$ por $Fernando$
 Última alteração	$Correção de órbita: implementei um modo "burro" de gerar excitação aleatória para cada máquina$
 Data				 $30/11/2011$ por $Fernando$
 */
#define ORDER 1

int no_tps = ORDER; // arbitrary TPSA order is defined locally

extern bool freq_map;

#include "tracy_lib.h"

//***************************************************************************************
//
//  MAIN CODE
//
//****************************************************************************************
int main(int argc, char *argv []) {
    
    
    /*printf("\nTracy3 - LNLS:  27/05/2014\n");*/
    printf("\nTracy3 - LNLS:  02/06/2014\n");
    
	/* for time handling */
	uint32_t start, stop;

	/*set the random value for random generator*/
	const long seed = 1121; //the default random seed number
	iniranf(seed); //initialize the seed
	setrancut(2.0); //default value of the normal cut for the normal distribution
	// turn on globval.Cavity_on and globval.radiation to get proper synchro radiation damping
	// ID s accounted too if: wiggler model and symplectic integrator (method = 1)
	globval.H_exact = false;

	// to be used with parallelized version of tracking functions
	globval.nr_cpus = 1;


	/* parameters to read the user input script .prm */
	long i=0L; //initialize the for loop to read command string
	char CommandStr[max_str];
	double nux = 0.0, nuy = 0.0, ksix = 0.0, ksiy = 0.0;
	bool chroma=true;
	double dP = 0.0;
	long lastpos = -1L;
	char str1[S_SIZE];

	// paramters to read the command line in user input script
	long CommandNo = -1L;  //the number of commands, since this value is also
	// the index of array UserCommandFlag[], so this
	// value is always less than 1 in the really case.
	const int NCOMMAND = 500;
	UserCommand UserCommandFlag[NCOMMAND];


	/************************************************************************
   read in files and flags
	 *************************************************************************/



	if (argc > 1) {
		read_script(argv[1], true,CommandNo, UserCommandFlag);
	} else {
		fprintf(stdout, "Not enough input parameters: an input filename has to be provided!\n");
		exit_(1);
	}

	/* get the family index of the special elements, prepare for printglob()*/
	if(strcmp(bpm_name,"")==0)
		globval.bpm = 0;
	else
		globval.bpm = ElemIndex(bpm_name);
	if(strcmp(skew_quad_name,"")==0)
		globval.qt = 0;
	else
		globval.qt = ElemIndex(skew_quad_name);
	if(strcmp(hcorr_name,"")==0)
		globval.hcorr = 0;
	else
		globval.hcorr = ElemIndex(hcorr_name);
	if(strcmp(vcorr_name,"")==0)
		globval.vcorr = 0;
	else
		globval.vcorr = ElemIndex(vcorr_name);
	if(strcmp(gs_name,"")==0)
		globval.gs = 0;
	else
		globval.gs = ElemIndex(gs_name);
	if(strcmp(ge_name,"")==0)
		globval.ge = 0;
	else
		globval.ge = ElemIndex(ge_name);

	//  globval.g = ElemIndex("g");  /* get family index of  girder*/

	/* print the summary of the element in lattice */
	printglob();

	/************************************************************************
    print files, very important file for debug
	 *************************************************************************/

	//print flat file with all the design values of the lattice,
	prtmfile("flat_file.out");
	// print location, twiss parameters and close orbit at all elements position to a file
	getcod(dP, lastpos);
	prt_cod("cod.out", globval.bpm, true);

	//get_matching_params_scl(); // get tunes and beta functions at entrance
	// compute up to 3rd order momentum compact factor
	get_alphac2();
	//cout << endl << "computing tune shifts" << endl;
	//dnu_dA(10e-3, 5e-3, 0.002);
	//get_ksi2(0.0); // this gets the chromas and writes them into chrom2.out





	/*********************************************************************
                            Flag factory
	 *********************************************************************/

	for(i=0; i<=CommandNo; i++){//read user defined command by sequence
		//assign user defined command
		strcpy(CommandStr,UserCommandFlag[i].CommandStr);

		//turn on flag for quadrupole fringe field
		if(strcmp(CommandStr,"QuadFringeOnFlag") == 0) {
			globval.quad_fringe = true;
			cout << "\n";
			cout << "globval.quad_fringe is " << globval.quad_fringe << "\n";
		}

		//set RF voltage
		else if(strcmp(CommandStr,"RFvoltageFlag") == 0) {
			printf("\nSetting RF voltage:\n");
			printf("    Old RF voltage is: %lf [MV]\n", get_RFVoltage(ElemIndex("cav"))
					/ 1e6);
			set_RFVoltage(ElemIndex("cav"), UserCommandFlag[i].RFvolt);
			printf("    New RF voltage is: %lf [MV]\n", get_RFVoltage(ElemIndex("cav"))
					/ 1e6);
		}
		//set Cavity on and off
		else if(strcmp(CommandStr,"CavityFlag") == 0) {
			printf("\nSetting Cavity:");
			if (strncmp("true", UserCommandFlag[i].CavityFlag, 4) == 0) {
				globval.Cavity_on = true;
				printf(" ON\n");
			} else  {
				globval.Cavity_on = false;
				printf(" OFF\n");
			}
		}
			//set radiation on and off
		else if(strcmp(CommandStr,"RadiationFlag") == 0) {
			printf("\nSetting Radiation:");
			if (strncmp("true", UserCommandFlag[i].RadiationFlag, 4) == 0) {
				globval.radiation = true;
				printf(" ON\n");
			} else  {
				globval.radiation = false;
				printf(" OFF\n");
			}
		}
		//set chamber on and off
		else if(strcmp(CommandStr,"VacuumChamberFlag") == 0) {
			printf("\nSetting Vacuum Chamber:");
			if (strncmp("true", UserCommandFlag[i].VacuumChamberFlag, 4) == 0) {
				globval.Aperture_on = true;
				printf(" ON\n");
				PrintCh();
			} else  {
				globval.Aperture_on = false;
				printf(" OFF\n");
			}
		}
		// Chamber factory
		else if(strcmp(CommandStr,"ReadChamberFlag") == 0) {
			ReadCh(UserCommandFlag[i].chamber_file); /* read vacuum chamber from a file "chamber.out" , soleil version*/
			PrintCh(); // print chamber into chamber.out
		}

		// read the misalignment errors to the elements, then do COD correction
		//  using SVD method.
		//  Based on the function error_and_correction() in nsls-ii_lib_templ.h

		// else if(strcmp(ReadaefileFlag, "") != 0){
		else if (strcmp(CommandStr,"ReadaefileFlag") == 0) {
			// *****  Apply corrections and output flatfile for n_stat sets of random #'s
			bool    cod = true;
			int     k, icod=0;
			FILE    *hOrbitFile, *vOrbitFile ;
			int     hcorrIdx[nCOR], vcorrIdx[nCOR]; //list of corr for orbit correction
			bool    coup = true;

			//initialize the corrector list
			for ( k = 0; k < nCOR; k++){
				hcorrIdx[k] = -1;
				vcorrIdx[k] = -1;
			}

			//Get response matrix between bpm and correctors, and then print the SVD setting to the files
			if (n_orbit!=0 || n_scale!=0) {

				// select correctors to be used
				readCorrectorList(hcorr_file, vcorr_file, hcorrIdx, vcorrIdx);

				fprintf(stdout, "\n\nSVD correction setting:\n");
				fprintf(stdout, "H-plane %d singular values:\n", nwh);
				fprintf(stdout, "V-plane %d singular values:\n\n",nwv);

				// compute beam response matrix
				printf("\n");
				printf("Computing beam response matrix\n");
				//get the response matrix between bpm and correctors
				gcmats(globval.bpm, globval.hcorr, 1, hcorrIdx);
				gcmats(globval.bpm, globval.vcorr, 2, vcorrIdx);
				/*    gcmat(globval.bpm, globval.hcorr, 1);
        gcmat(globval.bpm, globval.vcorr, 2);*/

				// print response matrices to files 'svdh.out' and file 'svdv.out'
				prt_gcmat(globval.bpm, globval.hcorr, 1);
				prt_gcmat(globval.bpm, globval.vcorr, 2);

			}

			//print the statistics of orbit in file 'OrbScanFile.out'
			OrbScanFile = file_write(OrbScanFileName);

			//write files with orbits at all element locations
			hOrbitFile = file_write(hOrbitFileName);
			vOrbitFile = file_write(vOrbitFileName);

			fprintf(hOrbitFile, "# First line: s-location (m) \n");
			fprintf(hOrbitFile, "# After orbit correction:  Horizontal closed orbit at all element locations (with %3d BPMs) at different loop\n", GetnKid(globval.bpm));
			fprintf(vOrbitFile, "# First line s-location (m) \n");
			fprintf(vOrbitFile, "# After orbit correction:  Vertical closed orbit at all element locations (with %3d BPMs) at different loop\n", GetnKid(globval.bpm));

			for (k = 0; k < globval.Cell_nLoc; k++){
				fprintf(hOrbitFile, "% 9.3e  ", Cell[k].S);
				fprintf(vOrbitFile, "% 9.3e  ", Cell[k].S);
			} // end for

			fprintf(hOrbitFile, "\n");
			fprintf(vOrbitFile, "\n");

			for (k = 1; k <= n_stat; k++) {// loop for n_stat sets of errors

				if (n_orbit!=0 || n_scale!=0) {

					cod = CorrectCOD_Ns(hOrbitFile, vOrbitFile, UserCommandFlag[i].ae_file,
									n_orbit,n_scale,k,nwh,nwv, hcorrIdx, vcorrIdx);
					/*      cod = CorrectCOD_N(ae_file, n_orbit, n_scale, k);*/
					printf("\n");

					if (cod){
						/*         printf("done with orbit correction, now do coupling",
               " correction plus vert. disp\n");*/
						if(n_orbit == 0)
							printf("iter # %3d n_obit = 0, no orbit correction \n",k);
						else
							printf("iter # %3d Orbit correction succeeded\n", k);
					}
					else
						if(!cod){
							icod = icod + 1;
							fprintf(stdout, "!!! iter # %3d error_and_correction\n",k);
						}
					//chk_cod(cod, "iter # %3d error_and_correction");
				}

				// Corrects coupling
				if (n_coupl != 0) {
					coup = CorrectCoupling_N(n_coupl);
				}

				// Ring_GetTwiss(chroma, dp);
				Ring_GetTwiss(true, 0.0);

				// for debugging
				//print flat lattice
				//sprintf(mfile_name, "flat_file.%03d.dat",k);
				//prtmfile(mfile_name);

			}

			fprintf(stdout, "Number of unstable orbits %d/%d", icod, n_stat);
			prt_cod("corr_after.out", globval.bpm, true);

			// close file giving orbit at BPM location
			fclose(hOrbitFile);
			fclose(vOrbitFile);
			fclose(OrbScanFile);
		}

		// set the field error into the lattice
		// The corresponding field error is replaced by the new value.
		// This feature is generic, works for all lattices
		else if (strcmp(CommandStr,"ReadfefileFlag") == 0) {
			fprintf(stdout,"\n Read field error from fe_file: \n");
			LoadFieldErrs(UserCommandFlag[i].fe_file, true, 1.0, true, 1);

			Ring_GetTwiss(true, 0.0);
			prtmfile("flat_file_fefile.out");
		}
		// read multipole errors from a file; specific for soleil lattice
		else if(strcmp(CommandStr,"ReadMultipoleFlag") == 0) {
			fprintf(stdout,"\n Read Multipoles file for lattice with thick sextupoles, specific for SOLEIL lattice: \n");
			ReadFieldErr(multipole_file);
			//first print the full lattice with error as a flat file
			prtmfile("flat_file_errmultipole.out"); // writes flat file with all element errors  /* very important file for debug*/
			Ring_GetTwiss(chroma = true, 0.0); /* Compute and get Twiss parameters */
			printglob();
		}

		//print the twiss paramaters in a file defined by the name
		else if(strcmp(CommandStr,"PrintTwissFlag") == 0) {
			cout << "\n";
			cout << "print the twiss parameters to file: "<< twiss_file << "\n";
			printlatt(twiss_file);
		}
		//print the close orbit
		else if(strcmp(CommandStr,"PrintCODFlag") == 0) {
			cout << "\n";
			cout << "print the close orbit to file: "<< cod_file << "\n";
			getcod(dP, lastpos);
			prt_cod(cod_file, globval.bpm, true);
		}
		//print the girder
		// else if(strcmp(CommandStr,"PrintGirderFlag") == 0) {
		//   cout << "\n";
		//   cout << "print the information of girder to file: "<< girder_file << "\n";


		// getcod(dP, lastpos);
		// prt_cod(cod_file, globval.bpm, true);
		// }



		// compute tunes by tracking (should be the same as by tps)
		else if (strcmp(CommandStr,"TuneTracFlag") == 0) {
			GetTuneTrac(1026L, 0.0, &nux, &nuy);
			fprintf(stdout, "From tracking: nux = % f nuz = % f \n", nux, nuy);
		}

		// compute chromaticities by tracking (should be the same as by DA)
		else if(strcmp(CommandStr,"ChromTracFlag") == 0) {
			start = stampstart();
			GetChromTrac(2L, 1026L, 1e-5, &ksix, &ksiy);
			stop = stampstop(start);
			fprintf(stdout, "From tracking: ksix= % f ksiz= % f \n", ksix, ksiy);
		}


		//generic function, to fit tunes using 1 family of quadrupoles
		// if (FitTuneFlag == true) {
		else if(strcmp(CommandStr,"FitTuneFlag") == 0) {
			double quad_bn[5]  = {0.0, 0.0, 0.0, 0.0, 0.0};
			double quad_bn_fit[5] = {0.0, 0.0, 0.0, 0.0, 0.0};
			long quad_idx[5] = {0, 0, 0, 0, 0};

			fprintf(stdout, "\n Fitting tunes:");
			/* quadrupole field strength before fitting*/
			for (int j = 1;j<=UserCommandFlag[i].n_quads;j++){
				quad_idx[j-1] = ElemIndex(UserCommandFlag[i].quads[(j-1)]);
				quad_bn[j-1] = Cell[Elem_GetPos(quad_idx[j-1], 1)].Elem.M->PB[HOMmax + 2];
				fprintf(stdout, " %s",UserCommandFlag[i].quads[(j-1)]);
			}

			/* fitting tunes*/
			fprintf(stdout, ", targetnux = %f, targetnuz = %f \n", UserCommandFlag[i].targetnux, UserCommandFlag[i].targetnuz);

			lnls_FitTune(quad_idx, UserCommandFlag[i].n_quads, UserCommandFlag[i].targetnux, UserCommandFlag[i].targetnuz);
			//FitTune(quad_idx[0], quad_idx[1], UserCommandFlag[i].targetnux, UserCommandFlag[i].targetnuz);


			/* integrated field strength after fitting*/
			for (int j = 1;j<=UserCommandFlag[i].n_quads;j++){
				quad_bn_fit[j-1] = Cell[Elem_GetPos(quad_idx[j-1], 1)].Elem.M->PB[HOMmax + 2];
			}


			/* print out the quadrupole strengths before and after the fitting */
			printf("\nBefore the fitting, the quadrupole field strengths are: \n");
			for (int j = 1;j<=UserCommandFlag[i].n_quads;j++)
				printf(" %s = %f,    ", UserCommandFlag[i].quads[j-1], quad_bn[j-1]);

			printf("\nAfter the fitting, the quadrupole field strengths are: \n");
			for (int j = 1;j<=UserCommandFlag[i].n_quads;j++)
				printf(" %s = %f,    ", UserCommandFlag[i].quads[j-1], quad_bn_fit[j-1]);

			/* Compute and get Twiss parameters */
			Ring_GetTwiss(chroma = true, 0.0);
			printglob(); /* print parameter list */
		}

		/* specific for soleil ring in which the quadrupole is cut into 2 parts*/
		//if (FitTune4Flag == true) {
		else if(strcmp(CommandStr,"FitTune4Flag") == 0) {
			double qf1_bn = 0.0, qf2_bn = 0.0, qd1_bn = 0.0, qd2_bn = 0.0;
			double qf1_bn_fit = 0.0, qf2_bn_fit = 0.0, qd1_bn_fit = 0.0, qd2_bn_fit =
					0.0;

			/* quadrupole field strength before fitting*/
			qf1_bn = Cell[Elem_GetPos(ElemIndex(UserCommandFlag[i].qf1), 1)].Elem.M->PB[HOMmax + 2];
			qf2_bn = Cell[Elem_GetPos(ElemIndex(UserCommandFlag[i].qf2), 1)].Elem.M->PB[HOMmax + 2];
			qd1_bn = Cell[Elem_GetPos(ElemIndex(UserCommandFlag[i].qd1), 1)].Elem.M->PB[HOMmax + 2];
			qd2_bn = Cell[Elem_GetPos(ElemIndex(UserCommandFlag[i].qd2), 1)].Elem.M->PB[HOMmax + 2];

			/* fitting tunes*/
			fprintf(
					stdout,
					"\n Fitting tunes for Soleil ring: %s %s %s %s, targetnux = %f, targetnuz = %f \n",
					UserCommandFlag[i].qf1, UserCommandFlag[i].qf2, UserCommandFlag[i].qd1, UserCommandFlag[i].qd2,
					UserCommandFlag[i].targetnux, UserCommandFlag[i].targetnuz);
			FitTune4(ElemIndex(UserCommandFlag[i].qf1), ElemIndex(UserCommandFlag[i].qf2),
					ElemIndex(UserCommandFlag[i].qd1), ElemIndex(UserCommandFlag[i].qd2),
					UserCommandFlag[i].targetnux, UserCommandFlag[i].targetnuz);

			/* integrated field strength after fitting*/
			qf1_bn_fit = Cell[Elem_GetPos(ElemIndex(UserCommandFlag[i].qf1), 1)].Elem.M->PB[HOMmax + 2];
			qf2_bn_fit = Cell[Elem_GetPos(ElemIndex(UserCommandFlag[i].qf2), 1)].Elem.M->PB[HOMmax + 2];
			qd1_bn_fit = Cell[Elem_GetPos(ElemIndex(UserCommandFlag[i].qd1), 1)].Elem.M->PB[HOMmax + 2];
			qd2_bn_fit = Cell[Elem_GetPos(ElemIndex(UserCommandFlag[i].qd2), 1)].Elem.M->PB[HOMmax + 2];
			/* print out the quadrupole strengths before and after the fitting*/
			printf("Before the fitting, the quadrupole field strengths are: \n");
			printf("    %s = %f,    %s = %f,    %s = %f,    %s = %f\n", UserCommandFlag[i].qf1, qf1_bn,
					UserCommandFlag[i].qf2, qf2_bn, UserCommandFlag[i].qd1, qd1_bn, UserCommandFlag[i].qd2, qd2_bn);
			printf("After the fitting, the quadrupole field strengths are: \n");
			printf("    %s = %f,    %s = %f,    %s = %f,    %s = %f\n", UserCommandFlag[i].qf1,
					qf1_bn_fit, UserCommandFlag[i].qf2, qf2_bn_fit, UserCommandFlag[i].qd1, qd1_bn_fit,
					UserCommandFlag[i].qd2, qd2_bn_fit);

			/* Compute and get Twiss parameters */
			Ring_GetTwiss(chroma = true, 0.0);
			printglob(); /* print parameter list */
		}

		/* fit the chromaticities*/
		else if(strcmp(CommandStr,"FitChromFlag") == 0) {

			double sxm1_bn = 0.0, sxm2_bn = 0.0;
			double sxm1_bn_fit = 0.0, sxm2_bn_fit = 0.0;
			sxm1_bn = Cell[Elem_GetPos(ElemIndex(UserCommandFlag[i].sxm1), 1)].Elem.M->PB[HOMmax + 3];
			sxm2_bn = Cell[Elem_GetPos(ElemIndex(UserCommandFlag[i].sxm2), 1)].Elem.M->PB[HOMmax + 3];

			fprintf(stdout,"\n Fitting chromaticities: %s %s, targetksix = %f,  targetksiz = %f\n",
					UserCommandFlag[i].sxm1, UserCommandFlag[i].sxm2, UserCommandFlag[i].targetksix,
					UserCommandFlag[i].targetksiz);

			FitChrom(ElemIndex(UserCommandFlag[i].sxm1), ElemIndex(UserCommandFlag[i].sxm2),
					UserCommandFlag[i].targetksix, UserCommandFlag[i].targetksiz);

			sxm1_bn_fit = Cell[Elem_GetPos(ElemIndex(UserCommandFlag[i].sxm1), 1)].Elem.M->PB[HOMmax + 3];
			sxm2_bn_fit = Cell[Elem_GetPos(ElemIndex(UserCommandFlag[i].sxm2), 1)].Elem.M->PB[HOMmax + 3];
			/* print out the sextupole strengths before and after the fitting*/
			printf("Before the fitting, the sextupole field strengths are \n");
			printf("    %s = %f,    %s = %f\n", UserCommandFlag[i].sxm1, sxm1_bn, UserCommandFlag[i].sxm2, sxm2_bn);
			printf("After the fitting, the sextupole field strengths are: \n");
			printf("    %s = %f,    %s = %f\n", UserCommandFlag[i].sxm1, sxm1_bn_fit, UserCommandFlag[i].sxm2, sxm2_bn_fit);

			Ring_GetTwiss(chroma = true, 0.0); /* Compute and get Twiss parameters */
			printglob(); /* print parameter list */
		}

		// coupling calculation
		else if(strcmp(CommandStr,"CouplingFlag") == 0) {
			Ring_GetTwiss(chroma = true, 0.0); /* Compute and get Twiss parameters */
			printlatt("linlat_coupling.out"); /* dump linear lattice functions into "linlat.out" */
			// GetEmittance(ElemIndex("cav"), true);  //only for test
			Coupling_Edwards_Teng();
			Ring_GetTwiss(chroma = true, 0.0); /* Compute and get Twiss parameters */
			printglob(); /* print parameter list */
		}

		// add coupling by random rotating of the full quadrupole magnets
		//if (ErrorCouplingFlag == true) {
		else if(strcmp(CommandStr,"ErrorCouplingFlag") == 0) {
			prtmfile("flat_file.out"); //print the elements without rotation errors
			SetErr(UserCommandFlag[i].err_seed, UserCommandFlag[i].err_rms);
			prtmfile("flat_file_errcoupling_full.out"); //print the elements with rotation errors
			Ring_GetTwiss(chroma = true, 0.0); /* Compute and get Twiss parameters */
			printlatt("linlat_errcoupling.out"); /* dump linear lattice functions into "linlat.out" */
			Coupling_Edwards_Teng();
			// GetEmittance(ElemIndex("cav"), true); //only for test
			Ring_GetTwiss(chroma = true, 0.0); /* Compute and get Twiss parameters */
			//  printlatt();
			printglob(); /* print parameter list */
		}

		//  add coupling by random rotating of the half quadrupole magnets, delicated for soleil
		else if(strcmp(CommandStr,"ErrorCoupling2Flag") == 0) {
			prtmfile("flat_file.out"); //print the elements without rotation errors
			SetErr2(UserCommandFlag[i].err_seed, UserCommandFlag[i].err_rms);
			prtmfile("flat_file_errcoupling_half.out"); //print the elements with rotation errors
			Ring_GetTwiss(chroma = true, 0.0); /* Compute and get Twiss parameters */
			printlatt("linlat_errcoupling2.out"); /* dump linear lattice functions into "linlat.out" */
			Coupling_Edwards_Teng();
			// GetEmittance(ElemIndex("cav"), true);
			Ring_GetTwiss(chroma = true, 0.0); /* Compute and get Twiss parameters */
			printglob(); /* print parameter list */
		}





		/******************************************************************************************/
		// COMPUTATION PART after setting the model
		/******************************************************************************************/
		// computes TuneShift with amplitudes
		else if(strcmp(CommandStr,"AmplitudeTuneShiftFlag") == 0) {
			TunesShiftWithAmplitude(UserCommandFlag[i]._AmplitudeTuneShift_nxpoint,
					UserCommandFlag[i]._AmplitudeTuneShift_nypoint,
					UserCommandFlag[i]._AmplitudeTuneShift_nturn,
					UserCommandFlag[i]._AmplitudeTuneShift_xmax,
					UserCommandFlag[i]._AmplitudeTuneShift_ymax,
					UserCommandFlag[i]._AmplitudeTuneShift_delta);
		}
		// compute tuneshift with energy
		else if(strcmp(CommandStr,"EnergyTuneShiftFlag") == 0) {
			TunesShiftWithEnergy(UserCommandFlag[i]._EnergyTuneShift_npoint,
					UserCommandFlag[i]._EnergyTuneShift_nturn,
					UserCommandFlag[i]._EnergyTuneShift_deltamax);
		}

		// Computes FMA
		else if(strcmp(CommandStr,"FmapFlag") == 0) {
			printf("\n begin Fmap calculation for on momentum particles: \n");
			if (globval.nr_cpus > 1) {
				fmap_mp(globval.nr_cpus, UserCommandFlag[i]._FmapFlag_nxpoint, UserCommandFlag[i]._FmapFlag_nypoint, UserCommandFlag[i]._FmapFlag_nturn,
						UserCommandFlag[i]._FmapFlag_x0, UserCommandFlag[i]._FmapFlag_xmax,
						UserCommandFlag[i]._FmapFlag_y0, UserCommandFlag[i]._FmapFlag_ymax,
						UserCommandFlag[i]._FmapFlag_delta,UserCommandFlag[i]._FmapFlag_diffusion);
			} else {
				fmap(UserCommandFlag[i]._FmapFlag_nxpoint, UserCommandFlag[i]._FmapFlag_nypoint, UserCommandFlag[i]._FmapFlag_nturn,
						UserCommandFlag[i]._FmapFlag_x0, UserCommandFlag[i]._FmapFlag_xmax,
						UserCommandFlag[i]._FmapFlag_y0, UserCommandFlag[i]._FmapFlag_ymax,
						UserCommandFlag[i]._FmapFlag_delta,UserCommandFlag[i]._FmapFlag_diffusion);
			}
		}

		// Compute FMA dp
		else if(strcmp(CommandStr,"FmapdpFlag") == 0) {
			printf("\n begin Fmap calculation for off momentum particles: \n");
			if (globval.nr_cpus > 1) {
				fmapdp_mp(globval.nr_cpus, UserCommandFlag[i]._FmapdpFlag_nxpoint, UserCommandFlag[i]._FmapdpFlag_nepoint, UserCommandFlag[i]._FmapdpFlag_nturn,
						UserCommandFlag[i]._FmapdpFlag_x0, UserCommandFlag[i]._FmapdpFlag_xmax,
						UserCommandFlag[i]._FmapdpFlag_emin, UserCommandFlag[i]._FmapdpFlag_emax,
						UserCommandFlag[i]._FmapdpFlag_z,
						UserCommandFlag[i]._FmapdpFlag_diffusion);
			} else {
				fmapdp(UserCommandFlag[i]._FmapdpFlag_nxpoint, UserCommandFlag[i]._FmapdpFlag_nepoint, UserCommandFlag[i]._FmapdpFlag_nturn,
						UserCommandFlag[i]._FmapdpFlag_x0, UserCommandFlag[i]._FmapdpFlag_xmax,
						UserCommandFlag[i]._FmapdpFlag_emin, UserCommandFlag[i]._FmapdpFlag_emax,
						UserCommandFlag[i]._FmapdpFlag_z,
						UserCommandFlag[i]._FmapdpFlag_diffusion);
		   }
		}
		// Computes Dynamic Aperture on XY axis
		else if(strcmp(CommandStr,"DynApXYFlag") == 0) {
			printf("\n begin XY Dynamic Aperture search: \n\n");
			if (globval.nr_cpus > 1) {
/*				DAXY_mp(globval.nr_cpus, UserCommandFlag[i]._DAXY_nxpoint, UserCommandFlag[i]._DAXY_nypoint, UserCommandFlag[i]._DAXY_nturn,
						UserCommandFlag[i]._DAXY_x0, UserCommandFlag[i]._DAXY_xmax,
						UserCommandFlag[i]._DAXY_y0, UserCommandFlag[i]._DAXY_ymax,
						UserCommandFlag[i]._DAXY_delta); */
			} else {
				daxy(UserCommandFlag[i]._DAXY_nxpoint, UserCommandFlag[i]._DAXY_nypoint, UserCommandFlag[i]._DAXY_nturn,
						UserCommandFlag[i]._DAXY_x0, UserCommandFlag[i]._DAXY_xmax,
						UserCommandFlag[i]._DAXY_y0, UserCommandFlag[i]._DAXY_ymax,
						UserCommandFlag[i]._DAXY_delta);
			}
		}
		
		// Computes Dynamic Aperture on XY axis
		else if(strcmp(CommandStr,"DynApXYRadialFlag") == 0) {
			printf("\n begin XY Dynamic Aperture search (radial): \n\n");
			if (globval.nr_cpus > 1) {
/*				DAXY_mp(globval.nr_cpus, UserCommandFlag[i]._DAXY_nxpoint, UserCommandFlag[i]._DAXY_nypoint, UserCommandFlag[i]._DAXY_nturn,
						UserCommandFlag[i]._DAXY_x0, UserCommandFlag[i]._DAXY_xmax,
						UserCommandFlag[i]._DAXY_y0, UserCommandFlag[i]._DAXY_ymax,
						UserCommandFlag[i]._DAXY_delta); */
			} else {
				daxy_radial(UserCommandFlag[i]._DAXY_nturn, UserCommandFlag[i]._DAXY_nr_radial, 
						UserCommandFlag[i]._DAXY_delta, UserCommandFlag[i]._DAXY_xscale, UserCommandFlag[i]._DAXY_yscale, 
						UserCommandFlag[i]._DAXY_r_tol);
			}
		}

		// Compute FMA dp
		else if(strcmp(CommandStr,"DynApEXFlag") == 0) {
			printf("\n begin EX Dynamic Aperture search: \n\n");
			if (globval.nr_cpus > 1) {
/*				DAEX_mp(globval.nr_cpus, UserCommandFlag[i]._DAEX_nxpoint, UserCommandFlag[i]._DAEX_nepoint, UserCommandFlag[i]._DAEX_nturn,
						UserCommandFlag[i]._DAEX_x0, UserCommandFlag[i]._DAEX_xmax,
						UserCommandFlag[i]._DAEX_emin, UserCommandFlag[i]._DAEX_emax,
						UserCommandFlag[i]._DAEX_z);*/
			} else {
				daex(UserCommandFlag[i]._DAEX_nxpoint, UserCommandFlag[i]._DAEX_nepoint, UserCommandFlag[i]._DAEX_nturn,
						UserCommandFlag[i]._DAEX_x0, UserCommandFlag[i]._DAEX_xmax,
						UserCommandFlag[i]._DAEX_emin, UserCommandFlag[i]._DAEX_emax,
						UserCommandFlag[i]._DAEX_z);
		    }	
		}


		//  // if (CodeComparaisonFlag) {
		//   else if(strcmp(CommandStr,"CodeComparaisonFlag") == 0) {
		//     fmap(200, 100, 1026, -32e-3, 7e-3, 0.0, true);
		//   }

		// MOMENTUM ACCEPTANCE
		else if(strcmp(CommandStr,"MomentumAccFlag") == 0) {
			bool cavityflag, radiationflag;
			/* record the initial values*/
			cavityflag = globval.Cavity_on;
			radiationflag = globval.radiation;

			/* set the dimension for the momentum tracking*/
			if (strncmp("6D", UserCommandFlag[i].TrackDim, 2) == 0) {
				globval.Cavity_on = true;
				globval.radiation = true;
			} else if (strncmp("4D", UserCommandFlag[i].TrackDim, 2) == 0) {
				globval.Cavity_on = false;
				globval.radiation = false;
			} else {
				printf("MomentumAccFlag: Error!!! DimTrack must be '4D' or '6D'\n");
				exit_(1);
			};

			/* calculate momentum acceptance*/
			printf("\n Calculate momentum acceptance: \n");
			MomentumAcceptance(UserCommandFlag[i]._MomentumAccFlag_nturn,
			    UserCommandFlag[i]._MomentumAccFlag_sstart,
				UserCommandFlag[i]._MomentumAccFlag_sstop,
				UserCommandFlag[i]._MomentumAccFlag_deltaminp,
				UserCommandFlag[i]._MomentumAccFlag_deltamaxp,
				UserCommandFlag[i]._MomentumAccFlag_nstepp,
				UserCommandFlag[i]._MomentumAccFlag_deltaminn,
				UserCommandFlag[i]._MomentumAccFlag_deltamaxn,
				UserCommandFlag[i]._MomentumAccFlag_nstepn,
				UserCommandFlag[i]._MomentumAccFlag_nnames,
				UserCommandFlag[i]._MomentumAccFlag_names);

			/* restore the initial values*/
			globval.Cavity_on = cavityflag;
			globval.radiation = radiationflag;
		}

		// induced amplitude
		else if(strcmp(CommandStr,"InducedAmplitudeFlag") == 0) {
			printf("\n Calculate induced amplitude: \n");
			InducedAmplitude(193L);
		}


		else if(strcmp(CommandStr,"EtaFlag") == 0) {
			// compute cod and Twiss parameters for different energy offsets
			for (int ii = 0; ii <= 40; ii++) {
				dP = -0.02 + 0.001 * ii;
				Ring_GetTwiss(chroma = false, dP); /* Compute and get Twiss parameters */
				printlatt("linlat_eta.out"); /* dump linear lattice functions into "linlat.out" */
				getcod(dP, lastpos);
				//     printcod();
				prt_cod("cod.out", globval.bpm, true);
				//system("mv linlat.out linlat_ooo.out");
				sprintf(str1, "mv cod.out cod_%02d.out", ii);
				system(str1);
				sprintf(str1, "mv linlat.out linlat_%02d.out", ii);
				system(str1);
			}
		}

		// track to get phase space
		else if(strcmp(CommandStr,"PhaseSpaceFlag") == 0) {
			bool cavityflag, radiationflag;
			/* record the initial values*/
			cavityflag = globval.Cavity_on;
			radiationflag = globval.radiation;

			/* set the dimension for the momentum tracking*/
			if (strncmp("6D", UserCommandFlag[i]._Phase_Dim, 2) == 0) {
				globval.Cavity_on = true;
			} else if (strncmp("4D", UserCommandFlag[i]._Phase_Dim, 2) == 0) {
				globval.Cavity_on = false;
			} else {
				printf("MomentumAccFlag: Error!!! _Phase_Dim must be '4D' or '6D'\n");
				exit_(1);
			};
			/* setting damping */
			if ( UserCommandFlag[i]._Phase_Damping == true) {
				globval.radiation = true;
			} else  {
				globval.radiation = false;
			}

			start = stampstart();
			Phase(UserCommandFlag[i]._Phase_X,
					UserCommandFlag[i]._Phase_Px,
					UserCommandFlag[i]._Phase_Y,
					UserCommandFlag[i]._Phase_Py,
					UserCommandFlag[i]._Phase_delta,
					UserCommandFlag[i]._Phase_ctau,
					UserCommandFlag[i]._Phase_nturn);
			printf("the simulation time for phase space in tracy 3 is \n");
			stop = stampstop(start);

			/* restore the initial values*/
			globval.Cavity_on = cavityflag;
			globval.radiation = radiationflag;
		}




		else if (strcmp(CommandStr,"TouschekFlag") == 0 ||strcmp(CommandStr,"IBSFlag") == 0 ||
				strcmp(CommandStr,"TousTrackFlag") == 0 ){
			//  ????????????? NSRL version, Check with Soleil version "MomentumAcceptance"
			// IBS & TOUSCHEK
			int k;
			double sigma_s, sigma_delta, tau, alpha_z, beta_z, gamma_z, eps[3];
			FILE *outf;

			int   n_turns     = 40;
			const double Qb   = UserCommandFlag[i]._Qb;   // total charge in one bunch [coulomb]
			const double coup = UserCommandFlag[i]._Coup; // coupling [%]

			//  else if(strcmp(CommandStr,"TouschekFlag") == 0) {
			double sum_delta[globval.Cell_nLoc + 1][2];
			double sum2_delta[globval.Cell_nLoc + 1][2];

			GetEmittance(ElemIndex("cav"), true);

			// initialize momentum aperture arrays
			for (k = 0; k <= globval.Cell_nLoc; k++) {
				sum_delta[k][0] = 0.0;
				sum_delta[k][1] = 0.0;
				sum2_delta[k][0] = 0.0;
				sum2_delta[k][1] = 0.0;
			}

			globval.eps[Y_] = coup * globval.eps[X_];  //0.008e-9;

			// get the twiss parameters
			alpha_z = -globval.Ascr[ct_][ct_] * globval.Ascr[delta_][ct_]
			                                                         - globval.Ascr[ct_][delta_] * globval.Ascr[delta_][delta_];
			beta_z = sqr(globval.Ascr[ct_][ct_]) + sqr(globval.Ascr[ct_][delta_]);
			gamma_z = (1 + sqr(alpha_z)) / beta_z;

			sigma_delta = sqrt(gamma_z * globval.eps[Z_]);
			sigma_s = sqrt(beta_z * globval.eps[Z_]);//50e-3
			beta_z = sqr(sigma_s) / globval.eps[Z_];
			alpha_z = sqrt(beta_z * gamma_z - 1);

			// INCLUDE LC (LC changes sigma_s and eps_z, but has no influence on sigma_delta)
			if (false) {
				double newLength, bunchLengthening;
				newLength = 50e-3;
				bunchLengthening = newLength / sigma_s;
				sigma_s = newLength;
				globval.eps[Z_] = globval.eps[Z_] * bunchLengthening;
				beta_z = beta_z * bunchLengthening;
				gamma_z = gamma_z / bunchLengthening;
				alpha_z = sqrt(beta_z * gamma_z - 1); // this doesn't change
			}

			Touschek(Qb, globval.delta_RF, globval.eps[X_], globval.eps[Y_],
					sigma_delta, sigma_s);

			// Intra Beam Scattering(IBS)
			if (strcmp(CommandStr,"IBSFlag") == 0) {
				// initialize eps_IBS with eps_SR
				for (k = 0; k < 3; k++)
					eps[k] = globval.eps[k];
				for (k = 0; k < 20; k++) //prototype (looping because IBS routine doesn't check convergence)
					IBS(Qb, globval.eps, eps, alpha_z, beta_z);
			}

			// TOUSCHEK TRACKING
			// Calculate Touschek lifetime
			// with the momentum acceptance which is determined by
			// the RF acceptance delta_RF and the momentum aperture
			// at each element location which is tracked over n turns,
			//the vacuum chamber is read from the file "chamber_file"
			// finally, write the momentum acceptance to file "mom_aper.out".
			if (strcmp(CommandStr,"TousTrackFlag") == 0) {
				globval.Aperture_on = true;
				ReadCh(UserCommandFlag[i].chamber_file);
				//      LoadApers("/home/simon/projects/src/lattice/Apertures.dat", 1, 1);
				tau = Touschek(Qb, globval.delta_RF, false, globval.eps[X_],
						globval.eps[Y_], sigma_delta, sigma_s, n_turns, true, sum_delta,
						sum2_delta); //the TRUE flag requires apertures loaded

				printf("Touschek lifetime = %10.3e hrs\n", tau / 3600.0);

				outf = file_write("mom_aper.out");
				for (k = 0; k <= globval.Cell_nLoc; k++)
					fprintf(outf, "%4d %7.2f %5.3f %6.3f\n", k, Cell[k].S, 1e2
							* sum_delta[k][0], 1e2 * sum_delta[k][1]);
				fclose(outf);
			}

		}
		else
			printf("Wrong!!!!!");
	}//end of looking for user defined flag



	return 0;
}//end of main()

