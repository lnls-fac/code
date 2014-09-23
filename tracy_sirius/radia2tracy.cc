/* Tracy-2

 J. Bengtsson, CBP, LBL      1990 - 1994   Pascal version
 SLS, PSI      1995 - 1997
 M. Boege      SLS, PSI      1998          C translation
 L. Nadolski   SOLEIL        2002          Link to NAFF, Radia field maps
 J. Bengtsson  NSLS-II, BNL  2004 -

 */


//#include "tracy_lib.h"

/* Spline routine adapted from NR with template */
/************************************************************************************************** 
  void spline(const double x[], const T y[], int const n, double const yp1,
        const double ypn, T y2[])
      
    Purpose:	  
       Function to be called only once
       Given arrays x[1..n] and y[1..n] containing a tabulated function, i.e., yi = f(xi), with
       x1 <x2 < :: : < xN, and given values yp1 and ypn for the first derivative of the interpolating
       function at points 1 and n, respectively, this routine returns an array y2[1..n] that contains
       the second derivatives of the interpolating function at the tabulated points xi. If yp1 and/or
       ypn are equal to 10e30 or larger, the routine is signaled to set the corresponding boundary
       condition for a natural spline, with zero second derivative on that boundary.
 ***************************************************************************************************/
template<typename T>
void spline(const double x[], const T y[], int const n, double const yp1,
        const double ypn, T y2[])
{
    int i, k;
    double sig;
    T p, u[n], qn, un;

    if (yp1 > 0.99e30)
        y2[1] = u[1] = 0.0;
    else {
        y2[1] = -0.5;
        u[1] = (3.0 / (x[2] - x[1])) * ((y[2] - y[1]) / (x[2] - x[1]) - yp1);
    }
    for (i = 2; i <= n - 1; i++) {
        sig = (x[i] - x[i - 1]) / (x[i + 1] - x[i - 1]);
        p = sig * y2[i - 1] + 2.0;
        y2[i] = (sig - 1.0) / p;
        u[i] = (y[i + 1] - y[i]) / (x[i + 1] - x[i]) - (y[i] - y[i - 1])
                / (x[i] - x[i - 1]);
        u[i] = (6.0 * u[i] / (x[i + 1] - x[i - 1]) - sig * u[i - 1]) / p;
    }
    if (ypn > 0.99e30)
        qn = un = 0.0;
    else {
        qn = 0.5;
        un = (3.0 / (x[n] - x[n - 1])) * (ypn - (y[n] - y[n - 1]) / (x[n] - x[n
                - 1]));
    }
    y2[n] = (un - qn * u[n - 1]) / (qn * y2[n - 1] + 1.0);
    for (k = n - 1; k >= 1; k--)
        y2[k] = y2[k] * y2[k + 1] + u[k];
}

/*********************************************************************************************** 
 void splint(const double xa[], const U ya[], const U y2a[], const int n,
        const T &x, T &y) 
	
  Purpose:
            SPLine INTerpolation. Once spline are known, only evaluate polynome
            Given the arrays xa[1..n] and ya[1..n], which tabulate a function (with the xai's in order),
            and given the array y2a[1..n], which is the output from spline above, and given a value of
            x, this routine returns a cubic-spline interpolated value y.
 ***********************************************************************************************/
template<typename T, typename U>
void splint(const double xa[], const U ya[], const U y2a[], const int n,
        const T &x, T &y)
{
    int klo, khi, k;
    double h;
    T a, b;

    klo = 1;
    khi = n;
    while (khi - klo > 1) {
        k = (khi + klo) >> 1;
        if (xa[k] > x)
            khi = k;
        else
            klo = k;
    }
    h = xa[khi] - xa[klo];
    if (h == 0.0)
        nrerror("Bad xa input to routine splint");
    a = (xa[khi] - x) / h;
    b = (x - xa[klo]) / h;
    y = a * ya[klo] + b * ya[khi] + ((a * a * a - a) * y2a[klo] + (b * b * b
            - b) * y2a[khi]) * (h * h) / 6.0;
}

/**********************************************************************************************
 void splin2(const double x1a[], const double x2a[], double **ya, double **y2a,
        const int m, const int n, const T &x1, const T &x2, T &y)
	
 Purpose:
    Main function computing the bicubic spline
    Given x1a, x2a, ya, m, n as described in splie2 and y2a as produced by that routine; and
    given a desired interpolating point x1,x2; this routine returns an interpolated function 
    value y by bicubic spline interpolation.
 ******************************************************************************************/
template<typename T>
void splin2(const double x1a[], const double x2a[], double **ya, double **y2a,
        const int m, const int n, const T &x1, const T &x2, T &y)
{
    int j;
    T ytmp[m + 1], yytmp[m + 1]; // Perform m evaluations of the row splines constructed by

    for (j = 1; j <= m; j++) //splie2, using the one-dimensional spline evaluator
        splint(x2a, ya[j], y2a[j], n, x2, yytmp[j]); //splint.
    spline(x1a, yytmp, m, 1.0e30, 1.0e30, ytmp); // Construct the one-dimensional column spline and evaluate it.
    splint(x1a, yytmp, ytmp, m, x1, y);
}

/************************************************************************************************** 
void splie2(double x1a[], double x2a[], double **ya, int m, int n, double **y2a)
  
  Purpose:
      precompute the auxiliary second-derivative table
      Given an m by n tabulated function ya[1..m][1..n], and tabulated independent variables
      x2a[1..n], this routine constructs one-dimensional natural cubic splines of the rows of ya
      and returns the second-derivatives in the array y2a[1..m][1..n]. (The array x1a[1..m] is
      included in the argument list merely for consistency with routine splin2.)
 ***************************************************************************************************/
void splie2(double x1a[], double x2a[], double **ya, int m, int n, double **y2a)
{
    int j;

    for (j = 1; j <= m; j++)
        // Values 10e30 signal a natural spline
        spline(x2a, ya[j], n, 1.0e30, 1.0e30, y2a[j]);
}

/****************************************************************************/
/* void  Read_IDfile(char *fic_radia, int *pnx, int *pnz,
 double tabx[IDXMAX],  double tabz[IDZMAX],
 double thetax[IDZMAX][IDXMAX], double thetaz[IDZMAX][IDXMAX])
 Purpose:
 Reads ID parameters from file specified by fic_radia
 First or Second order terms

 Input:
 fic_radia radia file to read ID description from
 The input format is the same for first and second order kicks

 Output:
 pnx    horizontal point number for theta matrices
 pnz    horizontal point number for theta matrices
 tabx   tabular for horizontal discretization values
 tabz   tabular for vertical discretization values
 thetax 2D horizontal matrix for first or second order kicks
 thetaz 2D vertical matrix for first or second order kicks

 Return:
 none

 Global variables:
 none

 Specific functions:
 none
 
 Comments:
 WARNING: the filename must be a lowercase name without special
 characters !!!

 and without its MANDATORY .dat extension
 18/10/03 add test for numerical zero to correct H chromaticity
 divergence
 ****************************************************************************/

#define ZERO_RADIA 1e-7
void Read_IDfile(char *fic_radia, double *L, int *pnx, int *pnz,
        double tabx[IDXMAX], double tabz[IDZMAX],
        double thetax[IDZMAX][IDXMAX], double thetaz[IDZMAX][IDXMAX]) {
    FILE *fi;
    char dummy[5000];
    int nx, nz;
    int i, j;
    traceID = false;

    /* open radia text file */
    if ((fi = fopen(fic_radia, "r")) == NULL) {
        fprintf(stdout, "Read_IDfile: Error while opening file %s \n",
                fic_radia);
        exit_(1);
    }

    fprintf(stdout, "\n");
    fprintf(stdout, "Reading ID file:  %s \n", fic_radia);

    /* first line */
    fscanf(fi, "%[^\n]\n", dummy); /* Read a full line */
    fprintf(stdout, "%s\n", dummy);
    /* second line */
    fscanf(fi, "%[^\n]\n", dummy);
    fprintf(stdout, "%s\n", dummy);
    /* third line */
    fscanf(fi, "%[^\n]\n", dummy);
    fprintf(stdout, "%s\n", dummy);
    /* fourth line : Undulator length */
    fscanf(fi, "%lf\n", L);
    fprintf(stdout, "Insertion of Length L = %lf m\n", *L);
    /* fifth line */
    fscanf(fi, "%[^\n]\n", dummy);
    fprintf(stdout, "%s\n", dummy);
    /* sisxth line : Number of Horizontal points */
    fscanf(fi, "%d\n", &nx);
    fprintf(stdout, "nx = %d\n", nx);
    /* seventh line */
    fscanf(fi, "%[^\n]\n", dummy);
    fprintf(stdout, "%s\n", dummy);
    /* Number of Vertical points */
    fscanf(fi, "%d\n", &nz);
    fprintf(stdout, "nz = %d\n", nz);

    /* Check dimensions */
    if (nx > IDXMAX || nz > IDZMAX) {
        fprintf(stdout,
                "Read_IDfile:  Increase the size of insertion tables \n");
        fprintf(stdout, "nx = % d (IDXmax = %d) and nz = %d (IDZMAX = % d) \n",
                nx, IDXMAX, nz, IDZMAX);
        exit_(1);
    }

    /* ninth line */
    fscanf(fi, "%[^\n]\n", dummy);
    //  fprintf(stdout, "%s\n", dummy);
    /* tenth line */
    fscanf(fi, "%[^\n]\n", dummy);
    //  fprintf(stdout,"%s\n", dummy);

    /* eleventh line : x scaling */
    //  fscanf(fi, "%[^\n]\n", &dummy);
    //  fprintf(stdout, "%s\n", dummy);

    for (j = 0; j < nx; j++)
        fscanf(fi, "%lf", &tabx[j]);
    fscanf(fi, "%[^\n]\n", dummy);

    /* Array creation for thetax */
    for (i = 0; i < nz; i++) {
        //    fscanf(fi,"%*lf"); /*read without storage */
        fscanf(fi, "%lf", &tabz[i]); /*read without storage */

        for (j = 0; j < nx; j++) {
            fscanf(fi, "%lf", &thetax[i][j]);
            if (fabs(thetax[i][j]) < ZERO_RADIA)
                thetax[i][j] = 0.0;
            if (traceID)
                fprintf(stdout, "%+12.8lf ", thetax[i][j]);
        }
        fscanf(fi, "\n");
        if (traceID)
            fprintf(stdout, "\n");
    }

    /* comment line */
    fscanf(fi, "%[^\n]\n", dummy);
    //  fprintf(stdout,"%s\n", dummy);
    /* comment line */
    fscanf(fi, "%[^\n]\n", dummy);
    //  fprintf(stdout,"%s\n", dummy);
    /* xscale */
    //  fscanf(fi,"%[^\n]\n", dummy);
    //  fprintf(stdout,"%s\n", dummy);
    for (j = 0; j < nx; j++) {
        fscanf(fi, "%lf", &tabx[j]);
    }

    /* Array creation for thetaz */
    for (i = 0; i < nz; i++) {
        fscanf(fi, "%*f");
        for (j = 0; j < nx; j++) {
            fscanf(fi, "%lf", &thetaz[i][j]);
            if (fabs(thetaz[i][j]) < ZERO_RADIA)
                thetaz[i][j] = 0.0;
            if (traceID)
                fprintf(stdout, "%+12.8lf ", thetaz[i][j]);
        }
        fscanf(fi, "\n");
        if (traceID)
            fprintf(stdout, "\n");
    }

    /* For debugging */
    if (traceID)
        for (j = 0; j < nx; j++) {
            fprintf(stdout, "tabx[%d] =% lf\n", j, tabx[j]);
        }
    if (traceID)
        for (j = 0; j < nz; j++) {
            fprintf(stdout, "tabz[%d] =% lf\n", j, tabz[j]);
        }

    *pnx = nx;
    *pnz = nz;

    fclose(fi);
}

/****************************************************************************/
/* void LinearInterpolation2(double X, double Z, double &TX, double &TZ,
 CellType &Cell, bool &out, int order)

 Purpose:
 Computes thx and thz in X and Z values using a bilinear interpolation
 interpolation of the array thetax(x,z) and thetaz(x,z)

 Input:
 X, Z location of the interpolation
 Cell element containing ID device
 order 1 for first order kick map interpolation
 2 for second order kick map interpolation

 Output:
 TX, TZ thetax and thetaz interpolated at X and Z
 out true if interpolation out of table

 Return:
 none

 Global variables:
 none

 Specific functions:
 
 Comments:
 Search for index could be speed up easily
 
 ****************************************************************************/
template<typename T>
void LinearInterpolation2(T &X, T &Z, T &TX, T &TZ, CellType &Cell, bool &out,
        int order) {
    int i, ix = 0, iz = 0;
    T T1, U, THX = 0.0, THZ = 0.0;
    double xstep = 0.0;
    double zstep = 0.0;
    int nx = 0, nz = 0;
    InsertionType *WITH;
    traceID = false;

    WITH = Cell.Elem.ID;

    if (order == 1) {
        nx = WITH->nx1;
        nz = WITH->nz1;

        xstep = WITH->tabx1[1] - WITH->tabx1[0]; /* increasing values */
        zstep = WITH->tabz1[0] - WITH->tabz1[1]; /* decreasing values */

        if (traceID)
            printf("LinearInterpolation2: xstep = % f zstep = % f\n", xstep,
                    zstep);

        /* test whether X and Z within the transverse map area */
        if (X < WITH->tabx1[0] || X > WITH->tabx1[nx - 1]) {
            printf("LinearInterpolation2: X out of borders \n");
            printf("X = % lf but tabx[0] = % lf and tabx[nx-1] = % lf\n",
                    is_double<T>::cst(X), WITH->tabx1[0], WITH->tabx1[nx - 1]);
            out = true;
            return;
        }

        if (Z > WITH->tabz1[0] || Z < WITH->tabz1[nz - 1]) {
            printf("LinearInterpolation2: Z out of borders \n");
            printf("Z = % lf but tabz[0] = % lf and tabz[nz-1] = % lf\n",
                    is_double<T>::cst(Z), WITH->tabz1[0], WITH->tabz1[nz - 1]);
            out = true;
            return;
        }

        out = false;

        /* looking for the index for X */
        i = 0;
        while (X >= WITH->tabx1[i] && i <= nx - 1) {
            i++;
            if (traceID)
                printf("%2d % lf % lf % lf \n", i, is_double<T>::cst(X),
                        WITH->tabx1[i], WITH->tabx1[i + 1]);
        }
        ix = i - 1;

        /* looking for the index for Z */
        i = 0;
        while (Z <= WITH->tabz1[i] && i <= nz - 1) {
            i++;
            if (traceID)
                printf("%2d % lf % lf % lf \n", i, is_double<T>::cst(Z),
                        WITH->tabz1[i], WITH->tabz1[i + 1]);
        }
        iz = i - 1;

        if (traceID)
            printf("LinearInterpolation2: Indices are ix=%d and iz=%d\n", ix,
                    iz);

        /** Bilinear Interpolation **/
        U = (X - WITH->tabx1[ix]) / xstep;
        T1 = -(Z - WITH->tabz1[iz]) / zstep;

        // first order kick map interpolation
        if (ix >= 0 && iz >= 0) {
            THX = (1.0 - U) * (1.0 - T1) * WITH->thetax1[iz][ix] + U * (1.0
                    - T1) * WITH->thetax1[iz][ix + 1] + (1.0 - U) * T1
                    * WITH->thetax1[iz + 1][ix] + U * T1
                    * WITH->thetax1[iz + 1][ix + 1];

            THZ = (1.0 - U) * (1.0 - T1) * WITH->thetaz1[iz][ix] + U * (1.0
                    - T1) * WITH->thetaz1[iz][ix + 1] + (1.0 - U) * T1
                    * WITH->thetaz1[iz + 1][ix] + U * T1
                    * WITH->thetaz1[iz + 1][ix + 1];
        }

        if (traceID) {
            printf("X=% f interpolation : U= % lf T =% lf\n",
                    is_double<T>::cst(X), is_double<T>::cst(U),
                    is_double<T>::cst(T1));
            printf("THX = % lf 11= % lf 12= %lf 21 = %lf 22 =%lf \n",
                    is_double<T>::cst(THX), WITH->thetax1[iz][ix],
                    WITH->thetax1[iz][ix + 1], WITH->thetax1[iz + 1][ix],
                    WITH->thetax1[iz + 1][ix + 1]);
            printf("Z=% f interpolation : U= % lf T =% lf\n",
                    is_double<T>::cst(Z), is_double<T>::cst(U),
                    is_double<T>::cst(T1));
            printf("THZ = % lf 11= % lf 12= %lf 21 = %lf 22 =%lf \n",
                    is_double<T>::cst(THZ), WITH->thetaz1[iz][ix],
                    WITH->thetaz1[iz][ix + 1], WITH->thetaz1[iz + 1][ix],
                    WITH->thetaz1[iz + 1][ix + 1]);
        }

        TX = THX;
        TZ = THZ;
    }

    if (order == 2) {
        nx = WITH->nx2;
        nz = WITH->nz2;
        xstep = WITH->tabx2[1] - WITH->tabx2[0]; /* increasing values */
        zstep = WITH->tabz2[0] - WITH->tabz2[1]; /* decreasing values */

        if (traceID)
            printf("LinearInterpolation2: xstep = % f zstep = % f\n", xstep,
                    zstep);

        /* test whether X and Z within the transverse map area */
        if (X < WITH->tabx2[0] || X > WITH->tabx2[nx - 1]) {
            printf("LinearInterpolation2: X out of borders \n");
            printf("X = % lf but tabx[0] = % lf and tabx[nx-1] = % lf\n",
                    is_double<T>::cst(X), WITH->tabx2[0], WITH->tabx2[nx - 1]);
            out = true;
            return;
        }

        if (Z > WITH->tabz2[0] || Z < WITH->tabz2[nz - 1]) {
            printf("LinearInterpolation2: Z out of borders \n");
            printf("Z = % lf but tabz[0] = % lf and tabz[nz-1] = % lf\n",
                    is_double<T>::cst(Z), WITH->tabz2[0], WITH->tabz2[nz - 1]);
            out = true;
            return;
        }
        /* looking for the index for X */
        i = 0;
        while (X >= WITH->tabx2[i] && i <= nx - 1) {
            i++;
            if (traceID)
                printf("%2d % lf % lf % lf \n", i, is_double<T>::cst(X),
                        WITH->tabx2[i], WITH->tabx2[i + 1]);
        }
        ix = i - 1;

        /* looking for the index for Z */
        i = 0;
        while (Z <= WITH->tabz2[i] && i <= nz - 1) {
            i++;
            if (traceID)
                printf("%2d % lf % lf % lf \n", i, is_double<T>::cst(Z),
                        WITH->tabz2[i], WITH->tabz2[i + 1]);
        }
        iz = i - 1;

        if (traceID)
            printf("LinearInterpolation2: Indices are ix=%d and iz=%d\n", ix,
                    iz);

        /** Bilinear Interpolation **/
        U = (X - WITH->tabx2[ix]) / xstep;
        T1 = -(Z - WITH->tabz2[iz]) / zstep;

        // second order kick map interpolation
        if (ix >= 0 && iz >= 0) {
            THX = (1.0 - U) * (1.0 - T1) * WITH->thetax2[iz][ix] + U * (1.0
                    - T1) * WITH->thetax2[iz][ix + 1] + (1.0 - U) * T1
                    * WITH->thetax2[iz + 1][ix] + U * T1
                    * WITH->thetax2[iz + 1][ix + 1];

            THZ = (1.0 - U) * (1.0 - T1) * WITH->thetaz2[iz][ix] + U * (1.0
                    - T1) * WITH->thetaz2[iz][ix + 1] + (1.0 - U) * T1
                    * WITH->thetaz2[iz + 1][ix] + U * T1
                    * WITH->thetaz2[iz + 1][ix + 1];
        }

        if (traceID) {
            printf("LSN X=% f interpolation : U= % lf T =% lf\n",
                    is_double<T>::cst(X), is_double<T>::cst(U),
                    is_double<T>::cst(T1));
            printf("THX = % lf 11= % lf 12= %lf 21 = %lf 22 =%lf \n",
                    is_double<T>::cst(THX), WITH->thetax2[iz][ix],
                    WITH->thetax2[iz][ix + 1], WITH->thetax2[iz + 1][ix],
                    WITH->thetax2[iz + 1][ix + 1]);
            printf("Z=% f interpolation : U= % lf T =% lf\n",
                    is_double<T>::cst(Z), is_double<T>::cst(U),
                    is_double<T>::cst(T1));
            printf("THZ = % lf 11= % lf 12= %lf 21 = %lf 22 =%lf \n",
                    is_double<T>::cst(THZ), WITH->thetaz2[iz][ix],
                    WITH->thetaz2[iz][ix + 1], WITH->thetaz2[iz + 1][ix],
                    WITH->thetaz2[iz + 1][ix + 1]);
        }

        TX = THX;
        TZ = THZ;
    }
}

/****************************************************************************/
/* void SplineInterpolation2(double X, double Z, double &TX, double &TZ,
 CellType &Cell, bool &out, int order)
 
 Purpose:
 Computes thx and thz in X and Z values using a bilinear interpolation
 interpolation of the array thetax(x, z) and thetaz(x, z)
 
 Input:
 X, Z location of the interpolation
 Cell element containing ID device
 Order 1 or 2 for first or second order maps
 
 Output:
 TX, TZ thetax and thetaz interpolated at X and Z
 out true if interpolation out of table
 
 Return:
 none
 
 Global variables:
 none
 
 Specific functions:
 
 Comments:
 4 November 2010 - Add order and separate 1st and second order tables
 
 ****************************************************************************/
template<typename T>
void SplineInterpolation2(T &X, T &Z, T &thetax, T &thetaz, CellType &Cell,
        bool &out, int order) {
    int nx, nz;
    InsertionType *WITH;
    double *tabx; /* spacing in H-plane */
    double *tabz; /* spacing in V-plane */

    WITH = Cell.Elem.ID;
    if (order == 1) {
        nx = WITH->nx1;
        nz = WITH->nz1;
        tabx = WITH->tabx1;
        tabz = WITH->tabz1;
    } else {
        nx = WITH->nx2;
        nz = WITH->nz2;
        tabx = WITH->tabx2;
        tabz = WITH->tabz2;
    }

    /* test whether X and Z within the transverse map area */
    if (X < tabx[0] || X > tabx[nx - 1] || Z > tabz[0] || Z < tabz[nz - 1]) {
        printf(
                "SplineInterpolation2: out of borders in element s= %4.2f %*s\n",
                Cell.S, 5, Cell.Elem.PName);
        printf("X = % lf but tabx[0] = % lf and tabx[nx-1] = % lf\n",
                is_double<T>::cst(X), tabx[0], tabx[nx - 1]);
        printf("Z = % lf but tabz[0] = % lf and tabz[nz-1] = % lf\n",
                is_double<T>::cst(Z), tabz[0], tabz[nz - 1]);
        out = true;
        return;
    }

    out = false;
    if (order == 1) {
        // H-plane
        splin2(WITH->TabzOrd1 - 1, WITH->TabxOrd1 - 1, WITH->tx1, WITH->f2x1, nz, nx,
                Z, X, thetax);
        /*    if (fabs(temp) > ZERO_RADIA)
         *thetax = (double) temp;
         else
         *thetax = 0.0;*/
        // V-plane
        splin2(WITH->TabzOrd1 - 1, WITH->TabxOrd1 - 1, WITH->tz1, WITH->f2z1, nz, nx,
                Z, X, thetaz);
        /*    if (fabs(temp) > ZERO_RADIA)
         *thetaz = (double) temp;
         else
         *thetaz = 0.0;*/
    }

    if (order == 2) {
        // H-plane
        splin2(WITH->TabzOrd2 - 1, WITH->TabxOrd2 - 1, WITH->tx2, WITH->f2x2, nz, nx,
                Z, X, thetax);
        /*    if (fabs(temp) > ZERO_RADIA)
         *thetax = (double) temp;
         else
         *thetax = 0.0;*/
        // V-plane
        splin2(WITH->TabzOrd2 - 1, WITH->TabxOrd2 - 1, WITH->tz2, WITH->f2z2, nz, nx,
                Z, X, thetaz);
        /*    if (fabs(temp) > ZERO_RADIA)
         *thetaz = (double) temp;
         else
         *thetaz = 0.0;*/
    }
}

void Matrices4Spline(InsertionType *WITH, int Order) {
    int kx, kz;

    if (Order == 1) {
        for (kx = 0; kx < WITH->nx1; kx++) {
            WITH->TabxOrd1[kx] = (float) WITH->tabx1[kx];
        }

        /* reordering: it has to be in increasing order */
        for (kz = 0; kz < WITH->nz1; kz++) {
            WITH->TabzOrd1[kz] = (float) WITH->tabz1[WITH->nz1 - kz - 1];
        }

        for (kx = 0; kx < WITH->nx1; kx++) {
            for (kz = 0; kz < WITH-> nz1; kz++) {
                WITH->tx1[kz + 1][kx + 1] = (float) (WITH->thetax1[WITH->nz1
                        - kz - 1][kx]);
                WITH->tz1[kz + 1][kx + 1] = (float) (WITH->thetaz1[WITH->nz1
                        - kz - 1][kx]);
            }
        }
        // computes second derivative matrices
        splie2(WITH->TabzOrd1 - 1, WITH->TabxOrd1 - 1, WITH->tx1, WITH->nz1,
                WITH->nx1, WITH->f2x1);
        splie2(WITH->TabzOrd1 - 1, WITH->TabxOrd1 - 1, WITH->tz1, WITH->nz1,
                WITH->nx1, WITH->f2z1);
    }

    if (Order == 2) {
        for (kx = 0; kx < WITH->nx2; kx++) {
            WITH->TabxOrd2[kx] = (float) WITH->tabx2[kx];
        }

        /* reordering: it has to be in increasing order */
        for (kz = 0; kz < WITH->nz2; kz++) {
            WITH->TabzOrd2[kz] = (float) WITH->tabz2[WITH->nz2 - kz - 1];
        }

        for (kx = 0; kx < WITH->nx2; kx++) {
            for (kz = 0; kz < WITH-> nz2; kz++) {
                WITH->tx2[kz + 1][kx + 1] = (float) (WITH->thetax2[WITH->nz2
                        - kz - 1][kx]);
                WITH->tz2[kz + 1][kx + 1] = (float) (WITH->thetaz2[WITH->nz2
                        - kz - 1][kx]);
            }
        }
        // computes second derivative matrices
        splie2(WITH->TabzOrd2 - 1, WITH->TabxOrd2 - 1, WITH->tx2, WITH->nz2,
                WITH->nx2, WITH->f2x2);
        splie2(WITH->TabzOrd2 - 1, WITH->TabxOrd2 - 1, WITH->tz2, WITH->nz2,
                WITH->nx2, WITH->f2z2);
    }

}
