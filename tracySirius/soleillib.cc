
/* Tracy-3

   J. Bengtsson, CBP, LBL      1990 - 1994   Pascal version
                 SLS, PSI      1995 - 1997
   M. Boege      SLS, PSI      1998          C translation
   L. Nadolski   SOLEIL        2002          Link to NAFF, Radia field maps
   J. Bengtsson  NSLS-II, BNL  2004 -
   J. Zhang      SOLEIL        2010         ADD SOLEIL PARTS IN TRACY 2.7
*/


/****************************************************************************/
/* void Get_Disp_dp(void)

   Purpose:
       Get dispersion w/ energy offset

   Input:
       none

   Output:
       none

   Return:
       none

   Global variables:
       trace

   specific functions:
       getcod, Ring_GetTwiss, getelem

   Comments:
       none

****************************************************************************/
void Get_Disp_dp(void)
{
  long i;
//  long lastpos = 0;
  const char nomfic[] = "dispersion.out";
  FILE *outf;
  double dP = 0e0;
  CellType Cell;
  long lastpos =0L;

  if (trace) fprintf(stdout,"Entering Get_Disp_dp function ...\n");

  if ((outf = fopen(nomfic, "w")) == NULL)
  {
    fprintf(stdout, "Get_Disp_dp: Error while opening file %s\n",nomfic);
    exit_(1);
  }

  for (i = 1; i <= 20; i++) {
    dP = -0.003 + 1e-6 + i*0.0006;
    getcod(dP, lastpos);
    Ring_GetTwiss(true, dP);  /* Compute and get Twiss parameters */
    getelem(0, &Cell);
    fprintf(outf,"%+e %+e %+e\n", dP, Cell.BeamPos[0], Cell.Eta[0]);
  }

  fclose(outf);
}

/****************************************************************************/
/* void InducedAmplitude(long spos)

   Purpose:
      Compute the induced amplitude for a particle getting for a energy offset dP
        process similar to a Touschek scattering
        The induced amplitude is transported to the first element of the lattice
        by scaling the maplitude with energy dependent betafunctions

   Input:
       spos : position where Touschek scattering occurs

   Output:
       amp_ind.out

   Return:
       none

   Global variables:
       none

   specific functions:
       none

   Comments:
       none

****************************************************************************/
void InducedAmplitude(long spos)
{
  Vector        x1;     /* tracking coordinates */
  long          i = 0L, k = 0L, imax = 50;
  FILE *        outf;
  double        dP = 0.0, dP20 = 0.0, dpmax = 0.06;
  Vector2       amp = {0.0, 0.0}, H = {0.0, 0.0};
  const char    nomfic[] = "amp_ind.out";
  long          lastpos = 0;
  CellType      Celldebut, Cell;
  Vector        codvector[Cell_nLocMax];

  globval.Cavity_on  = false;    /* Cavity on/off */
  globval.radiation  = false;    /* radiation on/off */

  /* Ouverture fichier moustache */
  if ((outf = fopen(nomfic, "w")) == NULL)
  {
    fprintf(stdout, "Error when open filename %s\n",nomfic);
    exit_(1);
  }

  fprintf(outf, "# Induced amplitude transported at lattice entrance\n");
  fprintf(outf, "#    dp           xind         zind       "
                     " Betax(entrance) Betaz(entrance)       Betax         betaz"
                     "       Hx(delta)/delta^2    Hz(delta)/delta^2    "
                     " Hx(delta)  Hz(delta)      etax(delta)        etaxp(delta)\n#\n");


  lastpos = 1;

  for (k = 0; k <= imax ; k++)  {
    dP = -dpmax + 2*dpmax*k/imax;
    /* Coordonnees initiales */
    x1[0] = 0.0; x1[1] = 0.0;
    x1[2] = 0.0; x1[3] = 0.0;
    x1[4] = dP ; x1[5] = 0.0;

    /* Computes closed orbit and store it in a vector */
    set_vectorcod(codvector, dP) ;
    Ring_GetTwiss(false, dP);  /* Compute and get Twiss parameters */
    getelem(1L, &Celldebut);
    getelem(spos, &Cell);

    /* compute H at s =spos */
    dP20 = ((dP == 0) ? 1.0 : dP*dP);
    i = 0; /* Horizontal */
    H[i] = ((1.0+Cell.Alpha[i]*Cell.Alpha[i])/Cell.Beta[i]*codvector[spos][0]*codvector[spos][0]+
            2.0*Cell.Alpha[i]*codvector[spos][0]*codvector[spos][1]+
            Cell.Beta[i]*codvector[spos][1]*codvector[spos][1])/dP20;
    i = 1; /* Vertical */
    H[i] = ((1.0+Cell.Alpha[i]*Cell.Alpha[i])/Cell.Beta[i]*codvector[spos][2]*codvector[spos][2]+
            2.0*Cell.Alpha[i]*codvector[spos][2]*codvector[spos][3]+
            Cell.Beta[i]*codvector[spos][3]*codvector[spos][3])/dP20;

    amp[0] = codvector[spos][0]*sqrt(Celldebut.Beta[0]/Cell.Beta[0]);
    amp[1] = codvector[spos][1];

    fprintf(outf, "%+10.5e %+10.5e %+10.5e %+10.5e %+10.5e %+10.5e %+10.5e "
                  "%+10.5e %+10.5e %+10.5e %+10.5e %+10.5e %+10.5e \n",
                  dP, codvector[spos][0], codvector[spos][1],
                  Celldebut.Beta[0], Celldebut.Beta[1], Cell.Beta[0], Cell.Beta[1],
                  H[0], H[1], H[0]*dP20, H[1]*dP20, Cell.Eta[0], Cell.Etap[0]);
    }
  fclose(outf);
}

/****************************************************************************/
/* void Hfonction(long pos, double dP)

   Purpose:
     Compute the Hfunction at position pos for the energy offset dP
     H is wrong at large dp since eta and eta' are computed
       by numerical differentiation, which means that
       eta(dp) = eta0 + eta2*dp*dp + O(4) instead of
       eta(dp) = eta0 + eta1*dp + eta2*dp*dp + O(3)

     A solution is to compute eta from the closed orbit by:
       xco(dp) = eta(dp)*dp => eta(dp) = xco(dp)/dp
       WARNING: this definition is true only if the lattice
       is perfect.
       Indeed in general : xco = eta(dp)*dp + x0(defaults)

   Input:
       pos:    element index in the lattice.

   Output:
       none

   Return:
       none

   Global variables:
       none

   specific functions:
       Ring_GetTwiss
       getelem

   Comments:
       none

****************************************************************************/

//void Hfonction(long pos, double dP,Vector2 H)
void Hfonction(long pos, double dP)
{
  CellType Cell;
  long i;
Vector2 H;

  Ring_GetTwiss(true, dP); /* Compute and get Twiss parameters */
  getelem(pos, &Cell);    /* Position of the element pos */

  i = 0; /* Horizontal */
  H[i] = (1+Cell.Alpha[i]*Cell.Alpha[i])/Cell.Beta[i]*Cell.Eta[i]*Cell.Eta[i]+
          2*Cell.Alpha[i]*Cell.Eta[i]*Cell.Etap[i]+
          Cell.Beta[i]*Cell.Etap[i]*Cell.Etap[i];
  i = 1; /* Vertical */
  H[i] = (1+Cell.Alpha[i]*Cell.Alpha[i])/Cell.Beta[i]*Cell.Eta[i]*Cell.Eta[i]+
          2*Cell.Alpha[i]*Cell.BeamPos[i]*Cell.Etap[i]+
    Cell.Beta[i]*Cell.Etap[i]*Cell.Etap[i];
}

/****************************************************************************/
/* void Hcofonction(long pos, double dP)

   Purpose:
       Compute the true Hfunction defined by the chromatic closed orbit
       at position pos and for a energy offset dP

       For a givien delta
       H = gamma xcod� + 2*alpha*xcod*xcod' + beta*xcod'*xcod'

   Input:
       none

   Output:
       none

   Return:
       none

   Global variables:
       none

   specific functions:
       getcod
       Ring_GetTwiss
       getelem

   Comments:
       Bug: Cell.BeamPos does not give closed orbit !!!

****************************************************************************/
//void Hcofonction(long pos, double dP,Vector2 H)
void Hcofonction(long pos, double dP)
{
  CellType Cell;
  long i;
  long lastpos = 1L;
  Vector2 H;
  getcod(dP, lastpos);   /* determine closed orbit */

  if (lastpos != globval.Cell_nLoc) printf("Ring unstable for dp=%+e @ pos=%ld\n", dP, lastpos);

  Ring_GetTwiss(true, dP); /* Compute and get Twiss parameters */
  getelem(pos, &Cell);    /* Position of the element pos */

  i = 0; /* Horizontal */
  H[i] = (1+Cell.Alpha[i]*Cell.Alpha[i])/Cell.Beta[i]*Cell.BeamPos[i]*Cell.BeamPos[i]+
          2*Cell.Alpha[i]*Cell.BeamPos[i]*Cell.BeamPos[i+1]+
          Cell.Beta[i]*Cell.BeamPos[i+1]*Cell.BeamPos[i+1];
  i = 1; /* Vertical */
  H[i] = (1+Cell.Alpha[i]*Cell.Alpha[i])/Cell.Beta[i]*Cell.BeamPos[i+1]*Cell.BeamPos[i+1]+
          2*Cell.Alpha[i]*Cell.BeamPos[i+1]*Cell.BeamPos[i+2]+
          Cell.Beta[i]*Cell.BeamPos[i+2]*Cell.BeamPos[i+2];
  fprintf(stdout,"H[0]=%10.6f,H[1]=%10.6f\n",H[0],H[1]);
}


/****************************************************************************/
/* void SetErr(long seed,double fac)

   Purpose:
       Set error
       Definir une distribution aleatoire de quadripoles tournes associee a chaque
       quadripole de la machine
       Distribution gaussienne d'ecart type fac et coupe a normcut*sigma
       This function works for the lattice with full quadrupoles

   Input:
       seed: random seed number
       fac :  RMS value of the rotation angle of the quadrupole
   Output:
       none

   Return:
       none

   Global variables:
       globval
       HOMmax

   specific functions:
       setrandcut, initranf
       getelem, putelem
       Mpole_SetPB

   Comments:
       Only valid if quad split into two part (cf pair variable)
       Rotation inversion to do as in BETA code
       Test if normal quad sin(theta) = 0. Do not work if tilt error

       Modified by Jianfeng Zhang 19/01/2011 @soleil

****************************************************************************/
void SetErr(long seed,double fac)
{
  double  normcut = 0.0;
  long    i = 0L;
 // CellType Cell;
  double theta = 0.0;
  bool prt=false;


  if(!prt){
    printf("\n");
    printf(" Setting random rotation errors to quadrupole magnets:\n");
    printf("   random seed number is: %ld, rms value of the rotation error is: %lf rad\n",seed,fac);
  }

  setrancut(normcut=2L);
  iniranf(seed);

  for (i = 1L; i <= globval.Cell_nLoc; i++)
  {
    if (Cell[i].Elem.Pkind == Mpole)
    {
      if (Cell[i].Elem.M->n_design == 2L && Cell[i].dT[1] == 0) //Quads but exclude skew quads
      {
        theta = fac*normranf(); /* random error every 2 elements (quad split into 2) */
        Cell[i].Elem.M->PBpar[HOMmax-2L] = -Cell[i].Elem.M->PBpar[HOMmax+2L]*sin(2.0*theta);
        Cell[i].Elem.M->PBpar[HOMmax+2L] =  Cell[i].Elem.M->PBpar[HOMmax+2L]*cos(2.0*theta);
        if (trace) printf("%6s % .5e % .5e % .5e\n",Cell[i].Elem.PName,
                           Cell[i].Elem.M->PBpar[HOMmax-2L], Cell[i].Elem.M->PBpar[HOMmax+2L],theta);

        Mpole_SetPB(Cell[i].Fnum, Cell[i].Knum, -2L);
        Mpole_SetPB(Cell[i].Fnum, Cell[i].Knum, 2L);
      }
    }
  }
}

/****************************************************************************/
/* void SetErr2(long seed,double fac)

   Purpose:
       Set error
       Definir une distribution aleatoire de quadripoles tournes associee a chaque
       quadripole de la machine
       Distribution gaussienne d'ecart type fac et coupe a normcut*sigma
       This function works for the lattice with two half quadrupoles

   Input:
       seed: random seed number
       fac :  RMS value of the rotation angle of the quadrupole
   Output:
       none

   Return:
       none

   Global variables:
       globval
       HOMmax

   specific functions:
       setrandcut, initranf
       getelem, putelem
       Mpole_SetPB

   Comments:
       Only valid if quad split into two part (cf pair variable)
       Rotation inversion to do as in BETA code
       Test if normal quad sin(theta) = 0. Do not work if tilt error


****************************************************************************/
void SetErr2(long seed,double fac)
{
  double  normcut = 0.0;
  long    i = 0L;
 // CellType Cell;
  double theta = 0.0;
  int pair = 0;
  bool prt=false;


  if(!prt){
    printf("\n");
    printf(" Setting random rotation errors to quadrupole magnets:\n");
    printf("   random seed number is: %ld, rms value of the rotation error is: %lf rad\n",seed,fac);
  }

  setrancut(normcut=2L);
  iniranf(seed);

  for (i = 1L; i <= globval.Cell_nLoc; i++)
  {
    if (Cell[i].Elem.Pkind == Mpole)
    {
      if (Cell[i].Elem.M->n_design == 2L && Cell[i].dT[1] == 0) // exclude skew quads
      {
        if ((pair%2)==0) theta = fac*normranf(); /* random error every 2 elements (quad split into 2) */
        pair++;
        Cell[i].Elem.M->PBpar[HOMmax-2L] = -Cell[i].Elem.M->PBpar[HOMmax+2L]*sin(2.0*theta);
        Cell[i].Elem.M->PBpar[HOMmax+2L] =  Cell[i].Elem.M->PBpar[HOMmax+2L]*cos(2.0*theta);
        if (!trace) printf("%6s % .5e % .5e % .5e\n",Cell[i].Elem.PName,
                           Cell[i].Elem.M->PBpar[HOMmax-2L], Cell[i].Elem.M->PBpar[HOMmax+2L],theta);

        Mpole_SetPB(Cell[i].Fnum, Cell[i].Knum, -2L);
        Mpole_SetPB(Cell[i].Fnum, Cell[i].Knum, 2L);
      }
    }
  }
}

/****************************************************************************/
/* void ReadCh(Const char *AperFile)

   Purpose:  read and set the definition of the vacuum chamber
             between different sections around the ring from file
	     AperFile.dat.

	     In AperFile.dat,
	       1) line begin with "#" is comment line
	       2) first line Name1: Start
	          first line Name2: All
	       3) MK1 and MK2 should be unique in the lattice
	       4) MK1 is defined before MK2 in the lattice
	       5)
	         MK1:  marker before the start element of the section for the aperture
	         Mk2:  marker after the end element of the section for the aperture
	       dxmin:   minimum x value of vacuum chamber
	       dxmax:   maxmum x value of vacuum chamber
	       dymin:   minimum y value of vacuum chamber
	       dymax:   maxmum y value of vacuum chamber



   Input:
       none

   Output:
       none

   Return:
       none

   Global variables:
       globval

   specific functions:
       none

   Comments:
       See also LoadApers in nsrl-ii.cc
       J.Zhang 07/10 soleil
****************************************************************************/
void ReadCh(const char *AperFile)
{
 char    in[max_str], Name1[max_str], Name2[max_str];
 char    *line;
  int     Fnum1=0, Fnum2=0, Kidnum1=0, Kidnum2=0, k1=0, k2=0;
  int     i=0, LineNum=0;
  double  dxmin=0.0, dxmax=0.0, dymin=0.0, dymax=0.0;  // min and max x and apertures
  FILE    *fp;
  bool  prt = false;

  fp = file_read(AperFile);

  printf("\n");
  printf("Loading and setting vacuum apertures to lattice elements...\n");

  while (line=fgets(in, max_str, fp)) {
  /* kill preceding whitespace generated by "table" key
        or "space" key, but leave \n
        so we're guaranteed to have something*/
     while(*line == ' ' || *line == '\t') {
       line++;
     }
    /* count the line number that has been read*/
    LineNum++;
    /* NOT read comment line or blank line with the end of line symbol '\n','\r' or '\r\n'*/
    if (strstr(line, "#") == NULL && strcmp(line,"\n") != 0 &&
        strcmp(line,"\r") != 0 &&strcmp(line,"\r\n") != 0)
    /* read the aperture setting */
    {
      sscanf(line,"%s %s %lf %lf %lf %lf",
	     Name1,Name2, &dxmin, &dxmax, &dymin, &dymax);

      if (strcmp("Start", Name1)==0 && strcmp("All", Name2)==0) {
	if(prt)
	  printf("setting all apertures to \n"
		 " dxmin = %e, dxmax = %e, dymin = %e, dymax = %e\n",
		 dxmin, dxmax, dymin, dymax);
	set_aper_type(All, dxmin, dxmax, dymin, dymax);
	//	ini_aper(dxmin, dxmax, dymin, dymax);
       }

      else {
        /* read the vacuum chamber between section */
    	  Fnum1 = ElemIndex(Name1);
	Fnum2 = ElemIndex(Name2);
	if(Fnum1>0 && Fnum2>0) {
	  /* if element Name1 is defined before element Name2, give error message*/
	  if(Fnum1 > Fnum2){
	    printf("\nReadCh(): \n"
	           "          aperture file, Line %d, Element %s should be defined after Element %s \n",
	            LineNum,Name1,Name2);
            exit_(1);
          }
	  /* if the element is not unique in the lattice, give error message*/
	  Kidnum1 = GetnKid(Fnum1);
	  Kidnum2 = GetnKid(Fnum2);
	  if(Kidnum1 > 1 || Kidnum2 >1){
	   printf("\nReadCh(): \n"
	          "          aperture file, Line %d, Element %s or Element %s is not unique in lattice \n",
	            LineNum,Name1,Name2);
            exit_(1);
	  }

	  if(prt)
	    printf("setting apertures to section:\n"
		   "  %s  %s dxmin = %e, dxmax = %e, dymin = %e, dymax = %e\n",
		   Name1, Name2, dxmin, dxmax, dymin, dymax);
	/* find the start and end index of the section*/
	  k1 = Elem_GetPos(Fnum1, 1);
	  k2 = Elem_GetPos(Fnum2, 1);
	/* set the vacuum chamber*/
	//read the marker before the first element, and the markder after the last elment
	  for(i=1; i<globval.Cell_nLoc; i++){
	    if(i>=k1 && i<k2){
	      Cell[i].maxampl[X_][0] = dxmin;
	      Cell[i].maxampl[X_][1] = dxmax;
	      Cell[i].maxampl[Y_][0] = dymin;
	      Cell[i].maxampl[Y_][1] = dymax;
	    }
	  }
	}
	else {
	  printf("\nReadCh(): \n"
	         "          aperture file, Line %d, lattice does not contain section between element %s and element %s\n",
	          LineNum,Name1, Name2);
	  exit_(1);
	  }
      }

    }
 //  else /* print the comment line */
 //     printf("%s", line);
  }
  fclose(fp);
  // turn on the global flag for CheckAmpl()
  globval.Aperture_on = true;

}

/****************************************************************************/
/* void Trac_Tab(double x, double px, double y, double py, double dp,
 long nmax, long pos, long *lastn, long *lastpos, FILE *outf1, double Tx[][NTURN])

   Purpose:
       Single particle tracking over NTURN turns
       The 6D phase trajectory is saved in a array

   Input:
       x, px, y, py 4 transverses coordinates
       dp           energy offset
       nmax         number of turns
       pos          starting position for tracking
       aperture     global physical aperture

   Output:
      lastn         last n (should be nmax if  not lost)
      lastpos       last position in the ring
      Tx            6xNTURN matrix of phase trajectory

   Return:
       none

   Global variables:
       NTURN number of turn for tracking
       globval

   specific functions:
       Cell_Pass

   Comments:
       useful for connection with NAFF

****************************************************************************/
void Trac_Tab(double x, double px, double y, double py, double dp,
	      long nmax, long pos, long &lastn, long &lastpos, FILE *outf1,
	      double Tx[][NTURN])
{
  bool lostF = true; /* Lost particle Flag */
  Vector x1;            /* tracking coordinates */
  long i;
  Vector2  aperture;
  aperture[0] = 1e0; aperture[1] = 1e0;

  x1[0] =  x; x1[1] = px;
  x1[2] =  y; x1[3] = py;
  x1[4] = dp; x1[5] = 0.0;

  lastn = 0;
  (lastpos)=pos;

  Cell_Pass(pos, globval.Cell_nLoc, x1, lastpos);
//Cell_Pass(pos -1, globval.Cell_nLoc, x1, lastpos);
  if(trace) fprintf(outf1, "\n");

  do {
    (lastn)++;
    if ((lastpos == globval.Cell_nLoc) &&
        (fabs(x1[0]) < aperture[0]) && (fabs(x1[2]) < aperture[1]))
     /* tracking entre debut anneau et element */
    {
     Cell_Pass(0,globval.Cell_nLoc, x1, lastpos);
     if(trace) fprintf(outf1, "%6ld %+10.5e %+10.5e %+10.5e %+10.5e"
		       " %+10.5e %+10.5e \n",
		       lastn, x1[0], x1[1], x1[2], x1[3], x1[4], x1[5]);
     i = (lastn)-1;
     Tx[0][i] = x1[0]; Tx[1][i] = x1[1];
     Tx[2][i] = x1[2]; Tx[3][i] = x1[3];
     Tx[4][i] = x1[4]; Tx[5][i] = x1[5];

    }
    else  {
      printf("Trac_Tab: Particle lost \n");
      fprintf(stdout, "%6ld %+10.5g %+10.5g %+10.5g"
	              " %+10.5g %+10.5g %+10.5g \n",
	              lastn, x1[0], x1[1], x1[2], x1[3], x1[4], x1[5]);
      lostF = false;
    }
   }
   while (((lastn) < nmax) && ((lastpos) == globval.Cell_nLoc) && (lostF == true));


   for (i = 1; i < nmax; i++) {
     fprintf(outf1, "%6ld %+10.5e %+10.5e %+10.5e %+10.5e %+10.5e %+10.5e \n", i,
                     Tx[0][i], Tx[1][i], Tx[2][i], Tx[3][i], Tx[4][i], Tx[5][i]);
   }
}



/****************************************************************************/
/* void TunesShiftWithAmplitude(long Nbx, long Nbz, long Nbtour, double xmax, double zmax,
               double energy)

   Purpose:
       Compute nux, nuz with respect to x : nudx.out   if xmax!=0
                        with respect to z : nudz.out   if zmax!=0
               for an energy offset delta=energy
               over Nbtour turns of the ring
               for x varying within [-xmax, xmax] around the closed orbit
               for z varying within [-zmax, zmax] around the closed orbit

   Input:
       Nbx    horizontal point number
       Nbz    vertical point number
       Nbtour turn number
       xmax   maximum horizontal amplitude
       zmax   maximum vertical amplitude
       energy enrgy offset

   Output:
       none

   Return:
       none

   Global variables:
       none

   Specific functions:
       Trac_Simple, Get_NAFF

   Comments:
       16/01/03 add test for non zero frequency
                add variation around the closed orbit

****************************************************************************/
#define nterm  4
void TunesShiftWithAmplitude(long Nbx, long Nbz, long Nbtour, double xmax, double zmax,
               double energy)
{
  FILE * outf;
  const char ficx[] = "nudx.out";
  const char ficz[] = "nudz.out";
  int i = 0;
  double Tab[6][NTURN], fx[nterm], fz[nterm];
  double x = 0.0 , xp = 0.0 , z = 0.0 , zp = 0.0;
  double x0 = 1e-6, xp0= 0.0 , z0 = 1e-6, zp0 = 0.0;
  double xstep = 0.0, zstep = 0.0;
  double nux = 0.0, nuz = 0.0;
  int nb_freq[2] = {0, 0};
  bool stable = true;
  struct tm *newtime;

  /* Get time and date */
  newtime = GetTime();

    if (!trace) printf("\n Entering TunesShiftWithAmplitude ... results in nudx.out\n\n");

    /////////////
    // H tuneshift
    /////////////

  if (fabs(xmax) > 0.0){

    /* Opening file */
    if ((outf = fopen(ficx, "w")) == NULL) {
      fprintf(stdout, "NuDx: error while opening file %s\n", ficx);
      exit_(1);
    }

    fprintf(outf,"# Tracy III -- %s -- %s \n", ficx, asctime2(newtime));
    fprintf(outf,"# nu = f(x) \n");
    fprintf(outf,"#    x[m]          z[m]           fx            fz \n");

    if ((Nbx <= 1) || (Nbz <= 1))
      fprintf(stdout,"NuDx: Error Nbx=%ld Nbz=%ld\n",Nbx,Nbz);

    xstep = xmax/Nbx*2.0;
    x0 = 1e-6 - xmax;
    z0 = 1e-3;

    for (i = 0; i <= Nbx; i++) {
      x  = x0 + i*xstep ;
      xp = xp0 ;
      z  = z0  ;
      zp = zp0 ;

      Trac_Simple4DCOD(x,xp,z,zp,energy,0.0,Nbtour,Tab,&stable); // tracking around closed orbit
      if (stable) {
        Get_NAFF(nterm, Nbtour, Tab, fx, fz, nb_freq); // gets frequency vectors
        Get_freq(fx,fz,&nux,&nuz);  // gets nux and nuz
      }

      else { // unstable
        nux = 0.0; nuz = 0.0;

      }
      fprintf(outf,"% 10.6e % 10.6e % 10.6e % 10.6e\n",
                    x, z, nux, nuz);
    }
    fclose(outf);
  }

    /////////////
    // V tuneshift
    /////////////

  if (fabs(zmax) > 0.0)
  {
    /* Opening file */
    if ((outf = fopen(ficz, "w")) == NULL) {
      fprintf(stdout, "NuDx: error while opening file %s\n", ficz);
      exit_(1);
    }

    fprintf(outf,"# tracy III -- %s -- %s \n", ficz, asctime2(newtime));
    fprintf(outf,"# nu = f(z) \n");
    fprintf(outf,"#    x[mm]         z[mm]          fx            fz \n");

    zstep = zmax/Nbz*2.0;
    x0 = 1e-3;
    z0 = 1e-6 - zmax;
    for (i = 0; i <= Nbz; i++) {
      x  = x0 ;
      xp = xp0;
      z  = z0 + i*zstep;
      zp = zp0;

      Trac_Simple4DCOD(x,xp,z,zp,energy,0.0,Nbtour,Tab,&stable);
      if (stable) {
        Get_NAFF(nterm, Nbtour, Tab, fx, fz, nb_freq);
        Get_freq(fx,fz,&nux,&nuz);  // gets nux and nuz
      }
      else {
        nux = 0.0; nuz =0.0;
      }
      fprintf(outf,"% 10.6e % 10.6e % 10.6e % 10.6e\n",
                    x, z, nux, nuz);
    }

    fclose(outf);
  }
}
#undef nterm


double get_D(const double df_x, const double df_y)
{
  double  D;

  const double D_min = -2.0, D_max = -10.0;

  if ((df_x != 0.0) || (df_y != 0.0))
    D = log(sqrt(pow(df_x, 2)+pow(df_y, 2)))/log(10.0);
  else
    D = D_min;

  return max(D, D_max);
}


/****************************************************************************/
/* void fmap(long Nbx, long Nbz, long Nbtour, double xmax, double zmax,
   double energy, bool diffusion, bool matlab)

   Purpose:
       Compute a frequency map of Nbx x Nbz points
       For each set of initial conditions the particle is tracked over
       Nbtour for an energy offset dp

       Frequency map is based on fixed beam energy, trace x versus z,
       or, tracking transverse dynamic aperture for fixed momentum
       (usually, on-momentum) particle.

       The stepsize follows a square root law

       Results in fmap.out

   Input:
       Nbx    horizontal step number
       Nby    vertical step number
       xmax   horizontal maximum amplitude
       zmax   vertical maximum amplitude
       Nbtour number of turn for tracking
       energy particle energy offset
       matlab  set file print format for matlab post-process; specific for nsrl-ii

   Output:
       status true if stable
              false otherwise

   Return:
       none

   Global variables:
       none

   Specific functions:
       Trac_Simple, Get_NAFF

   Comments:
       15/10/03 run for the diffusion: nasty patch for retrieving the closed orbit
       16/02/03 patch removed

****************************************************************************/
#define NTERM2  10
void fmap(long Nbx, long Nbz, long Nbtour, double x0, double xmax,
		  double z0, double zmax, double energy, bool diffusion)
{
	FILE * outf;
	const char fic[] = "fmap.out";
	long i = 0L, j = 0L;
	double Tab[DIM][NTURN], Tab0[DIM][NTURN];
	double fx[NTERM2], fz[NTERM2], fx2[NTERM2], fz2[NTERM2], dfx, dfz;
	double x = 0.0, xp = 0.0, z = 0.0, zp = 0.0;
	double xp0 = 0.0, zp0 = 0.0;
	const double ctau = 0.0;
	double xstep = 0.0, zstep = 0.0, pos;
	double nux1 = 0.0, nuz1 = 0.0, nux2 = 0.0, nuz2 = 0.0;
	int nstable, nb_freq[2] = {0, 0};
	long nturn = Nbtour;
	bool stopcal, status = true;
	struct tm *newtime;

	/* Get time and date */
	time_t aclock;
	time(&aclock);                 /* Get time in seconds */
	newtime = localtime(&aclock);  /* Convert time to struct */

	if (trace) printf("Entering fmap ... results in %s\n\n",fic);

	/* Opening file */
	if ((outf = fopen(fic, "w")) == NULL) {
		fprintf(stdout, "fmap: error while opening file %s\n", fic);
		exit_(1);
	}

	fprintf(outf,"# TRACY III SYNCHROTRON LNLS-- %s -- %s \n", fic, asctime2(newtime));
	fprintf(outf,"# nu = f(x) \n");
	// fprintf(outf,"#    x[mm]          z[mm]           fx             fz"
	//	 "            dfx            dfz      D=log_10(sqrt(df_x^2+df_y^2))\n");
	//
	fprintf(outf,"#    x[m]          z[m]           fx             fz"
			"            dfx            dfz\n");


	if ((Nbx < 1) || (Nbz < 1)) // <=
		fprintf(stdout,"fmap: Error Nbx=%ld Nbz=%ld\n",Nbx,Nbz);


	xp = xp0;
	zp = zp0;

	// steps in both planes
	xstep = (xmax-x0)/((double)Nbx);
	zstep = (zmax-z0)/((double)Nbz);

	if (diffusion){ nturn = 2*Nbtour;}

	// Tracking part + NAFF
	for (i = 1; i <= Nbx; i++) {
		x  = 1e-6 + x0 + ((double)i)*xstep;

		fprintf(stdout,"\n");
		for (j = 0; j<= Nbz; j++) {

			z  =1e-6 + z0 + ((double)(Nbz-j))*zstep;

			if (!globval.Cavity_on)
				Trac_Simple4DCOD(x,xp,z,zp,energy,ctau,nturn,Tab,&status);
			else
				Trac_Simple6DCOD(x,xp,z,zp,energy,ctau,nturn,Tab,&status);

			if (status) { // if trajectory is stable
				// gets frequency vectors
				Get_NAFF(NTERM2, Nbtour, Tab, fx, fz, nb_freq);
				Get_freq(fx,fz,&nux1,&nuz1);  // gets nux and nuz
				if (diffusion){
					Get_Tabshift(Tab,Tab0,Nbtour,Nbtour);
					// gets frequency vectors
					Get_NAFF(NTERM2, Nbtour, Tab0, fx2, fz2, nb_freq);
					Get_freq(fx2,fz2,&nux2,&nuz2); // gets nux and nuz
				}
			} // unstable trajectory
			else { //zeroing output
				nux1 = 0.0; nuz1 = 0.0;
				nux2 = 0.0; nuz2 = 0.0;
			}
			if(diffusion){
				dfx = nux1 - nux2; dfz = nuz1 - nuz2;
				fprintf(outf,"%10.6e %10.6e %10.6e %10.6e %10.6e %10.6e\n",
						x, z, nux1, nuz1, dfx, dfz);
				fprintf(stdout,"%14.6e %14.6e %14.6e %14.6e %14.6e %14.6e\n",
						x, z, nux1, nuz1, dfx, dfz);
			}else{
				// printout value
				fprintf(outf,"%10.6e %10.6e %10.6e %10.6e\n",
						x, z, nux1, nuz1);
				fprintf(stdout,"%14.6e %14.6e %14.6e %14.6e\n",
						x, z, nux1, nuz1);
			}
		}
	}

	fclose(outf);
}


/****************************************************************************/
/* void fmapdp(long Nbx, long Nbe, long Nbtour, double xmax, double emax,
   double z, bool *status)

   Purpose:
       Compute a frequency map of Nbx x Nbz points
       For each set of initial conditions the particle is tracked over
       Nbtour for an energy offset dp

       Frequency map is based on fixed vertical amplitude z, trace x versus energy,
       or, tracking x for off-momentum particle.

       The stepsize follows a square root law

       Results in fmapdp.out

   Input:
       Nbx              horizontal step number
       Nbe              energy step number
       Nbtour           number of turns for tracking
       xmax             horizontal maximum amplitude
       emax             maximum energy
       z                vertical amplitude
       diffusion        flag to calculate tune diffusion
       matlab  set file print format for matlab post-process; specific for nsrl-ii
   Output:
       status true if stable
              false otherwise

   Return:
       none

   Global variables:
       none

   Specific functions:
       Trac_Simple, Get_NAFF

   Comments:
       15/10/03 run for the diffusion: nasty patch for retrieving the closed orbit
       23/10/04 for 6D turn off diffusion automatically and horizontal amplitude
       is negative for negative energy offset since this is true for the cod

****************************************************************************/

void fmapdp(long Nbx, long Nbe, long Nbtour, double x0, double xmax,
		double emin, double emax, double z, bool diffusion)
{
	FILE * outf;
	const char fic[] = "fmapdp.out";
	long i = 0L, j = 0L;
	double Tab[DIM][NTURN], Tab0[DIM][NTURN];
	double fx[NTERM2], fz[NTERM2], fx2[NTERM2], fz2[NTERM2], dfx, dfz;
	double x = 0.0, xp = 0.0, zp = 0.0, dp = 0.0, ctau = 0.0;
	double xp0 = 0.0, zp0 = 0.0, pos =0.0;
	double xstep = 0.0, estep = 0.0;
	double nux1 = 0.0, nuz1 = 0.0, nux2 = 0.0, nuz2 = 0.0;

	int nb_freq[2] = {0, 0}, nstable;
	long nturn = Nbtour;
	bool status=true, stopcal;
	struct tm *newtime;

	/* Get time and date */
	time_t aclock;
	time(&aclock);                 /* Get time in seconds */
	newtime = localtime(&aclock);  /* Convert time to struct */

	if (trace) printf("Entering fmap ... results in %s\n\n",fic);

	/* Opening file */
	if ((outf = fopen(fic, "w")) == NULL) {
		fprintf(stdout, "fmap: error while opening file %s\n", fic);
		exit_(1);
	}

	fprintf(outf,"# TRACY III SYNCHROTRON LNLS-- %s -- %s \n", fic, asctime2(newtime));
	fprintf(outf,"# nu = f(x) \n");
	fprintf(outf,"#    dp[%%]         x[mm]          fx            fz           dfx           dfz\n");


	if ((Nbx < 1) || (Nbe < 1)) //<=
		fprintf(stdout,"fmap: Error Nbx=%ld Nbe=%ld\n",Nbx,Nbe);


	xp = xp0;
	zp = zp0;

	// IF 6D Tracking diffusion turn off
	if (globval.Cavity_on == true) 	diffusion = false;
	if (diffusion) nturn = 2*Nbtour;

	xstep = (xmax-x0)/((double)Nbx);
	estep = (emax-emin)/Nbe;

	for (i = 0; i <= Nbe; i++) {
		dp  = emin + i*estep;

		fprintf(stdout,"\n");
		for (j = 1; j<= Nbx; j++)
		{
			x  = 1e-6 + x0 + ((double)j)*xstep;

			if (!globval.Cavity_on)
				Trac_Simple4DCOD(x,xp,z,zp,dp,ctau,nturn,Tab,&status);
			else
				Trac_Simple6DCOD(x,xp,z,zp,dp,ctau,nturn,Tab,&status);

			if (status) {
				Get_NAFF(NTERM2, Nbtour, Tab, fx, fz, nb_freq);
				Get_freq(fx,fz,&nux1,&nuz1);  // gets nux and nuz
				if (diffusion){
					Get_Tabshift(Tab,Tab0,Nbtour,Nbtour); // shift data for second round NAFF
					Get_NAFF(NTERM2, Nbtour, Tab0, fx2, fz2, nb_freq); // gets frequency vectors
					Get_freq(fx2,fz2,&nux2,&nuz2);// gets nux and nuz
				}
			} // unstable trajectory
			else { //zeroing output
				nux1 = 0.0; nuz1 = 0.0;
				nux2 = 0.0; nuz2 = 0.0;
			}

			// printout value
			dfx = nux2 - nux1; dfz = nuz2 - nuz1;
			if (diffusion) {
				fprintf(outf,"% 10.6e % 10.6e % 10.6e % 10.6e % 10.6e % 10.6e\n", dp, x, nux1, nuz2, dfx, dfz);
				fprintf(stdout,"% 10.6e % 10.6e % 10.6e % 10.6e % 10.6e % 10.6e\n", dp, x, nux1, nuz2, dfx, dfz);
			}else{
				fprintf(outf,"% 10.6e % 10.6e % 10.6e % 10.6e\n", dp, x, nux1, nuz1);
				fprintf(stdout,"% 10.6e % 10.6e % 10.6e % 10.6e\n", dp, x, nux1, nuz1);
			}
		}
	}
	fclose(outf);
}
#undef NTERM2

/****************************************************************************/
/* void TunesShiftWithEnergy(long Nb, long Nbtour, double emax)

   Purpose:
       Computes tunes versus energy offset by tracking
       by linear energy step between -emax and emax

   Input:
       Nb+1   numbers of points
       NbTour number of turns for tracking
       emax   maximum energy

   Output:
       none

   Return:
       none

   Global variables:
       trace

   Specific functions:
       Trac_Simple, Get_NAFF

   Comments:
       none

****************************************************************************/
#define NTERM  4
void TunesShiftWithEnergy(long Nb, long Nbtour, double emax)
{
  FILE * outf;
  const char fic[] = "nudp.out";
  long i = 0L;
//  long lastpos = 0L;
  double Tab[DIM][NTURN];
  double fx[NTERM], fz[NTERM];
  double x  = 0.0,  xp  = 0.0, z  = 0.0,  zp  = 0.0, ctau  = 0.0, dp  = 0.0;
  double x0 = 1e-6, xp0 = 0.0, z0 = 1e-6, zp0 = 0.0, ctau0 = 0.0, dp0 = 0.0;
  double nux1 = 0.0, nuz1 = 0.0;
  int nb_freq[2] = {0, 0};
  bool status = true;
  struct tm *newtime;

  /* Get time and date */
  newtime = GetTime();

  if (!trace) printf("\n Entering TunesShiftWithEnergy ...\n\n");

  /* Opening file */
  if ((outf = fopen(fic, "w")) == NULL) {
    fprintf(stdout, "NuDp: error while opening file %s\n", fic);
    exit_(1);
  }

  fprintf(outf,"# TRACY III -- %s -- %s \n", fic, asctime2(newtime));
  fprintf(outf,"#    dP/P           fx            fz          xcod         pxcod          zcod         pzcod\n");
  if (trace) fprintf(stdout,"#    dP/P           fx            fz          xcod         pxcod          zcod         pzcod\n");

  if (Nb <= 1L)
    fprintf(stdout,"NuDp: Error Nb=%ld\n",Nb);

  // start loop over energy
  dp0 = -emax;

  for (i = 0L; i < Nb; i++) {
    dp   = dp0 + i*emax/(Nb-1)*2;
    x    = x0  ;
    xp   = xp0 ;
    z    = z0  ;
    zp   = zp0 ;
    ctau = ctau0;

    Trac_Simple4DCOD(x,xp,z,zp,dp,ctau,Nbtour,Tab,&status); // tracking around closed orbit
    if (status) {
       Get_NAFF(NTERM, Nbtour, Tab, fx, fz, nb_freq); // get frequency vectors
       Get_freq(fx,fz,&nux1,&nuz1);  // gets nux and nuz
    }
    else {
       nux1 = 0.0; nuz1 = 0.0;
       status = true;
    }

    long lastpos=0L;
    getcod(dp, lastpos); // get cod for printout


    fprintf(outf,"%14.6e %14.6e %14.6e %14.6e %14.6e %14.6e %14.6e\n",
            dp, nux1,nuz1, globval.CODvect[0], globval.CODvect[1],
            globval.CODvect[2], globval.CODvect[3]);

    if (trace) fprintf(stdout,"%14.6e %14.6e %14.6e %14.6e %14.6e %14.6e %14.6e\n",
            dp, nux1,nuz1, globval.CODvect[0], globval.CODvect[1],
            globval.CODvect[2], globval.CODvect[3]);
  }

  fclose(outf);
}
#undef NTERM




/****************************************************************************/
/* void Phase(double x,double xp,double y, double yp,double energy, double ctau, long Nbtour)

   Purpose:
       Compute 6D phase space
       Results in phase.out

   Input:
       x, xp, y, yp, energy, ctau starting position
       Nbtour turn number

   Output:
       none

   Return:
       none

   Global variables:
       trace

   Specific functions:
       Trac_Simple6DCOD, Get_NAFF

   Comments:
       1 December 2010, Call to a Tracking round around the 6D and not 4D closed orbit

****************************************************************************/
void Phase(double x,double xp,double y, double yp,double energy, double ctau, long Nbtour)
{
  double Tab[6][NTURN];
  FILE *outf;
  const char fic[] = "phase.out";
  int i;
  bool status;
  struct tm *newtime;

  /* Get time and date */
  newtime = GetTime();

  if (Nbtour > NTURN) {
    fprintf(stdout, "Phase: error Nbtour=%ld > NTURN=%d\n",Nbtour,NTURN);
    exit_(1);
  }

  if ((outf = fopen(fic, "w")) == NULL)  {
    fprintf(stdout, "Phase: error while opening file %s\n", fic);
    exit_(1);
  }

  fprintf(outf,"# TRACY III -- %s -- %s \n", fic, asctime2(newtime));
  fprintf(outf,"# Phase Space \n");
  fprintf(outf,
  "#    x           xp             z            zp           dp          ctau\n");

  // initialization to zero (case where unstable
  for (i = 0; i < Nbtour; i++) {
    Tab[0][i] = 0.0;
    Tab[1][i] = 0.0;
    Tab[2][i] = 0.0;
    Tab[3][i] = 0.0;
    Tab[4][i] = 0.0;
    Tab[5][i] = 0.0;
  }

  Trac_Simple6DCOD(x,xp,y,yp,energy,ctau,Nbtour,Tab,&status);
  for (i = 0; i < Nbtour; i++) {
    fprintf(outf,"% .5e % .5e % .5e % .5e % .5e % .5e\n",
            Tab[0][i],Tab[1][i],Tab[2][i],Tab[3][i],Tab[4][i],Tab[5][i]);
  }
  fclose(outf);
}

/****************************************************************************/
/* void PhasePoly(long pos, double x0,double px0, double z0, double pz0, double delta0,
               double ctau0, long Nbtour)

   Purpose:
       Compute 6D phase space at position pos (=element number in the lattice )
       for several particles: first aim was for injection study
       Results in phasepoly.out

   Input:
       x, xp, y, yp, energy, ctau starting position
       Nbtour turn number

   Output:
       none

   Return:
       none

   Global variables:
       trace

   Specific functions:
       Trac_Simple, Get_NAFF

   Comments:
       none

****************************************************************************/
#include "math.h"

void PhasePoly(long pos, double x0,double px0, double z0, double pz0, double delta0,
               double ctau0, long Nbtour)
{
  FILE *outf;
  const char  *fic="phasepoly.out";
  long        lastpos = 0,lastn = 0;
  int         i,j;
  double      x, z, px, pz, delta, ctau;
  double      ex = 1368E-9, el = 1.78E-4;
  double      betax = 9.0, /*betaz = 8.2, */betal = 45.5;
  Vector      xsynch;
  int         nx = 1, ne = 400;
  struct tm   *newtime;

  /* Get time and date */
  newtime = GetTime();

  fprintf(stdout,"Closed orbit:\n");
  fprintf(stdout,"      x            px           z           pz        delta       ctau\n");
  fprintf(stdout,"% 12.8f % 12.8f % 12.8f % 12.8f % 12.8f % 12.8f\n",
          globval.CODvect[0], globval.CODvect[1], globval.CODvect[2],
          globval.CODvect[3], globval.CODvect[4], globval.CODvect[5]);
  lastpos = pos;
  globval.CODvect = xsynch;
//  xsynch[0] = globval.CODvect[0];
//  xsynch[1] = globval.CODvect[1];
//  xsynch[2] = globval.CODvect[2];
//  xsynch[3] = globval.CODvect[3];
//  xsynch[4] = globval.CODvect[4];
//  xsynch[5] = globval.CODvect[5];

  if ((outf = fopen(fic, "w")) == NULL)  {
    fprintf(stdout, "Phase: error while opening file %s\n", fic);
    exit_(1);
  }

  fprintf(outf,"# TRACY III -- %s -- %s \n", fic, asctime2(newtime));
  fprintf(outf,"# 6D Phase Space \n");
  fprintf(outf,
  "# num         x           xp             z            zp           dp          ctau\n");

  trace = true;
  for (j = 0; j < ne; j++){
    for (i = 0; i < nx; i++){
       x     = x0     + xsynch[0] + sqrt(ex*betax)*cos(2.0*M_PI/nx*i)*0;
       px    = px0    + xsynch[1] + sqrt(ex/betax)*sin(2.0*M_PI/nx*i)*0;
       z     = z0     + xsynch[2];
       pz    = pz0    + xsynch[3];
       delta = delta0 + xsynch[4] + sqrt(el/betal)*sin(2*M_PI/ne*j)*0 ;
       ctau  = ctau0  + xsynch[5] + sqrt(el*betal)*cos(2*M_PI/ne*j)*0 + j*0.002;
       fprintf(outf, "%6ld %+10.5e %+10.5e %+10.5e %+10.5e %+10.5e %+10.5e",
                      0L, x, px, z, pz, delta, ctau);
       Trac(x,px,z,pz,delta,ctau, Nbtour,pos, lastn, lastpos, outf);
       fprintf(outf,"\n");
    }
  }
  fclose(outf);
}

/****************************************************************************/
/* void PhasePortrait(double x0,double px0,double z0, double pz0, double delta0,
                   double end, double Nb, long Nbtour, int num)

   Purpose:
       Compute a phase portrait: Nb orbits
       Results in phaseportrait.out

   Input:
       x0, px0, z0, Pz0, delta0, starting position
       num cooordinate to vary (0 is x and 4 is delta)
       end is the last value for the varying coordinate
       Nb is the number of orbits to draw
       Nbtour turn number

   Output:
       none

   Return:
       none

   Global variables:
       none

   Specific functions:
       Trac_Simple

   Comments:
       Change of tracking routine: do not use a tabular to store data

****************************************************************************/
void PhasePortrait(double x0,double px0,double z0, double pz0, double delta0,
                   double ctau0, double end, long Nb, long Nbtour, int num)
{
  double Tab[6][NTURN];
  FILE *outf;
  const char fic[] = "phaseportrait.out";
  int i = 0, j = 0;
  double start = 0.0, step = 0.0;
  double x = 0.0, px = 0.0, z = 0.0, pz = 0.0, delta = 0.0, ctau = 0.0;
  bool status = true;
  struct tm *newtime;

  /* Get time and date */
  newtime = GetTime();

  if (Nbtour > NTURN) {
    fprintf(stdout, "Phase: error Nbtour=%ld > NTURN=%d\n",Nbtour,NTURN);
    exit_(1);
  }

  if ((outf = fopen(fic, "w")) == NULL) {
    fprintf(stdout, "Phase: error while opening file %s\n", fic);
    exit_(1);
  }

  fprintf(outf,"# TRACY III  -- %s \n", asctime2(newtime));
  fprintf(outf,"#  x           xp            z           zp           dp          ctau\n#\n");

  x = x0; px = px0;
  z = z0; pz = pz0;
  delta = delta0;

  switch (num) {
    case 0:
      start = x0; break;
    case 1:
      start = px0; break;
    case 2:
      start = z0; break;
    case 3:
      start = pz0; break;
    case 4:
      start = delta0; break;
    case 5:
      start = ctau0; break;
  }

  /** Step between initial conditions **/
  step = (end - start)/Nb;

  for (j = 0; j <= Nb; j++){
    switch (num){
      case 0:
        x     = start + j*step;  break;
      case 1:
        px    = start + j*step;  break;
      case 2:
        z     = start + j*step;  break;
      case 3:
        pz    = start + j*step;  break;
      case 4:
        delta = start + j*step;  break;
      case 5:
        ctau  = start + j*step;  break;
    }

   fprintf(stdout,"% .5e % .5e % .5e % .5e % .5e % .5e\n",
            x,px,z,pz,delta,ctau);
    Trac_Simple4DCOD(x,px,z,pz,delta,ctau,Nbtour,Tab,&status);
   for (i = 0; i < Nbtour; i++) {
      fprintf(outf,"% .5e % .5e % .5e % .5e % .5e % .5e\n",
            Tab[0][i],Tab[1][i],Tab[2][i],Tab[3][i],Tab[4][i],Tab[5][i]);
    }
  }
  fclose(outf);
}


/****************************************************************************/
/* void Check_Trac(double x, double px, double y, double py, double dp)

   Purpose:
       Diagnosis for tracking
       Used only for debuging
       Print particle coordinates after each element over 1 single turn

   Input:
       x, px, y, py, dp starting conditions for tracking

   Output:
       none

   Return:
       none

   Global variables:
       trace

   Specific functions:
       Trac_Simple, Get_NAFF

   Comments:
       none

****************************************************************************/
void Check_Trac(double x, double px, double y, double py, double dp)
{
  Vector x1;             /* Tracking coordinates */
  long lastpos = globval.Cell_nLoc;
  FILE *outf;
  const char fic[] = "check_ampl.out";
  int i;

  if ((outf = fopen(fic, "w")) == NULL)
  {
    fprintf(stdout, "Phase: error while opening file %s\n", fic);
    exit_(1);
  }

  x1[0] =  x; x1[1] = px;
  x1[2] =  y; x1[3] = py;
  x1[4] = dp; x1[5] = 0e0;

  fprintf(outf,"# i    x   xp  z   zp   delta cT \n");

  for (i = 1; i<= globval.Cell_nLoc; i++)
  {
    Cell_Pass(i,i+1, x1, lastpos);
    fprintf(outf,"%4d % .5e % .5e % .5e % .5e % .5e % .5e\n",
            i, x1[0],x1[1],x1[2],x1[3],x1[4],x1[5]);
  }
}

/****************************************************************************/
/* void Enveloppe(double x, double px, double y, double py, double dp, double nturn)

   Purpose:
       Diagnosis for tracking
       Used only for debuging
       Print particle coordinates after each element over 1 single turn

   Input:
       x, px, y, py, dp starting conditions for tracking

   Output:
       none

   Return:
       none

   Global variables:
       trace

   Specific functions:
       Trac_Simple, Get_NAFF

   Comments:
       none

****************************************************************************/
void Enveloppe(double x, double px, double y, double py, double dp, double nturn)
{
  Vector x1; /* Tracking coordinates */
  long lastpos = globval.Cell_nLoc;
  FILE *outf;
  const char fic[] = "enveloppe.out";
  int i,j ;
  CellType Cell;

  /* Get cod the delta = energy*/
  getcod(dp, lastpos);

  printf("xcod=%.5e mm zcod=% .5e mm \n", globval.CODvect[0]*1e3, globval.CODvect[2]*1e3);

  if ((outf = fopen(fic, "w")) == NULL)
  {
    fprintf(stdout, "Enveloppe: error while opening file %s\n", fic);
    exit_(1);
  }

  x1[0] =  x + globval.CODvect[0]; x1[1] = px + globval.CODvect[1];
  x1[2] =  y + globval.CODvect[2]; x1[3] = py + globval.CODvect[3];
  x1[4] = dp; x1[5] = 0e0;

  fprintf(outf,"# i    x   xp  z   zp   delta cT \n");

  for (j = 1; j <= nturn; j++)
  {
    for (i = 0; i< globval.Cell_nLoc; i++)
    {/* loop over full ring */

      getelem(i, &Cell);
      Cell_Pass(i,i+1, x1, lastpos);
      if (lastpos != i+1)
      {
       printf("Unstable motion ...\n"); exit_(1);
      }

      fprintf(outf,"%6.2f % .5e % .5e % .5e % .5e % .5e % .5e\n",
              Cell.S, x1[0],x1[1],x1[2],x1[3],x1[4],x1[5]);
    }
  }
}


/****************************************************************************/
/* void Multipole_thicksext(void)

   Purpose:
       Set multipole in dipoles, quadrupoles, thick sextupoles, skew quadrupole,
           horizontal and vertical corrector.

   Input:
       none

   Output:
       none

   Return:
       none

   Global variables:
       trace

   Specific functions:
       getelem, SetKLpar, GetKpar

   Comments:
       Test for short and long quadrupole could be changed using the length
       instead of the name. Maybe more portable, in particular if periodicity
       is broken
       Should be rewritten because list already exists now ..

       Copy from Tracy II.
****************************************************************************/

void Multipole_thicksext(char const *fic_hcorr, char const *fic_vcorr, char const *fic_skew)
{
  int i = 0;
  int ndip  = 0,  /* Number of dipoles */
      nquad = 0,  /* Number of quadrupoles */
      nsext = 0,  /* Number of sextupoles  */
      nhcorr= 0,  /* Number of horizontal correctors */
      nvcorr= 0,  /* Number of vertical correctors */
      nqcorr= 0;  /* Number of skew quadrupoles */

  int dlist[500];     /* dipole list */
  int qlist[500];     /* Quadrupole list */
  int slist[500];     /* Sextupole list */
  int hcorrlist[120]; /* horizontal corrector list */
  int vcorrlist[120]; /* vertical corrector list */
  int qcorrlist[120]; /* skew quad list */
  int hcorrlistThick[120]; /* horizontal corrector list */
  int vcorrlistThick[120]; /* vertical corrector list */
  int qcorrlistThick[120]; /* skew quad list */

  CellType Cell;

  int    mOrder = 0;     /* multipole order */
  double mKL = 0.0 ;     /* multipole integrated strength */
  double corr_strength = 0.0;
  double hcorr[120], vcorr[120], qcorr[120];
  double b2 = 0.0, b3 = 0.0;
  double dBoB2 = 0.0, dBoB3 = 0.0, dBoB4 = 0.0, dBoB5 = 0.0, dBoB6 = 0.0,
         dBoB7 = 0.0, dBoB9 = 0.0, dBoB11 = 0.0, dBoB15 = 0.0, dBoB21 = 0.0,
         dBoB27 = 0.0;
  double dBoB6C = 0.0, dBoB6L = 0.0, dBoB10C = 0.0, dBoB10L = 0.0,
         dBoB14C = 0.0, dBoB14L = 0.0, dBoB3C = 0.0, dBoB3L = 0.0,
         dBoB4C = 0.0, dBoB4L = 0.0;
  double dBoB5rms = 0.0, dBoB7rms = 0.0;
  double x0i = 0.0, x02i = 0.0, x03i = 0.0, x04i = 0.0, x05i = 0.0,
         x06i = 0.0, x07i = 0.0, x08i = 0.0, x012i = 0.0, x010i = 0.0,
         x018i = 0.0, x024i = 0.0, x1i = 0.0;
  double theta = 0.0, brho = 0.0, conv = 0.0 ;

  FILE *fi;
/*********************************************************/



  printf("Enter multipole ... \n");

/* Make lists of dipoles, quadrupoles and  sextupoles */
  for (i = 0; i <= globval.Cell_nLoc; i++)
  {
    getelem(i, &Cell); /* get element */

    if (Cell.Elem.Pkind == Mpole)
    {
      if (Cell.Elem.M->Pirho!= 0.0)
      {
        dlist[ndip] = i;
        ndip++;
        if (trace) printf("%s % f\n",Cell.Elem.PName, Cell.Elem.M->PB[0 + HOMmax]);
      }
      else if (Cell.Elem.M->PBpar[2L + HOMmax] != 0.0)
      {
        qlist[nquad] = i;
        nquad++;
        if (trace) printf("%s % f\n",Cell.Elem.PName, Cell.Elem.M->PBpar[2L + HOMmax]);
      }
      else if (Cell.Elem.M->PBpar[3L + HOMmax] != 0.0)
      {
        slist[nsext] = i;
        nsext++;
        if (trace) printf("%s % f\n",Cell.Elem.PName, Cell.Elem.M->PBpar[3L + HOMmax]);
      }
      else if ( Cell.Elem.PName[0] == 'c' && Cell.Elem.PName[1] == 'h')
      {
        hcorrlist[nhcorr] = i;
        nhcorr++;
        if (trace) printf("%s \n",Cell.Elem.PName);
      }
      else if ( Cell.Elem.PName[0] == 'c' && Cell.Elem.PName[1] == 'v')
      {
        vcorrlist[nvcorr] = i;
        nvcorr++;
        if (trace) printf("%s \n",Cell.Elem.PName);
      }
      else if ( Cell.Elem.PName[0] == 'q' && Cell.Elem.PName[1] == 't')
      {
        qcorrlist[nqcorr] = i;
        nqcorr++;
        if (trace) printf("%s \n",Cell.Elem.PName);
      }
    }
  }


 /* find sextupole associated with the corrector */
 // solution 1: find by names
 // solution 2: use a predfined list
 // solution 3: smothing smart ???
  for (i=0; i< nhcorr; i++){
    if (trace) fprintf(stdout, "%d\n", i);
    getelem(hcorrlist[i]-1, &Cell);
    if (Cell.Elem.PName[0] == 's' && Cell.Elem.PName[1] == 'x')
      hcorrlistThick[i] = hcorrlist[i]-1;
    else{
      getelem(hcorrlist[i]+1, &Cell);
      if (Cell.Elem.PName[0] == 's' && Cell.Elem.PName[1] == 'x')
        hcorrlistThick[i] = hcorrlist[i]+1;
      else{
        getelem(hcorrlist[i]+2, &Cell);
        if (Cell.Elem.PName[0] == 's' && Cell.Elem.PName[1] == 'x')
          hcorrlistThick[i] = hcorrlist[i]+2;
        else{
          getelem(hcorrlist[i]-2, &Cell);
          if (Cell.Elem.PName[0] == 's' && Cell.Elem.PName[1] == 'x')
            hcorrlistThick[i] = hcorrlist[i]-2;
          else{
            getelem(hcorrlist[i]+3, &Cell);
            if (Cell.Elem.PName[0] == 's' && Cell.Elem.PName[1] == 'x')
              hcorrlistThick[i] = hcorrlist[i]+3;
            else{
              getelem(hcorrlist[i]-3, &Cell);
              if (Cell.Elem.PName[0] == 's' && Cell.Elem.PName[1] == 'x')
                hcorrlistThick[i] = hcorrlist[i]-3;
              else fprintf(stdout, "Warning Sextupole not found for VCOR\n");
            }
          }
        }
      }
    }
  }

 for (i=0; i< nvcorr; i++){
   if (trace) fprintf(stdout, "%d\n", i);
   getelem(vcorrlist[i]-1, &Cell);
   if (Cell.Elem.PName[0] == 's' && Cell.Elem.PName[1] == 'x')
     vcorrlistThick[i] = vcorrlist[i]-1;
   else{
     getelem(vcorrlist[i]+1, &Cell);
     if (Cell.Elem.PName[0] == 's' && Cell.Elem.PName[1] == 'x')
        vcorrlistThick[i] = vcorrlist[i]+1;
     else{
       getelem(vcorrlist[i]+2, &Cell);
       if (Cell.Elem.PName[0] == 's' && Cell.Elem.PName[1] == 'x')
          vcorrlistThick[i] = vcorrlist[i]+2;
       else{
         getelem(vcorrlist[i]-2, &Cell);
         if (Cell.Elem.PName[0] == 's' && Cell.Elem.PName[1] == 'x')
             vcorrlistThick[i] = vcorrlist[i]-2;
         else{
           getelem(vcorrlist[i]+3, &Cell);
           if (Cell.Elem.PName[0] == 's' && Cell.Elem.PName[1] == 'x')
             vcorrlistThick[i] = vcorrlist[i]+3;
           else{
             getelem(vcorrlist[i]-3, &Cell);
             if (Cell.Elem.PName[0] == 's' && Cell.Elem.PName[1] == 'x')
               vcorrlistThick[i] = vcorrlist[i]-3;
             else fprintf(stdout, "Warning Sextupole not found for VCOR\n");
           }
         }
       }
     }
   }
 }

 for (i=0; i< nqcorr; i++){
 if (trace) fprintf(stdout, "%d\n", i);
   getelem(qcorrlist[i]-1, &Cell);
   if (Cell.Elem.PName[0] == 's' && Cell.Elem.PName[1] == 'x')
     qcorrlistThick[i] = qcorrlist[i]-1;
   else{
     getelem(qcorrlist[i]+1, &Cell);
     if (Cell.Elem.PName[0] == 's' && Cell.Elem.PName[1] == 'x')
       qcorrlistThick[i] = qcorrlist[i]+1;
     else{
       getelem(qcorrlist[i]+2, &Cell);
       if (Cell.Elem.PName[0] == 's' && Cell.Elem.PName[1] == 'x')
         qcorrlistThick[i] = qcorrlist[i]+2;
       else{
         getelem(qcorrlist[i]-2, &Cell);
         if (Cell.Elem.PName[0] == 's' && Cell.Elem.PName[1] == 'x')
           qcorrlistThick[i] = qcorrlist[i]-2;
         else{
           getelem(qcorrlist[i]+3, &Cell);
           if (Cell.Elem.PName[0] == 's' && Cell.Elem.PName[1] == 'x')
             qcorrlistThick[i] = qcorrlist[i]+3;
           else{
             getelem(qcorrlist[i]-3, &Cell);
             if (Cell.Elem.PName[0] == 's' && Cell.Elem.PName[1] == 'x')
               qcorrlistThick[i] = qcorrlist[i]-3;
             else fprintf(stdout, "Warning Sextupole not found for QT\n");
           }
         }
       }
     }
   }
 }


 if (!trace) printf("Elements: ndip=%d nquad=%d  nsext=%d nhcorr=%d nvcorr=%d nqcorr=%d\n",
                     ndip,nquad,nsext,nhcorr,nvcorr,nqcorr);

 /***********************************************************************************/
 /*                                                                                 */
 /*                        Set multipoles for dipole                                */
 /*                                                                                 */
 /*                        x0ni w/ n = p-1 for a 2p-poles                           */
 /*                                                                                 */
 /***********************************************************************************/

  x0i   = 1.0/20e-3;  /* 1/radius */
  x02i  = x0i*x0i;
  x03i  = x02i*x0i;
  x04i  = x02i*x02i;
  x05i  = x04i*x0i;
  x06i  = x03i*x03i;
  x07i  = x06i*x0i;

 // dBoB2 =  2.2e-4*1;  /* gradient, used for curve trajectory simulation */
  dBoB3 = -3.0e-4*1;  /* hexapole */
  dBoB4 =  2.0e-5*1;  /* octupole */
  dBoB5 = -1.0e-4*1;  /* decapole */
  dBoB6 = -6.0e-5*1;  /* 12-poles */
  dBoB7 = -1.0e-4*1;  /* 14-poles */

 for (i = 0; i < ndip; i++)
 {
   getelem(dlist[i], &Cell);
   theta = Cell.Elem.PL*Cell.Elem.M->Pirho;

   /* gradient error */
   mKL =GetKLpar(Cell.Fnum, Cell.Knum, mOrder=2L);
   mKL += dBoB2*theta*x0i;
   SetKLpar(Cell.Fnum, Cell.Knum, mOrder=2L, mKL);

   if (trace) printf("num= %4d name = %s Fnum = %3ld, Knum=%3ld theta=% e mKl=% e\n",i,
               Cell.Elem.PName,Cell.Fnum, Cell.Knum, theta, mKL);

   /* sextupole error */
   mKL = dBoB3*theta*x02i;
   SetKLpar(Cell.Fnum, Cell.Knum, mOrder=3L, mKL);
 if (trace) printf("num= %4d name = %s Fnum = %3ld, Knum=%3ld theta=% e mKl=% e\n",i,
               Cell.Elem.PName,Cell.Fnum, Cell.Knum, theta, mKL);

   /* octupole error */
   mKL = dBoB4*theta*x03i;
   SetKLpar(Cell.Fnum, Cell.Knum, mOrder=4L, mKL);
 if (trace) printf("num= %4d name = %s Fnum = %3ld, Knum=%3ld theta=% e mKl=% e\n",i,
               Cell.Elem.PName,Cell.Fnum, Cell.Knum, theta, mKL);

   /* decapole error */
   mKL = dBoB5*theta*x04i;
   SetKLpar(Cell.Fnum, Cell.Knum, mOrder=5L, mKL);
 if (trace) printf("num= %4d name = %s Fnum = %3ld, Knum=%3ld theta=% e mKl=% e\n",i,
               Cell.Elem.PName,Cell.Fnum, Cell.Knum, theta, mKL);

   /* 12-pole error */
   mKL = dBoB6*theta*x05i;
   SetKLpar(Cell.Fnum, Cell.Knum, mOrder=6L, mKL);
 if (trace) printf("num= %4d name = %s Fnum = %3ld, Knum=%3ld theta=% e mKl=% e\n",i,
               Cell.Elem.PName,Cell.Fnum, Cell.Knum, theta, mKL);

   /* 14-pole error */
   mKL = dBoB7*theta*x06i;
   SetKLpar(Cell.Fnum, Cell.Knum, mOrder=7L, mKL);
    if (trace) printf("num= %4d name = %s Fnum = %3ld, Knum=%3ld theta=% e mKl=% e\n",i,
               Cell.Elem.PName,Cell.Fnum, Cell.Knum, theta, mKL);

 }

 /***********************************************************************************
  *
  ***********                Set multipoles for quadripole           ****************
  *
  *                          x0ni w/ n = p-2 for a 2p-poles
  *
  ***********************************************************************************/

 x0i  = 1.0/30e-3;       /* 1/Radius in meters */
 b2   = 0.0;             /* Quadrupole strength */
 x02i = x0i*x0i;
 x04i = x02i*x02i;       /* 10-poles */
 x08i = x04i*x04i;       /* 20-poles */
 x012i= x08i*x04i;       /* 28-poles */

 dBoB6C  =  2.4e-4*1;
 dBoB10C =  0.7e-4*1;
 dBoB14C =  0.9e-4*1;
 dBoB6L  =  0.7e-4*1;
 dBoB10L =  1.9e-4*1;
 dBoB14L =  1.0e-4*1;


 x1i  = 1.0/30e-3;       /* rayon reference = 30 mm pour mesure sextupole et octupole*/
 dBoB3L  =  2.9e-4*1;  /* sextupole qpole long */
 dBoB4L  =  -8.6e-4*1;  /* octupole qpole long */
 dBoB3C  =  -1.6e-4*1;  /* sextupole qpole court */
 dBoB4C  =  -3.4e-4*1;  /* octupole qpole court */


 for (i = 0; i < nquad; i++)
 {
   getelem(qlist[i], &Cell);
//    b2 = Cell.Elem.PL*GetKpar(Cell.Fnum, Cell.Knum, 2L);
   b2 = GetKLpar(Cell.Fnum, Cell.Knum, 2L);

   /* 12-pole multipole error */
   if ((strncmp(Cell.Elem.PName,"qp2",3)==0) || (strncmp(Cell.Elem.PName,"qp7",3)==0))
         mKL= b2*dBoB6L*x04i;
   else
      mKL= b2*dBoB6C*x04i;
   SetKLpar(Cell.Fnum, Cell.Knum, mOrder=6L, mKL);
   if (trace) printf("num= %4d name = %s Fnum = %3ld, Knum=%3ld b2=% e mKl=% e\n",i,
               Cell.Elem.PName,Cell.Fnum, Cell.Knum, b2, mKL);

   /* 20-pole multipole error */
   if ((strncmp(Cell.Elem.PName,"qp2",3)==0) || (strncmp(Cell.Elem.PName,"qp7",3)==0))
     mKL= b2*dBoB10L*x08i;
   else
     mKL= b2*dBoB10C*x08i;
   SetKLpar(Cell.Fnum, Cell.Knum, mOrder=10L, mKL);
   if (trace) printf("num= %4d name = %s Fnum = %3ld, Knum=%3ld b2=% e mKl=% e\n",i,
               Cell.Elem.PName,Cell.Fnum, Cell.Knum, b2, mKL);

   /* 28-pole multipole error */
   if ((strncmp(Cell.Elem.PName,"qp2",3)==0) || (strncmp(Cell.Elem.PName,"qp7",3)==0))
     mKL= b2*dBoB14L*x012i;
   else
     mKL= b2*dBoB14C*x012i;
   SetKLpar(Cell.Fnum, Cell.Knum, mOrder=14L, mKL);
   if (trace) printf("num= %4d name = %s Fnum = %3ld, Knum=%3ld b2=% e mKl=% e\n",i,
               Cell.Elem.PName,Cell.Fnum, Cell.Knum, b2, mKL);

   /* sextupole mesure quadrupoles longs*/
   if ((strncmp(Cell.Elem.PName,"qp2",3)==0) || (strncmp(Cell.Elem.PName,"qp7",3)==0))
      mKL= b2*dBoB3L*x1i;
   else
      mKL= b2*dBoB3C*x1i;
   SetKLpar(Cell.Fnum, Cell.Knum, mOrder=3L, mKL);
   if (trace) printf("num= %4d name = %s Fnum = %3ld, Knum=%3ld b2=% e mKl=% e\n",i,
               Cell.Elem.PName,Cell.Fnum, Cell.Knum, b2, mKL);

   /* octupole mesure quadrupoles longs*/
   if ((strncmp(Cell.Elem.PName,"qp2",3)==0) || (strncmp(Cell.Elem.PName,"qp7",3)==0))
      mKL= b2*dBoB4L*x1i*x1i;
   else
      mKL= b2*dBoB4C*x1i*x1i;
   SetKLpar(Cell.Fnum, Cell.Knum, mOrder=4L, mKL);
   if (trace) printf("num= %4d name = %s Fnum = %3ld, Knum=%3ld b2=% e mKl=% e\n",i,
               Cell.Elem.PName,Cell.Fnum, Cell.Knum, b2, mKL);
 }

 /***********************************************************************************
  *
  ***********              Set multipoles for sextupole              ****************
  *
  *                        x0ni w/ n = p-3 for a 2p-poles
  *
  ***********************************************************************************/

  b3    = 0.0;
  x0i   = 1.0/32e-3;
  x02i  = x0i*x0i;
  x04i  = x02i*x02i;
  x06i  = x04i*x02i;   /* 18-poles */
  x012i = x06i*x06i;   /* 30-poles */
  x018i = x012i*x06i;  /* 42-poles */
  x024i = x012i*x012i; /* 54-poles */

  /* multipoles from dipolar unallowed component */
  dBoB5  =   5.4e-4*1;
  dBoB7  =   3.3e-4*1;
  dBoB5rms  =  4.7e-4*1; // for test
  dBoB7rms  =  2.1e-4*1; // for test

  /* allowed multipoles */
  dBoB9  =  -4.7e-4*1;
  dBoB15 =  -9.0e-4*1;
  dBoB21 =  -20.9e-4*1;
  dBoB27 =    0.8e-4*1;
/*
  dBoB9  =  3.1e-3*1;
  dBoB15 =  5.0e-4*1;
  dBoB21 =  -2.0e-2*1;
  dBoB27 =  1.1e-2*1;
*/
 for (i = 0; i < nsext; i++)
 {
   getelem(slist[i], &Cell);
   b3 = GetKLpar(Cell.Fnum, Cell.Knum, 3L);

   /* 10-pole multipole error */
   mKL= b3*dBoB5*x02i;
   SetKLpar(Cell.Fnum, Cell.Knum, mOrder=5L, mKL);
   if (trace) printf("num= %4d name = %s Fnum = %3ld, Knum=%3ld b3=% e mKl=% e\n",i,
               Cell.Elem.PName,Cell.Fnum, Cell.Knum, b3, mKL);

   /* 14-pole multipole error */
   mKL= b3*dBoB7*x04i;
   SetKLpar(Cell.Fnum, Cell.Knum, mOrder=7L, mKL);
   if (trace) printf("num= %4d name = %s Fnum = %3ld, Knum=%3ld b3=% e mKl=% e\n",i,
               Cell.Elem.PName,Cell.Fnum, Cell.Knum, b3, mKL);

   /* 18-pole multipole error */
   mKL= b3*dBoB9*x06i;
   SetKLpar(Cell.Fnum, Cell.Knum, mOrder=9L, mKL);
   if (trace) printf("num= %4d name = %s Fnum = %3ld, Knum=%3ld b3=% e mKl=% e\n",i,
               Cell.Elem.PName,Cell.Fnum, Cell.Knum, b3, mKL);

   /* 30-pole multipole error */
   mKL= b3*dBoB15*x012i;
   SetKLpar(Cell.Fnum, Cell.Knum, mOrder=15L, mKL);
   if (trace) printf("num= %4d name = %s Fnum = %3ld, Knum=%3ld b3=% e mKl=% e\n",i,
               Cell.Elem.PName,Cell.Fnum, Cell.Knum, b3, mKL);

   /* 42-pole multipole error */
   mKL= b3*dBoB21*x018i;
   SetKLpar(Cell.Fnum, Cell.Knum, mOrder=21L, mKL);
   if (trace) printf("num= %4d name = %s Fnum = %3ld, Knum=%3ld b3=% e mKl=% e\n",i,
               Cell.Elem.PName,Cell.Fnum, Cell.Knum, b3, mKL);

   /* 54-pole multipole error */
   mKL= b3*dBoB27*x024i;
   SetKLpar(Cell.Fnum, Cell.Knum, mOrder=27L, mKL);
   if (trace) printf("num= %4d name = %s Fnum = %3ld, Knum=%3ld b3=% e mKl=% e\n",i,
               Cell.Elem.PName,Cell.Fnum, Cell.Knum, b3, mKL);
}

 /***********************************************************************************
  *
  ******  Set multipoles for sextupole horizontal correctors         ****************
  *
  *                x0ni w/ n = p-1 for a 2p-poles
  *
  ***********************************************************************************/
  x0i   = 1.0/35e-3;  /* 1/radius */
  x02i  = x0i*x0i;
  x03i  = x02i*x0i;
  x04i  = x02i*x02i;
  x05i  = x04i*x0i;
  x06i  = x03i*x03i;
  x010i = x05i*x05i;

  dBoB5  = 0.430*1;  /* decapole */
  dBoB7  = 0.063*1;  /* 14-poles */
  dBoB11 =-0.037*1;  /* 22-poles */

  brho = globval.Energy/0.299792458; /* magnetic rigidity */
  conv = 8.14e-4;  /*conversion des A en T.m*/

  /* open H corrector file */
  if ((fi = fopen(fic_hcorr,"r")) == NULL)
  {
    fprintf(stderr, "Error while opening file %s \n",fic_hcorr);
    exit(1);
  }

  for (i = 0; i < nhcorr; i++)
  {
    fscanf(fi,"%le \n", &hcorr[i]);
  }
  fclose(fi); /* close H corrector file */

  for (i = 0; i < nhcorr; i++){
    getelem(hcorrlistThick[i], &Cell);
    corr_strength = hcorr[i]*conv/brho;

    /* gradient error */
    mKL = GetKLpar(Cell.Fnum, Cell.Knum, mOrder=5L);
    mKL += dBoB5*corr_strength*x04i;
    SetKLpar(Cell.Fnum, Cell.Knum, mOrder=5L, mKL);

    if (trace) printf("num= %4d name = %s Fnum = %3ld, Knum=%3ld BL/brho=% e mKl=% e\n",i,
    Cell.Elem.PName,Cell.Fnum, Cell.Knum, corr_strength, mKL);
    /* 14-pole error */
    mKL = GetKLpar(Cell.Fnum, Cell.Knum, mOrder=7L);
    mKL += dBoB7*corr_strength*x06i;
    SetKLpar(Cell.Fnum, Cell.Knum, mOrder=7L, mKL);

    if (trace) printf("num= %4d name = %s Fnum = %3ld, Knum=%3ld BL/brho=% e mKl=% e\n",i,
    Cell.Elem.PName,Cell.Fnum, Cell.Knum, corr_strength, mKL);

    /* 22-pole error */
    mKL = GetKLpar(Cell.Fnum, Cell.Knum, mOrder=11L);
    mKL += dBoB11*corr_strength*x010i;
    SetKLpar(Cell.Fnum, Cell.Knum, mOrder=11, mKL);

    if (trace) printf("num= %4d name = %s Fnum = %3ld, Knum=%3ld BL/brho=% e mKl=% e\n",i,
    Cell.Elem.PName,Cell.Fnum, Cell.Knum, corr_strength, mKL);
  }

 /***********************************************************************************
  *
  ******  Set multipoles for vertical correctors           ****************
  *
  *                    x0ni w/ n = p-1 for a 2p-poles
  *
  ***********************************************************************************/

  x0i   = 1.0/35e-3;  /* 1/radius */
  x02i  = x0i*x0i;
  x03i  = x02i*x0i;
  x04i  = x02i*x02i;
  x05i  = x04i*x0i;
  x06i  = x03i*x03i;
  x010i = x05i*x05i;

  dBoB5  = -0.430*1;  /* decapole */
  dBoB7  =  0.063*1;  /* 14-poles */
  dBoB11 =  0.037*1;  /* 22-poles */

  brho = globval.Energy/0.299792458; /* magnetic rigidity */
  conv = 4.642e-4;  /*conversion des A en T.m*/


  /* open V corrector file */
  if ((fi = fopen(fic_vcorr,"r")) == NULL)
  {
    fprintf(stderr, "Error while opening file %s \n",fic_vcorr);
    exit(1);
  }

  for (i = 0; i < nvcorr; i++){
    fscanf(fi,"%le\n", &vcorr[i]);
  }
  fclose(fi); /* close V corrector file */

//  for (i = 0; i < nvcorr; i++)
//  {
//    getelem(vcorrlist[i], &Cell);
//    corr_strength = vcorr[i]*conv/brho;
//
//    /* skew decapole error */
//    mKL = dBoB5*corr_strength*x04i;
//    SetKLpar(Cell.Fnum, Cell.Knum, mOrder=-5L, mKL);
//
//    if (trace) printf("num= %4d name = %s Fnum = %3ld, Knum=%3ld BL/brho=% e mKl=% e\n",i,
//                Cell.Elem.PName,Cell.Fnum, Cell.Knum, corr_strength, mKL);
//    /* skew 14-pole error */
//    mKL = dBoB7*corr_strength*x06i;
//    SetKLpar(Cell.Fnum, Cell.Knum, mOrder=-7L, mKL);
//
//    if (trace) printf("num= %4d name = %s Fnum = %3ld, Knum=%3ld BL/brho=% e mKl=% e\n",i,
//             Cell.Elem.PName,Cell.Fnum, Cell.Knum, corr_strength, mKL);
//
//    /* skew 22-pole error */
//    mKL = dBoB11*corr_strength*x010i;
//    SetKLpar(Cell.Fnum, Cell.Knum, mOrder=-11L, mKL);
//
//    if (trace) printf("num= %4d name = %s Fnum = %3ld, Knum=%3ld BL/brho=% e mKl=% e\n",i,
//                Cell.Elem.PName,Cell.Fnum, Cell.Knum, corr_strength, mKL);
//  }

 for (i = 0; i < nvcorr; i++)
 {
   getelem(vcorrlistThick[i], &Cell);
   corr_strength = vcorr[i]*conv/brho;

   /* skew decapole error */
   mKL = GetKLpar(Cell.Fnum, Cell.Knum, mOrder=-5L);
   mKL += dBoB5*corr_strength*x04i;
   SetKLpar(Cell.Fnum, Cell.Knum, mOrder=-5L, mKL);

   if (trace) printf("num= %4d name = %s Fnum = %3ld, Knum=%3ld BL/brho=% e mKl=% e\n",i,
   Cell.Elem.PName,Cell.Fnum, Cell.Knum, corr_strength, mKL);

   /* skew 14-pole error */
   mKL = GetKLpar(Cell.Fnum, Cell.Knum, mOrder=-7L);
   mKL += dBoB7*corr_strength*x06i;
   SetKLpar(Cell.Fnum, Cell.Knum, mOrder=-7L, mKL);

   if (trace) printf("num= %4d name = %s Fnum = %3ld, Knum=%3ld BL/brho=% e mKl=% e\n",i,
   Cell.Elem.PName,Cell.Fnum, Cell.Knum, corr_strength, mKL);

   /* skew 22-pole error */
   mKL = GetKLpar(Cell.Fnum, Cell.Knum, mOrder=-11L);
   mKL += dBoB11*corr_strength*x010i;
   SetKLpar(Cell.Fnum, Cell.Knum, mOrder=-11L, mKL);

   if (trace) printf("num= %4d name = %s Fnum = %3ld, Knum=%3ld BL/brho=% e mKl=% e\n",i,
   Cell.Elem.PName,Cell.Fnum, Cell.Knum, corr_strength, mKL);
 }
 /***********************************************************************************
  *
  ******                Set multipoles for skew quadripole           ****************
  *
  *                        x0ni w/ n = p-2 for a 2p-poles
  *
  ***********************************************************************************/

 /* Set multipoles for skew quad */
  x0i   = 1.0/35e-3;  /* 1/radius */
  x02i  = x0i*x0i;

  dBoB4  = -0.680*1;  /* Octupole */

  /* open skew quaI (A) *
310
450
500
520
540
550
560
d file */

  // brho = 2.75/0.299792458; /* magnetic rigidity */
   brho = globval.Energy/0.299792458; /* magnetic rigidity */
   conv = 93.83e-4;  /*conversion des A en T*/


  if ((fi = fopen(fic_skew,"r")) == NULL)
  {
    fprintf(stderr, "Error while opening file %s \n",fic_skew);
    exit(1);
  }

  for (i = 0; i < nqcorr; i++)
  {
    fscanf(fi,"%le \n", &qcorr[i]);
  }
  fclose(fi); /* close skew quad file */

//  for (i = 0; i < nqcorr; i++)
//  {
//    getelem(qcorrlist[i], &Cell);
//
//    /* skew octupole */
//    mKL = dBoB4*qcorr[i]*conv/brho*x02i;
//    SetKLpar(Cell.Fnum, Cell.Knum, mOrder=-4L, mKL);
//
//    if (trace) printf("num= %4d name = %s Fnum = %3ld, Knum=%3ld BL/brho=% e mKl=% e\n",i,
//                Cell.Elem.PName,Cell.Fnum, Cell.Knum, corr_strength, mKL);
//  }
 for (i = 0; i < nqcorr; i++)
 {
   getelem(qcorrlist[i], &Cell);

   /* skew octupole */
   mKL = GetKLpar(Cell.Fnum, Cell.Knum, mOrder=-4L);
   mKL += dBoB4*qcorr[i]*conv/brho*x02i;
   SetKLpar(Cell.Fnum, Cell.Knum, mOrder=-4L, mKL);

   if (trace) printf("num= %4d name = %s Fnum = %3ld, Knum=%3ld BL/brho=% e mKl=% e\n",i,
   Cell.Elem.PName,Cell.Fnum, Cell.Knum, corr_strength, mKL);
 }
}

/****************************************************************************/
/* void Multipole_thinsext(void)

   Purpose:
       Set multipole in dipoles, quadrupoles, thin sextupoles, skew quadrupole,
           horizontal and vertical corrector.

   Input:
       none

   Output:
       none

   Return:
       none

   Global variables:
       trace

   Specific functions:
       getelem, SetKLpar, GetKpar

   Comments:
       Test for short and long quadrupole could be changed using the length
       instead of the name. Maybe more portable, in particular if periodicity
       is broken
       Should be rewritten because list already exists now ..

****************************************************************************/

void Multipole_thinsext(char const *fic_hcorr, char const *fic_vcorr, char const *fic_skew)
{
  int i = 0;
  int ndip  = 0,  /* Number of dipoles */
      nquad = 0,  /* Number of quadrupoles */
      nsext = 0,  /* Number of sextupoles  */
      nhcorr= 0,  /* Number of horizontal correctors */
      nvcorr= 0,  /* Number of vertical correctors */
      nqcorr= 0;  /* Number of skew quadrupoles */

  int dlist[500];     /* dipole list */
  int qlist[500];     /* Quadrupole list */
  int slist[500];     /* Sextupole list */
  int hcorrlist[120]; /* horizontal corrector list */
  int vcorrlist[120]; /* vertical corrector list */
  int qcorrlist[120]; /* skew quad list */

  CellType Cell;

  int    mOrder = 0;     /* multipole order */
  double mKL = 0.0 ;     /* multipole integrated strength */
  double corr_strength = 0.0;
  double hcorr[120], vcorr[120], qcorr[120];
  double b2 = 0.0, b3 = 0.0;
  double dBoB2 = 0.0, dBoB3 = 0.0, dBoB4 = 0.0, dBoB5 = 0.0, dBoB6 = 0.0,
         dBoB7 = 0.0, dBoB9 = 0.0, dBoB11 = 0.0, dBoB15 = 0.0, dBoB21 = 0.0,
         dBoB27;
  double  dBoB6C = 0.0,  dBoB6L = 0.0, dBoB10C = 0.0, dBoB10L = 0.0,
         dBoB14C = 0.0, dBoB14L = 0.0,  dBoB3C = 0.0,  dBoB3L = 0.0,
          dBoB4C = 0.0,  dBoB4L = 0.0;
  double x0i = 0.0, x02i = 0.0, x03i = 0.0, x04i = 0.0, x05i = 0.0,
         x06i = 0.0, x07i = 0.0, x08i = 0.0, x012i = 0.0, x010i = 0.0,
         x018i = 0.0, x024i = 0.0, x1i = 0.0;
  double theta = 0.0, brho = 0.0, conv = 0.0 ;


  FILE *fi;
/*********************************************************/

  printf("Enter multipole ... \n");

/* Make lists of dipoles, quadrupoles and  sextupoles */
  for (i = 0; i <= globval.Cell_nLoc; i++)
  {
    getelem(i, &Cell); /* get element */

    if (Cell.Elem.Pkind == Mpole)
    {
      if (fabs(Cell.Elem.M->Pirho) > 0.0)
      {
        dlist[ndip] = i;
        ndip++;
        if (trace) printf("%s % f\n",Cell.Elem.PName, Cell.Elem.M->PB[0 + HOMmax]);
      }
      else if (fabs(Cell.Elem.M->PBpar[2L + HOMmax]) > 0.0)
      {
        qlist[nquad] = i;
        nquad++;
        if (trace) printf("%s % f\n",Cell.Elem.PName, Cell.Elem.M->PBpar[2L + HOMmax]);
      }
      else if (fabs(Cell.Elem.M->PBpar[3L + HOMmax]) > 0.0)
      {
        slist[nsext] = i;
        nsext++;
        if (trace) printf("%s % f\n",Cell.Elem.PName, Cell.Elem.M->PBpar[3L + HOMmax]);
      }
      else if ( Cell.Elem.PName[0] == 'c' && Cell.Elem.PName[1] == 'h')
      {
        hcorrlist[nhcorr] = i;
        nhcorr++;
        if (trace) printf("%s \n",Cell.Elem.PName);
      }
      else if ( Cell.Elem.PName[0] == 'c' && Cell.Elem.PName[1] == 'v')
      {
        vcorrlist[nvcorr] = i;
        nvcorr++;
        if (trace) printf("%s \n",Cell.Elem.PName);
      }
      else if ( Cell.Elem.PName[0] == 'q' && Cell.Elem.PName[1] == 't')
      {
        qcorrlist[nqcorr] = i;
        nqcorr++;
        if (trace) printf("%s \n",Cell.Elem.PName);
      }
    }
  }

 if (!trace) printf("Elements: ndip=%d nquad=%d  nsext=%d nhcorr=%d nvcorr=%d nqcorr=%d\n",
                     ndip,nquad,nsext,nhcorr,nvcorr,nqcorr);

 /***********************************************************************************/
 /*                                                                                 */
 /***********                Set multipoles for dipole               ****************/
 /*
  *                        x0ni w/ n = p-1 for a 2p-poles
  */
 /***********************************************************************************/

  x0i   = 1.0/20e-3;  /* 1/radius */
  x02i  = x0i*x0i;
  x03i  = x02i*x0i;
  x04i  = x02i*x02i;
  x05i  = x04i*x0i;
  x06i  = x03i*x03i;
  x07i  = x06i*x0i;

  dBoB2 =  1.7e-4*0;  /* gradient */
  dBoB3 = -3.7e-4*0;  /* hexapole */
  dBoB4 = -4.1e-5*0;  /* octupole */
  dBoB5 = -9.6e-5*0;  /* decapole */
  dBoB6 = -5.7e-5*0;  /* 12-poles */
  dBoB7 = -4.3e-5*0;  /* 14-poles */

 for (i = 0; i < ndip; i++)
 {
   getelem(dlist[i], &Cell);
   theta = Cell.Elem.PL*Cell.Elem.M->Pirho;

   /* gradient error */
   mKL = dBoB2*theta*x0i;
   SetKLpar(Cell.Fnum, Cell.Knum, mOrder=2L, mKL);

   if (trace) printf("num= %4d name = %s Fnum = %3ld, Knum=%3ld theta=% e mKl=% e\n",i,
               Cell.Elem.PName,Cell.Fnum, Cell.Knum, theta, mKL);

   /* sextupole error */
   mKL = dBoB3*theta*x02i;
   SetKLpar(Cell.Fnum, Cell.Knum, mOrder=3L, mKL);

   /* octupole error */
   mKL = dBoB4*theta*x03i;
   SetKLpar(Cell.Fnum, Cell.Knum, mOrder=4L, mKL);

   /* decapole error */
   mKL = dBoB5*theta*x04i;
   SetKLpar(Cell.Fnum, Cell.Knum, mOrder=5L, mKL);

   /* 12-pole error */
   mKL = dBoB6*theta*x05i;
   SetKLpar(Cell.Fnum, Cell.Knum, mOrder=6L, mKL);

   /* 14-pole error */
   mKL = dBoB7*theta*x06i;
   SetKLpar(Cell.Fnum, Cell.Knum, mOrder=7L, mKL);
 }

 /***********************************************************************************/
 /*                                                                                 */
 /***********                Set multipoles for quadripole           ****************/
 /*
  *                          x0ni w/ n = p-2 for a 2p-poles
  */
 /***********************************************************************************/

 x0i  = 1.0/30e-3;       /* 1/Radius in meters */
 b2   = 0.0;             /* Quadrupole strength */
 x02i = x0i*x0i;
 x04i = x02i*x02i;       /* 10-poles */
 x08i = x04i*x04i;       /* 20-poles */
 x012i= x08i*x04i;       /* 28-poles */

 dBoB6C  =  2.4e-4*1;
 dBoB10C =  0.7e-4*1;
 dBoB14C =  0.9e-4*1;
 dBoB6L  =  0.7e-4*1;
 dBoB10L =  1.9e-4*1;
 dBoB14L =  1.0e-4*1;


 x1i  = 1.0/30e-3;      /* rayon reference = 30 mm pour mesure sextupole et octupole*/
 dBoB3L  =   2.9e-4*1;   /* sextupole qpole long */
 dBoB4L  =  -8.6e-4*1;  /* octupole qpole long */
 dBoB3C  =  -1.6e-4*1;  /* sextupole qpole court */
 dBoB4C  =  -3.4e-4*1;  /* octupole qpole court */


 for (i = 0; i < nquad; i++)
 {
   getelem(qlist[i], &Cell);
   b2 = Cell.Elem.PL*GetKpar(Cell.Fnum, Cell.Knum, 2L);

   /* 12-pole multipole error */
   if ((strncmp(Cell.Elem.PName,"qp2",3)==0) || (strncmp(Cell.Elem.PName,"qp7",3)==0))
      mKL= b2*dBoB6L*x04i;
   else
      mKL= b2*dBoB6C*x04i;
   SetKLpar(Cell.Fnum, Cell.Knum, mOrder=6L, mKL);
   if (trace) printf("num= %4d name = %s Fnum = %3ld, Knum=%3ld b2=% e mKl=% e\n",i,
               Cell.Elem.PName,Cell.Fnum, Cell.Knum, b2, mKL);

   /* 20-pole multipole error */
   if ((strncmp(Cell.Elem.PName,"qp2",3)==0) || (strncmp(Cell.Elem.PName,"qp7",3)==0))
     mKL= b2*dBoB10L*x08i;
   else
     mKL= b2*dBoB10C*x08i;
   SetKLpar(Cell.Fnum, Cell.Knum, mOrder=10L, mKL);
   if (trace) printf("num= %4d name = %s Fnum = %3ld, Knum=%3ld b2=% e mKl=% e\n",i,
               Cell.Elem.PName,Cell.Fnum, Cell.Knum, b2, mKL);

   /* 28-pole multipole error */
   if ((strncmp(Cell.Elem.PName,"qp2",3)==0) || (strncmp(Cell.Elem.PName,"qp7",3)==0))
     mKL= b2*dBoB14L*x012i;
   else
     mKL= b2*dBoB14C*x012i;
   SetKLpar(Cell.Fnum, Cell.Knum, mOrder=14L, mKL);
   if (trace) printf("num= %4d name = %s Fnum = %3ld, Knum=%3ld b2=% e mKl=% e\n",i,
               Cell.Elem.PName,Cell.Fnum, Cell.Knum, b2, mKL);

/* sextupole mesure quadrupoles longs*/
   if ((strncmp(Cell.Elem.PName,"qp2",3)==0) || (strncmp(Cell.Elem.PName,"qp7",3)==0))
      mKL= b2*dBoB3L*x1i;
   else
      mKL= b2*dBoB3C*x1i;
   SetKLpar(Cell.Fnum, Cell.Knum, mOrder=3L, mKL);
   if (trace) printf("num= %4d name = %s Fnum = %3ld, Knum=%3ld b2=% e mKl=% e\n",i,
               Cell.Elem.PName,Cell.Fnum, Cell.Knum, b2, mKL);

   /* octupole mesure quadrupoles longs*/
   if ((strncmp(Cell.Elem.PName,"qp2",3)==0) || (strncmp(Cell.Elem.PName,"qp7",3)==0))
      mKL= b2*dBoB4L*x1i*x1i;
   else
      mKL= b2*dBoB4C*x1i*x1i;
   SetKLpar(Cell.Fnum, Cell.Knum, mOrder=4L, mKL);
   if (trace) printf("num= %4d name = %s Fnum = %3ld, Knum=%3ld b2=% e mKl=% e\n",i,
               Cell.Elem.PName,Cell.Fnum, Cell.Knum, b2, mKL);

 }

 /***********************************************************************************/
 /*                                                                                 */
 /***********              Set multipoles for sextupole              ****************/
 /*
  *                        x0ni w/ n = p-3 for a 2p-poles
  */
 /***********************************************************************************/

  b3    = 0.0;
  x0i   = 1.0/32e-3;
  x02i  = x0i*x0i;
  x04i  = x02i*x02i;
  x06i  = x04i*x02i;   /* 18-poles */
  x012i = x06i*x06i;   /* 30-poles */
  x018i = x012i*x06i;  /* 42-poles */
  x024i = x012i*x012i; /* 54-poles */

  dBoB9  =  -4.7e-4*1;
  dBoB15 =  -9.0e-4*1;
  dBoB21 =  -20.9e-4*1;
  dBoB27 =  0.8e-4*1 ;
/*
  dBoB9  =  3.1e-3*1;
  dBoB15 =  5.0e-4*1;
  dBoB21 =  -2.0e-2*1;
  dBoB27 =  1.1e-2*1;
*/

 for (i = 0; i < nsext; i++)
 {
   getelem(slist[i], &Cell);
   b3 = GetKpar(Cell.Fnum, Cell.Knum, 3L);

   /* 18-pole multipole error */
   mKL= b3*dBoB9*x06i;
   SetKLpar(Cell.Fnum, Cell.Knum, mOrder=9L, mKL);
   if (trace) printf("num= %4d name = %s Fnum = %3ld, Knum=%3ld b3=% e mKl=% e\n",i,
               Cell.Elem.PName,Cell.Fnum, Cell.Knum, b3, mKL);

   /* 30-pole multipole error */
   mKL= b3*dBoB15*x012i;
   SetKLpar(Cell.Fnum, Cell.Knum, mOrder=15L, mKL);
   if (trace) printf("num= %4d name = %s Fnum = %3ld, Knum=%3ld b3=% e mKl=% e\n",i,
               Cell.Elem.PName,Cell.Fnum, Cell.Knum, b3, mKL);

   /* 42-pole multipole error */
   mKL= b3*dBoB21*x018i;
   SetKLpar(Cell.Fnum, Cell.Knum, mOrder=21L, mKL);
   if (trace) printf("num= %4d name = %s Fnum = %3ld, Knum=%3ld b3=% e mKl=% e\n",i,
               Cell.Elem.PName,Cell.Fnum, Cell.Knum, b3, mKL);

   /* 54-pole multipole error */
   mKL= b3*dBoB27*x024i;
   SetKLpar(Cell.Fnum, Cell.Knum, mOrder=27L, mKL);
   if (trace) printf("num= %4d name = %s Fnum = %3ld, Knum=%3ld b3=% e mKl=% e\n",i,
               Cell.Elem.PName,Cell.Fnum, Cell.Knum, b3, mKL);
}

 /***********************************************************************************/
 /*                                                                                 */
 /******            Set multipoles for horizontal correctors         ****************/
 /*
  *                x0ni w/ n = p-1 for a 2p-poles
  */
 /***********************************************************************************/
  x0i   = 1.0/35e-3;  /* 1/radius */
  x02i  = x0i*x0i;
  x03i  = x02i*x0i;
  x04i  = x02i*x02i;
  x05i  = x04i*x0i;
  x06i  = x03i*x03i;
  x010i = x05i*x05i;

  dBoB5  = 0.430*1;  /* decapole */
  dBoB7  = 0.063*1;  /* 14-poles */
  dBoB11 =-0.037*1;  /* 22-poles */

  brho = 2.75/0.299792458; /* magnetic rigidity */
  conv = 8.14e-4;  /*conversion des A en T.m*/

  /* open H corrector file */
  if ((fi = fopen(fic_hcorr,"r")) == NULL)
  {
    fprintf(stdout, "Error while opening file %s \n",fic_hcorr);
    exit_(1);
  }

  for (i = 0; i < nhcorr; i++)
  {
    fscanf(fi,"%le \n", &hcorr[i]);
  }
  fclose(fi); /* close H corrector file */

 for (i = 0; i < nhcorr; i++)
 {
   getelem(hcorrlist[i], &Cell);
   corr_strength = hcorr[i]*conv/brho;

   /* gradient error */
   mKL = dBoB5*corr_strength*x04i;
   SetKLpar(Cell.Fnum, Cell.Knum, mOrder=5L, mKL);

   if (trace) printf("num= %4d name = %s Fnum = %3ld, Knum=%3ld BL/brho=% e mKl=% e\n",i,
               Cell.Elem.PName,Cell.Fnum, Cell.Knum, corr_strength, mKL);
   /* 14-pole error */
   mKL = dBoB7*corr_strength*x06i;
   SetKLpar(Cell.Fnum, Cell.Knum, mOrder=7L, mKL);

   if (trace) printf("num= %4d name = %s Fnum = %3ld, Knum=%3ld BL/brho=% e mKl=% e\n",i,
            Cell.Elem.PName,Cell.Fnum, Cell.Knum, corr_strength, mKL);

   /* 22-pole error */
   mKL = dBoB11*corr_strength*x010i;
   SetKLpar(Cell.Fnum, Cell.Knum, mOrder=11, mKL);

   if (trace) printf("num= %4d name = %s Fnum = %3ld, Knum=%3ld BL/brho=% e mKl=% e\n",i,
               Cell.Elem.PName,Cell.Fnum, Cell.Knum, corr_strength, mKL);
 }

 /***********************************************************************************/
 /*                                                                                 */
 /******            Set multipoles for vertical correctors           ****************/
 /*
  *                    x0ni w/ n = p-1 for a 2p-poles
  */
 /***********************************************************************************/

  x0i   = 1.0/35e-3;  /* 1/radius */
  x02i  = x0i*x0i;
  x03i  = x02i*x0i;
  x04i  = x02i*x02i;
  x05i  = x04i*x0i;
  x06i  = x03i*x03i;
  x010i = x05i*x05i;

  dBoB5  = -0.430*1;  /* decapole */
  dBoB7  =  0.063*1;  /* 14-poles */
  dBoB11 =  0.037*1;  /* 22-poles */

  brho = 2.75/0.299792458; /* magnetic rigidity */
  conv = 4.642e-4;  /*conversion des A en T.m*/

  /* open V corrector file */
  if ((fi = fopen(fic_vcorr,"r")) == NULL)
  {
    fprintf(stdout, "Error while opening file %s \n",fic_vcorr);
    exit_(1);
  }

  for (i = 0; i < nvcorr; i++)
  {
    //   fscanf(fi,"%s %le %le %le \n", dummy,&dummyf,&dummyf,&vcorr[i]);
    fscanf(fi,"%le\n", &vcorr[i]);
}
  fclose(fi); /* close V corrector file */

 for (i = 0; i < nvcorr; i++)
 {
   getelem(vcorrlist[i], &Cell);
   corr_strength = vcorr[i]*conv/brho;

   /* skew decapole error */
   mKL = dBoB5*corr_strength*x04i;
   SetKLpar(Cell.Fnum, Cell.Knum, mOrder=-5L, mKL);

   if (trace) printf("num= %4d name = %s Fnum = %3ld, Knum=%3ld BL/brho=% e mKl=% e\n",i,
               Cell.Elem.PName,Cell.Fnum, Cell.Knum, corr_strength, mKL);
   /* skew 14-pole error */
   mKL = dBoB7*corr_strength*x06i;
   SetKLpar(Cell.Fnum, Cell.Knum, mOrder=-7L, mKL);

   if (trace) printf("num= %4d name = %s Fnum = %3ld, Knum=%3ld BL/brho=% e mKl=% e\n",i,
            Cell.Elem.PName,Cell.Fnum, Cell.Knum, corr_strength, mKL);

   /* skew 22-pole error */
   mKL = dBoB11*corr_strength*x010i;
   SetKLpar(Cell.Fnum, Cell.Knum, mOrder=-11, mKL);

   if (trace) printf("num= %4d name = %s Fnum = %3ld, Knum=%3ld BL/brho=% e mKl=% e\n",i,
               Cell.Elem.PName,Cell.Fnum, Cell.Knum, corr_strength, mKL);
 }

 /***********************************************************************************/
 /*                                                                                 */
 /******                Set multipoles for skew quadripole           ****************/
 /*
  *                        x0ni w/ n = p-2 for a 2p-poles
  */
 /***********************************************************************************/

 /* Set multipoles for skew quad */
  x0i   = 1.0/35e-3;  /* 1/radius */
  x02i  = x0i*x0i;

  dBoB4  = -0.680*1;  /* Octupole */

  /* open skew quaI (A) *
310
450
500
520
540
550
560
d file */

  brho = 2.75/0.299792458; /* magnetic rigidity */
  conv = 93.83e-4;  /*conversion des A en T*/


  /* open skew quad file */
  if ((fi = fopen(fic_skew,"r")) == NULL)
  {
    fprintf(stdout, "Error while opening file %s \n",fic_skew);
    exit_(1);
  }

  for (i = 0; i < nqcorr; i++)
  {
    fscanf(fi,"%le \n", &qcorr[i]);
  }
  fclose(fi); /* close skew quad file */

 for (i = 0; i < nqcorr; i++)
 {
   getelem(qcorrlist[i], &Cell);

   /* skew octupole */
   mKL = dBoB4*qcorr[i]*conv/brho*x02i;
   SetKLpar(Cell.Fnum, Cell.Knum, mOrder=-4L, mKL);

   if (trace) printf("num= %4d name = %s Fnum = %3ld, Knum=%3ld BL/brho=% e mKl=% e\n",i,
               Cell.Elem.PName,Cell.Fnum, Cell.Knum, corr_strength, mKL);
 }
}

/****************************************************************************/
/* void SetSkewQuad(void)

   Purpose:
       Set SkewQuad in normal quadrupole
       The name of each quadrupole has to be unique

   Input:
       none

   Output:
       none

   Return:
       none

   Global variables:
       trace

   Specific functions:
       GetElem, SetKLpar, GetKpar

   Comments:
       none

****************************************************************************/
void SetSkewQuad(void)
{
  FILE *fi;
  const char fic_skew[] = "QT-solamor_2_3.dat";
  int i;
  double theta[500]; /* array for skew quad tilt*/
  double b2, mKL;
  CellType Cell;
  long mOrder;

  int nquad = 0;  /* Number of skew quadrupoles */
  int qlist[500];  /* Quadrupole list */

  /* make quadrupole list */
  for (i = 0; i <= globval.Cell_nLoc; i++)
  {
    getelem(i, &Cell); /* get element */

    if (Cell.Elem.Pkind == Mpole)
    {
      if (fabs(Cell.Elem.M->PBpar[2L + HOMmax]) > 0.0)
      {
        qlist[nquad] = i;
        nquad++;
        if (trace) printf("%s % f\n",Cell.Elem.PName,
                           Cell.Elem.M->PBpar[2L + HOMmax]);
      }
    }
  }

  /* open skew quad file */
  if ((fi = fopen(fic_skew,"r")) == NULL)
  {
    fprintf(stdout, "Error while opening file %s \n",fic_skew);
    exit_(1);
  }

  /* read tilt in radians */
  for (i = 0; i < nquad; i++)
  {
    fscanf(fi,"%le \n", &theta[i]);
    theta[i+1] = theta[i];
    i++;
  }
  fclose(fi);


  for (i = 0; i < nquad; i++)
  {
    if (trace) fprintf(stdout,"%le \n", theta[i]);

    getelem(qlist[i], &Cell);

    /* Get KL for a quadrupole */
    b2 = Cell.Elem.PL*GetKpar(Cell.Fnum, Cell.Knum, 2L);

    mKL = b2*sin(2*theta[i]);
    SetKLpar(Cell.Fnum, Cell.Knum, mOrder=-2L, mKL);
    mKL = b2*cos(2*theta[i]);
    SetKLpar(Cell.Fnum, Cell.Knum, mOrder=2L, mKL);

    if (trace) printf("num= %4d name = %s Fnum = %3ld, Knum=%3ld KL=% e, KtiltL=% e\n"
                ,i,
                Cell.Elem.PName,Cell.Fnum, Cell.Knum,
                Cell.Elem.M->PBpar[HOMmax+2],
                Cell.Elem.M->PBpar[HOMmax-2]);
 }
}

/****************************************************************************/
/* void SetDecapole(void)

   Purpose:
       Set decapole in horizontal correctors

   Input:
       none

   Output:
       none

   Return:
       none

   Global variables:
       trace

   Specific functions:
       GetElem, SetKLpar, GetKpar

   Comments:
       none

****************************************************************************/
// void SetDecapole(void)
// {
//   FILE *fi;
//   const char fic_deca[] ="/home/nadolski/soltracy/deca.dat";
//   int i;
//   double mKL[56]; /* array for skew quad tilt*/
//   CellType Cell;
//   long mOrder=5L;


//   /* open skew quad file */
//   if ((fi = fopen(fic_deca,"r")) == NULL){
//     fprintf(stderr, "Error while opening file %s \n",fic_deca);
//     exit(1);
//   }

//   /* read decapole strength */
//   for (i = 0; i < globval.hcorr; i++){
//     fscanf(fi,"%le \n", &mKL[i]);
//   }
//   fclose(fi);

//   for (i = 0; i < globval.hcorr; i++){
//     if (trace) fprintf(stdout,"%le \n", mKL[i]);

//     getelem(globval.hcorr_list[i], &Cell);
//     SetKLpar(Cell.Fnum, Cell.Knum, mOrder, mKL[i]);

//     if (trace) printf("num= %4d name = %s Fnum = %3ld, Knum=%3ld KL=% e, KtiltL=% e\n"
//                 ,i,
//                 Cell.Elem.PName,Cell.Fnum, Cell.Knum,
//                 Cell.Elem.M->PBpar[HOMmax+mOrder],
//                 Cell.Elem.M->PBpar[HOMmax-mOrder]);
//  }
// }

/****************************************************************************/
/* void MomentumAcceptance(double deb, double fin,
                           double ep_min, double ep_max, long nstepp,
                           double em_min, double em_max, long nstepm,
                           long nnames  , char names[])
   Purpose:
        Compute momemtum acceptance along the ring, track the particle with
	different energy, momentum acceptance is the energy when the particle
	is lost or the last energy if the particle is not lost.

         Based on the version in tracy 2.

   Input:
       sdeb     minimum position for momentum acceptance,"debut" is beginning in French
       sfin     maximum position for momentum acceptance,"fin"   is end in French

       ep_min   minimum energy deviation for positive momentum acceptance
       ep_max   maximum energy deviation for positive momentum acceptance
       nstepp   number of energy steps for positive momentum acceptance

       em_min   minimum energy deviation for negative momentum acceptance
       em_max   maximum energy deviation for negative momentum acceptance
       nstepm   number of energy steps for negative momentum acceptance
       
       nnames   number of families or types of elements for calculations
       names    name of the families or types of elements for calculations

       * 1 grande section droite
       * 13 entree premier bend
       * 22 sortie SX4
       * 41 section droite moyenne
       * 173 fin superperiode

   Output:
       output file momAccept.out : file of results
       output file momAcceptPhase.out : file of tracking results during the process

   Return:
       none

   Global variables:
       none


   Comments:
       30/06/03 add fflush(NULL) to force writing at the end to correct
                unexpected bug: rarely the output file is not finished
       31/07/03 add closed orbit a element: useful for 6D tracking
                delta_closed_orbite = dp(cavity)/2
       21/10/03 add array for vertical initial conditions using tracking
                removed choice of tracking: now this should be done outside

       23/07/10  modify the call variable to the Cell_Pass( ): j-1L --> j (L3435, L3590)
	         since the Cell_Pass( ) is tracking from element i0 to i1(tracy 3), and
		       the Cell_Pass( ) is tracking from element i0+1L to i1(tracy 2).

****************************************************************************/
void MomentumAcceptance(long nturn, double sdeb, double sfin, double ep_min, double ep_max,
			long nstepp, double em_min, double em_max, long nstepm, long nnames, char names[6][max_str])
{
  double        dP = 0.0, dp1 = 0.0, dp2 = 0.0;
  long          lastpos = 0L, lastn = 0L, type_mo[6], fam_mo[6], num_points = 0L, Fnum=0L;
  long          i = 0L, j = 0L, pos = 0L, type_jj=0L, fam_jj=0L, vec_ind[Cell_nLocMax];
  double        x = 0.0, px = 0.0, z = 0.0, pz = 0.0, ctau0 = 0.0, delta = 0.0;
  Vector        x0;
  FILE          *outf2, *outf1;
  // Nonzero vertical amplitude
  const double  zmax = 0.3e-4; // 30 um at each element
  struct tm     *newtime;  // for time
  bool          calc_ind, trace=true, all_elem=false;

  x0.zero();

  /* Get time and date */
  newtime = GetTime();
// Determine which families or types of elements will be used to calculations;
for (i = 0L; i < nnames; i++){
      if (strcmp("all", names[i]) == 0) {
            all_elem = true;
      } else if (strcmp("dip", names[i]) == 0) {
            type_mo[type_jj] = Dip;
            type_jj++;
      } else if (strcmp("quad", names[i]) == 0) {
            type_mo[type_jj] = Quad;
            type_jj++;
      } else if (strcmp("sext", names[i]) == 0) {
            type_mo[type_jj] = Sext;
            type_jj++;
      } else if (strcmp("corr", names[i]) == 0) { 
            type_mo[type_jj] = Corr;
            type_jj++;
      } else {
            Fnum = ElemIndex(names[i]);
            if(Fnum > 0){
                fam_mo[fam_jj]=Fnum;
                fam_jj++;
            }
            else
                printf("SetFieldErrors: undefined element %s\n", names[i]);
      }
}

// Find out the indices of the elements to calculate the mom_accep.
for (i = 0L; i < globval.Cell_nLoc; i++){
    if (Cell[i].S > sfin){
        break;
    } else if (Cell[i].S >= sdeb) {
	    calc_ind = all_elem;
        for (j = 0L; j < type_jj; j++){
            calc_ind = (calc_ind || ( (Cell[i].Elem.Pkind == Mpole) && (Cell[i].Elem.M->n_design == type_mo[j]) ));
        }
        for (j = 0L; j < fam_jj; j++){
            calc_ind = (calc_ind || ( Cell[i].Fnum == fam_mo[j] ));
        }
        if ( calc_ind ){
            vec_ind[num_points] = i;
            num_points++;
        }
    }
}

  /* File opening for writing */

  outf1 = fopen("momAcceptPhase.out", "w");
  outf2 = fopen("momAccept.out", "w");

  fprintf(outf2,"# TRACY III v. SYNCHROTRON LNLS -- %s \n", asctime2(newtime));
  fprintf(outf2,"#  name        s        dp     s_lost    name_lost  plane_lost(1=x,2=y)   turn_lost\n#\n");

  fprintf(outf1,"# TRACY III v. SYNCHROTRON LNLS -- %s \n", asctime2(newtime));
  fprintf(outf1,"#  i        x           xp            z           zp           dp          ctau\n#\n");


  /***************************************************************/
  fprintf(stdout,"\nBeginning calculation of momentum acceptance for %ld elements \n\n", num_points);
  /***************************************************************/
  fprintf(stdout,"Computing positive momentum acceptance ... \n");
  /***************************************************************/
  fprintf(stdout,"#  name       s          dp    \n"); 
  
  for ( j = 0L; j < num_points; j++ ){
  
    pos = vec_ind[j];
    getcod(dP=0.0, lastpos);       /* determine closed orbit */

    // coordinates around closed orbit which is non zero for 6D tracking
    x     = Cell[pos].BeamPos[0];
    px    = Cell[pos].BeamPos[1];
    z     = Cell[pos].BeamPos[2] + zmax;
    pz    = Cell[pos].BeamPos[3];
    delta = Cell[pos].BeamPos[4];
    ctau0 = Cell[pos].BeamPos[5];
    //fprintf(stdout,"%3ld %6.4g %6.4g %6.4g %6.4g %6.4g %6.4g\n",
    //        pos, x, px, z, pz, delta, ctau0);

    dp1 = 0.0;
    dp2 = 0.0;
    i   = 0L;

    do /* Tracking over nturn */
    {
      i++;
      dp1 = dp2;

      if (nstepp != 1L)
        dp2= ep_max - (nstepp - i)*(ep_max - ep_min)/(nstepp - 1L);
      else
        dp2 = ep_max;
    
    // Calcula a abertura em momemtum no final do elemento (pos+1L);
      Trac(x, px, z, pz, dp2+delta , ctau0, nturn, pos+1L, lastn, lastpos, outf1);
    }while (((lastn) == nturn) && (i != nstepp));

    if ((lastn) == nturn)
      dp1 = dp2;

    fprintf(stdout,"  %-7s %10.5f %10.5f\n", Cell[pos].Elem.PName, Cell[pos].S, dp1);
    fprintf(outf2,"  %-7s %10.5f %8.5f %10.5f   %-8s           %-10d   %6ld\n", Cell[pos].Elem.PName,
        Cell[pos].S, dp1, Cell[lastpos].S, Cell[lastpos].Elem.PName,status.lossplane, lastn);

  }

  /***************************************************************/
  /***************************************************************/
  // NEGATIVE MOMENTUM ACCEPTANCE
  /***************************************************************/
  /***************************************************************/

  fprintf(outf2,"\n"); /* A void line */


  /***************************************************************/
  fprintf(stdout,"\nComputing negative momentum acceptance ... \n");
  /***************************************************************/
  fprintf(stdout,"#  name       s          dp    \n");
  
for ( j = 0L; j < num_points; j++ ){
    pos = vec_ind[j];
    getcod(dP=0.0, lastpos);       /* determine closed orbit */

    // coordinates around closed orbit which is non zero for 6D tracking
    x     = Cell[pos].BeamPos[0];
    px    = Cell[pos].BeamPos[1];
    z     = Cell[pos].BeamPos[2] + zmax;
    pz    = Cell[pos].BeamPos[3];
    delta = Cell[pos].BeamPos[4];
    ctau0 = Cell[pos].BeamPos[5];
    // fprintf(stdout,"%3ld %6.4g %6.4g %6.4g %6.4g %6.4g %6.4g\n",
    //        pos, x, px, z, pz, delta, ctau0);

    dp1 = 0.0;
    dp2 = 0.0;
    i   = 0L;
    do /* Tracking over nturn */
    {
      i++;
      dp1 = dp2;
      if (nstepm != 1L) {
        dp2= em_max - (nstepm - i)*(em_max - em_min)/(nstepm - 1L);
      }
      else {
        dp2 = em_max;
      }

    // Calcula a abertura em momemtum no final do elemento (pos+1L);
      Trac(x, px, z, pz, dp2+delta, ctau0, nturn, pos+1L, lastn, lastpos, outf1);
      
    }while (((lastn) == nturn) && (i != nstepm));

    if ((lastn) == nturn) dp1 = dp2;
    
    fprintf(stdout,"  %-7s %10.5f %10.5f\n", Cell[pos].Elem.PName, Cell[pos].S, dp1);
    fprintf(outf2,"  %-7s %10.5f %8.5f %10.5f   %-8s           %-10d   %6ld\n", Cell[pos].Elem.PName,
        Cell[pos].S, dp1, Cell[lastpos].S, Cell[lastpos].Elem.PName,status.lossplane, lastn);
}

  fflush(NULL); // force writing at the end (BUG??)
  fclose(outf1);
  fclose(outf2);
}

/****************************************************************************/
/* set_vectorcod(double codvector[Cell_nLocMax][6], double dP)

   Purpose:
      Store closed orbit computed for a Dp energy offset

   Input:
       dP  offset energy

   Output:
       codvector : closed orbit all around the ring

   Return:
       none

   Global variables:
       status

   Specific functions:
       getcod

   Comments:
       Does not work for a transfer line

****************************************************************************/
void set_vectorcod(Vector  codvector[], double dP)
{
  long      k = 0L, lastpos = 0L;
  CellType  Cell;
  Vector    zerovector;

  zerovector.zero();

  getcod(dP, lastpos);  /* determine closed orbit */


  if (status.codflag == 1) { /* cod exists */
    for (k = 1L; k <= globval.Cell_nLoc; k++){
      getelem(k,&Cell);
      codvector[k] = Cell.BeamPos;
    }
    // cod at entrance of the ring is the one at the exit (1-periodicity)
    CopyVec(6L, Cell.BeamPos, codvector[0]);
  }
  else { /* nostable cod */
    for (k = 1L; k <= globval.Cell_nLoc; k++)
      codvector[k] = zerovector;
  }
}

// LAURENT
/****************************************************************************/
/* void spectrum(long Nbx, long Nbz, long Nbtour, double xmax, double zmax,
   double energy, bool *status)

   Purpose:
       Compute a frequency map of Nbx x Nbz points
       For each set of initial conditions the particle is tracked over
       Nbtour for an energy offset dp

       The stepsize follows a square root law

       Results in fmap.out

   Input:
       Nbx    horizontal step number
       Nby    vertical step number
       xmax   horizontal maximum amplitude
       zmax   vertical maximum amplitude
       Nbtour number of turn for tracking
       energy particle energy offset

   Output:
       status true if stable
              false otherwise

   Return:
       none

   Global variables:
       none

   Specific functions:
       Trac_Simple, Get_NAFF

   Comments:
       15/10/03 run for the diffusion: nasty patch for retrieving the closed orbit

****************************************************************************/
void spectrum(long Nbx, long Nbz, long Nbtour, double xmax, double zmax,
              double energy, bool diffusion)
{
 FILE *xoutf, *zoutf;
 const char xfic[] = "xspectrum.out";
 const char zfic[] = "zspectrum.out";
 long i, j, k;
 #define nterm2  20
 double Tab[6][NTURN], fx[nterm2], fz[nterm2], fx2[nterm2], fz2[nterm2];
 double x = 0.0, xp = 0.0, z = 0.0, zp = 0.0;
 double x0 = 1e-6, xp0 = 0.0, z0 = 1e-6, zp0 = 0.0;
 double xstep = 0.0, zstep = 0.0;
 int nb_freq[2] = {0, 0};
 long nturn = Nbtour;
 bool status=true;
 struct tm *newtime;

 /* Get time and date */
 time_t aclock;
 time(&aclock);                 /* Get time in seconds */
 newtime = localtime(&aclock);  /* Convert time to struct */

 if (diffusion) nturn = 2*Nbtour;

// if (trace) printf("Entering fmap ... results in %s\n\n",fic);

 /* Opening file */
 if ((xoutf = fopen(xfic, "w")) == NULL) {
   fprintf(stdout, "fmap: error while opening file %s\n", xfic);
   exit_(1);
 }

 if ((zoutf = fopen(zfic, "w")) == NULL) {
   fprintf(stdout, "fmap: error while opening file %s\n", zfic);
   exit_(1);
 }

 fprintf(xoutf,"# TRACY II v. 2.6 -- %s -- %s \n", xfic, asctime2(newtime));
 fprintf(zoutf,"# TRACY II v. 2.6 -- %s -- %s \n", zfic, asctime2(newtime));
// fprintf(outf,"# nu = f(x) \n");
// fprintf(outf,"#    x[m]          z[m]           fx            fz           dfx           dfz\n");

 if ((Nbx <= 1) || (Nbz <= 1))
   fprintf(stdout,"fmap: Error Nbx=%ld Nbz=%ld\n",Nbx,Nbz);

 xp = xp0;
 zp = zp0;

 xstep = xmax/sqrt((double)Nbx);
 zstep = zmax/sqrt((double)Nbz);

 for (i = 0; i <= Nbx; i++) {
   x  = x0 + sqrt((double)i)*xstep;
   for (j = 0; j<= Nbz; j++) {
     z  = z0 + sqrt((double)j)*zstep;
     Trac_Simple4DCOD(x,xp,z,zp,energy,0.0,nturn,Tab,&status);
     if (status) {
      Get_NAFF(nterm2, Nbtour, Tab, fx, fz, nb_freq);
     }
     else {
      fx[0]  = 0.0; fz[0]  = 0.0;
      fx2[0] = 0.0; fz2[0] = 0.0;
     }

     // printout value
         if (!diffusion){

       fprintf(xoutf,"%14.6e %14.6e", x, z);
       fprintf(zoutf,"%14.6e %14.6e", x, z);
       fprintf(stdout,"%14.6e %14.6e", x, z);

       for (k = 0; k < nb_freq[0]; k++){
         fprintf(xoutf," %14.6e", fx[k]);
         fprintf(stdout," %14.6e", fx[k]);
       }

       for (k = 0; k < nb_freq[1]; k++){
         fprintf(zoutf," %14.6e", fz[k]);
         fprintf(stdout," %14.6e", fz[k]);
       }

       fprintf(stdout,"\n");
       fprintf(xoutf,"\n");
       fprintf(zoutf,"\n");
     }
//     else {
//       fprintf(outf,"%14.6e %14.6e %14.6e %14.6e %14.6e %14.6e\n",
//        x, z, fx[0], fz[0], fx[0]-fx2[0], fz[0]-fz2[0]);
//       fprintf(stdout,"%14.6e %14.6e %14.6e %14.6e %14.6e %14.6e\n",
//        x, z, fx[0], fz[0], fx[0]-fx2[0], fz[0]-fz2[0]);
//     }
   }
 }

 fclose(xoutf);
 fclose(zoutf);
}

/****************************************************************************/
/* void TracCO(double x, double px, double y, double py, double dp, double ctau,
          long nmax, long pos, long *lastn, long *lastpos, FILE *outf1)

   Purpose:
      Single particle tracking
      Same as Trac but with respect to closed orbit

   Input:
      x, px, y, py 4 transverses coordinates
      dp           energy offset
      nmax         number of turns
      pos          starting position for tracking
      aperture     global physical aperture


   Output:
      lastn       last n (should be nmax if  not lost)
      lastpos     last position in the ring

   Return:
       none

   Global variables:
       globval

   specific functions:
       Cell_Pass

   Comments:
       BUG: last printout is wrong because not at pos but at the end of the ring
       26/04/03 print output for phase space is for position pos now

****************************************************************************/
void TracCO(double x, double px, double y, double py, double dp, double ctau,
	    long nmax, long pos, long &lastn, long &lastpos, FILE *outf1)
{
  bool lostF; /* Lost particle Flag */
  Vector x1;     /* tracking coordinates */
  Vector2  aperture;
  CellType Cell;

  aperture[0] = 1e0;
  aperture[1] = 1e0;

  /* Get closed orbit */
  Ring_GetTwiss(true, 0.0);
  getcod(dp, lastpos);
  getelem(pos-1,&Cell);

  if (!trace) printf("dp= % .5e %% xcod= % .5e mm zcod= % .5e mm \n",
             dp*1e2, Cell.BeamPos[0]*1e3, Cell.BeamPos[2]*1e3);

  /* Tracking coordinates around the closed orbit */
    x1[0] =  x + Cell.BeamPos[0]; x1[1] = px   + Cell.BeamPos[1];
    x1[2] =  y + Cell.BeamPos[2]; x1[3] = py   + Cell.BeamPos[3];
    x1[4] = dp; x1[5] = ctau; // line true in 4D tracking
//    x1[4] = dp + Cell.BeamPos[4]; x1[5] = ctau + Cell.BeamPos[5];

    lastn = 0;
    lostF = true;

    (lastpos) = pos;

    if (!trace) fprintf(outf1, "\n");

    do
    {
      (lastn)++;
      if (!trace) { // print initial conditions
        fprintf(outf1, "%6ld %+10.5e %+10.5e %+10.5e %+10.5e"
		" %+10.5e %+10.5e \n",
		lastn, x1[0], x1[1], x1[2], x1[3], x1[4], x1[5]);
      }

    //  Cell_Pass(pos-1L, globval.Cell_nLoc, x1, lastpos);
      Cell_Pass(pos, globval.Cell_nLoc, x1, lastpos);
      Cell_Pass(0,pos-1L, x1, lastpos);
    }
    while (((lastn) < nmax) && ((lastpos) == pos-1L));

    if (lastpos != pos-1L)
    {
      printf("TracCO: Particle lost \n");
      fprintf(stdout, "turn=%6ld %+10.5g %+10.5g %+10.5g"
	      " %+10.5g %+10.5g %+10.5g \n",
	      lastn, x1[0], x1[1], x1[2], x1[3], x1[4], x1[5]);
    }
  }


/****************************************************************************/
/*   void getA4antidamping()

   Purpose:

   Input:
       none

   Output:
       none

   Return:
       none

   Global variables:
       none

   specific functions:
       none

   Comments:

****************************************************************************/
void getA4antidamping()
  {
  /* function to get A for anti damping condition */
  /* See publication at ALS for off momentum particle dynamics */

  CellType Cell;
  int qlist[320];
  int nquad=0, i;
  double A = 0.0;

  for (i = 0; i <= globval.Cell_nLoc; i++)
  {
    getelem(i, &Cell); /* get element */

    if (Cell.Elem.Pkind == Mpole)
    {
      if (fabs(Cell.Elem.M->PBpar[2L + HOMmax]) > 0.0)
      {
        qlist[nquad] = i;
        nquad++;
        if (!trace) printf("%s % f\n",Cell.Elem.PName, Cell.Elem.M->PBpar[2L + HOMmax]);
      }
    }
  }
  fprintf(stdout,"Nombre de quadrupoles %d\n", nquad);

  Ring_GetTwiss(true, 0.0);
  for (i = 0; i < nquad; i++)
  {
    getelem(qlist[i],&Cell);
    fprintf(stdout,"%d Name = %s L=%g A= %g etax=%g \n", i, Cell.Elem.PName, Cell.Elem.PL, A,Cell.Eta[0]);
    A += Cell.Elem.PL*2.0*(Cell.Elem.M->PBpar[2L + HOMmax]*Cell.Eta[0])*
                       (Cell.Elem.M->PBpar[2L + HOMmax]*Cell.Eta[0]);
    i++;
  }
  fprintf(stdout,"A= %g\n", A*1.706);
  }


/****************************************************************************/
/* void fmapfull(long Nbx, long Nbz, long Nbtour, double xmax, double zmax,
   double energy, bool *status)

   Purpose:
       Compute a frequency map of Nbx x Nbz points
       For each set of initial conditions the particle is tracked over
       Nbtour for an energy offset dp

       The stepsize follows a square root law

       Results in fmap.out

   Input:
       Nbx    horizontal step number
       Nby    vertical step number
       xmax   horizontal maximum amplitude
       zmax   vertical maximum amplitude
       Nbtour number of turn for tracking
       energy particle energy offset

   Output:
       status true if stable
              false otherwise

   Return:
       none

   Global variables:
       none

   Specific functions:
       Trac_Simple, Get_NAFF

   Comments:
       Note enough precision for diffusion

****************************************************************************/
#define NTERM  10
void fmapfull(long Nbx, long Nbz, long Nbtour, double xmax, double zmax,
              double energy, bool diffusion)
{
 FILE * outf;
 const char fic[] = "fmapfull.out";
 int i, j, k;
 double Tab[DIM][NTURN], Tab0[DIM][NTURN];
 double fx[NTERM], fz[NTERM], fx2[NTERM], fz2[NTERM];
 double x  = 0.0, xp = 0.0, z = 0.0, zp = 0.0;
 double x0 = 1e-6, xp0 = 0.0, z0 = 1e-6, zp0 = 0.0;
 double xstep = 0.0, zstep = 0.0;
 int nb_freq[2] = {0, 0};
 double nux1[NTERM], nuz1[NTERM],nux2[NTERM], nuz2[NTERM];
 long nturn = Nbtour;
 bool status=true;
 struct tm *newtime;
 char name[14];

 /* Get time and date */
 time_t aclock;
 time(&aclock);                 /* Get time in seconds */
 newtime = localtime(&aclock);  /* Convert time to struct */

 if (diffusion) nturn = 2*Nbtour;

 if (trace) printf("Entering fmap ... results in %s\n\n",fic);

 /* Opening file */
 if ((outf = fopen(fic, "w")) == NULL) {
   fprintf(stdout, "fmapfull: error while opening file %s\n", fic);
   exit_(1);
 }

 fprintf(outf,"# TRACY II v. 2.6 -- %s -- %s \n", fic, asctime2(newtime));
 fprintf(outf,"# Frequency map freq = f(x,z) \n");
 fprintf(outf,"#    x[m]          z[m]          ");

 for (k = 0; k < NTERM; k++){
   sprintf(name,"f%dx           ",k);
   fprintf(outf,"%s",name);
 }
 for (k = 0; k < NTERM; k++){
   sprintf(name,"f%dz           ",k);
   fprintf(outf,"%s",name);
 }

 if (!diffusion){
   fprintf(outf,"\n");
 }
 else{
   for (k = 0; k < NTERM; k++){
     sprintf(name,"df%dx          ",k);
     fprintf(outf,"%s",name);
   }
   for (k = 0; k < NTERM; k++){
     sprintf(name,"df%dz          ",k);
     fprintf(outf,"%s",name);
   }
   fprintf(outf,"\n");
 }

 if ((Nbx <= 1) || (Nbz <= 1))
   fprintf(stdout,"fmap: Error Nbx=%ld Nbz=%ld\n",Nbx,Nbz);

 xp = xp0;
 zp = zp0;

 xstep = xmax/sqrt((double)Nbx);
 zstep = zmax/sqrt((double)Nbz);

 for (i = 0; i <= Nbx; i++) {
   x  = x0 + sqrt((double)i)*xstep;
   for (j = 0; j<= Nbz; j++) {
     z  = z0 + sqrt((double)j)*zstep;
     Trac_Simple4DCOD(x,xp,z,zp,energy,0.0,nturn,Tab,&status);

     if (status) {
       Get_NAFF(NTERM, Nbtour, Tab, fx, fz, nb_freq);

       for (k = 0; k < nb_freq[0]; k++){
         nux1[k] = fx[k];
       }
       for (k = 0; k < nb_freq[1]; k++){
         nuz1[k] = fz[k];
       }
       for (k = nb_freq[0]; k < NTERM; k++){
         nux1[k] = 0.0;
       }
       for (k = nb_freq[1]; k < NTERM; k++){
         nuz1[k] = 0.0;
       }
       if (diffusion){
         Get_Tabshift(Tab,Tab0,Nbtour,Nbtour); // shift data for second round NAFF
         Get_NAFF(NTERM, Nbtour, Tab0, fx2, fz2, nb_freq); // gets frequency vectors

         for (k = 0; k < nb_freq[0]; k++){
           nux2[k] = fx2[k];
         }
         for (k = 0; k < nb_freq[1]; k++){
           nuz2[k] = fz2[k];
         }
         for (k = nb_freq[0]; k < NTERM; k++){
           nux2[k] = 0.0;
         }
         for (k = nb_freq[1]; k < NTERM; k++){
           nuz2[k] = 0.0;
         }
       }
     }
     else {
      for (k = 0; k < NTERM; k++){
        nux1[k] = 0.0;
        nuz1[k] = 0.0;
        nux2[k] = 0.0;
        nuz2[k] = 0.0;
      }
     }

     // printout value
     if (!diffusion){
       fprintf(outf,"%14.6e %14.6e ", x, z);
       for (k = 0; k < NTERM; k++){
         fprintf(outf,"%14.6e ", nux1[k]);
       }
       for (k = 0; k < NTERM; k++){
         fprintf(outf,"%14.6e ", nuz1[k]);
       }
       fprintf(outf,"\n");
//       fprintf(stdout,"%14.6e %14.6e %14.6e %14.6e\n", x, z, nux1, nuz1);
     }
     else {
       fprintf(outf,"%14.6e %14.6e ", x, z);
       for (k = 0; k < NTERM; k++){
         fprintf(outf,"%14.6e ", nux1[k]);
       }
       for (k = 0; k < NTERM; k++){
         fprintf(outf,"%14.6e ", nuz1[k]);
       }
       for (k = 0; k < NTERM; k++){
         fprintf(outf,"%14.6e ", nux2[k]);
       }
       for (k = 0; k < NTERM; k++){
         fprintf(outf,"%14.6e ", nuz2[k]);
       }
       fprintf(outf,"\n");
//       fprintf(stdout,"%14.6e %14.6e %14.6e %14.6e %14.6e %14.6e\n",
//        x, z, nux1, nuz1, fx[0]-fx2[0], fz[0]-fz2[0]);
     }
   }
 }

 fclose(outf);
}
#undef NTERM

/****************************************************************************/
/* void Dyna(long Nbx, long Nbz, long Nbtour, double xmax, double zmax,
   double energy, bool *status)

   Purpose:
       Compute a frequency map of Nbx x Nbz points
       For each set of initial conditions the particle is tracked over
       Nbtour for an energy offset dp

       The stepsize follows a square root law

       Results in fmap.out

   Input:
       Nbx    horizontal step number
       Nby    vertical step number
       xmax   horizontal maximum amplitude
       zmax   vertical maximum maplitude
       Nbtour number of turn for tracking
       energy particle energy offset

   Output:
       status true if stable
              false otherwise

   Return:
       none

   Global variables:
       none

   Specific functions:
       Trac_Simple, Get_NAFF

   Comments:
       none

****************************************************************************/
#define NTERM2  2
void Dyna(long Nbx, long Nbz, long Nbtour, double xmax, double zmax,
               double energy, bool diffusion)
{
  FILE * outf;
  const char fic[] = "dyna.out";
  long i, j;
  double Tab[6][NTURN], fx[NTERM2], fz[NTERM2];
  double x = 0.0, xp = 0.0, z = 0.0, zp = 0.0;
  double x0 = 1e-6, xp0 = 0.0, z0 = 1e-6, zp0 = 0.0;
  double xstep = 0.0, zstep = 0.0;
  int nb_freq[2] = {0, 0};
  long nturn = Nbtour;
  bool status=true;
  struct tm *newtime;

  /* Get time and date */
  newtime = GetTime();

  if (diffusion) nturn = 2*Nbtour;

  if (trace) printf("Entering fmap ... results in %s\n\n",fic);

  /* Opening file moustache */
  if ((outf = fopen(fic, "w")) == NULL)
  {
    fprintf(stdout, "fmap: error while opening file %s\n", fic);
    exit_(1);
  }

  fprintf(outf,"# TRACY II v. 2.6 -- %s -- %s \n", fic, asctime2(newtime));
  fprintf(outf,"# nu = f(x) \n");
  fprintf(outf,"#    x[m]          z[m]           fx            fz \n");

  if ((Nbx <= 1) || (Nbz <= 1))
    fprintf(stdout,"fmap: Error Nbx=%ld Nbz=%ld\n",Nbx,Nbz);

  xp = xp0;
  zp = zp0;

  xstep = xmax/sqrt((double)Nbx);
  zstep = zmax/sqrt((double)Nbz);

  for (i = 0; i <= Nbx; i++) {
    x  = x0 + sqrt((double)i)*xstep;
    for (j = 0; j<= Nbz; j++) {
      z  = z0 + sqrt((double)j)*zstep;
      Trac_Simple4DCOD(x,xp,z,zp,energy,0.0,nturn,Tab,&status);
      if (status) Get_NAFF(NTERM2, Nbtour, Tab, fx, fz, nb_freq);
      else {
       fx[0] = 0.0; fz[0] = 0.0;
      }
      fprintf(outf,"%14.6e %14.6e %14.6e %14.6e %d\n", x, z, fx[0], fz[0], status);
      fprintf(stdout,"%14.6e %14.6e %14.6e %14.6e %d\n", x, z, fx[0], fz[0], status);
      if (diffusion) {
        if (status) Get_NAFF(NTERM2, Nbtour, Tab, fx, fz, nb_freq);
        fprintf(outf,"%14.6e %14.6e %14.6e %14.6e %d\n", x, z, fx[0], fz[0], status);
        fprintf(stdout,"%14.6e %14.6e %14.6e %14.6e %d\n", x, z, fx[0], fz[0], status);
      }
    }
  }

  xp = xp0;
  zp = zp0;

  for (i = 0; i <= Nbx; i++)  {
    x  = x0 - sqrt((double)i)*xstep;
    for (j = 0; j<= Nbz; j++) {
      z  = z0 + sqrt((double)j)*zstep;
      Trac_Simple4DCOD(x,xp,z,zp,energy,0.0,nturn,Tab,&status);
      if (status) Get_NAFF(NTERM2, Nbtour, Tab, fx, fz, nb_freq);
      else {
       fx[0] = 0.0; fz[0] =0.0;
      }
      fprintf(outf,"%14.6e %14.6e %14.6e %14.6e %d\n", x, z, fx[0], fz[0], status);
      fprintf(stdout,"%14.6e %14.6e %14.6e %14.6e %d\n", x, z, fx[0], fz[0], status);
      if (diffusion) {
        if (status) Get_NAFF(NTERM2, Nbtour, Tab, fx, fz, nb_freq);
        fprintf(outf,"%14.6e %14.6e %14.6e %14.6e\n", x, z, fx[0], fz[0]);
        fprintf(stdout,"%14.6e %14.6e %14.6e %14.6e\n", x, z, fx[0], fz[0]);
      }
    }
  }

  fclose(outf);
}

/****************************************************************************/
/* void Phase2(long pos, double x,double xp,double y, double yp,double energy, double ctau,
               long Nbtour)

   Purpose:
       Compute 6D phase space at position pos (=element number in the lattice )
       Results in phase.out

   Input:
       x, xp, y, yp, energy, ctau starting position
       Nbtour turn number

   Output:
       none

   Return:
       none

   Global variables:
       trace

   Specific functions:
       Trac_Simple, Get_NAFF

   Comments:
       none

****************************************************************************/
void Phase2(long pos, double x,double px,double y, double py,double energy,
            double ctau, long Nbtour)
{
  FILE *outf;
  const char fic[] = "phase2.out";
  long lastpos = 0,lastn = 0;
  struct tm *newtime;

  /* Get time and date */
  newtime = GetTime();

  lastpos = pos;

  if ((outf = fopen(fic, "w")) == NULL) {
    fprintf(stdout, "Phase: error while opening file %s\n", fic);
    exit_(1);
  }

  fprintf(outf,"# TRACY II v. 2.6 -- %s -- %s \n", fic, asctime2(newtime));
  fprintf(outf,"# Phase Space \n");
  fprintf(outf,
  "# num         x           xp             z            zp           dp          ctau\n");

  trace = true;
  Trac(x,px,y,py,energy,ctau, Nbtour,pos, lastn, lastpos, outf);
  fclose(outf);
}

void Phase3(long pos, double x,double px,double y, double py,double energy,
            double ctau, long Nbtour)
{
  FILE *outf;
  const char  *fic="phase3.out";
  long        lastpos = 0,lastn = 0;
  struct tm   *newtime;
  Vector      x1;

  /* Get time and date */
  newtime = GetTime();

  lastpos = pos;

  if ((outf = fopen(fic, "w")) == NULL) {
    fprintf(stdout, "Phase: error while opening file %s\n", fic);
    exit_(1);
  }

  fprintf(outf,"# TRACY II v. 2.6 -- %s -- %s \n", fic, asctime2(newtime));
  fprintf(outf,"# Phase Space \n");
  fprintf(outf,
  "# num         x           xp             z            zp           dp          ctau\n");

  trace = true;
  x1[0] = x;   x1[1] = px;     x1[2] = y;
  x1[3] = py;  x1[4] = energy; x1[5] = ctau;
  Cell_Pass(0L, pos-1L, x1, lastpos);

  x  = x1[0];       px= x1[1];   y = x1[2];
  py = x1[3];  energy = x1[4]; ctau =x1[5];

  Trac(x,px,y,py,energy,ctau, Nbtour, pos, lastn, lastpos, outf);
  fclose(outf);
}

/****************************************************************************/
/* void Coupling_Edwards_Teng(void)

   Purpose:

       Compute the oneturn matrix in the uncoupled frame using
       the coupled matrix.

       Deduce the projected emittance using the invariant given
       by GetEmittance.

       Source:
       Parametrization of linear coupled motion in periodic system
       by D.A. Edwards and L.C. Teng
       PAC73

       Let be T the oneturn matrix, I the 2x2 identity matrix
       We search for a basis where the system is uncoupled:
                                -1                                -1
         ( M n )  (  Icos(phi) D sin(phi) ) ( A 0 ) ( Icos(phi) -D sin(phi) )
      T =(     ) =(                       ) (     ) (                       )
         ( m N )  ( -Dsin(phi)  Icos(phi) ) ( 0 B ) ( Dsin(phi)   Icos(phi) )
               -1
      T = R U R

                                         ( alpha1  beta1 )
      A = Icos(mu1) + J1sin(mu1)  w/ J1 =(               )
                                         (-gamma1 -alpha1)

                                         ( alpha2  beta2 )
      B = Icos(mu2) + J2sin(mu2)  w/ J2 =(               )
                                         (-gamma2 -alpha2)

                   2             2     2             2  T
      Given V = (<u >, <uu'>, <u' >, <v >, <uu'>, <v' >)
                   2             2     2             2  T
      and   X = (<x >, <xx'>, <x' >, <z >, <zz'>, <z' >)

      Then X = U2T V where U2T if constucted using the uncoupling R matrix

   Input:
       none

   Output:
       none

   Return:
       none

   Global variables:
       globval

   Specific functions:
       getelem
       GetEmittance

   Comments:
       22/06/03 Now works even if coupling is null
       Should be generalized in 6D
       17/07/03 use of M_PI instead of pi
       22/03/04 save status cavity/radiation and restore it at the end
       28/07/10 modified for tracy 3
****************************************************************************/
void Coupling_Edwards_Teng(void)
{
  int i,j;
  bool chroma=true, trace=false;
  bool radiationflag, cavityflag;
  double dP      = 0.0;
  double diffcmu = 0.0,   /* cos(mu1) - cos(mu2)*/
         c2phi   = 0.0,   /* cos(2*phi) */
         s2phi   = 0.0,   /* sin(2*phi) */
         phi     = 0.0,
         tphi    = 0.0,   /* tan(phi) */
         cphi    = 0.0,   /* cos(phi) */
         sphi    = 0.0;   /* sin(phi) */

 Matrix  M, N, m, n, D, A, B, R, S;
 Matrix  Rinv, Dinv, nm, MminusN, tS, tn, U2T, dummy, T, U, Sigma;
 Vector V;


  double W1 = 0.0, W2 = 0.0;
  double alpha_1 = 0.0, beta1 = 0.0, gamma1 = 0.0, nu1 = 0.0, epsilon1 = 0.0;
  double alpha_2 = 0.0, beta2 = 0.0, gamma2 = 0.0, nu2 = 0.0, epsilon2 = 0.0;
  double alpha_3 = 0.0, beta3 = 0.0, gamma3 = 0.0, epsilon3 = 0.0;


  /* initialization to unit matrix */
  ZeroMat(6L, M);
  ZeroMat(6L, N);
  ZeroMat(6L, m);
  ZeroMat(6L, n);
  ZeroMat(6L, D);
  ZeroMat(6L, Dinv);
  ZeroMat(6L, A);
  ZeroMat(6L, B);
  ZeroMat(6L, nm);
  ZeroMat(6L, MminusN);
  ZeroMat(6L, tn);
  ZeroMat(6L, tS);
  ZeroMat(6L, S);
  ZeroMat(6L, dummy);
  UnitMat(6L, U2T);
  UnitMat(6L, R);
  UnitMat(6L, Rinv);

  /* Build up symplectic S matrix */
  S[0][1] = 1.0; S[1][0] = -1.0;

  /* Compute invariants */
  GetEmittance(ElemIndex("cav"), true);


  /* Set everything to 4D integrator */
  radiationflag        = globval.radiation;
  cavityflag           = globval.Cavity_on;
  globval.MatMeth      = false;    /* matrix method */
  globval.Cavity_on    = false;    /* Cavity on/off */
  globval.radiation    = false;    /* radiation on/off */
  globval.emittance    = false;    /* emittance  on/off */
  globval.pathlength   = false;    /* Path lengthening computation */

  /* Compute Oneturn matrix and store it into globval.OneTurnMat*/
  Ring_GetTwiss(chroma=false, dP=0e0);
//  printglob();

  /* Copy the oneturn matrix into the Edwards and Teng Form */
  /*
      T = ( M n )
          ( m N )
   */


  /* Compute and get Twiss parameters */
  for (i = 0; i <= 1; i ++)
  {
    for (j = 0; j <= 1; j ++)
    {
        M[i][j] = globval.OneTurnMat[i][j];
        N[i][j] = globval.OneTurnMat[i+2][j+2];
        m[i][j] = globval.OneTurnMat[i+2][j];
        n[i][j] = globval.OneTurnMat[i][j+2];
    }
  }
//  fprintf(stdout,"M "); prtmat(2L,M);
//  fprintf(stdout,"N ");prtmat(2L,N);

  CopyMat(2L, M, MminusN);
  SubMat(2L,N,MminusN);
//  fprintf(stdout,"M-N ");  prtmat(2L,MminusN);
  CopyMat(2L, m, nm);
  MulLMat(2l, n, nm);

  /*                                                       -1/2
                         1        (     2 det(m) + Tr(nm) )
  cos(mu1) - cos(mu2) =  -Tr(M-N) ( 1 + ----------------- )
                         2        (      (0.5Tr(M-N))**2  )
  */
  diffcmu = 0.5*TrMat(2L,MminusN)*sqrt(1.0 + (2.0*DetMat(2L,m) + TrMat(2L,nm))/
                                      (0.25*TrMat(2L,MminusN)*TrMat(2L,MminusN)));
  /* cos(2phi) */
  c2phi   = 0.5*TrMat(2L,MminusN)/diffcmu;

  /* sin(2phi) */
  s2phi   = sqrt(1.0-c2phi*c2phi);

  phi     = 0.5*atan(s2phi/c2phi);

  /* tan(phi), cos(phi), sin(phi) */
  tphi    = tan(phi);
  cphi    = cos(phi);
  sphi    = sin(phi);

  /* Compute D matrix */
  /*                      ~~
   *                 m + SnS
   *  D = - ----------------------------
   *         (cos(mu1)-cos(mu2)) sin(2phi)
   */
  if (fabs(phi) > 1e-12)
  {    /* D is  defined and D is inversible ortherwise set to matrix null */
    CopyMat(2L, n, tn);
    TpMat(2L,tn);
    CopyMat(2L, S, tS);
    TpMat(2l,tS);
    CopyMat(2L, tS, dummy);

    MulLMat(2l, tn, dummy);
    MulLMat(2l, S, dummy);
    AddMat(2L, m, dummy);
    MulcMat(2L, -1.0/diffcmu/s2phi ,dummy);
    CopyMat(2L, dummy, D);

    if (TrMat(4L,D) < 0.0)
    { /* Trace of D has to remain positive */
      phi = - phi;
      MulcMat(2L, -1.0 ,D);
      tphi = -tphi;
      sphi = -sphi;
    }

    /*  Compute A matrix   */
    /*          -1         */
    /* A = M - D mtan(phi) */
     CopyMat(2L, D, Dinv);
     if(!InvMat(2L, Dinv)) fprintf(stdout,"Matrix D is singular\n");
  //  fprintf(stdout,"Dinv matrix "); prtmat(4L, Dinv);

    CopyMat(2L, m, dummy);
  //  fprintf(stdout,"m matrix "); prtmat(4L, dummy);
    MulcMat(2L, -tphi ,dummy);
  //  fprintf(stdout,"-tphim matrix "); prtmat(4L, dummy);
    MulLMat(2l, Dinv, dummy);
  //  fprintf(stdout,"-tphi Dinv m matrix "); prtmat(4L, dummy);
    AddMat(2L,M,dummy);
    CopyMat(2L, dummy, A);

    /* Compute B matrix */
    /* B = N +Dntan(phi) */
    CopyMat(2L, n, dummy);
    MulcMat(2L, tphi ,dummy);
    MulLMat(2l, D, dummy);
    AddMat(2L,N,dummy);
    CopyMat(2L, dummy, B);

    /* Build up the R matrix */
    /*                    -1
     *      (  Icos(phi) D sin(phi) )
     *   T =(                       )
     *      ( -Dsin(phi)  Icos(phi) )
     */
    MulcMat(4L, cphi ,R);
    CopyMat(2L, D, dummy);
    MulcMat(4L, -sphi , dummy);
    for (i = 0; i <= 1; i ++)
      for (j = 0; j <= 1; j ++)
        R[i+2][j] = dummy[i][j];
    CopyMat(2L, Dinv, dummy);
    MulcMat(4L, sphi , dummy);
    for (i = 0; i <= 1; i ++)
      for (j = 0; j <= 1; j ++)
        R[i][j+2] = dummy[i][j];

    CopyMat(4L, R, Rinv);
    if(!InvMat(4L, Rinv)) fprintf(stdout,"Matrix R is singular\n");

    /* Build up uncoupled matrix */
    UnitMat(6L, U);
    CopyMat(2L, A, U);
    for (i = 0; i <= 1; i ++)
      for (j = 0; j <= 1; j ++)
        U[i+2][j+2] = B[i][j];
    if (trace) {fprintf(stdout,"Uncoupled matrix "); prtmat(4L, U);}

    CopyMat(4L, Rinv, T);
    MulLMat(4L, U, T);
    MulLMat(4L, R, T);
    /* for checking, back to T */
    if (trace) {fprintf(stdout,"Coupled matrix "); prtmat(4L, T);}


    /* Build up transformation matrix for sigma terms from uncoupled to coupled frame */
    /* R is the decoupling matrix computed from Edwards' and Teng's decomposition */
    /* From R. Nagaoka's notes */
    U2T[0][0] = R[0][0]*R[0][0];
    U2T[0][1] = 2.0*R[0][0]*R[0][1];
    U2T[0][2] = R[0][1]*R[0][1];
    U2T[0][3] = R[0][2]*R[0][2];
    U2T[0][4] = 2.0*R[0][1]*R[0][3];
    U2T[0][5] = R[0][3]*R[0][3];

    U2T[1][0] = R[0][0]*R[1][0];
    U2T[1][1] = R[0][0]*R[1][1] + R[0][1]*R[1][0];
    U2T[1][2] = R[0][1]*R[1][1];
    U2T[1][3] = R[0][2]*R[1][2];
    U2T[1][4] = R[0][1]*R[1][3] + R[0][3]*R[1][2];
    U2T[1][5] = R[0][3]*R[1][3];

    U2T[2][0] = R[1][0]*R[1][0];
    U2T[2][1] = 2.0*R[1][0]*R[1][1];
    U2T[2][2] = R[1][1]*R[1][1];
    U2T[2][3] = R[1][2]*R[1][2];
    U2T[2][4] = 2.0*R[1][2]*R[1][3];
    U2T[2][5] = R[1][3]*R[1][3];

    U2T[3][0] = R[2][0]*R[2][0];
    U2T[3][1] = 2.0*R[2][0]*R[2][1];
    U2T[3][2] = R[2][1]*R[2][1];
    U2T[3][3] = R[2][2]*R[2][2];
    U2T[3][4] = 2.0*R[2][2]*R[2][3];
    U2T[3][5] = R[2][3]*R[2][3];

    U2T[4][0] = R[2][0]*R[3][0];
    U2T[4][1] = R[2][0]*R[3][1] + R[2][1]*R[3][0];
    U2T[4][2] = R[2][1]*R[3][1];
    U2T[4][3] = R[2][2]*R[3][2];
    U2T[4][4] = R[2][2]*R[3][3] + R[2][3]*R[3][2];
    U2T[4][5] = R[2][3]*R[3][3];

    U2T[5][0] = R[3][0]*R[3][0];
    U2T[5][1] = 2.0*R[3][0]*R[3][1];
    U2T[5][2] = R[3][1]*R[3][1];
    U2T[5][3] = R[3][2]*R[3][2];
    U2T[5][4] = 2.0*R[3][2]*R[3][3];
    U2T[5][5] = R[3][3]*R[3][3];

    if (trace) {fprintf(stdout,"R "); prtmat(4L,R);}
    if (trace) {fprintf(stdout,"U2T"); prtmat(6L, U2T);}

  }
  else { /* no coupling */
    fprintf(stdout,"\nThere is no coupling ...\n");
    CopyMat(2L, M, A);
    CopyMat(2L, N, B);
  }

//  fprintf(stdout,"Sigma "); prtmat(6L, globval.ElemMat[0]);

//  V[0] = globval.ElemMat[1][0][0];
//  V[1] = globval.ElemMat[1][0][1];
//  V[2] = globval.ElemMat[1][1][1];
//  V[3] = globval.ElemMat[1][2][2];
//  V[4] = globval.ElemMat[1][2][3];
//  V[5] = globval.ElemMat[1][3][3];

  /* Compute Twiss parameter in the uncoupled frame */
  /* Mode 1*/
  nu1    = globval.TotalTune[0];
  alpha_1 = (A[0][0]-A[1][1])/sin(2.0*M_PI*nu1);
  beta1  =  A[0][1]/sin(2.0*M_PI*nu1);
  gamma1 = -A[1][0]/sin(2.0*M_PI*nu1);

  /* Mode 2*/
  nu2    = globval.TotalTune[1];
  alpha_2 = (B[0][0]-B[1][1])/sin(2.0*M_PI*nu2);
  beta2  =  B[0][1]/sin(2.0*M_PI*nu2);
  gamma2 = -B[1][0]/sin(2.0*M_PI*nu2);

  /* Build up sigma matrix in uncoupled frame */
  ZeroMat(6L,Sigma);
  /* Mode 1 */
  epsilon1    =  globval.eps[0];
  Sigma[0][0] =  beta1*epsilon1;
  Sigma[1][1] =  gamma1*epsilon1;
  Sigma[0][1] = -alpha_1*epsilon1;
  Sigma[1][0] =  Sigma[0][1];

  /* Mode 2 */
  epsilon2    =  globval.eps[1];
  Sigma[2][2] =  beta2*epsilon2;
  Sigma[3][3] =  gamma2*epsilon2;
  Sigma[2][3] = -alpha_2*epsilon2;
  Sigma[3][2] =  Sigma[2][3];

  /* Mode 3 */
  epsilon3    =  globval.eps[2];
  Sigma[4][4] =  beta3*epsilon3;
  Sigma[5][5] =  gamma3*epsilon3;
  Sigma[4][5] = -alpha_3*epsilon3;
  Sigma[5][4] =  Sigma[4][5];

//  fprintf(stdout,"Uncoupled sigma  "); prtmat(4L, Sigma);

  V[0] = Sigma[0][0];
  V[1] = Sigma[0][1];
  V[2] = Sigma[1][1];
  V[3] = Sigma[2][2];
  V[4] = Sigma[2][3];
  V[5] = Sigma[3][3];

  if (!trace)
  {
    fprintf(stdout,"**************************************\n");
    fprintf(stdout,"nu1    = % 10.6f beta1 = % 10.6f\n",globval.TotalTune[0],beta1);
    fprintf(stdout,"alpha_1 = % 10.6f gamma1= % 10.6f\n",alpha_1,gamma1);
    fprintf(stdout,"nu2    = % 10.6f beta2 = % 10.6f\n",globval.TotalTune[1],beta2);
    fprintf(stdout,"alpha_2 = % 10.6f gamma2= % 10.6f\n",alpha_2,gamma2);
    fprintf(stdout,"**************************************\n");
  }

  /* Build up invariant: should be the same as invariant given by globval.eps*/
  W1 = sqrt(V[0]*V[2] - V[1]*V[1]);
  W2 = sqrt(V[3]*V[5] - V[4]*V[4]);

  /*** Print results */
  if (!trace)
  {
   fprintf(stdout,"Coupling using Edwards' and Teng's formalism\n");
   fprintf(stdout,"cos(mu1)-cos(mu2) = % 10.6f cos(2*phi) = % 10.6f sin(2*phi) = % 10.6f\n",
           diffcmu,c2phi,s2phi);
   fprintf(stdout,"phi = % 10.6f \n", 0.5*atan(s2phi/c2phi));
   fprintf(stdout,"Invariant in local coordinates:  W1 = % 10.6e, W2 = % 10.6e, W2/W1 = %10.6e\n",
           W1, W2, W2/W1);
  }

  if (trace){
  fprintf(stdout,"Symplectic matrix D whose derterminant is % 10.6f ", DetMat(2L,D));
  prtmat(2L,D);
  fprintf(stdout,"Symplectic matrix A whose derterminant is % 10.6f ", DetMat(2L,A));
  prtmat(2L,A);
  fprintf(stdout,"Symplectic matrix B whose derterminant is % 10.6f ", DetMat(2L,B));
  prtmat(2L,B);
  fprintf(stdout,"Symplectic matrix R whose derterminant is % 10.6f ", DetMat(4L,R));
  prtmat(4L,R);
  }

  /* Transform the sigma matrix from uncoupled frame to coupled frame */
//  PrintVec(6L, V);
  LinTrans(6L,U2T,V);
//  PrintVec(6L, V);

  /* Build up projected emittances */
  W1 = sqrt(V[0]*V[2] - V[1]*V[1]);
  W2 = sqrt(V[3]*V[5] - V[4]*V[4]);

  // store result and restore tracking mode 4D or 6D

  globval.epsp[0]    = W1;
  globval.epsp[1]    = W2;
  globval.Cavity_on  = cavityflag;       /* Cavity on/off */
  globval.radiation  = radiationflag;    /* radiation on/off */


  if (!trace)
  {
    fprintf(stdout,"Projected emittances:            Ex = % 10.6e, Ez = % 10.6e, Ez/Ex = %10.6e\n",
            W1, W2, W2/W1);
    fprintf(stdout,"**************************************\n");
  }
 }


/****************************************************************************/
/* void PhaseLongitudinalHamiltonien(void)

   Purpose:
       Compute longitudinal phase space from analytical model
                                                         2              3
                                (                   delta          delta  )
      H(phi,delta) =    omegaRF*(dCoC delta + alpha1----- + alpha2*-----  )
                                (                     2              3    )

                       eVRF (                                               )
                     - -----( cos(phi) - cos(phis) + (phi - phis) sin(phis) )
                        ET  (                                               )


      Integration method Ruth integrator H(phi, delta) = A(delta) + B(phi)

   Parameters:
       omegaRF RF frequency/2pi
       eVRF    RF voltage in electron volt
       phis    synchronous phase
       alpha1  first order momentum compaction factor
       alpha2  second order momentum compaction factor
       dCoC    betatron path lengthening

   Input:
       none

   Output:
       longitudinale.out

   Return:
       none

   Global variables:
       trace

   Specific functions:
       PassA, PassB, Hsynchrotron

   Comments:
       none

****************************************************************************/
/* SOLEIL value for SOLAMOR2 */
#define alpha1 4.38E-4
#define alpha2 4.49E-3
#define dCoC  0E-6
#define phis  -0.238
#define E 2.75E3
#define eVRF 4
#define T 1.181E-6
#define omegaRF 352.202E6

void PhaseLongitudinalHamiltonien(void)
{
  long i,j;
  const double t = T;        // To get a one turn map
  double phi, delta, H0;
  long imax = 1000L,         // turn number
       jmax = 25L;          // starting condition number

  /* Constant stepsize for Ruth's and Forest's Integrator */
  /* Laskar's integrator is not a good idea here, since the correction factor is
     not integrable */
  const double D1 = 0.675603595979829E0;
	const double D2 =-0.175603595979829E0;
	const double C2 = 0.135120719195966E1;
	const double C3 =-0.170241438391932E1;

  FILE *outf;
  const char fic[] = "longitudinal.out";
  struct tm *newtime;

  /* Get time and date */
  time_t aclock;
  time(&aclock);                 /* Get time in seconds */
  newtime = localtime(&aclock);  /* Convert time to struct */

  if ((outf = fopen(fic, "w")) == NULL)
  {
    fprintf(stdout, "PhaseLongitudinalHamiltonien: error while opening file %s\n", fic);
    exit_(1);
  }

  printf("Last stable orbit %f\n", acos(1.0-T*E/eVRF*Hsynchrotron(0.0,-0.098)));

  fprintf(outf,"# TRACY II v. 2.6  -- %s \n", asctime2(newtime));
  fprintf(outf,"#  i          ctau              dp             DH/H               H \n#\n");

  for (j = 0L; j < jmax; j++)
  {
    phi = 0.061417777*j; delta = 0.0001;
    H0 = Hsynchrotron(phi,delta);
    fprintf(outf,"%4ld % 16.8f % 16.8f % 16.8e % 16.8f\n",0L,fmod(phi,2.0*M_PI)*0.8512/2.0/M_PI,delta, 0.0, H0);

    for (i = 0L; i < imax; i++){
  // Leap Frog integrator
  //    PassA(&phi, delta, t*0.5);
  //    PassB(phi, &delta, t);
  //    PassA(&phi, delta, t*0.5);
  // 4th order symplectic integrator
      PassA(&phi, delta, t*D1);
      PassB(phi, &delta, t*C2);
      PassA(&phi, delta, t*D2);
      PassB(phi, &delta, t*C3);
      PassA(&phi, delta, t*D2);
      PassB(phi, &delta, t*C2);
      PassA(&phi, delta, t*D1);
      fprintf(outf,"%4ld % 16.8f % 16.8f % 16.8e % 16.8f\n",i,fmod(phi,2.0*M_PI)*0.8512/2.0/M_PI,
              delta,(H0-Hsynchrotron(phi,delta))/H0,Hsynchrotron(phi,delta));
    }
      fprintf(outf,"\n");
  }
  fclose(outf);
}


/****************************************************************************/
/* void PassA(double *phi, double delta0, double step)

   Purpose:
       Integrate exp(step*liederivativeof(H(delta,phi))
                                                         2              3
                                (                   delta          delta  )
      H(phi,delta) =    omegaRF*(dCoC delta + alpha1----- + alpha2*-----  )
                                (                     2              3    )


   parameters:
       omegaRF RF frequency/2pi
       eVRF    RF voltage in electron volt
       phis    synchronous phase
       alpha1  first order momentum compaction factor
       alpha2  second order momentum compaction factor
       dCoC    betatron path lengthening

   Input:
       phi, delta coordinates
       step stepsize for integration

   Output:
       phi new phase after t=step

   Return:
       none

   Global variables:
       trace

   Specific functions:
       none

   Comments:
       none

****************************************************************************/
void PassA(double *phi, double delta0, double step)
{
  *phi -= omegaRF*2.0*M_PI*(dCoC + alpha1*delta0 + alpha2*delta0*delta0)*step;
}

/****************************************************************************/
/* void PassB(double phi0, double *delta, double step)

   Purpose:
       Integrate exp(step*liederivativeof(H(delta,phi))

                       eVRF (                                               )
      H(phi,delta) = - -----( cos(phi) - cos(phis) + (phi - phis) sin(phis) )
                        ET  (                                               )


   parameters:
       omegaRF RF frequency/2pi
       eVRF    RF voltage in electron volt
       phis    synchronous phase
       alpha1  first order momentum compaction factor
       alpha2  second order momentum compaction factor
       dCoC    betatron path lengthening

   Input:
       phi, delta coordinates
       step stepsize for integration

   Output:
       phi new phase after t=step

   Return:
       none

   Global variables:
       trace

   Specific functions:
       none

   Comments:
       none

****************************************************************************/
void PassB(double phi0, double *delta, double step)
{
  *delta += eVRF/E/T*(sin(phi0) - sin(phis))*step;
}

/****************************************************************************/
/* double Hsynchrotron(double phi, double delta)

   Purpose:
       Compute Hamiltonian
                                                         2              3
                                (                   delta          delta  )
      H(phi,delta) =    omegaRF*(dCoC delta + alpha1----- + alpha2*-----  )
                                (                     2              3    )

                       eVRF (                                               )
                     - -----( cos(phi) - cos(phis) + (phi - phis) sin(phis) )
                        ET  (                                               )


   Input:
       omegaRF RF frequency/2pi
       eVRF    RF voltage in electron volt
       phis    synchronous phase
       alpha1  first order momentum compaction factor
       alpha2  second order momentum compaction factor
       dCoC    betatron path lengthening

   Output:
       none

   Return:
       Hamiltonian computed in phi and delta

   Global variables:
       none

   Specific functions:
       none

   Comments:
       none

****************************************************************************/
double Hsynchrotron(double phi, double delta)
{
  double H = 0.0;

  H  = omegaRF*2.0*M_PI*(dCoC*delta + alpha1*delta*delta/2.0 + alpha2*delta*delta*delta/3.0);
  H -= eVRF/E/T*(cos(phi) - cos(phis) + (phi-phis)*sin(phis));
  return H;
}


double EnergySmall(double *X, double irho)
{
 double A, B;
 double h = irho;

 A = (1.0+h*X[0])*(X[1]*X[1]+X[3]*X[3])/2.0/(1.0+X[4]);
 B = -h*X[4]*X[0]+h*h*X[0]*X[0]/0.5;
 return (A+B);
}

double EnergyDrift(double *X)
{
 double A;

 A = (X[1]*X[1]+X[3]*X[3])/2.0/(1.0+X[4]);
 return (A);
}

/****************************************************************************/
/* void Enveloppe2(double x, double px, double y, double py, double dp, double nturn)

   Purpose:
       Diagnosis for tracking
       Used only for debuging
       Print particle coordinates after each element over 1 single turn

   Input:
       x, px, y, py, dp starting conditions for tracking

   Output:
       none

   Return:
       none

   Global variables:
       trace

   Specific functions:
       Trac_Simple, Get_NAFF

   Comments:
       none

****************************************************************************/
void Enveloppe2(double x, double px, double y, double py, double dp, double nturn)
{
  Vector x1; /* Tracking coordinates */
  long lastpos = globval.Cell_nLoc;
  FILE *outf;
  const char fic[] = "enveloppe2.out";
  int i,j ;
  CellType Cell;
  /* Array for Enveloppes */
  double Envxp[Cell_nLocMax], Envxm[Cell_nLocMax];
  double Envzp[Cell_nLocMax], Envzm[Cell_nLocMax];


  /* Get cod the delta = energy*/
  getcod(dp, lastpos);
//  /* initialization to chromatic closed orbit */
//  for (i = 0; i<= globval.Cell_nLoc; i++)
//  {
//   getelem(i, &Cell);
//   Envxm[i] = Cell.BeamPos[0];   Envxp[i] = Cell.BeamPos[0];
//   Envzm[i] = Cell.BeamPos[2];   Envzp[i] = Cell.BeamPos[2];
//  }

  printf("xcod=%.5e mm zcod=% .5e mm \n",
	 globval.CODvect[0]*1e3, globval.CODvect[2]*1e3);

  if ((outf = fopen(fic, "w")) == NULL) {
    fprintf(stdout, "Enveloppe: error while opening file %s\n", fic);
    exit_(1);
  }

  x1[0] =  x + globval.CODvect[0]; x1[1] = px + globval.CODvect[1];
  x1[2] =  y + globval.CODvect[2]; x1[3] = py + globval.CODvect[3];
  x1[4] = dp; x1[5] = 0e0;

  fprintf(outf,"# s       envx(+)       envx(-)       envz(+)       envz(-)     delta \n");

  for (i = 0; i< globval.Cell_nLoc; i++)
  {/* loop over full ring: one turn for intialization */

    getelem(i,&Cell);
    Cell_Pass(i,i+1, x1, lastpos);
    if (lastpos != i+1)
    {
     printf("Unstable motion ...\n"); exit_(1);
    }

    Envxp[i] = x1[0]; Envxm[i] = x1[0]; Envzp[i] = x1[2]; Envzm[i] = x1[2];
  }

  for (j = 1; j < nturn; j++) {
    /* loop over full ring */
   for (i = 0; i<= globval.Cell_nLoc; i++) {

      getelem(i, &Cell);
      Cell_Pass(i, i+1, x1, lastpos);
      if (lastpos != i+1)
      {
       printf("Unstable motion ...\n"); exit_(1);
      }
      if (x1[0] >= Envxp[i]) Envxp[i] = x1[0];
      if (x1[0] <= Envxm[i]) Envxm[i] = x1[0];
      if (x1[2] >= Envzp[i]) Envzp[i] = x1[2];
      if (x1[2] <= Envzm[i]) Envzm[i] = x1[2];
      }
  }

  for (i = 0; i<= globval.Cell_nLoc; i++)
  {
    getelem(i,&Cell);
    fprintf(outf,"%6.2f % .5e % .5e % .5e % .5e % .5e\n",
            Cell.S, Envxp[i],Envxm[i],Envzp[i],Envzm[i],dp);
  }
}

/****************************************************************************/
/* double get_RFVoltage(const int Fnum)

   Purpose:
       Get RF voltage of family Fnum

   Input:
       Fnum: family name

   Output:
       none

   Return:
       RF voltage

   Global variables:
       none

   Specific functions:
       none

   Comments:
       10/2010  by L.Nadolski
****************************************************************************/
double get_RFVoltage(const int Fnum){

    double V_RF = 0.0;
    bool prt = false;

  V_RF = Cell[Elem_GetPos(Fnum, 1)].Elem.C->Pvolt; //RF voltage in Volts
  if (prt) fprintf(stdout, "RF voltage of cavity %s is %f MV \n",
    Cell[Elem_GetPos(Fnum, 1)].Elem.PName, V_RF/1e6);
  return V_RF;
}

/****************************************************************************/
/* void set_RFVoltage(const int Fnum, const double V_RF)

   Purpose:
       Set RF voltage to the first kid in the family Fnum

   Input:
       Fnum: family name

   Output:
       none

   Return:
       RF voltage

   Global variables:
       none

   Specific functions:
       none

   Comments:
       10/2010  by L.Nadolski
****************************************************************************/
void set_RFVoltage(const int Fnum, const double V_RF){

  int k, n = 0;


  n = GetnKid(Fnum);
  bool prt = false;

  for (k=1; k <=n; k++){
    Cell[Elem_GetPos(Fnum, k)].Elem.C->Pvolt = V_RF; // in Volts
  }
  if(prt)
  fprintf(stdout, "Setting cavity %s to %f MV \n",
  Cell[Elem_GetPos(Fnum, 1)].Elem.PName, V_RF/1e6);
}


/****************************************************************************************************/
/* void ReadFieldErr(const char *FieldErrorFile)

   Purpose:
       Read multipole errors from a file

        The input format of the file is:

	seed   radom_number ; this set is optional, and only works for the rms error

	keyWords  sys/rms  raduis when the field error is meausred "r0", field error order "n",
	                   field error component "Bn", field error component "An"; "n","Bn,""An",...

   Input:


   Output:
       none

   Return:


   Global variables:
       none

   Specific functions:
       none

   Comments:
       10/2010  Written by Jianfeng Zhang
       01/2011  Fix the bug for reading the end of line symbol "\n" , "\r",'\r\n'
	        at different operation system
       04/2011 	Change the set of 'seed' for rms error in file, now it's mandatory.
*****************************************************************************************************/
void ReadFieldErr(const char *FieldErrorFile)
{
  bool  rms, set_rnd = false;
  char    in[max_str], name[max_str],keywrd[max_str], *prm;
  char    *line;
  int     n = 0;    /* field error order*/
  int     LineNum = 0;
  int     seed_val; // random seed number for the rms error
  double  Bn = 0.0, An = 0.0, r0 = 0.0; /* field error components and radius when the field error is measured */
  /* conversion number from A to T.m for soleil*/
  double  _convHcorr = 8.14e-4,_convVcorr = 4.642e-4, _convQt = 93.83e-4;
  FILE    *inf;

 const bool  prt = false;

  inf = file_read(FieldErrorFile);

  printf("\n");
  /* read lines*/
  while (line=fgets(in, max_str, inf)) {

  /* kill preceding whitespace generated by "table" key
        or "space" key, but leave \n
        so we're guaranteed to have something*/
     while(*line == ' ' || *line == '\t') {
       line++;
     }

    /* count line number for debug*/
    LineNum++;

    /* check the line is whether comment line or null line*/
    if (strstr(line, "#") == NULL && strcmp(line,"\n") != 0 &&
         strcmp(line,"\r") != 0 &&strcmp(line,"\r\n") != 0) {


        sscanf(line, "%s", name);

	if (strcmp("seed", name) == 0) { // the line to set random seed
          sscanf(line, "%*s %d", &seed_val);
          printf("ReadFieldErr: setting random seed to %d\n", seed_val);
          set_rnd = true;
	  iniranf(seed_val);
      } else{//line to set (n Bn An sequence)

	/*read and assign the key words and measure radius*/
	  sscanf(line, " %*s %s %lf",keywrd, &r0);
	  if (prt) printf("\nsetting <%s> multipole error to: %-5s r0 = %7.1le\n",keywrd,name,r0);

	  rms = (strcmp("rms", keywrd) == 0)? true : false;
	  if (rms && !set_rnd) {
              printf("ReadFieldErr: seed not defined\n");
              exit(1);
          }

	  // skip first three parameters
	  strtok(line, " \t");
	  strtok(NULL, " \t");
	  strtok(NULL, " \t");

	  /* read the end of line symbol '\n','\r','\r\n' at different operation system*/
	  while ((prm = strtok(NULL, " \t")) != NULL && strcmp(prm, "\n") != 0 &&
	       strcmp(prm, "\r") != 0 && strcmp(prm, "\r\n") != 0) {

	    /* read and assign n Bn An*/
	    sscanf(prm, "%d", &n);
	    prm = get_prm(); /*move the pointer to the next block of the line, delimiter is table key */
	    sscanf(prm, "%lf", &Bn);
	    prm = get_prm();
	    sscanf(prm, "%lf", &An);

	    if (prt)
	      printf(" n = %2d, Bn = %9.1e, An = %9.1e\n", n, Bn, An);

        /**SOLEIL CODE TO IMPLEMENT MULTIPOLES ON ORBIT AND COUPLING CORRECTORS**/
	    /* set multipole errors to horizontal correctors of soleil ring*/
	    //if(strcmp("hcorr", name) == 0)
	    //  AddCorrQtErr_fam(fic_hcorr,globval.hcorr,_convHcorr,keywrd,r0,n,Bn,An);
	    /* set multipole errors to vertical correctors of soleil ring*/
        //   else if(strcmp("vcorr", name) == 0)
	    // AddCorrQtErr_fam(fic_vcorr,globval.vcorr,_convVcorr,keywrd,r0,n,Bn,An);
	    /* set multipole errors to skew quadrupoles of soleil ring*/
        // else if(strcmp("qt", name) == 0)
	    //   AddCorrQtErr_fam(fic_skew,globval.qt,_convQt,keywrd,r0,n,Bn,An);
	    //else
        /*******************************************************************/
	    /* set errors for other multipole*/
	    AddFieldErrors(name,keywrd, r0, n, Bn, An) ;
	}
    }//end of read the (n Bn An) sequence

  //end of the line
  }else
      continue;
     // printf("%s", line);
  }

  fclose(inf);
}

/***********************************************************************
void AddFieldErrors(const char *name, const char *keywrd,const double r0,
		    const int n, const double Bn, const double An)

   Purpose:
       Add field error of the elements with the same type or single element,
       with the previous value, and then  the summation value replaces
       the previous value.

   Input:
      name         type name or element name
      keyword      "rms" or "sys"
                   "rms":  random  multipole error
		           "sys":  systematic multipole error
      r0           radius at which error is measured, error field is relative
                   to the design field strength when r0 !=0
      n            order of the error
      Bn           relative B component for the n-th error
      An           relative A component for the n-th error


   Output:
      None

  Return:
      None

  Global variables
      None

  Specific functions:
     None

 Comments:
     10/2010  Written by Jianfeng Zhang
**********************************************************************/
void AddFieldErrors(const char *name,const char *keywrd, const double r0,
		    const int n, const double Bn, const double An)
{
  int     Fnum = 0;

  if (strcmp("all", name) == 0) {
    printf("all: not yet implemented\n");
  } else if (strcmp("dip", name) == 0) {
    AddFieldValues_type(Dip,keywrd, r0, n, Bn, An);
  } else if (strcmp("quad", name) == 0) {
    AddFieldValues_type(Quad, keywrd,r0, n, Bn, An);
  } else if (strcmp("sext", name) == 0) {
    AddFieldValues_type(Sext, keywrd, r0, n, Bn, An);
  } else if (strcmp("corr", name) == 0) { //Caso sejam corretoras
    AddFieldValues_type(Corr,keywrd, r0, n, Bn, An);
  } else {/*add error to elements*/
    Fnum = ElemIndex(name);
    if(Fnum > 0)
      AddFieldValues_fam(Fnum,keywrd, r0, n, Bn, An);
    else
      printf("SetFieldErrors: undefined element %s\n", name);
  }
}


/***********************************************************************
void SetFieldValues_type(const int N, const char *keywrd, const double r0,
			 const int n, const double Bn, const double An)

   Purpose:
       Add the field error of the upright multipole with the design order "type"
       with the previous value, and then the summation value replaces the previous value.
   Input:
      N            type name
      keywrd       "rms" or "sys"
                   "rms":  random  multipole error
		   "sys":  systematic multipole error
      r0           radius at which error is measured, error field is relative
                   to the design field strength when r0 != 0
		   if r0 == 0, the Bn and An are absolute value.
      n            order of the error
      Bn           relative B component of  n-th error
      An           relative A component of  n-th error



   Output:
      None

  Return:
      None

  Global variables
      None

  Specific functions:
     None

 Comments:
     14/10/2010  Written by Jianfeng Zhang

     Only works for soleil lattice, since the Q2/Q7, QP2a,b/QP7a,b are
     long quadrupoles, which have different multipole errors from other
     short quadrupoles
**********************************************************************/
void AddFieldValues_type(const int N, const char *keywrd, const double r0,
			 const int n, const double Bn, const double An)
{
  double  bnL = 0.0, anL = 0.0, KLN = 0.0;
    int   k = 0, Np = 0;

    //Adicionei essa variavel para aplicar corretamente erros nas corretoras também
    Np = N;

      // find the strength for multipole
    for(k = 1; k <= globval.Cell_nLoc; k++)
    {
        //only set upright multipole, NOT set skew multipole(skew quadrupole,etc)
        if ((Cell[k].Elem.Pkind == Mpole) && Cell[k].Elem.M->n_design == N && Cell[k].Elem.M->PdTpar == 0)
	{
	  //find the integrated design field strength
	  if(N == 1)
            KLN = Cell[k].Elem.PL*Cell[k].Elem.M->Pirho; /*dipole angle*/
      else if(N == 0) // Caso seja corretoras
      {
            Np = 1;
            KLN = GetKLpar(Cell[k].Fnum, Cell[k].Knum, Np);
            if(KLN == 0.0)
                KLN = GetKLpar(Cell[k].Fnum, Cell[k].Knum, -Np);
      }
	  else
	        KLN = GetKLpar(Cell[k].Fnum, Cell[k].Knum, Np);/*other multipoles*/


	  //absolute integrated multipole error strength
	  if (r0 == 0){
	    bnL = Bn;
	    anL = An;
	  }else{
	    bnL = Bn/pow(r0, n-Np)*KLN;
            anL = An/pow(r0, n-Np)*KLN;
	  }


	  //NOT add the multipole errors of short quadrupole to long quadrupole qp2 & qp7 of soleil ring
	    // for the lattice with quadrupoles which are cut into two halves
          if(N == 2 && strncmp(Cell[k].Elem.PName,"qp2",3)==0)
	    Add_bnL_sys_elem(Cell[k].Fnum, Cell[k].Knum,keywrd, n, 0, 0);
	  else if(N == 2 && strncmp(Cell[k].Elem.PName,"qp7",3)==0)
	    Add_bnL_sys_elem(Cell[k].Fnum, Cell[k].Knum, keywrd, n, 0, 0);
	    // for the lattice with full quadrupoles
	  else if(N == 2 && strncmp(Cell[k].Elem.PName,"q2",2)==0)
	    Add_bnL_sys_elem(Cell[k].Fnum, Cell[k].Knum, keywrd, n, 0, 0);
	  else if(N == 2 && strncmp(Cell[k].Elem.PName,"q7",2)==0)
	    Add_bnL_sys_elem(Cell[k].Fnum, Cell[k].Knum, keywrd, n, 0, 0);
	  else
	  //add errors to multipoles except qp2, qp7
	     Add_bnL_sys_elem(Cell[k].Fnum, Cell[k].Knum, keywrd,n, bnL,anL);
      }
  }

}
/***********************************************************************
void AddFieldValues_fam(const int Fnum, const char *keywrd, const double r0,
			const int n, const double Bn, const double An)

   Purpose:
       add field error of all the kids in a family, with the previous value,
       and then the summation value replaces the previous value.

   Input:
      Fnum            family name
      keywrd       "rms" or "sys"
                   "rms":  random  multipole error
		   "sys":  systematic multipole error
      r0              radius at which error is measured
                      for the case of r0 ???????

      n               order of the error
      Bn              relative B component for the n-th error
      An              relative A component for the n-th error



   Output:
      None

  Return:
      None

  Global variables
      None

  Specific functions:
     None

 Comments:
     10/2010  Written by Jianfeng Zhang
**********************************************************************/
void AddFieldValues_fam(const int Fnum, const char *keywrd, const double r0,
			const int n, const double Bn, const double An)
{
    int     loc = 0, ElemNum = 0, N = 0, k = 0;
    double  bnL = 0.0, anL = 0.0, KLN = 0.0;

    for(k = 1; k <= GetnKid(Fnum); k++){
        loc = Elem_GetPos(Fnum, k); /*element index of kid*/
        N = Cell[loc].Elem.M->n_design;/*design field order*/

        // find the integrated design field strength for multipole
        if (Cell[loc].Elem.M->n_design == 1)
            KLN = Cell[loc].Elem.PL*Cell[loc].Elem.M->Pirho; /* dipole angle */
        else if(Cell[loc].Elem.M->n_design == 0){ //Caso seja corretoras
            N = 1;
            KLN = GetKLpar(Cell[loc].Fnum, Cell[loc].Knum, N);
            if(KLN == 0.0)
                KLN = GetKLpar(Cell[loc].Fnum, Cell[loc].Knum, -N);
        }else
            KLN = GetKLpar(Cell[loc].Fnum, Cell[loc].Knum, N);/* other multipole*/

	   /* absolute integrated field strength*/
        if (r0 == 0){ //?????????
            bnL = Bn;
            anL = An;
        }else{
            bnL = Bn/pow(r0, n-N)*KLN;
            anL = An/pow(r0, n-N)*KLN;
        }
        //add absolute multipole field error for the element
        Add_bnL_sys_elem(Cell[loc].Fnum, Cell[loc].Knum,keywrd, n, bnL, anL);

    }
}

/***********************************************************************
void add_bnL_sys_elem(const int Fnum, const int Knum, const char *keywrd,
		      const int n, const double bnL, const double anL)

   Purpose:
       Add the field error with the previous value, then
	the summmation value replace the previous value,
	in the PBsys definition of multipole.

   Input:
      Fnum           family index
      Knum           kids index
      keywrd         "rms" or "sys"
                     "rms":  random  multipole error
		     "sys":  systematic multipole error
      n              order of the error
      bnL            absolute integrated B component for the n-th error
      anL            absolute integrated A component for the n-th error



   Output:
      None

  Return:
      None

  Global variables
      None

  Specific functions:
     None

 Comments:
     10/2010  Written Jianfeng Zhang

     Rms error on the quadrupoles: only works for full quadrupole, not for half quadrupole
**********************************************************************/
void Add_bnL_sys_elem(const int Fnum, const int Knum, const char *keywrd,
		      const int n, const double bnL, const double anL)
{
  elemtype  elem;
  double *elemMPB; //skew components of the multipole
 // double *elemMPBb; //right components of the multipole
  const bool  prt = false;

  elem = Cell[Elem_GetPos(Fnum, Knum)].Elem;


   if(strcmp("sys",keywrd)==0){

     elemMPB = elem.M->PBsys;

   }
  if(strcmp("rms",keywrd)==0){

    elemMPB = elem.M->PBrms;
   /* save the random scale factor of rms error PBrms*/
    elem.M->PBrnd[HOMmax+n] = normranf();
    elem.M->PBrnd[HOMmax-n] = normranf();

  }

  if (elem.PL != 0.0) {

    elemMPB[HOMmax+n] += bnL/elem.PL;
    elemMPB[HOMmax-n] += anL/elem.PL;
  } else {

    // thin kick
    elemMPB[HOMmax+n] += bnL;
    elemMPB[HOMmax-n] += anL;
  }

  Mpole_SetPB(Fnum, Knum, n);    //set for Bn component
  Mpole_SetPB(Fnum, Knum, -n);   //set for An component

  if (prt)
    printf("add the %s error:  n=%d component of %s, bnL = %e,  %e, anL = %e,  %e\n",
	   keywrd,n, Cell[Elem_GetPos(Fnum, Knum)].Elem.PName,
	   bnL, elemMPB[HOMmax+n],anL, elemMPB[HOMmax-n]);
}

/***********************************************************************
void SetCorrQtErr_fam(char const *fic, const int Fnum, const double conv, const double r0,
			const int n, const double Bn, const double An)

   Purpose:
       Set multipole field error to the thick sextupole which also functions as
       skew quadrupoles, horizontal and vertical correctors which are used for
       orbit correction.

   Input:
      fic             file name with measured corrector value or qt values
      Fnum            family index of horizontal or vertical corrector or skew quadrupole
      conv            conversion from A to T.m for soleil
      r0              radius at which error is measured
      n               order of the error
      Bn              integrated B component for the n-th error
      An              integrated A component for the n-th error

   Output:
      None

  Return:
      None

  Global variables
      None

  Specific functions:
     None

 Comments:

     a.) Measured corrector value is read from a file "fic"
     b.) correctors are at the same location of some sextupoles,
	 so their multipole errors are added to the thick sextupoles
	 which also functions as these correctors.

       10/2010  Written by Jianfeng Zhang
**********************************************************************/
void AddCorrQtErr_fam(char const *fic, const int Fnum, const double conv, const char *keywrd, const double r0,
			const int n, const double Bn, const double An)
{
  int     i = 0, N = 0, corr_index = 0;
  double  bnL = 0.0, anL = 0.0;
  double  brho = 0.0, conv_strength = 0.0;
  double  corr;   /* skew quadrupole horizontal or vertical corrector error, read from a file*/
  int    corrlistThick[120];   /* index of associated sextupole*/

  FILE  *fi;



  brho = globval.Energy/0.299792458; /* magnetic rigidity */

  // assign the design order
    if(Cell[Elem_GetPos(Fnum,1)].Elem.M->n_design == 2 )
    N = 2; /* skew quadrupole*/
    else
    N = 1; /* correctors, they act like dipoles, so N =1, but in the lattice reading, their n_design = 0!!!!*/


  /* Open file with multipole errors*/
   if ((fi = fopen(fic,"r")) == NULL)
  {
    fprintf(stderr, "Error while opening file %s \n",fic);
    exit_(1);
  }


  /* find index of sextupole associated with the corrector */
 // solution 1: find by names
 // solution 2: use a predefined list
 // solution 3: something smart ???
  for (i=0; i< GetnKid(Fnum); i++){
    if (trace) fprintf(stdout, "%d\n", i);

     corr_index = Elem_GetPos(Fnum, i+1);

    if (Cell[corr_index-1].Elem.PName[0] == 's' && Cell[corr_index-1].Elem.PName[1] == 'x')
      corrlistThick[i] = corr_index-1;
    else{

      if (Cell[corr_index+1].Elem.PName[0] == 's' && Cell[corr_index+1].Elem.PName[1] == 'x')
        corrlistThick[i] = corr_index+1;
      else{

        if (Cell[corr_index+2].Elem.PName[0] == 's' && Cell[corr_index+2].Elem.PName[1] == 'x')
          corrlistThick[i] = corr_index+2;
        else{

          if (Cell[corr_index-2].Elem.PName[0] == 's' && Cell[corr_index-2].Elem.PName[1] == 'x')
            corrlistThick[i] = corr_index-2;
          else{

            if (Cell[corr_index+3].Elem.PName[0] == 's' && Cell[corr_index+3].Elem.PName[1] == 'x')
              corrlistThick[i] = corr_index+3;
            else{

              if (Cell[corr_index-3].Elem.PName[0] == 's' && Cell[corr_index-3].Elem.PName[1] == 'x')
                corrlistThick[i] = corr_index-3;
              else fprintf(stdout, "Warning: Sextupole not found associated with corrector or skew quadrupole! \n");
            }
          }
        }
      }
    }
  }


  // add the multipole errors to the associated sextupole
   for (i = 0; i < GetnKid(Fnum); i++)
  {
    fscanf(fi,"%le \n", &corr); /* read the corrector values from a file */

    if (r0 == 0.0) {
    // input is: (b_n*L), (a_n*L) ???
      Add_bnL_sys_elem(Cell[corrlistThick[i]].Fnum,Cell[corrlistThick[i]].Knum,keywrd, n, Bn, An);
    } else {
        conv_strength = corr*conv/brho;
	// absolute integrated error field strength
        bnL = Bn/pow(r0, n-N)*conv_strength;
        anL = An/pow(r0, n-N)*conv_strength;

        Add_bnL_sys_elem(Cell[corrlistThick[i]].Fnum,Cell[corrlistThick[i]].Knum,keywrd, n, bnL, anL);

      }
    }
  fclose(fi); /* close corrector file */
}

/****************************************************************************/
/* void FitTune4(long qf1,long qf2, long qd1, long qd2, double nux, double nuy)

   Purpose:
       Fit tunes to the target values using quadrupoles "qf1","qf2", "qd1", and "qd2".
       Specific for soleil lattice, in which each quadrupole is cut into two parts
       in order to get the optical parameters at the center of quadrupoles.
   Input:
       qf1: tuned half quadrupole
       qf2: tuned another half quadrupole
       qd1: tuned half quadrupole
       qd2: tuned another half quadrupole
       nux: target horizontal tune
       nuy: target vertical tune
   Output:
       none

   Return:
       none

   Global variables:

   specific functions:

   Comments:
     See also:
          FitTune(long qf, long qd, double nux, double nuy) in physlib.cc

****************************************************************************/
void FitTune4(long qf1,long qf2, long qd1, long qd2, double nux, double nuy)
{
  long      i;
  iVector2  nq1 = {0,0},nq2 = {0,0}, nq={0,0};
  Vector2   nu = {0.0, 0.0};
  fitvect   qfbuf, qdbuf;

  /* Get elements for the first quadrupole family */
  nq1[X_] = GetnKid(qf1); // get number of elements for family qf1
  nq2[X_] = GetnKid(qf2); // get number of elements for family qf2
  for (i = 1; i <= (nq1[X_]+nq2[X_]); i++)
    {
      if(i<=nq1[X_])
        qfbuf[i-1] = Elem_GetPos(qf1, i);
      else
        qfbuf[i-1] = Elem_GetPos(qf2, (i-nq1[X_]));
    }

  /* Get elements for the second quadrupole family*/
  nq1[Y_] = GetnKid(qd1);  // get number of elements for family qd1
  nq2[Y_] = GetnKid(qd2);  // get number of elements for family qd2
  for (i = 1; i <= (nq1[Y_]+nq2[Y_]); i++)
    {
      if(i<=nq1[Y_])
        qdbuf[i-1] = Elem_GetPos(qd1, i);
      else
        qdbuf[i-1] = Elem_GetPos(qd2, (i-nq1[Y_]));
    }

  nu[X_] = nux; nu[Y_] = nuy;
  nq[X_] = nq1[X_]+nq1[X_],nq[Y_] = nq1[Y_]+nq1[Y_];

  /* fit tunes */
  Ring_Fittune(nu, nueps, nq, qfbuf, qdbuf, nudkL, nuimax);
}



