/* Tracy-2

   J. Bengtsson, CBP, LBL      1990 - 1994   Pascal version
                 SLS, PSI      1995 - 1997
   M. Boege      SLS, PSI      1998          C translation
   L. Nadolski   SOLEIL        2002          Link to NAFF, Radia field maps
   J. Bengtsson  NSLS-II, BNL  2004 -        
   J. Zhang      SOLEIL        2010         ADD SOLEIL PARTS IN TRACY 2.7
*/

 /**** Protypes ****/
void SetErr2(long seed,double fac);  //set error for lattice with two half quadrupoles
void SetErr(long seed,double fac);   //set error for lattice with one full quadrupoles
void InducedAmplitude(long spos);
void Hfonction(long pos, double dP);
//void Hcofonction(long pos, double dP,Vector2 H);
void Hcofonction(long pos, double dP);
void Get_Disp_dp(void);
void read_corrh(void);
void set_vectorcod(Vector codvector[], double dP);
void SetDecapole(void);

/* Tracking */
void Phase(double x,double xp,double y, double yp,double energy, double ctau, long Nbtour);
void Phase2(long pos, double x,double xp,double y, double yp,double energy, double ctau,
            long Nbtour);
void PhasePoly(long pos, double x0,double px0, double z0, double pz0, double delta0,
               double ctau0, long Nbtour);
void Check_Trac(double x, double px, double y, double py, double dp);
void PhasePortrait(double x0,double px0,double z0, double pz0, double delta0, double ctau,
                          double end, long Nb, long Nbtour, int num);
void PhasePortrait2(long pos,double x0,double px0,double z0, double pz0, double delta0, double ctau,
                          double end, long Nb, long Nbtour, int num);
void Multipole_thicksext(char const *fic_hcorr, char const *fic_vcorr, char const *fic_skew);
void Multipole_thinsext(char const *fic_hcorr, char const *fic_vcorr, char const *fic_skew);
void MomentumAcceptance(long nturn, double sdeb, double sfin, double ep_min, double ep_max,
			long nstepp, double em_min, double em_max, long nstepm, long nnames, char names[6][max_str]);

void Trac_Tab(double x, double px, double y, double py, double dp,
            long nmax, long pos, long *lastn, long *lastpos, FILE *outf1, double Tx[][NTURN]);
void SetSkewQuad(void);
void Trac_COD(double x, double px, double y, double py, double dp, double ctau,
                 long nmax, long &lastn, long &lastpos);
void Dyna(long Nbx, long Nbz, long Nbtour, double xmax, double zmax,
               double energy, bool diffusion);
void daxy(long Nbx, long Nbz, long Nbtour, double x0, double xmax,
		double z0, double zmax, double energy);
void daex(long Nbx, long Nbe, long Nbtour, double x0, double xmax,
		double emin, double emax, double z);
                            
void daxy_radial(long Nbtour, long nr_radial, double energy, double xscale, double zscale, double r_tol);

/* Frequency map analysis */
void TunesShiftWithEnergy(long Nb, long Nbtour, double emax);
//void fmap(long Nbx, long Nbz, long Nbtour, double xmax, double zmax,
//                 double energy, bool diffusion, bool matlab);
//void fmapdp(long Nbx, long Nbe, long Nbtour, double xmax, double emax,
//              double z, bool diffusion, bool matlab);
void fmap(long Nbx, long Nbz, long Nbtour, double x0, double xmax,
		double z0, double zmax, double energy, bool diffusion);
void fmapdp(long Nbx, long Nbe, long Nbtour, double x0, double xmax,
		double emin, double emax, double z, bool diffusion);
void Nu_Naff(void);
void TunesShiftWithAmplitude(long Nbx, long Nbz, long Nbtour, double xmax, double ymax,
                 double energy);

/* Vacuum chamber */
void ReadCh(const char *AperFile);

void Enveloppe(double x, double px, double y, double py,
                      double dp, double nturn);


/* Longitudinal Hamiltonian*/
void PhaseLongitudinalHamiltonien(void);
void PassA(double *phi, double delta0, double step);
void PassB(double phi0, double *delta, double step);
double Hsynchrotron(double phi, double delta);

/* Miscelleneous */ 
void Enveloppe2(double x, double px, double y, double py,
                      double dp, double nturn);
void Phase3(long pos, double x,double px,double y, double py,double energy,
            double ctau, long Nbtour);
double EnergySmall(double *X, double irho);
double EnergyDrift(double *X);
void getA4antidamping();
void fmapfull(long Nbx, long Nbz, long Nbtour, double xmax, double zmax,
              double energy, bool diffusion);
void spectrum(long Nbx, long Nbz, long Nbtour, double xmax, double zmax,
              double energy, bool diffusion);
	      
/* coupling*/
void Coupling_Edwards_Teng(void);

/* get and set RF voltage */
double get_RFVoltage(const int Fnum);

void set_RFVoltage(const int Fnum, const double V_RF);

/* Read multipole errors from a file for soleil*/
void ReadFieldErr(const char *FieldErrorFile);

void AddFieldErrors(const char *name,const char *keywrd, const double r0,
		    const int n, const double Bn, const double An); 
		    
void AddFieldValues_type(const int N, const char *keywrd, const double r0,
			 const int n, const double Bn, const double An);

void AddFieldValues_fam(const int Fnum, const char *keywrd, const double r0,
			const int n, const double Bn, const double An);

void Add_bnL_sys_elem(const int Fnum, const int Knum, const char *keywrd,
		      const int n, const double bnL, const double anL);
		      								 			 
void AddCorrQtErr_fam(char const *fic, const int Fnum, const double conv, const char *keywrd, const double r0,
			const int n, const double Bn, const double An);
			 
/* fit tunes for soleil lattice, in which each quadrupole is cut into two parts*/			
void FitTune4(long qf1,long qf2, long qd1, long qd2, double nux, double nuy);			 
			 	


	      
