/* Tracy-2

   J. Bengtsson, CBP, LBL      1990 - 1994   Pascal version
                 SLS, PSI      1995 - 1997
   M. Boege      SLS, PSI      1998          C translation
   L. Nadolski   SOLEIL        2002          Link to NAFF, Radia field maps
   J. Bengtsson  NSLS-II, BNL  2004 -        


   To generate a lattice flat file.

   Type codes:

     marker     -1
     drift	 0
     multipole   1
     cavity      2
     thin kick   3
     wiggler     4

   Integration methods:

     linear, matrix style (obsolete)              0
     2nd order symplectic integrator (obsolete)   2
     4th order symplectic integrator              4

   Format:

     name, family no, kid no, element no
     type code, integration method, no of integration steps
     apertures: xmin, xmax, ymin, ymax

   The following lines follows depending on element type.

     type

     drift:	 L

     multipole:  hor., ver. displ., roll angle (design), roll angle (error)
                 L, 1/rho, entrance angle, exit angle
		 no of nonzero multipole coeff., n design
		 n, b , a
		     n   n
		     .
		     .
		     .

     wiggler:    L [m], lambda [m]
                 no of harmonics
                 harm no, kxV [1/m], BoBrhoV [1/m], kxH, BoBrhoH, phi
                    ...

     cavity:	 cavity voltage/beam energy [eV], omega/c, beam energy [eV]

     thin kick:	 hor., ver. displacement, roll angle (total)
		 no of nonzero multipole coeff.
		 n, b , a
		     n   n
		     .
		     .
		     .

     kick_map:   scale order <file name>

*/


#include "tracy_lib.h"


#define snamelen   10

// numerical type codes
#define marker_   -1
#define drift_     0
#define mpole_     1
#define cavity_    2
#define thinkick_  3
#define wiggler_   4
#define insertion_ 6
#define FieldMap_  7


ifstream  inf;


void get_kind(const int kind, elemtype &Elem)
{

  switch (kind) {
  case marker_:
    Elem.Pkind = PartsKind(marker);
    break;
  case drift_:
    Elem.Pkind = PartsKind(drift);
    Drift_Alloc(&Elem);
    break;
  case mpole_:
    Elem.Pkind = PartsKind(Mpole);
    Mpole_Alloc(&Elem);
    Elem.M->Pthick = pthicktype(thick);
    break;
  case cavity_:
    Elem.Pkind = PartsKind(Cavity);
    Cav_Alloc(&Elem);
    break;
  case thinkick_:
    Elem.Pkind = PartsKind(Mpole);
    Mpole_Alloc(&Elem);
    Elem.M->Pthick = pthicktype(thin);
    break;
  case wiggler_:
    Elem.Pkind = PartsKind(Wigl);
    Wiggler_Alloc(&Elem);
    break;
  case insertion_:
    Elem.Pkind = PartsKind(Insertion);
    Insertion_Alloc(&Elem);
    break;
  default:
    cout << "get_kind: unknown type " << kind << " " << Elem.PName << endl;
    exit_(1);
    break;
  }
}


void rdmfile(const char *mfile_dat)
 {
    char line[max_str], file_name[max_str];
    int j, nmpole, kind, method, n;
    long int i;
    //double dTerror;

    bool prt = false;

    cout << endl;
    cout << "reading machine file: " << mfile_dat << endl;

    file_rd(inf, mfile_dat);

    while (inf.getline(line, max_str) != NULL) {
        if (prt)
            printf("%s\n", line);
        sscanf(line, "%*s %*d %*d %ld", &i);

        Cell[i].dS[X_] = 0.0;
        Cell[i].dS[Y_] = 0.0;
        Cell[i].dT[X_] = 1.0;
        Cell[i].dT[Y_] = 0.0;

        sscanf(line, "%s %ld %ld", Cell[i].Elem.PName, &Cell[i].Fnum,
                &Cell[i].Knum);

        if (Cell[i].Knum == 1) {
            strcpy(ElemFam[Cell[i].Fnum - 1].ElemF.PName, Cell[i].Elem.PName);
            globval.Elem_nFam = max(Cell[i].Fnum, globval.Elem_nFam);
        }

        if (i > 0) {
            ElemFam[Cell[i].Fnum - 1].KidList[Cell[i].Knum - 1] = i;
            ElemFam[Cell[i].Fnum - 1].nKid = max(Cell[i].Knum,
                    ElemFam[Cell[i].Fnum - 1].nKid);
        }

        inf.getline(line, max_str);
        if (prt)
            printf("%s\n", line);
        sscanf(line, "%d %d %d", &kind, &method, &n);
        get_kind(kind, Cell[i].Elem);
        if (i > 0)
            ElemFam[Cell[i].Fnum - 1].ElemF.Pkind = Cell[i].Elem.Pkind;

        inf.getline(line, max_str);
        if (prt)
            printf("%s\n", line);
        sscanf(line, "%lf %lf %lf %lf", &Cell[i].maxampl[X_][0],
                &Cell[i].maxampl[X_][1], &Cell[i].maxampl[Y_][0],
                &Cell[i].maxampl[Y_][1]);

        Cell[i].Elem.PL = 0.0;

        switch (Cell[i].Elem.Pkind) {
        case undef:
            cout << "rdmfile: unknown type " << i << endl;
            exit_(1);
            break;
        case marker:
            break;
        case drift:
            inf.getline(line, max_str);
            if (prt)
                printf("%s\n", line);
            sscanf(line, "%lf", &Cell[i].Elem.PL);
            break;
        case Cavity:
            inf.getline(line, max_str);
            if (prt)
                printf("%s\n", line);
            sscanf(line, "%lf %lf %d %lf", &Cell[i].Elem.C->Pvolt,
                    &Cell[i].Elem.C->Pfreq, &Cell[i].Elem.C->Ph,
                    &globval.Energy);
            globval.Energy *= 1e-9;
            Cell[i].Elem.C->Pvolt *= globval.Energy * 1e9;
            Cell[i].Elem.C->Pfreq *= c0 / (2.0 * M_PI);
            break;
        case Mpole:
            Cell[i].Elem.M->Pmethod = method;
            Cell[i].Elem.M->PN = n;

            if (Cell[i].Elem.M->Pthick == thick) {
                inf.getline(line, max_str);
                if (prt)
                    printf("%s\n", line);
                sscanf(line, "%lf %lf %lf %lf", &Cell[i].dS[X_],
                        &Cell[i].dS[Y_], &Cell[i].Elem.M->PdTpar, &Cell[i].Elem.M->PdTsys); //troquei o dterror por sys para gerar o erro ao escrever o flat_file também.
                Cell[i].dT[X_] = cos(dtor(Cell[i].Elem.M->PdTsys + Cell[i].Elem.M->PdTpar));
                Cell[i].dT[Y_] = sin(dtor(Cell[i].Elem.M->PdTsys + Cell[i].Elem.M->PdTpar));

                inf.getline(line, max_str);
                if (prt)
                    printf("%s\n", line);
                sscanf(line, "%lf %lf %lf %lf %lf", &Cell[i].Elem.PL,
                        &Cell[i].Elem.M->Pirho, &Cell[i].Elem.M->PTx1,
                        &Cell[i].Elem.M->PTx2, &Cell[i].Elem.M->Pgap);
                if (Cell[i].Elem.M->Pirho != 0.0)
                    Cell[i].Elem.M->Porder = 1;
            } else {
                inf.getline(line, max_str);
                if (prt)
                    printf("%s\n", line);
                sscanf(line, "%lf %lf %lf", &Cell[i].dS[X_], &Cell[i].dS[Y_],
                        &Cell[i].Elem.M->PdTsys);
                Cell[i].dT[X_] = cos(dtor(Cell[i].Elem.M->PdTsys));
                Cell[i].dT[Y_] = sin(dtor(Cell[i].Elem.M->PdTsys));
            }

            Cell[i].Elem.M->Pc0 = sin(Cell[i].Elem.PL * Cell[i].Elem.M->Pirho
                    / 2.0);
            Cell[i].Elem.M->Pc1 = cos(dtor(Cell[i].Elem.M->PdTpar))
                    * Cell[i].Elem.M->Pc0;
            Cell[i].Elem.M->Ps1 = sin(dtor(Cell[i].Elem.M->PdTpar))
                    * Cell[i].Elem.M->Pc0;

            inf.getline(line, max_str);
            if (prt)
                printf("%s\n", line);
            sscanf(line, "%d %d", &nmpole, &Cell[i].Elem.M->n_design);
            for (j = 1; j <= nmpole; j++) {
                inf.getline(line, max_str);
                if (prt)
                    printf("%s\n", line);
                sscanf(line, "%d", &n);
                sscanf(line, "%*d %lf %lf", &Cell[i].Elem.M->PB[HOMmax + n],
                        &Cell[i].Elem.M->PB[HOMmax - n]);
                Cell[i].Elem.M->PBpar[HOMmax + n] = Cell[i].Elem.M->PB[HOMmax
                        + n];
                Cell[i].Elem.M->PBpar[HOMmax - n] = Cell[i].Elem.M->PB[HOMmax
                        - n];
                Cell[i].Elem.M->Porder = max(n, Cell[i].Elem.M->Porder);
            }
            break;
        case Wigl:
            Cell[i].Elem.W->Pmethod = method;
            Cell[i].Elem.W->PN = n;

            inf.getline(line, max_str);
            if (prt)
                printf("%s\n", line);
            sscanf(line, "%lf %lf", &Cell[i].Elem.PL, &Cell[i].Elem.W->lambda);

            inf.getline(line, max_str);
            if (prt)
                printf("%s\n", line);
            sscanf(line, "%d", &Cell[i].Elem.W->n_harm);

            if (Cell[i].Knum == 1)
                Wiggler_Alloc(&ElemFam[Cell[i].Fnum - 1].ElemF);
            for (j = 0; j < Cell[i].Elem.W->n_harm; j++) {
                inf.getline(line, max_str);
                if (prt)
                    printf("%s\n", line);
                sscanf(line, "%d %lf %lf %lf %lf %lf",
                        &Cell[i].Elem.W->harm[j], &Cell[i].Elem.W->kxV[j],
                        &Cell[i].Elem.W->BoBrhoV[j], &Cell[i].Elem.W->kxH[j],
                        &Cell[i].Elem.W->BoBrhoH[j], &Cell[i].Elem.W->phi[j]);
                ElemFam[Cell[i].Fnum - 1].ElemF.W->BoBrhoV[j]
                        = Cell[i].Elem.W->BoBrhoV[j];
                ElemFam[Cell[i].Fnum - 1].ElemF.W->BoBrhoH[j]
                        = Cell[i].Elem.W->BoBrhoH[j];
            }
            break;
        case Insertion:
            Cell[i].Elem.ID->Pmethod = method;
            Cell[i].Elem.ID->PN = n;

            inf.getline(line, max_str);
            if (prt)
                printf("%s\n", line);
            sscanf(line, "%lf %d %s", &Cell[i].Elem.ID->scaling1, &n, file_name);

            if (n == 1) {
                Cell[i].Elem.ID->firstorder = true;
                Cell[i].Elem.ID->secondorder = false;

                strcpy(Cell[i].Elem.ID->fname1, file_name);
                Read_IDfile(Cell[i].Elem.ID->fname1, &Cell[i].Elem.PL,
                        &Cell[i].Elem.ID->nx1, &Cell[i].Elem.ID->nz1,
                        Cell[i].Elem.ID->tabx1, Cell[i].Elem.ID->tabz1,
                        Cell[i].Elem.ID->thetax1, Cell[i].Elem.ID->thetaz1);
            } else if (n == 2) {
                Cell[i].Elem.ID->firstorder = false;
                Cell[i].Elem.ID->secondorder = true;

                // Ximenes 2013-01-10
                Cell[i].Elem.ID->scaling2 = Cell[i].Elem.ID->scaling1;
                Cell[i].Elem.ID->scaling1 = 0;
                // Ximenes 2013-01-10
                
                strcpy(Cell[i].Elem.ID->fname2, file_name);
                Read_IDfile(Cell[i].Elem.ID->fname2, &Cell[i].Elem.PL,
                        &Cell[i].Elem.ID->nx2, &Cell[i].Elem.ID->nz2,
                        Cell[i].Elem.ID->tabx2, Cell[i].Elem.ID->tabz2,
                        Cell[i].Elem.ID->thetax2, Cell[i].Elem.ID->thetaz2);
            } else {
                cout << "rdmfile: undef order " << n << endl;
                exit_(1);
            }

            if (Cell[i].Elem.ID->Pmethod == 1)
                Cell[i].Elem.ID->linear = true;
            else
                Cell[i].Elem.ID->linear = false;

            if (!Cell[i].Elem.ID->linear) {
                Cell[i].Elem.ID->tx1 = dmatrix(1, Cell[i].Elem.ID->nz1, 1,
                        Cell[i].Elem.ID->nx1);
                Cell[i].Elem.ID->tz1 = dmatrix(1, Cell[i].Elem.ID->nz1, 1,
                        Cell[i].Elem.ID->nx1);
                Cell[i].Elem.ID->tx2 = dmatrix(1, Cell[i].Elem.ID->nz2, 1,
                        Cell[i].Elem.ID->nx2);
                Cell[i].Elem.ID->tz2 = dmatrix(1, Cell[i].Elem.ID->nz2, 1,
                        Cell[i].Elem.ID->nx2);
                Cell[i].Elem.ID->TabxOrd1 = (double *) malloc(
                        (Cell[i].Elem.ID->nx1) * sizeof(double));
                Cell[i].Elem.ID->TabzOrd1 = (double *) malloc(
                        (Cell[i].Elem.ID->nz1) * sizeof(double));
                Cell[i].Elem.ID->TabxOrd2 = (double *) malloc(
                        (Cell[i].Elem.ID->nx2) * sizeof(double));
                Cell[i].Elem.ID->TabzOrd2 = (double *) malloc(
                        (Cell[i].Elem.ID->nz2) * sizeof(double));
                Cell[i].Elem.ID->f2x1 = dmatrix(1, Cell[i].Elem.ID->nz1, 1,
                        Cell[i].Elem.ID->nx1);
                Cell[i].Elem.ID->f2z1 = dmatrix(1, Cell[i].Elem.ID->nz1, 1,
                        Cell[i].Elem.ID->nx1);
                Cell[i].Elem.ID->f2x2 = dmatrix(1, Cell[i].Elem.ID->nz2, 1,
                        Cell[i].Elem.ID->nx2);
                Cell[i].Elem.ID->f2z2 = dmatrix(1, Cell[i].Elem.ID->nz2, 1,
                        Cell[i].Elem.ID->nx2);
                Matrices4Spline(Cell[i].Elem.ID, 1);
                Matrices4Spline(Cell[i].Elem.ID, 2);
            }

            break;
        case FieldMap:
            break;
        default:
            cout << "rdmfile: unknown type" << endl;
            exit_(1);
            break;
        }

        if (i == 0)
            Cell[i].S = 0.0;
        else
            Cell[i].S = Cell[i - 1].S + Cell[i].Elem.PL;
    }

    globval.Cell_nLoc = i;

    globval.dPcommon = 1e-8;
    globval.CODeps = 1e-14;
    globval.CODimax = 40;

    SI_init();

    cout << endl;
    cout << "rdmfile: read " << globval.Cell_nLoc << " elements" << endl;

    inf.close();
}
