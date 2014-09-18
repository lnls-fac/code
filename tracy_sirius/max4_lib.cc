/*****************************************************
*        MAX4 specific library                       *  
*                                                    *    
*           S.Leemann                                *  
*                                                    *   
 ****************************************************/   

#include "tracy_lib.h"


//copied here form nsls-ii_lib.cc; needed for LoadFieldErr_scl
char* get_prm_scl(void)
{
  char  *prm;

  prm = strtok(NULL, " \t");
  if ((prm == NULL) || (strcmp(prm, "\r\n") == 0)) {
    printf("get_prm: incorrect format\n");
    exit_(1);
  }

  return prm;
}




//copied here form nsls-ii_lib.cc to add incrementing seed value
void LoadFieldErr_scl(const char *FieldErrorFile, const bool Scale_it,
		      const double Scale, const bool new_rnd, const int m) 
{  
  bool    rms, set_rnd;
  char    line[max_str], name[max_str], type[max_str], *prm;
  int     k, n, seed_val;
  double  Bn, An, r0;
  FILE    *inf;

  const bool  prt = true;

  inf = file_read(FieldErrorFile);

  set_rnd = false; 
  printf("\n");
  while (fgets(line, max_str, inf) != NULL) {
    if (strstr(line, "#") == NULL) {
      // check for whether to set new seed
      sscanf(line, "%s", name); 
      if (strcmp("seed", name) == 0) {
	set_rnd = true;
	sscanf(line, "%*s %d", &seed_val); 
	seed_val += 2*m;
	printf("setting random seed to %d\n", seed_val);
	iniranf(seed_val); 
      } else {
	sscanf(line, "%*s %s %lf", type, &r0);
	printf("%-4s %3s %7.1le", name, type, r0);
	rms = (strcmp("rms", type) == 0)? true : false;
	if (rms && !set_rnd) {
	  printf("LoadFieldErr: seed not defined\n");
	  exit_(1);
	}
	// skip first three parameters
	strtok(line, " \t");
	for (k = 1; k <= 2; k++)
	  strtok(NULL, " \t");
	while (((prm = strtok(NULL, " \t")) != NULL) &&
	       (strcmp(prm, "\r\n") != 0)) {
	  sscanf(prm, "%d", &n);
	  prm = get_prm_scl();
	  sscanf(prm, "%lf", &Bn);
	  prm = get_prm_scl(); 
	  sscanf(prm, "%lf", &An);
	  if (Scale_it)
	    {Bn *= Scale; An *= Scale;}
	  if (prt)
	    printf(" %2d %9.1e %9.1e\n", n, Bn, An);
	  // convert to normalized multipole components
	  SetFieldErrors(name, rms, r0, n, Bn, An, true);
	}
      }
    } else
      printf("%s", line);
  }
 
  fclose(inf);
}




void get_cod_rms_data(const int n_seed, const int nfam, const int fnums[], const double dx, const double dy, const double dr,
		      double x_mean[][6], double x_sigma[][6], double theta_mean[][2], double theta_sigma[][2])
{
  const int  n_elem = globval.Cell_nLoc+1;

  bool       cod;
  long int   j;
  int        i, k, ncorr[2];
  double     x1[n_elem][6], x2[n_elem][6], theta1[n_elem][6], theta2[n_elem][6], a1L, b1L;;

  for (j = 0; j <= globval.Cell_nLoc; j++){
    for (k = 0; k < 6; k++) {
      x1[j][k] = 0.0; x2[j][k] = 0.0;
    }
    for (k = 0; k < 2; k++){
      theta1[j][k] = 0;
      theta2[j][k] = 0;
    }
  }  
   
  for (i = 0; i < n_seed; i++) {
    // reset orbit trims
    set_bn_design_fam(globval.hcorr, Dip, 0.0, 0.0);
    set_bn_design_fam(globval.vcorr, Dip, 0.0, 0.0);

    for (j = 0; j < nfam; j++)
      misalign_rms_fam(fnums[j], dx, dy, dr, true);
    
    cod = orb_corr(3);
    
    if (cod) {
      
      for (k = 0; k < 2; k++)
	ncorr[k] = 0;
      
      for (j = 0; j <= globval.Cell_nLoc; j++){ // read back beam pos at bpm

	if ( Cell[j].Elem.Pkind == Mpole ) {
	  for (k = 0; k < 6; k++) {
	    x1[j][k] += Cell[j].BeamPos[k];
	    x2[j][k] += sqr(Cell[j].BeamPos[k]);
	  }
	  
	  if ( (Cell[j].Fnum == globval.hcorr) || (Cell[j].Fnum == globval.vcorr) ){ // read back corr strength at corr
	    get_bnL_design_elem(Cell[j].Fnum, Cell[j].Knum, Dip, b1L, a1L);
	    if ( Cell[j].Fnum == globval.hcorr ){
	      ncorr[X_]++;
	      theta1[ncorr[X_]-1][X_] += b1L;
	      theta2[ncorr[X_]-1][X_] += sqr(b1L);
	    } else if ( Cell[j].Fnum == globval.vcorr ){
	      ncorr[Y_]++;
	      theta1[ncorr[Y_]-1][Y_] += a1L;
	      theta2[ncorr[Y_]-1][Y_] += sqr(a1L);
	    }
	  }
	}
      }
      
    } else
      printf("orb_corr: failed\n");    
  }
  
  for (k = 0; k < 2; k++)
    ncorr[k] = 0;
  
  for (j = 0; j <= globval.Cell_nLoc; j++){
        
    if ( Cell[j].Elem.Pkind == Mpole ) {
      for (k = 0; k < 6; k++) {
	x_mean[j][k] = x1[j][k]/n_seed;
	x_sigma[j][k] = sqrt((n_seed*x2[j][k]-sqr(x1[j][k]))
			     /(n_seed*(n_seed-1.0)));
      }
      
      if ( Cell[j].Fnum == globval.hcorr ){
	ncorr[X_]++;
	theta_mean[ncorr[X_]-1][X_] = theta1[ncorr[X_]-1][X_]/n_seed;
	theta_sigma[ncorr[X_]-1][X_] = sqrt((n_seed*theta2[ncorr[X_]-1][X_]-sqr(theta1[ncorr[X_]-1][X_]))
					    /(n_seed*(n_seed-1.0)));
	
      } else if ( Cell[j].Fnum == globval.vcorr ){
	ncorr[Y_]++;
	theta_mean[ncorr[Y_]-1][Y_] = theta1[ncorr[Y_]-1][Y_]/n_seed;
	theta_sigma[ncorr[Y_]-1][Y_] = sqrt((n_seed*theta2[ncorr[Y_]-1][Y_]-sqr(theta1[ncorr[Y_]-1][Y_]))
					    /(n_seed*(n_seed-1.0)));
      }
    }
  }
}




void prt_cod_rms_data(const char name[], double x_mean[][6], double x_sigma[][6], double theta_mean[][2], double theta_sigma[][2])
{
  long     j;
  int      k, ncorr[2];
  FILE     *fp;
  struct    tm *newtime;

  fp = file_write(name);


  /* Get time and date */
  newtime = GetTime();

  fprintf(fp,"# TRACY III v.3.5 -- %s -- %s \n",
	  name, asctime2(newtime));
  fprintf(fp,"#         s   name              code  xcod_mean +/-  xcod_rms   ycod_mean +/-  ycod_rms"
	     "   dipx_mean +/-  dipx_sigma dipy_mean +/-  dipy_sigma\n");
  fprintf(fp,"#        [m]                             [mm]           [mm]       [mm]           [mm]"
	     "      [mrad]         [mrad]     [mrad]         [mrad]\n");
  fprintf(fp, "#\n");


  for (k = 0; k < 2; k++)
    ncorr[k] = 0;
  
  for (j = 0; j <= globval.Cell_nLoc; j++){
   
    fprintf(fp, "%4li %8.3f %s %6.2f %10.3e +/- %10.3e %10.3e +/- %10.3e",
	    j, Cell[j].S, Cell[j].Elem.PName, get_code(Cell[j]),
	    1e3*x_mean[j][x_], 1e3*x_sigma[j][x_],
	    1e3*x_mean[j][y_], 1e3*x_sigma[j][y_]);
   
    if ( Cell[j].Fnum == globval.hcorr ){
      ncorr[X_]++;
      fprintf(fp, " %10.3e +/- %10.3e %10.3e +/- %10.3e\n",
	      1e3*theta_mean[ncorr[X_]-1][X_], 1e3*theta_sigma[ncorr[X_]-1][X_], 0.0, 0.0);

    } else if ( Cell[j].Fnum == globval.vcorr ){
      ncorr[Y_]++;
      fprintf(fp, " %10.3e +/- %10.3e %10.3e +/- %10.3e\n",
	      0.0, 0.0, 1e3*theta_mean[ncorr[Y_]-1][Y_], 1e3*theta_sigma[ncorr[Y_]-1][Y_]);
    } else 
      fprintf(fp, " %10.3e +/- %10.3e %10.3e +/- %10.3e\n",
	      0.0, 0.0, 0.0, 0.0);
  }

  fclose(fp);
}




void add_family( const char *name, int &nfam, int fnums[] )
{
  int fnum;
  fnum = ElemIndex(name);
  if (fnum != 0)
    fnums[nfam++] = fnum;
  else {
    printf("Family not defined. %s %d\n", name, fnum);  
    exit(1);
  }
}




//copied here form nsls-ii_lib.cc to make changes
void get_cod_rms_scl(const double dx, const double dy, const double dr,
		     const int n_seed)
{
  const int  n_elem = globval.Cell_nLoc+1;

  int      fnums[25], nfam; 
  double   x_mean[n_elem][6], x_sigma[n_elem][6], theta_mean[n_elem][2], theta_sigma[n_elem][2];

  nfam = 0;
  add_family("qf", nfam, fnums);
  add_family("qfm", nfam, fnums);
  add_family("qfend", nfam, fnums);
  add_family("qdend", nfam, fnums);
  add_family("sfi", nfam, fnums);
  add_family("sfo", nfam, fnums);
  add_family("sfm", nfam, fnums);
  add_family("sd", nfam, fnums);
  add_family("sdend", nfam, fnums);

  get_cod_rms_data(n_seed, nfam, fnums, dx, dy, dr, x_mean, x_sigma, theta_mean, theta_sigma);
  prt_cod_rms_data("cod_rms.out", x_mean, x_sigma, theta_mean, theta_sigma);

}




/////////////////////////////////////////////////////////////////////////////////////////////////




//this is a mashup of get_cod_rms_scl
//instead of assigning errors to families we load and apply AlignErr.dat and FieldErr.dat
//a correction is then applied and the results saved
//this is repeated for n_seed seeds and overall statistics saved in cod_rms.out

void get_cod_rms_scl_new(const int n_seed)
{
     
  const int  n_elem = globval.Cell_nLoc+1;
  
  double     x_mean[n_elem][6], x_sigma[n_elem][6], theta_mean[n_elem][2], theta_sigma[n_elem][2];
  bool       cod;
  long int   j;
  int        i, k, ncorr[2];
  double     x1[n_elem][6], x2[n_elem][6], theta1[n_elem][6], theta2[n_elem][6], a1L, b1L;;
  
    
  
     
  for (j = 0; j <= globval.Cell_nLoc; j++){
    for (k = 0; k < 6; k++) {
      x1[j][k] = 0.0; x2[j][k] = 0.0;
    }
    for (k = 0; k < 2; k++){
      theta1[j][k] = 0;
      theta2[j][k] = 0;
    }
//    printf("1  is one \n");
  }  
  
  
     
  for (i = 0; i < n_seed; i++) {
    
    // reset orbit trims
    set_bn_design_fam(globval.hcorr, Dip, 0.0, 0.0);
    set_bn_design_fam(globval.vcorr, Dip, 0.0, 0.0);
    
    LoadFieldErr_scl("/home/zhang/codes/TracyIII/lattice/FieldErr.dat", false, 1.0, true, i);
    LoadAlignTol("/home/zhang/codes/TracyIII/lattice/AlignErr.dat", false, 1.0, true, i);

    cout << endl << "*** COD ITERATION " << i+1 << " ***" << endl;
   
    cod = orb_corr(3);
    
     
    if (cod) {
      
      for (k = 0; k < 2; k++)
	ncorr[k] = 0;
      
      for (j = 0; j <= globval.Cell_nLoc; j++){ // read back beam pos at bpm
	
	if ( Cell[j].Elem.Pkind == Mpole ) {
	  for (k = 0; k < 6; k++) {
	    x1[j][k] += Cell[j].BeamPos[k];
	    x2[j][k] += sqr(Cell[j].BeamPos[k]);
	  }
	  
	  if ( (Cell[j].Fnum == globval.hcorr) || (Cell[j].Fnum == globval.vcorr) ){ // read back corr strength at corr
	    get_bnL_design_elem(Cell[j].Fnum, Cell[j].Knum, Dip, b1L, a1L);
	    if ( Cell[j].Fnum == globval.hcorr ){
	      ncorr[X_]++;
	      theta1[ncorr[X_]-1][X_] += b1L;
	      theta2[ncorr[X_]-1][X_] += sqr(b1L);
	    } else if ( Cell[j].Fnum == globval.vcorr ){
	      ncorr[Y_]++;
	      theta1[ncorr[Y_]-1][Y_] += a1L;
	      theta2[ncorr[Y_]-1][Y_] += sqr(a1L);
	    }
	  }
	}
      }
      
    } else
      printf("orb_corr: failed\n");    
  }
  
  for (k = 0; k < 2; k++)
    ncorr[k] = 0;
  
  for (j = 0; j <= globval.Cell_nLoc; j++){
    
    if ( Cell[j].Elem.Pkind == Mpole ) {
      for (k = 0; k < 6; k++) {
	x_mean[j][k] = x1[j][k]/n_seed;
	x_sigma[j][k] = sqrt((n_seed*x2[j][k]-sqr(x1[j][k]))
			     /(n_seed*(n_seed-1.0)));
      }
      
      if ( Cell[j].Fnum == globval.hcorr ){
	ncorr[X_]++;
	theta_mean[ncorr[X_]-1][X_] = theta1[ncorr[X_]-1][X_]/n_seed;
	theta_sigma[ncorr[X_]-1][X_] = sqrt((n_seed*theta2[ncorr[X_]-1][X_]-sqr(theta1[ncorr[X_]-1][X_]))
					    /(n_seed*(n_seed-1.0)));
	
      } else if ( Cell[j].Fnum == globval.vcorr ){
	ncorr[Y_]++;
	theta_mean[ncorr[Y_]-1][Y_] = theta1[ncorr[Y_]-1][Y_]/n_seed;
	theta_sigma[ncorr[Y_]-1][Y_] = sqrt((n_seed*theta2[ncorr[Y_]-1][Y_]-sqr(theta1[ncorr[Y_]-1][Y_]))
					    /(n_seed*(n_seed-1.0)));
      }
    }
  }
  
  prt_cod_rms_data("cod_rms.out", x_mean, x_sigma, theta_mean, theta_sigma);
  // this writes the statictics over N seeds to file
  
}




/////////////////////////////////////////////////////////////////////////////////////////////////



// get dynamic aperture and output to file: dynap.out, dynap_dp.out
double get_dynap_scl(const double delta, const int n_track2)
{
  char      str[max_str];
  int       i;
  double    x_aper[n_aper], y_aper[n_aper], DA;
  FILE      *fp;

  const int  prt = true;

  fp = file_write("dynap.out");
  dynap(fp, 5e-3, 0.0, 0.1e-3, n_aper, n_track2, x_aper, y_aper, false, prt);
  fclose(fp);
  DA = get_aper(n_aper, x_aper, y_aper);

  if (true) {
    sprintf(str, "dynap_dp%3.1f.out", 1e2*delta);
    fp = file_write(str);
    dynap(fp, 5e-3, delta, 0.1e-3, n_aper, n_track2,
	  x_aper, y_aper, false, prt);
    fclose(fp);
    DA += get_aper(n_aper, x_aper, y_aper);

    for (i = 0; i < nv_; i++)
      globval.CODvect[i] = 0.0;
    sprintf(str, "dynap_dp%3.1f.out", -1e2*delta);
    fp = file_write(str);
    dynap(fp, 5e-3, -delta, 0.1e-3, n_aper,
	  n_track2, x_aper, y_aper, false, prt);
    fclose(fp);
    DA += get_aper(n_aper, x_aper, y_aper);
  }

  return DA/3.0;
}




/////////////////////////////////////////////////////////////////////////////////////////////////



// get tunes and beta functions
void get_matching_params_scl()
{
  double nux, nuy, betax, betay;
  
  nux = globval.TotalTune[X_];
  nuy = globval.TotalTune[Y_];
  betax = globval.OneTurnMat[0][1]/sin(2*pi*nux);
  betay = globval.OneTurnMat[2][3]/sin(2*pi*nuy);
  
  printf("\n");
  printf("beta_x* = %10.9e\n", betax);
  printf("beta_y* = %10.9e\n", betay);
  printf("\n");
}



