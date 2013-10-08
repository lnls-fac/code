/* Tracy-2

   J. Bengtsson, CBP, LBL      1990 - 1994   Pascal version
                 SLS, PSI      1995 - 1997
   M. Boege      SLS, PSI      1998          C translation
   L. Nadolski   SOLEIL        2002          Link to NAFF, Radia field maps
   J. Bengtsson  NSLS-II, BNL  2004 -        

*/


extern const int   nCOR;
extern const char  hOrbitFileName[];     
extern const char  vOrbitFileName[];    
extern const char  OrbScanFileName[];    
 
 extern FILE     *OrbScanFile;

/****** for orbit correction *********/
void prt_gcmat(int bpm, int corr, int plane);

void gcmat(int bpm, int corr, int plane);

void lsoc(int niter, int bpm, int corr, int plane);

/***The following functions are copied from nsls-ii_lib_templ.h, need to be tested***/
bool CorrectCOD_Ns(FILE *hOrbitFile, FILE *vOrbitFile, const char *ae_file, const int n_orbit,
     const int n, const int k, const int nwh, const int nwv, int *hcorrIdx, int *vcorrIdx);
     
void readCorrectorList(const char *hCorrListName, const char *vCorrListName, int *hcorrIdx, int *vcorrIdx);

void gcmats(int bpm, int corr, int plane, int *corrIdx);

void LoadFieldErrs(const char *FieldErrorFile, const bool Scale_it,
     const double Scale, const bool new_rnd, const int ik);
     
bool CorrectCOD_Ns(FILE *hOrbitFile, FILE *vOrbitFile, const char *ae_file, const int n_orbit,
     const int n, const int k, const int nwh, const int nwv, int *hcorrIdx, int *vcorrIdx);
     
bool CorrectCODs(FILE *hOrbitFile, FILE *vOrbitFile, int n_orbit, int nwh, int nwv, int *hcorrIdx, int *vcorrIdx);

void lsoc2(int niter, int bpm, int corr, int plane, int nval);

void lsoc2s(int niter, int bpm, int corr, int plane, int nval, int *corIdx);

void Align_BPM2quad(const int n);


/*** The following functions are copied from physlib_templ.h, need to be tested ***/
void codstats(FILE *hOrbitFile, FILE *vOrbitFile, double *mean, double *sigma, double *xmax, long lastpos, bool all);

void corstat(double *mean, double *sigma, double *xmax, long lastpos);

