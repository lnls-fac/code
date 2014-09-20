/***************************************************************************
                          soleilcommon.c  -  description
                             -------------------
    begin                : Thu Oct 30 2003
    copyright            : (C) 2003 by nadolski
    email                : nadolski@synchrotron-soleil.fr
 ***************************************************************************/
/*
  Transferred from Tracy 2.7 soleilcommon.c and 
  modified based on Read_Lattice() in Tracy III physlib.cc
*/
/* Current revision $Revision$
 On branch $Name$
 Latest change $Date$ by $Author$
*/


/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/

//#include "tracy.h"

//#include "soleilcommon.h"
//#include "soleillib.h"
//#include "datatyp.h"
//#include "physlib.h"

#include "tracy_lib.h"

/****************************************************************************/
/* void  Read_Lattice(char *fic)

   Purpose:
       Read lattice file (fic.lat) and print statistics
       Generate debugging info if problem in fic.lax
       Initialize Tracy
       Initialize the RING
       Define the vacuum chamber
       Compute Twiss parameters and chromaticities for on momentum particle
         and save them in the file named linlat.lat

   Input:
       fic lattice file w/o its mandatory extension .lat

   Output:
       none

   Return:
       none

   Global variables:
       globval
       S_SIZE

   Specific functions:

       t2init, Lattice_Read
       Cell_Init()
       DefineCh
       Ring_GetTwiss
       printglob

   Comments:
       27/04/03 energy RF acceptance added set to 6%
       29/04/03 eps added for energy RF acceptance
       28/10/03 modified for transfer lines, filename added in output
       02/06/08 energy RF acceptance set to 1 just to avoid overflow during tracking
       22/06/10 add new globval.  flag and modify new name of variables
                 from Tracy III Read_Lattice(), which is defined in physlib.cc 

****************************************************************************/
void Read_Lattice(char *fic)
{
  char fic_maille[S_SIZE + 4] = "";
  char fic_erreur[S_SIZE + 4] = "";
  bool status;
  bool chroma = true;
  double dP = 0.0;
  const double RFacceptance = 1.0; // maximum excursion during tracking
 
  Vector2  beta, alpha, eta, etap;
  Vector   codvect;
//  double beta[2], alpha[2], eta[2], etap[2], codvect[6];
  int i;

  strcpy(fic_maille, fic);
  strcpy(fic_erreur, fic);

  /* automatic generation of filenames for lattice and error */
  strcat(fic_maille, ".lat");
  strcat(fic_erreur, ".lax");

  /* Initialisation de Tracy */

  t2init();

  /* open the lattice Input file  */

  if ((fi = fopen(fic_maille, "r")) == NULL)
  {
    fprintf(stdout,
       "ReadLattice: Error while opening file %s \n",
       fic_maille);
    fprintf(stdout, "The lattice file name is wrong! \n");
    exit(1);
  }

  /* opens the lattice Output file */
  if ((fo = fopen(fic_erreur, "w")) == NULL)
  {
    fprintf(stdout,
       "ReadLattice: Error while opening file %s \n Access issue",
       fic_erreur);
    exit(1);
  }

  /* Reads lattice and set principle parameters
   * Energy CODeps and energy offset
   * print statistics
   */
  status = Lattice_Read(&fi, &fo);

  if (status == false)
  {
    fprintf(stdout,
       "Lattice_Read function has returned false\n");
    fprintf(stdout, "See file %s \n", fic_erreur);
    exit(1);
  }
  fprintf(stdout, "Lattice file: %s\n", fic_maille);

  /* initializes cell structure: construction of the RING */
  /* Creator of all the matrices for each element         */
  Cell_Init();

  // for a ring 
  if (globval.RingType == 1)
  {      
    
    /* Defines global variables for Tracy code */
    
    globval.H_exact     = false; // Small Ring Hamiltonian
    globval.quad_fringe = false; // quadrupole fringe fields on/off
    globval.EPU         = false; // Elliptically Polarizing Undulator
    globval.IBS         = false; /* diffusion on/off */
    
    globval.MatMeth    = false; /* matrix method */
    globval.Cavity_on  = false; /* Cavity on/off */
    globval.radiation  = false; /* radiation on/off */
    globval.emittance  = false; /* emittance  on/off */
    globval.pathlength = false; /* Path lengthening computation */
    globval.CODimax    = 40L;   /* maximum number of iterations for COD algo */
    globval.dPcommon   = 1e-10; /* Common energy step for energy differentiation */
    globval.delta_RF  = RFacceptance;/* energy acceptance for SOLEIL */

   /* define x/y physical aperture, use the default values: +- 1 meter  */
    globval.Aperture_on = false;
    
    /* Compute and get Twiss parameters */
    Ring_GetTwiss(chroma = true, dP = 0.0);

  //  Cell_SetdP(dP);  /* added for correcting BUG if non convergence: compute on momentum linear matrices */
  }
  
  else 
  { // for transfer lines  
    /* Initial settings : */
    beta[0]  = 8.1;
    alpha[0] = 0.0;
    beta[1]  = 8.1;
    alpha[1] = 0.0;
    eta[0]   = 0.0;
    etap[0]  = 0.0;
    eta[1]   = 0.0;
    etap[1]  = 0.0;

     for (i = 0; i < ss_dim; i++) {
    {
      codvect[i] = 0.0;
      globval.CODvect[i] = codvect[i];
    }
    dP = codvect[4];

    /* Defines global variables for Tracy code */
    globval.MatMeth = false;  /* matrix method */
    globval.Cavity_on = false;  /* Cavity on/off */
    globval.radiation = false;  /* radiation on/off */
    globval.emittance = false;  /* emittance  on/off */
    globval.pathlength = false;  /* Path lengthening computation */
    globval.CODimax = 10L;  /* maximum number of iterations for COD algo */
    globval.dPcommon = 1e-10;  /* Common energy step for energy differentiation */
    globval.delta_RF = RFacceptance;  /* 6% + epsilon energy acceptance for SOLEIL */
    globval.dPparticle = dP;
     
  /* define x/y physical aperture, use the default values: +- 1 meter  */
    globval.Aperture_on = false;
    
    
    TransTwiss(alpha, beta, eta, etap, codvect);
    }
  } 
  /* SOLEIL print out lattice functions, with all the optical information for the lattice with design values */
  printlatt("linlat.out");  
}





