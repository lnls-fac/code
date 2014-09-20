char* get_prm_scl(void);  

void LoadFieldErr_scl(const char *FieldErrorFile, const bool Scale_it,
		      const double Scale, const bool new_rnd, const int m) ;
		      
void get_cod_rms_data(const int n_seed, const int nfam, const int fnums[], 
                      const double dx, const double dy, const double dr,
		      double x_mean[][6], double x_sigma[][6], 
		      double theta_mean[][2], double theta_sigma[][2]) ;

void prt_cod_rms_data(const char name[], double x_mean[][6], 
                      double x_sigma[][6], double theta_mean[][2], 
		      double theta_sigma[][2]) ;	

void add_family( const char *name, int &nfam, int fnums[] ) ;

void get_cod_rms_scl(const double dx, const double dy, const double dr,
		     const int n_seed) ;
		     
void get_cod_rms_scl_new(const int n_seed) ;

double get_dynap_scl(const double delta, const int n_track2) ;

void get_matching_params_scl() ;
	


    

