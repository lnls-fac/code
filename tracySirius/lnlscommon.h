/*
       Transferred from Tracy 2.7 soleilcommon.h
       
*/
/***************************************************************************
                          soleilcommon.h  -  description
                             -------------------
    begin                : Thu Oct 30 2003
    copyright            : (C) 2003 by nadolski
    email                : nadolski@synchrotron-soleil.fr
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/

#ifndef __LNLSCOMMON_H
#define __LNLSCOMMON_H

#define NTURN 10000
#define DIM 6

/* high level functions for reading lattice file*/  
void lnls_read_lattice(char *fic);

/* Vacuum chamber */
// void PrintCh(void);      // nsrl-ii:  physlib.cc   
//void  ChamberOn(void);    // nsrl-ii:  soleillib.cc (same)
//void ChamberOff(void);    // nsrl-ii: physlib.cc   

/* tracking */
//void GetChromTrac(long Nb, long Nbtour, double emax, double *xix, double *xiz);  //nsrl-ii physlib.cc
//void GetTuneTrac(long Nbtour, double emax, double *nux, double *nuz);    //nsrl-ii physlib.cc


//nsrl-ii physlib.cc
/* close orbit */
// simple precision
//void findcodS(double dP);   
//void computeFandJS(float *x, int n, float **fjac, float *fvect);     
//void Newton_RaphsonS(int ntrial,float x[],int n,float tolx);
// double precision
//void findcod(double dP);
//void computeFandJ(int n, double *x, vector *fjac, double *fvect);
//int Newton_Raphson(int n, double x[],int ntrial,double tolx);


/* Transport mode routine */
//void TransTwiss(double *alpha, double *beta, double *eta, double *etap, double *codvect);


// Tracy III:  naffutils.h
/* Frequency Map Analysis */
//void Get_NAFF(int nterm, long ndata, double T[DIM][NTURN],
//                     double *fx, double *fz, int nbf[2]);
//void Get_Tabshift(double Tab[DIM][NTURN], double Tab0[DIM][NTURN], long nbturn, long nshift);
//void Get_freq(double *fx, double *fz, double *nux, double *nuz);
// repeative definition
// //void GetChromTrac(long Nb, long Nbtour, double emax, double *xix, double *xiz);
// //void GetTuneTrac(long Nbtour, double emax, double *nux, double *nuz);

/* Mandatory for f2c */
//void MAIN__(void);

#endif
