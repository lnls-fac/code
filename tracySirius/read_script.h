#ifndef READ_SCRIPT_H
#define READ_SCRIPT_H


/* class to read the parameters of the bool flags in the user input script */
 class UserCommand
 {
   public:
   char  CommandStr[max_str];   // bool flag name
   
 /***** parameters *******/
    //RFVoltFlag
   double RFvolt;   // RF voltage
   char CavityFlag[max_str]; // Turn cavity on and off
   char VacuumChamberFlag[max_str]; // Turn cavity on and off
   char RadiationFlag[max_str]; // Turn radiation on and off
   
   //chamber file
   char chamber_file[max_str];
   
    // misalignment error file
   char    ae_file[max_str];
   
   // field error file
   char    fe_file[max_str]; 
   
    // FitTuneFlag ; 
   char quads[5][max_str];
   double targetnux, targetnuz;
   int n_quads;
   // FitTune4Flag  ; 
    char qf1[max_str],qf2[max_str],qd1[max_str],qd2[max_str]; 
 // FitChromFlag ; 
   char sxm1[max_str],sxm2[max_str]; 
   double targetksix, targetksiz ;
  //add coupling error to full/half quadrupoles
   long err_seed; 
   double err_rms;
  //AmplitudeTuneShiftFlag;
   long _AmplitudeTuneShift_nxpoint, _AmplitudeTuneShift_nypoint;
   long _AmplitudeTuneShift_nturn;
   double _AmplitudeTuneShift_xmax, _AmplitudeTuneShift_ymax, _AmplitudeTuneShift_delta;
 
 //EnergyTuneShiftFlag;
   long _EnergyTuneShift_npoint, _EnergyTuneShift_nturn;
   double _EnergyTuneShift_deltamax;
 
 //extern bool FmapFlag;
   long _FmapFlag_nxpoint, _FmapFlag_nypoint, _FmapFlag_nturn;
   double _FmapFlag_x0, _FmapFlag_xmax, _FmapFlag_y0,_FmapFlag_ymax, _FmapFlag_delta;
   bool _FmapFlag_diffusion; 
 
 //extern bool FmapdpFlag;
   long _FmapdpFlag_nxpoint, _FmapdpFlag_nepoint, _FmapdpFlag_nturn;
   double _FmapdpFlag_x0, _FmapdpFlag_xmax, _FmapdpFlag_emin, _FmapdpFlag_emax, _FmapdpFlag_z;
   bool _FmapdpFlag_diffusion;	
   
   
 //extern bool DynamicAperXY;
   long _DAXY_nxpoint, _DAXY_nypoint, _DAXY_nturn;
   double _DAXY_x0, _DAXY_xmax, _DAXY_y0,_DAXY_ymax, _DAXY_delta;

 //extern bool DynamicAperXYRadial;
   long _DAXY_nr_radial;
   double _DAXY_xscale, _DAXY_yscale, _DAXY_r_tol;
 
 //extern bool DynamicAperEX;
   long _DAEX_nxpoint, _DAEX_nepoint, _DAEX_nturn;
   double _DAEX_x0, _DAEX_xmax, _DAEX_emin, _DAEX_emax, _DAEX_z;
   	

   
  //MomentumAccFlag;
   char TrackDim[3], _MomentumAccFlag_names[12][max_str];
   long  _MomentumAccFlag_nturn, _MomentumAccFlag_nstepn,
      _MomentumAccFlag_nstepp, _MomentumAccFlag_nnames;
   double _MomentumAccFlag_deltaminn, _MomentumAccFlag_deltamaxn;
   double _MomentumAccFlag_deltaminp, _MomentumAccFlag_deltamaxp;
   double _MomentumAccFlag_sstart, _MomentumAccFlag_sstop;
 
  // /* Phase space */
   double _Phase_X, _Phase_Px, _Phase_Y, _Phase_Py,_Phase_delta, _Phase_ctau;
   long _Phase_nturn;
   char _Phase_Dim[3];
   bool _Phase_Damping;
 
   //Touschek lifetime
   bool TouschekFlag, IBSFlag, TousTrackFlag;
   double _Qb, _Coup;
   
    
    //set default values
  UserCommand(void)   //constructor
 {  
  
  // /* fmap for on momentum particle*/
   _FmapFlag_nxpoint=31L, _FmapFlag_nypoint=21L, _FmapFlag_nturn=516L;
   _FmapFlag_x0=0.0, _FmapFlag_xmax=0.025, _FmapFlag_x0=0.0, _FmapFlag_ymax=0.005, _FmapFlag_delta=0.0;
   _FmapFlag_diffusion = true;

/*fmap for off momentum particle*/
 _FmapdpFlag_nxpoint=31L, _FmapdpFlag_nepoint=21L, _FmapdpFlag_nturn=516L;
 _FmapdpFlag_x0=0.0, _FmapdpFlag_xmax=0.025, _FmapdpFlag_emin=-0.005, _FmapdpFlag_emax=0.005, _FmapdpFlag_z=0.0;
 _FmapdpFlag_diffusion = true;			
 
 
//  Dynamic Aperture in the plane X Y
   _DAXY_nxpoint=31L, _DAXY_nypoint=21L, _DAXY_nturn=516L;
   _DAXY_x0=0.0, _DAXY_xmax=0.025, _DAXY_x0=0.0, _DAXY_ymax=0.005, _DAXY_delta=0.0;

//  Dynamic Aperture in the plane E X
 _DAEX_nxpoint=31L, _DAEX_nepoint=21L, _DAEX_nturn=516L;
 _DAEX_x0=0.0, _DAEX_xmax=0.025, _DAEX_emin=-0.005, _DAEX_emax=0.005, _DAEX_z=0.0;		

/* tune shift with amplitude*/
 _AmplitudeTuneShift_nxpoint=31L;  _AmplitudeTuneShift_nypoint=21L;
 _AmplitudeTuneShift_nturn=516L;   _AmplitudeTuneShift_xmax=0.025;
 _AmplitudeTuneShift_ymax=0.005,   _AmplitudeTuneShift_delta=0.0;

/* tune shift with energy*/
 _EnergyTuneShift_npoint=31L;  _EnergyTuneShift_nturn=516L;
 _EnergyTuneShift_deltamax=0.06;

/* random rotation coupling error*/
 err_seed=0L;  err_rms=0.0;  

/* momentum acceptance */
 TrackDim[3] = '6D';
 _MomentumAccFlag_nturn=5000L,  _MomentumAccFlag_nnames=12L;
 _MomentumAccFlag_sstart=0.00, _MomentumAccFlag_sstop=52.0;
 _MomentumAccFlag_nstepn=100L, _MomentumAccFlag_nstepp=100L;
 _MomentumAccFlag_deltaminn=-0.01, _MomentumAccFlag_deltamaxn=-0.05;
 _MomentumAccFlag_deltaminp=0.01, _MomentumAccFlag_deltamaxp=0.05;

/* Phase space */
 _Phase_X=0.0, _Phase_Px=0.0, _Phase_Y=0.0, _Phase_Py=0.0,
 _Phase_delta=0.0, _Phase_ctau=0.0;
 _Phase_nturn=512L;
 _Phase_Dim[3]='4D';
 _Phase_Damping = false;

/* IBS */
 _Qb=0;
 _Coup=0;
  
/* fit tunes for full quadrupole*/
 targetnux = 0.0, targetnuz = 0.0;

/* fit charomaticities*/
 targetksix = 0.0, targetksiz = 0.0;
 
 
};  
 
 };

/***** file names************/
 //files with multipole errors
 extern char fic_hcorr[max_str],fic_vcorr[max_str], fic_skew[max_str];
 extern char multipole_file[max_str];


 extern char twiss_file[max_str];
 extern char cod_file[max_str];
 extern char girder_file[max_str];
  
 //files with the status of hcorr/vcorr status, to choose which correctors are used for orbit correction
 extern char    hcorr_file[max_str], vcorr_file[max_str];
// extern char    fe_file[max_str]; //the same as multipole_file[max_str]?????

//COD correction
 extern int nwh, nwv; 

extern char hcorr_name[max_str], vcorr_name[max_str];
extern char skew_quad_name[max_str], bpm_name[max_str];
extern char gs_name[max_str], ge_name[max_str];

// function
 void read_script(const char *param_file_name, bool rd_lat,long& CommNo, UserCommand UserCommandFlag[]);

#endif
