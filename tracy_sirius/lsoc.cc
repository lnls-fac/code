/* Tracy-2

   J. Bengtsson, CBP, LBL      1990 - 1994   Pascal version
                 SLS, PSI      1995 - 1997
   M. Boege      SLS, PSI      1998          C translation
   L. Nadolski   SOLEIL        2002          Link to NAFF, Radia field maps
   J. Bengtsson  NSLS-II, BNL  2004 -        


   
*/

#include "tracy_lib.h"

/* for add alignment errors and do COD correction  */

#ifdef GSL
#include<gsl/gsl_matrix.h> //gnu math lib
#include<gsl/gsl_linalg.h> //gnu math lib
#endif

//non-global variables
bool    first_h = true, first_v = true;
int     m; //number of bpm           
int     n[2];//number of correctors  
double  *w_lsoc[2], **A_lsoc[2],**U_lsoc[2], **V_lsoc[2];  //response matrix between bpm and correctors 



//global values
  /* parameters for orbit correction */
 const int   nCOR = 250; // maximum number of correctors
 const char  hOrbitFileName[]     = "horbit.out"; // LSN
 const char  vOrbitFileName[]     = "vorbit.out"; //LSN
 const char  OrbScanFileName[]    = "OrbScanFile.out";
 
 FILE     *OrbScanFile;
 


/****************************************************************
void prt_gcmat(int bpm, int corr, int plane)
  
  Purpose:
    Print the reponse matrix between bpm and correctors.
    Write the response function to file svdh.out or svdv.out
    
*****************************************************************/
void prt_gcmat(int bpm, int corr, int plane)
{
  int     i, j;
  FILE    *outf = NULL;

  printf("bpm family number = %d, corr family number = %d, plane = %d\n", bpm, corr, plane);

  if (plane == 1)
    outf = file_write("svdh.out");
  else if (plane == 2)
    outf = file_write("svdv.out");
  else {
    printf("prt_gcmat: undefined plane %d, plane must be '1' or '2'\n", plane);
    exit_(1);
  }

  fprintf(outf,"# total monitors: %d\n", m); 

  if (plane == 1)
    fprintf(outf,"# total horizontal correctors: %d\n", n[plane-1]);
  else
    fprintf(outf,"# total vertical correctors: %d\n", n[plane-1]);

  fprintf(outf, "#A [%d][%d]= \n", m, n[plane-1]);
  for (i = 1; i <= m; i++) {
    for (j = 1; j <= n[plane-1]; j++)
      fprintf(outf, "% .3e ", A_lsoc[plane-1][i][j]);
    fprintf(outf, "\n");
  }

  fprintf(outf, "#U [%d][%d]= \n", m, n[plane-1]);
  for (i = 1; i <= m; i++) {
    for (j = 1; j <= n[plane-1]; j++)
      fprintf(outf, "% .3e ", U_lsoc[plane-1][i][j]);
    fprintf(outf, "\n");
  }

  fprintf(outf, "#w [%d]= \n", n[plane-1]);
  for (j = 1; j <= n[plane-1]; j++)
    fprintf(outf, "% .3e ", w_lsoc[plane-1][j]);
  
  fprintf(outf, "\n#V [%d][%d]= \n", m, n[plane-1]);
  for (i = 1; i <= n[plane-1]; i++) {
    for (j = 1; j <= n[plane-1]; j++)
      fprintf(outf, "% .3e ", V_lsoc[plane-1][i][j]);
    fprintf(outf, "\n");
  }

  fclose(outf);
}


/**********************************************************************************
 void gcmat(int bpm, int corr, int plane)
 
 Purpose: 
    Get correlation matrix

                -----------
              \/beta  beta
                    i     j
        A   = ------------- cos(nu pi - 2 pi|nu  - nu |)
         ij   2 sin(pi nu)                     i     j

  
*********************************************************************************/
void gcmat(int bpm, int corr, int plane)
{

  bool      first;
  int       i, j;
  long int  loc;
  double    nu, betai, betaj, nui, nuj, spiq;

  const double  eps = 1e-10;

  m = GetnKid(bpm); n[plane-1] = GetnKid(corr);

  if (m > mnp) {
    printf("gcmat: max no of BPM exceeded %d (%d)\n", m, mnp);
    exit_(1);
  }

  if (n[plane-1] > mnp) {
    printf("gcmat: max no of correctors exceeded %d (%d)\n", n[plane-1], mnp);
    exit_(1);
  }

  first = (plane == 1)? first_h : first_v;
  if (first) {
    if (plane == 1)
      first_h = false;
    else
      first_v = false;
    A_lsoc[plane-1] = dmatrix(1, m, 1, n[plane-1]);
    U_lsoc[plane-1] = dmatrix(1, m, 1, n[plane-1]);
    w_lsoc[plane-1] = dvector(1, n[plane-1]);
    V_lsoc[plane-1] = dmatrix(1, n[plane-1], 1, n[plane-1]);
  }

  nu = globval.TotalTune[plane-1]; spiq = sin(M_PI*nu);

  for (i = 1; i <= m; i++) {
    loc = Elem_GetPos(bpm, i);
    betai = Cell[loc].Beta[plane-1]; nui = Cell[loc].Nu[plane-1];
    for (j = 1; j <= n[plane-1]; j++) {
      loc = Elem_GetPos(corr, j);
      betaj = Cell[loc].Beta[plane-1]; nuj = Cell[loc].Nu[plane-1];
      A_lsoc[plane-1][i][j] =
	sqrt(betai*betaj)/(2.0*spiq)*cos(nu*M_PI-fabs(2.0*M_PI*(nui-nuj)));
    }
  }

  for (i = 1; i <= m; i++)
    for (j = 1; j <= n[plane-1]; j++)
      U_lsoc[plane-1][i][j] = A_lsoc[plane-1][i][j];

  dsvdcmp(U_lsoc[plane-1], m, n[plane-1], w_lsoc[plane-1], V_lsoc[plane-1]);

  for (j = 1; j <= n[plane-1]; j++)
    if (w_lsoc[plane-1][j] < eps) {
      printf("gcmat: singular beam response matrix"
	     " %12.3e, plane = %d, j = %d\n",
	     w_lsoc[plane-1][j], plane, j);
      prt_gcmat(bpm, corr, plane);
      exit_(1);
    }
}

void lsoc(int niter, int bpm, int corr, int plane)
{
  int       i, j;
  long int  k;
  svdarray  b, x;

  for (i = 1; i <= niter; i++) {
    for (j = 1; j <= m; j++) {
      k = Elem_GetPos(bpm, j);
      b[j] = -Cell[k].BeamPos[(plane-1)*2] + Cell[k].dS[plane-1];
    }
      
    dsvbksb(U_lsoc[plane-1], w_lsoc[plane-1], V_lsoc[plane-1],
	    m, n[plane-1], b, x);

    for (j = 1; j <= n[plane-1]; j++)
      if (plane == 1)
        SetdKpar(corr, j, Dip, -x[j]);
      else
        SetdKpar(corr, j, -Dip, x[j]);
  }
}




/**************************************************************
// The following files are copied from nsls-ii_lib_templ.h
   To be tested.
*************************************************************/
/******************************************************************************
bool CorrectCOD_Ns(FILE *hOrbitFile, FILE *vOrbitFile, const char *ae_file, const int n_orbit,
     const int n, const int k, const int nwh, const int nwv, int *hcorrIdx, int *vcorrIdx)
     
  Purpose:
          Read in the alignment error from an external file, and then correct the orbits
	  using SVD method.
  Input:
    hOrbitFile    file in which horizontal orbit is saved
    vOrbitFile    file in which vertical orbit is saved
    ae_file       file from which alignment error is readed
    nhw           number of horizontal singular values to be taken for the correction
    nwv           number of vertical singular values to be taken for the correction
  
  Return:
          bool flag cod, if true, then the orbit is corrected successfully,
	                 if false, then the orbit is NOT corrected successfully.   
  
  Comments:         
       modif LSN
       Add two arguments for SVD correction
       nhw and nwv number of singular values to be taken for the correction
       n_orbit number of iteration for orbit correction
       n number of scaling
*******************************************************************************/
bool CorrectCOD_Ns(FILE *hOrbitFile, FILE *vOrbitFile, const char *ae_file, const int n_orbit,
     const int n, const int k, const int nwh, const int nwv, int *hcorrIdx, int *vcorrIdx)
{
  bool    cod = false;
  
  // Clear trim setpoints
  set_bnL_design_fam(globval.hcorr, Dip, 0.0, 0.0);
  set_bnL_design_fam(globval.vcorr, Dip, 0.0, 0.0);

  // load misalignments
  LoadAlignTol(ae_file, true, 1.0, true, k);

  if (bba) {
    // Beam based alignment
    Align_BPM2quad(Quad);
  }
    
  cod = CorrectCODs(hOrbitFile, vOrbitFile, n_orbit, nwh, nwv, hcorrIdx, vcorrIdx); 
    
  return cod;
}

/************************************************************************************
void readCorrectorList(const char *hCorrListName, const char *vCorrListName, int *hcorrIdx, int *vcorrIdx,
                        int& NhcorrIdx,int& NvcorrIdx)

  Purpose:
      Read the files with horizontal and vertical correctors status, then return the list with 
      kid number of the correctors which are used for orbit correction.   
  Input:
       hCorrListName          file with horizontal corrector index
       vCorrListName          file with vertical corrector index
       
  Output:
       hcorrIdx    array with the kid number of the horizontal correctors which are used for orbit correction 
       vcorrIdx    array with the kid number of the vertical correctors which are used for orbit correction 
 
  Comments:
          Jianfeng Zhang  06/04/2011
	   Add int& NhcorrIdx,int& NvcorrIdx, to return the numbers of correctors used for orbit correction
*************************************************************************************/
void readCorrectorList(const char *hCorrListName, const char *vCorrListName, int *hcorrIdx, int *vcorrIdx)
{
  int   k, status, nKid, temp;
  FILE  *hCorrFile, *vCorrFile;
  int   NhcorrIdx = 0, NvcorrIdx = 0; //number of corretors used for orbit correction
  bool  prt = false;
  long int loc;
  char line[max_str]="not_defined";
  
  status = -1; temp = -1;
  hCorrFile = file_read(hCorrListName);
  vCorrFile = file_read(vCorrListName);
  
  // get number of correctors defined in lattice
  nKid = GetnKid(globval.hcorr);
  printf("Horizontal Correctors: Fnum %ld  nKid = %d\n", globval.hcorr, nKid);
  
  // first line is a comment
  if (fgets(line, max_str, hCorrFile) == 0)
    exit(1);
  
  // loop over correctors
  for (k = 1; k <= nKid; k++){
     
     if (fgets(line, max_str, hCorrFile) == NULL) {
       printf("Error in file %s\n", hCorrListName);
       return;
     }
     sscanf(line, "%d %d", &temp, &status);
     if (prt) printf("H-plane: %d (%d) stat read %d\n", temp, k, status);     
     
     loc = Elem_GetPos(globval.hcorr, k);
     if (status == 0) {
       Cell[loc].Elem.M->Status = false;
     } 
     else{
       NhcorrIdx ++;
       hcorrIdx[NhcorrIdx-1] = k;
     }
        
  }
  
  fclose(hCorrFile);
  
  // get number of correctors defined in lattice
  nKid = GetnKid(globval.vcorr);
  printf("Vertical Correctors: Fnum %ld  nKid = %d\n", globval.vcorr, nKid);
  
  // first line is a comment
  if (fgets(line, max_str, vCorrFile) == 0)
    return;
  
  // loop over correctors
  for (k = 1; k <= nKid; k++){
     
     if (fgets(line, max_str, vCorrFile) == NULL) {
       printf("Error in file %s\n", vCorrListName);
       return;
     }
     sscanf(line, "%d %d", &temp, &status);
     if (prt) printf("V-plane: %d (%d) stat read %d\n", temp, k, status);     
     
     loc = Elem_GetPos(globval.vcorr, k);
     if (status == 0) {
       Cell[loc].Elem.M->Status = false;
     }
     else{
       NvcorrIdx ++;
       vcorrIdx[NvcorrIdx-1] = k;
     }
  }
  
  fclose(vCorrFile);
    
}


/**************************************************************
  void gcmats(int bpm, int corr, int plane, int *corrIdx, int NcorrIdx)
  
  Purpose:
    Get the response function between BPM and Correctors
    Get correlation matrix

                -----------
              \/beta  beta
                    i     j
        A   = ------------- cos(nu pi - 2 pi|nu  - nu |)
         ij   2 sin(pi nu)                     i     j
	 
  
  Input:
       bpm         family number of 'bpm'
       corr        family number of 'correctors'
       plane       '1' for horizontal, '2' for vertical
       corrIdx     list of the kid number of the correctors
       NcorrIdx    number of correctors used for orbit correction
       
  Output:
      
  Return:
        Response function between BPM and correctors: A_lsoc
	
  Comments:
 
  **************************************************************/
void gcmats(int bpm, int corr, int plane, int *corrIdx)
{
  bool      first;
  int       i, j;
  long int  loc;
  double    nu, betai, betaj, nui, nuj, spiq;

  const double  eps = 1e-10;

  m = GetnKid(bpm); // number of BPMs
    
  //n[plane-1] = GetnKid(corr); // number of correctors
  n[plane-1] = 0;
  
  // count number of valid correctors. Not very smart ...(????????)
  for (i = 0; i < nCOR; i++){
    //printf("i=%d, elem=%d\n", i, corrIdx[i]);
    if (corrIdx[i] > 0) n[plane-1]++;
  }
  printf("gcmats: %d active correctors in %d plane\n", n[plane-1], plane);  
  

  if (m > mnp) {
    printf("Error!!!! gcmats: max no of BPM exceeded maximum number: %d (%d)\n", m, mnp);
    exit(1);
  }

  if (n[plane-1] > mnp) {
    printf("Error!!!! gcmats: max no of correctors exceeded maximum number: %d (%d)\n", n[plane-1], mnp);
    exit(1);
  }

  first = (plane == 1)? first_h : first_v;
  if (first) {
    if (plane == 1)
      first_h = false;
    else
      first_v = false;
    A_lsoc[plane-1] = dmatrix(1, m, 1, n[plane-1]);
    U_lsoc[plane-1] = dmatrix(1, m, 1, n[plane-1]);
    w_lsoc[plane-1] = dvector(1, n[plane-1]);
    V_lsoc[plane-1] = dmatrix(1, n[plane-1], 1, n[plane-1]);
  }

  nu = globval.TotalTune[plane-1]; spiq = sin(M_PI*nu);

  for (i = 1; i <= m; i++) {
    loc = Elem_GetPos(bpm, i);
    betai = Cell[loc].Beta[plane-1]; nui = Cell[loc].Nu[plane-1]; //beta function and nu at the BPM position
    for (j = 1; j <= n[plane-1]; j++) {
      loc = Elem_GetPos(corr, corrIdx[j-1]);
      betaj = Cell[loc].Beta[plane-1]; nuj = Cell[loc].Nu[plane-1];//beta function and nu at the corrector position
      A_lsoc[plane-1][i][j] =
  sqrt(betai*betaj)/(2.0*spiq)*cos(nu*M_PI-fabs(2.0*M_PI*(nui-nuj)));//response function between BPM and correctors
    }
  }

  for (i = 1; i <= m; i++)
    for (j = 1; j <= n[plane-1]; j++)
      U_lsoc[plane-1][i][j] = A_lsoc[plane-1][i][j];

#ifndef GSL
  dsvdcmp(U_lsoc[plane-1], m, n[plane-1], w_lsoc[plane-1], V_lsoc[plane-1]);
#else
  size_t gsl_dm = m;
  size_t gsl_dn = n[plane-1];

  gsl_matrix *gslm_A = gsl_matrix_alloc(gsl_dm, gsl_dn);
  for (size_t i = 0; i < gsl_dm; ++i) {
      for (size_t j = 0; j < gsl_dn; ++j) {
          gsl_matrix_set(gslm_A, i, j, U_lsoc[plane-1][i+1][j+1]);
      }
  }
  gsl_vector *gslv_work = gsl_vector_alloc(gsl_dn);
  gsl_vector *gslv_S = gsl_vector_alloc(gsl_dn);
  gsl_matrix *gslm_V = gsl_matrix_alloc(gsl_dn, gsl_dn);
  gsl_linalg_SV_decomp(gslm_A, gslm_V, gslv_S, gslv_work);
  
  for (size_t i = 0; i < gsl_dn; ++i) w_lsoc[plane-1][i+1] = gsl_vector_get(gslv_S, i);
  for (size_t i = 0; i < gsl_dm; ++i)
      for (size_t j = 0; j < gsl_dn; ++j)
          U_lsoc[plane-1][i+1][j+1] = gsl_matrix_get(gslm_A, i, j);
  for (size_t i = 0; i < gsl_dn; ++i)
      for (size_t j = 0; j < gsl_dn; ++j)
          V_lsoc[plane-1][i+1][j+1] = gsl_matrix_get(gslm_V, i, j);

  gsl_vector_free(gslv_work);
  gsl_vector_free(gslv_S);  
  gsl_matrix_free(gslm_V);
  gsl_matrix_free(gslm_A);
#endif

  for (j = 1; j <= n[plane-1]; j++)
    if (w_lsoc[plane-1][j] < eps) {
      printf("gcmats: singular beam response matrix"
       " %12.3e, plane = %d, j = %d\n",
       w_lsoc[plane-1][j], plane, j);
      exit(0);
    }
}


/*******************************************************************************
 void LoadFieldErrs(const char *FieldErrorFile, const bool Scale_it,
     const double Scale, const bool new_rnd, const int ik) 
     
  Purpose:
    Load field errors for all elements specified in input file FieldErrorFile
    
  Input:
    FieldErrorFile         file with field error
    Scale_it               if ture, scale the filed error  
    Scale                  scale of the field error, Scale_it must be true
    new_rnd                whether to generate new scale value for the rms error
    ik       
********************************************************************************/
void LoadFieldErrs(const char *FieldErrorFile, const bool Scale_it,
     const double Scale, const bool new_rnd, const int ik) 
{  
  bool    rms, set_rnd = false;
  char    line[max_str], name[max_str], type[max_str], *prm;
  int     k, n, seed_val;
  double  Bn, An, r0;
  FILE    *inf;

  const bool  prt = true;

  inf = file_read(FieldErrorFile);

 
  while (fgets(line, max_str, inf) != NULL) {
    if (strstr(line, "#") == NULL) { // if line does not strat with #
      // check for whether to set new seed
      sscanf(line, "%s", name); 
      if (strcmp("seed", name) == 0) { // if seed number
          set_rnd = true;
          sscanf(line, "%*s %d", &seed_val); 
          printf("LoadFieldErr: setting random seed to %d\n", seed_val+ik);
          iniranf(seed_val+ik); 
      } else { // then it is an & bn definition
          sscanf(line, "%*s %s %lf", type, &r0); // read reference radius
          printf("\n");
          printf("%-4s %3s %7.1le\n", name, type, r0);
          rms = (strcmp("rms", type) == 0)? true : false;
          if (rms && !set_rnd) { 
              printf("LoadFieldErr: seed not defined\n");
              exit(1);
          } //end if
          // skip first three parameters
          strtok(line, " "); // set pointer 
          for (k = 1; k <= 2; k++)
              strtok(NULL, " "); // pointer move to nxt element
          while (((prm = strtok(NULL, " ")) != NULL) &&
            (strcmp(prm, "\r\n") != 0)) {
                sscanf(prm, "%d", &n);
                prm = get_prm();
                sscanf(prm, "%lf", &Bn);
                prm = get_prm(); 
                sscanf(prm, "%lf", &An);
                if (Scale_it) {
                   Bn *= Scale; 
                   An *= Scale;
                }
                if (prt)
                  printf(" %1d %9.1e %9.1e\n", n, Bn, An);
                // convert to normalized multipole components
                SetFieldErrors(name, rms, r0, n, Bn, An, false); //troquei true por false, para não implementar o erro aleatório de
          } // end while                 excitação ainda. ele será implementado quando os erros de alinhamento forem contabilizados.
        } // end if seed
    } // end if #
  } // end while file

  fclose(inf);
}



/*****************************************************************************************
bool CorrectCODs(FILE *hOrbitFile, FILE *vOrbitFile, int n_orbit, int nwh, int nwv, 
                int *hcorrIdx, int *vcorrIdx)

  Purpose:
    Correct the orbit, and print the statistics of the orbit to the file 'OrbScanFile'.
// correction algorithms

// control of orbit



  Input:
    hOrbitFile      file to be printed with the horizontal closed orbit 
    vOrbitFile      file to be printed with the vertical closed orbit 
    n_orbit         number of interation to do orbit correction
    nwh             singular number in horizontal orbit correction
    nwv             singular number in vertical orbit correction
    hcorrIdx        array with the kid number of horizontal correctors
    vcorrIdx        array with the kid number of vertical correctors
  Output: 
  
  Comments:
    // closed orbit correction by n_orbit iterations
// modif LSN
// Add two argument for SVD correction
// nhw and nwv number of singular values to be taken for the correction
// Modif switch sextupole by 50% for iteration #1

  
    Jianfeng Zhang 08/04/2011    Modify the routine to reduce and restore 
                                 sextupole strength, to make it work in a 
				 general way, not lattice specific. 
******************************************************************************************/
bool CorrectCODs(FILE *hOrbitFile, FILE *vOrbitFile, int n_orbit, int nwh, int nwv, int *hcorrIdx, int *vcorrIdx)
{
  bool      cod;
  int       i,j;
  long int  lastpos;
  Vector2   mean, sigma, max;
  const double  sexred = 0.999; //  reduction for sextupoles strength

   //reduce sextupole by 99.9% for not be too off in tune values
   // because the first time the COD is realy large, so the field
   // in sextupole is not linear anymore.
   for(j = 0;j <= globval.Cell_nLoc; j++)
   	if(Cell[j].Elem.Pkind == Mpole&&Cell[j].Elem.M->n_design == Sext)
   		SetdKrpar(Cell[j].Fnum,Cell[j].Knum,Sext,-sexred);
   

  cod = getcod(0.0, lastpos);
  
  if (cod) {
    codstat(mean, sigma, max, globval.Cell_nLoc, false); // get orbit stats at all BPMs
    fprintf(OrbScanFile, "\n");//print the statistics of the orbit at all BPMs to the file
    fprintf(OrbScanFile,"Initial RMS orbit (BPMs):   "
      " x = % 7.1e mm, y = % 7.1e mm\n",
      1e3*sigma[X_], 1e3*sigma[Y_]);
      fprintf(OrbScanFile,"Initial MEAN orbit (BPMs):  "
              " x = % 7.1e mm, y = % 7.1e mm\n",
              1e3*mean[X_], 1e3*mean[Y_]);
      fprintf(OrbScanFile,"Initial MAX orbit (BPMs):   "
              " x = % 7.1e mm, y = % 7.1e mm\n",
              1e3*max[X_], 1e3*max[Y_]);
    codstat(mean, sigma, max, globval.Cell_nLoc, true);// get orbit stats at all lattice elements
    fprintf(OrbScanFile,"Initial RMS orbit (all):    "
      " x = % 7.1e mm, y = % 7.1e mm\n",
      1e3*sigma[X_], 1e3*sigma[Y_]);

     //orbit correction
    for (i = 0; i < n_orbit; i++){
    	
    	lsoc2s(1, globval.bpm, globval.hcorr, 1, nwh, hcorrIdx); // correct horizontal orbit
    	lsoc2s(1, globval.bpm, globval.vcorr, 2, nwv, hcorrIdx); // correct vertical orbit
    	//fprintf(stdout, "iter %d get Orbit before\n", i);
    	cod = getcod(0.0, lastpos);                    // find closed orbit
    	//fprintf(stdout, "iter %d get Orbit after\n", i);

    	if (!cod) break;
    }

    //restore sexupole strengths to nominal values
    for(j = 0;j <= globval.Cell_nLoc; j++)
    	if(Cell[j].Elem.Pkind == Mpole&&Cell[j].Elem.M->n_design == Sext)
    		SetdKrpar(Cell[j].Fnum,Cell[j].Knum,Sext,1./(1.-sexred)-1.);

    //Iterate again to correct sextupole effects
    for (i = 0; i < n_orbit; i++){
    	
    	lsoc2s(1, globval.bpm, globval.hcorr, 1, nwh, hcorrIdx); // correct horizontal orbit
    	lsoc2s(1, globval.bpm, globval.vcorr, 2, nwv, hcorrIdx); // correct vertical orbit
    	//fprintf(stdout, "iter %d get Orbit before\n", i);
    	cod = getcod(0.0, lastpos);                    // find closed orbit
    	//fprintf(stdout, "iter %d get Orbit after\n", i);

    	if (!cod) break;
    }


    if (cod) {
      // get and print out corrected orbit, and return the statistics of the orbit at all lattice elements
      codstats(hOrbitFile, vOrbitFile, mean, sigma, max, globval.Cell_nLoc, true);
      // return COD stats at BPM location
      codstat(mean, sigma, max, globval.Cell_nLoc, false);
      
      fprintf(OrbScanFile,"Corrected RMS orbit (BPMs): "
        " x = % 7.1e mm, y = % 7.1e mm\n",
        1e3*sigma[X_], 1e3*sigma[Y_]);
      fprintf(OrbScanFile,"Corrected MEAN orbit (BPMs):"
              " x = % 7.1e mm, y = % 7.1e mm\n",
              1e3*mean[X_], 1e3*mean[Y_]);
      fprintf(OrbScanFile,"Corrected MAX orbit (BPMs): "
              " x = % 7.1e mm, y = % 7.1e mm\n",
              1e3*max[X_], 1e3*max[Y_]);
      codstat(mean, sigma, max, globval.Cell_nLoc, true);
      fprintf(OrbScanFile,"Corrected RMS orbit (all):  "
        " x = % 7.1e mm, y = % 7.1e mm\n",
        1e3*sigma[X_], 1e3*sigma[Y_]);
      // get stats for correctors
      corstat(mean, sigma, max, globval.Cell_nLoc);
      fprintf(OrbScanFile,"Corrected RMS CM:     "
              " x = % 7.1e mrad, y = % 7.1e mrad\n",
              1e3*sigma[X_], 1e3*sigma[Y_]);
      fprintf(OrbScanFile,"Corrected MEAN CM:    "
              " x = % 7.1e mrad, y = % 7.1e mrad\n",
              1e3*mean[X_], 1e3*mean[Y_]);
      fprintf(OrbScanFile,"Corrected MAX CM:     "
              " x = % 7.1e mrad, y = % 7.1e mrad\n",
              1e3*max[X_], 1e3*max[Y_]);
    }

    fflush(OrbScanFile);
  }

  return cod;
}

/**************************************************************** 
void lsoc2(int niter, int bpm, int corr, int plane, int nval)
 
 Purpose:
   add argument nval number of singular values to be taken

*****************************************************************/
void lsoc2(int niter, int bpm, int corr, int plane, int nval)
// add argument nval number of singular values to be taken
{
  long int  k;
  svdarray  b, x;

  for (int i = 1; i <= niter; i++) {
    for (int j = 1; j <= m; j++) {
      k = Elem_GetPos(bpm, j);
      b[j] = -Cell[k].BeamPos[(plane-1)*2] + Cell[k].dS[plane-1];
    }

    #ifndef GSL
    dsvbksb(U_lsoc[plane-1], w_lsoc[plane-1], V_lsoc[plane-1],
            m, n[plane-1], b, x);
    #else
    #define gsl_dm m
    #define gsl_dn n[plane-1]
    gsl_matrix *gslm_A = gsl_matrix_alloc(gsl_dm, gsl_dn);
    gsl_vector *gslv_work = gsl_vector_alloc(gsl_dn);
    gsl_vector *gslv_S = gsl_vector_alloc(gsl_dn);
    gsl_matrix *gslm_V = gsl_matrix_alloc(gsl_dn, gsl_dn);
    gsl_vector *gslv_b = gsl_vector_alloc(gsl_dm); 
    
    gsl_vector *gslv_x = gsl_vector_alloc(gsl_dn);

    for (int j = 0; j < gsl_dm; ++j) {
        gsl_vector_set(gslv_b, j, b[j+1]);
    }
    
    if (nval > gsl_dn || nval <1){
       fprintf(stdout, "Warning nval %d larger than gsl_dn %d\n", nval, gsl_dn);
       nval = gsl_dn;
       } 
    
    for (int j = 0; j < gsl_dn; ++j) {
        
        // select number of singular values
        if (j < nval)
            gsl_vector_set(gslv_S, j, w_lsoc[plane-1][j+1]);
        else
            gsl_vector_set(gslv_S, j, w_lsoc[plane-1][j+1]*0);
            
        for (int i = 0; i < gsl_dm; ++i) {
            gsl_matrix_set(gslm_A, i, j, U_lsoc[plane-1][i+1][j+1]);
        }
        for (int i = 0; i < gsl_dn; ++i) 
            gsl_matrix_set(gslm_V, i, j, V_lsoc[plane-1][i+1][j+1]);
    }
    
    
    
    
    gsl_linalg_SV_solve(gslm_A, gslm_V, gslv_S, gslv_b, gslv_x);

    for (int i = 0; i < gsl_dn; ++i)
        x[i+1] = gsl_vector_get(gslv_x, i);

    gsl_vector_free(gslv_work);
    gsl_vector_free(gslv_S);  
    gsl_vector_free(gslv_b);  
    gsl_vector_free(gslv_x);  
    gsl_matrix_free(gslm_V);
    gsl_matrix_free(gslm_A);
 #undef gsl_dm
    #undef gsl_dn
    #endif

    for (int j = 1; j <= n[plane-1]; j++)
      if (plane == 1)
        SetdKpar(corr, j, Dip, -x[j]);
      else
        SetdKpar(corr, j, -Dip, x[j]);
  }
}

/****************************************************************************
 void lsoc2s(int niter, int bpm, int corr, int plane, int nval, int *corIdx)

  Purpose:
     Orbit correction.
      
    add argument nval number of singular values to be taken
    add array of index of correctors to use
    
  Input:
    niter                   interation time to do orbit correction      
    bpm                     family number of bpm
    corr                    family number of correctors
    plane                   '1', horizontal plane; '2',vertical plane.
    nval                    singular number to do orbit correction
    corIdx                  array with corrector kid number
*****************************************************************************/
void lsoc2s(int niter, int bpm, int corr, int plane, int nval, int *corIdx)
// add argument nval number of singular values to be taken
// add array of index of correctors to use
{
  long int  k;
  svdarray  b, x;

  for (int i = 1; i <= niter; i++) {
    for (int j = 1; j <= m; j++) {
      k = Elem_GetPos(bpm, j);
      b[j] = -Cell[k].BeamPos[(plane-1)*2] + Cell[k].dS[plane-1];//add the displacement error of bpm
    }

    #ifndef GSL
    dsvbksb(U_lsoc[plane-1], w_lsoc[plane-1], V_lsoc[plane-1],
            m, n[plane-1], b, x);
    #else
    #define gsl_dm m
    #define gsl_dn n[plane-1]
    gsl_matrix *gslm_A = gsl_matrix_alloc(gsl_dm, gsl_dn);
    gsl_vector *gslv_work = gsl_vector_alloc(gsl_dn);
    gsl_vector *gslv_S = gsl_vector_alloc(gsl_dn);
    gsl_matrix *gslm_V = gsl_matrix_alloc(gsl_dn, gsl_dn);
    gsl_vector *gslv_b = gsl_vector_alloc(gsl_dm); 
    
    gsl_vector *gslv_x = gsl_vector_alloc(gsl_dn);

    for (int j = 0; j < gsl_dm; ++j) {
        gsl_vector_set(gslv_b, j, b[j+1]);
    }
    
    if (nval > gsl_dn || nval <1){
       fprintf(stdout, "Warning nval %d larger than gsl_dn %d\n", nval, gsl_dn);
       nval = gsl_dn;
       } 
    
    for (int j = 0; j < gsl_dn; ++j) {
        
        // select number of singular values
        if (j < nval)
            gsl_vector_set(gslv_S, j, w_lsoc[plane-1][j+1]);
        else
            gsl_vector_set(gslv_S, j, w_lsoc[plane-1][j+1]*0);
            
        for (int i = 0; i < gsl_dm; ++i) {
            gsl_matrix_set(gslm_A, i, j, U_lsoc[plane-1][i+1][j+1]);
        }
        for (int i = 0; i < gsl_dn; ++i) 
            gsl_matrix_set(gslm_V, i, j, V_lsoc[plane-1][i+1][j+1]);
    }
            
    gsl_linalg_SV_solve(gslm_A, gslm_V, gslv_S, gslv_b, gslv_x);

    for (int i = 0; i < gsl_dn; ++i)
        x[i+1] = gsl_vector_get(gslv_x, i); //get the value of correctors
    
    //free memory
    gsl_vector_free(gslv_work);
    gsl_vector_free(gslv_S);  
    gsl_vector_free(gslv_b);  
    gsl_vector_free(gslv_x);  
    gsl_matrix_free(gslm_V);
    gsl_matrix_free(gslm_A);
 #undef gsl_dm
    #undef gsl_dn
    #endif

    // set correctors to computed values
    for (int j = 1; j <= n[plane-1]; j++)
      if (plane == 1)
        SetdKpar(corr, corIdx[j-1], Dip, -x[j]);
      else
        SetdKpar(corr, corIdx[j-1], -Dip, x[j]);
  }
}

/**************************************************************
void Align_BPM2quad(const int n)

  Purpose:
    Align BPMs to adjacent multipoles.

***************************************************************/
void Align_BPM2quad(const int n)
{
  

  bool     prt = false;
  int      j;
  long int  loc = -1, locUSQUAD = -1, locDSQUAD = -1,  locQUAD = -1;

  double USQUADPosition = -1.0;
  double DSQUADPosition = -1.0;
  double BPM2USQUAD = 0.0;
  double BPM2DSQUAD = 0.0;
  
  const int  n_step = 10; // number of step for the search loop

  printf("\n");
  for (int i = 1; i <= GetnKid(globval.bpm); i++) {
    loc = Elem_GetPos(globval.bpm, i);

    if ((loc == 1) || (loc == globval.Cell_nLoc)) {
      printf("Align_BPMs: BPM at entrance or exit of lattice: %ld\n", loc);
      exit(1);
    }

    if (prt)  printf("BPM no %1d (%8.3f)\n", i, DSQUADPosition);
    
    // look for adjacent downstream quadrupole
    j = 1; DSQUADPosition = -1.0;
    do {
      if ((Cell[loc+j].Elem.Pkind == Mpole) &&
        (Cell[loc+j].Elem.M->n_design == n)) {
          locDSQUAD = loc+j;
          DSQUADPosition = Cell[locDSQUAD].S - 0.5*Cell[locDSQUAD].Elem.PL ; // BPM to Quad center
          BPM2DSQUAD = fabs(DSQUADPosition   - Cell[loc].S);
          if (prt) printf("downstream quadrupole %s (%4.3f m)\n", Cell[locDSQUAD].Elem.PName, BPM2DSQUAD);
          break;
        }
      j++;
    } while ((j <= n_step) && ((loc + j) <= globval.Cell_nLoc));
      
    // look for upstream quadrupole
    j = 1; USQUADPosition = -1.0;
    do {
      if ((Cell[loc-j].Elem.Pkind == Mpole) &&
        (Cell[loc-j].Elem.M->n_design == n)) {
          locUSQUAD = loc-j;
          USQUADPosition = Cell[loc-j].S - 0.5*Cell[loc-j].Elem.PL; // BPM to Quad center
          BPM2USQUAD = fabs(USQUADPosition - Cell[loc].S);
          if (prt) printf("upstream quadrupole %s (%4.3f m) \n", Cell[locUSQUAD].Elem.PName, -BPM2USQUAD);
          break;
        }
      j++;
    } while ((j <= n_step) && ((loc - j) > 0));
    
    // is up and dow stream quad found     
    if ((USQUADPosition != -1.0) && (DSQUADPosition != -1.0))
    { // both up and down stream quads
      if (BPM2USQUAD > BPM2DSQUAD){
        locQUAD = locDSQUAD;}
      else{ 
        locQUAD = locUSQUAD;}
    }else if (USQUADPosition == -1.0){ // just downstream quad
       locQUAD = locDSQUAD;}
     else if (DSQUADPosition == -1.0){ // just upstream quad
     locQUAD = locUSQUAD;}
    
    // if Quad found, set BPM error to quadrupole errors 
    if ((DSQUADPosition != -1.0) || (USQUADPosition != -1.0)){
      for (int k = 0; k <= 1; k++)
        Cell[loc].Elem.M->PdSsys[k] = Cell[locQUAD].dS[k];
        Mpole_SetdS(globval.bpm, i);
          if (prt) printf("BPM no %1d is aligned to quadrupole %s\n", i, Cell[locQUAD].Elem.PName);
    }
    else
      printf("Align_BPMs: no multipole adjacent to BPM no %d\n", i);
  }
}


/********************************************************************************* 
   The following functions are copied from physlib_templ.h, need to be tested 
**********************************************************************************/

/***************************************************************************
void codstats(FILE *hOrbitFile, FILE *vOrbitFile, double *mean, 
             double *sigma, double *xmax, long lastpos, bool all)
 
Purpose:
     Routines for closed orbit correction
     return the mean orbit, rms orbit and maximum orbit, based on the orbits at 
     all lattice elements or all bpm postion, 
     and print the COD at all lattice elements or all bpm position to the files 
     'horbit.out','vorbit.out'
  
  Input: 
     hOrbitFile    name of file to be printed with cod 
     vOrbitFile    name of file to be printed with cod
     mean           mean value of the orbit, horizontal or vertical 
     sigma          rms value of the orbit, horizontal or vertical
     xmax           maximum value of the orbit, horizontal or vertical
     lastpos        last element index in the lattice
     all            true, then do statistics on the orbit at all elements
                    false, ...............................at all bpm 

***************************************************************************/
void codstats(FILE *hOrbitFile, FILE *vOrbitFile, double *mean, double *sigma, double *xmax, long lastpos, bool all)
{
  long i = 0L, j = 0L, n = 0L;
  Vector2 sum, sum2;
  double codvec[2][lastpos];
  double TEMP;
  long nprint = 0L;
  
  //initialize
  for (j = 0; j <= 1; j++) {
    sum[j] = 0.0; sum2[j] = 0.0; xmax[j] = 0.0;
  }
  //initialize
  for (j = 0; j <= 1; j++) {
     for (i = 0; i <= lastpos; i++) {
        codvec[j][i] = 0.0;
     } // for i
  } // for j
  
  //start loop at 1 since in Cell_Pass element 0 is skipped (element 0 is alaways marker)
  // data in index 0 is garbage
  for (i = 1; i <= lastpos; i++) {
    if (all || Cell[i].Fnum == globval.bpm) {
      n++;
      for (j = 1; j <= 2; j++) {
        TEMP = Cell[i].BeamPos[j * 2 - 2];
        codvec[j-1][n-1] = TEMP;
// if display changed for BPM
/*           if (Cell[i].Fnum == globval.bpm) { // got a BPM
              codvec[j-1][n-1] -= Cell[i].Elem.M->PdSsys[j-1];
              }*/
        sum[j - 1]  += TEMP;
        sum2[j - 1] += TEMP * TEMP;
        xmax[j - 1] = max(xmax[j - 1], TEMP);
      } // for j
    } // if loop
  } // for i

  // save number of useful data
  nprint = n;
    
  for (j = 0; j <= 1; j++) {
    if (n != 0)
      mean[j] = sum[j] / n;
    else
      mean[j] = 0.0;
    if (n != 0 && n != 1) {
      TEMP = sum[j];
      sigma[j] = (n * sum2[j] - TEMP * TEMP) / (n * (n - 1.0));
    } else
      sigma[j] = 0.0;
    if (sigma[j] >= 0.0)
      sigma[j] = sqrt(sigma[j]);
    else
      sigma[j] = 0.0;
  }

// store data in orbit files
// two loops for speed efficiency ?
     for (i = 0; i < nprint; i++) {
        fprintf(hOrbitFile, "% 9.3e  ", codvec[X_][i]);
     } // for i
     fprintf(hOrbitFile, "\n");
     fflush(hOrbitFile);
    
     
  
     for (i = 0; i < nprint; i++) {
        fprintf(vOrbitFile, "% 9.3e  ", codvec[Y_][i]);
     } // for i
     fprintf(vOrbitFile, "\n");
     fflush(vOrbitFile);
}

/***************************************************************************
 void corstat(double *mean, double *sigma, double *xmax, long lastpos)
 
 Purpose: 
   Compute RMS, mean, max values for correctors
***************************************************************************/

void corstat(double *mean, double *sigma, double *xmax, long lastpos)
{
  long i, j, n[2];
  Vector2 sum, sum2;
  double TEMP;

  for (j = 0; j <= 1; j++) {
    sum[j] = 0.0; sum2[j] = 0.0; xmax[j] = 0.0; n[j] = 0;
  }
  
  for (i = 0; i <= lastpos; i++) {
    if (Cell[i].Fnum == globval.hcorr) {
      j = 1;
      n[j-1]++;
      TEMP = Elem_GetKval(globval.hcorr, n[j-1], (long) Dip);
      sum[j - 1] += TEMP;
      sum2[j - 1] += TEMP * TEMP;
      xmax[j - 1] = max(xmax[j - 1], fabs(TEMP));
    } else if (Cell[i].Fnum == globval.vcorr) {
      j = 2;
      n[j-1]++;
      TEMP = Elem_GetKval(globval.vcorr, n[j-1], (long) (-Dip));
      sum[j - 1] += TEMP;
      sum2[j - 1] += TEMP * TEMP;
      xmax[j - 1] = max(xmax[j - 1], fabs(TEMP));
      }    
  }
  
  for (j = 0; j <= 1; j++) {
    if (n[j] != 0)
      mean[j] = sum[j] / n[j];
    else
      mean[j] = 0.0;
    if (n[j] != 0 && n[j] != 1) {
      TEMP = sum[j];
      sigma[j] = (n[j] * sum2[j] - TEMP * TEMP) / (n[j] * (n[j] - 1.0));
    } else
      sigma[j] = 0.0;
    if (sigma[j] >= 0.0)
      sigma[j] = sqrt(sigma[j]);
    else
      sigma[j] = 0.0;
  }
}
