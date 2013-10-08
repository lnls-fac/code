/* Tracy-2

 J. Bengtsson, CBP, LBL      1990 - 1994   Pascal version
 SLS, PSI      1995 - 1997
 M. Boege      SLS, PSI      1998          C translation
 L. Nadolski   SOLEIL        2002          Link to NAFF, Radia field maps
 J. Bengtsson  NSLS-II, BNL  2004 -

 Element propagators.                                                      */

//#include "tracy_lib.h"

double c_1, d_1, c_2, d_2, cl_rad, q_fluct;
double I2, I4, I5, dcurly_H, dI4;
ElemFamType ElemFam[Elem_nFamMax];
CellType Cell[Cell_nLocMax + 1];

// for IBS
int i_, j_;
double **C_;

// Dynamic model

/****************************************************************************/
/* void GtoL(ss_vect<T> &X, Vector2 &S, Vector2 &R,
 const double c0, const double c1, const double s1)

 Purpose:
 Global to local coordinates

 ****************************************************************************/
template<typename T>
void GtoL(ss_vect<T> &X, Vector2 &S, Vector2 &R, const double c0,
        const double c1, const double s1) {
    ss_vect<T> x1;

    /* Simplified rotated p_rot */
    X[px_] += c1;
    X[3] += s1;
    /* Translate */
    X[x_] -= S[X_];
    X[y_] -= S[Y_];
    /* Rotate */
    x1 = X;
    X[x_] = R[X_] * x1[x_] + R[Y_] * x1[y_];
    X[px_] = R[X_] * x1[px_] + R[Y_] * x1[py_];
    X[y_] = -R[Y_] * x1[x_] + R[X_] * x1[y_];
    X[py_] = -R[Y_] * x1[px_] + R[X_] * x1[py_];
    /* Simplified p_rot */
    X[px_] -= c0;
}

/****************************************************************************/
/* void LtoG(ss_vect<T> &X, Vector2 &S, Vector2 &R,
 double c0, double c1, double s1)

 Purpose:
 Local to global coordinates

 ****************************************************************************/
template<typename T>
void LtoG(ss_vect<T> &X, Vector2 &S, Vector2 &R, double c0, double c1,
        double s1) {
    ss_vect<T> x1;

    /* Simplified p_rot */
    X[px_] -= c0;
    /* Rotate */
    x1 = X;
    X[x_] = R[X_] * x1[x_] - R[Y_] * x1[y_];
    X[px_] = R[X_] * x1[px_] - R[Y_] * x1[py_];
    X[y_] = R[Y_] * x1[x_] + R[X_] * x1[y_];
    X[py_] = R[Y_] * x1[px_] + R[X_] * x1[py_];
    /* Translate */
    X[x_] += S[X_];
    X[y_] += S[Y_];
    /* p_rot rotated */
    X[px_] += c1;
    X[py_] += s1;
}
/**********************************************************/
/*

 Purpose:
 Get the longitudinal momentum ps
 **********************************************************/

template<typename T>
inline T get_p_s(ss_vect<T> &x) {
    T p_s, p_s2;

    if (!globval.H_exact)
        p_s = 1.0 + x[delta_];
    else {
        p_s2 = sqr(1.0 + x[delta_]) - sqr(x[px_]) - sqr(x[py_]);
        if (p_s2 >= 0.0)
            p_s = sqrt(p_s2);
        else {
            // avoid compile warning
            p_s = 0.0;
            printf("get_p_s: *** Speed of light exceeded!\n");
            exit_(1);
        }
    }
    return (p_s);
}

/****************************************************************************/
/* Drift(double L, ss_vect<T> &x)

 Purpose:
 Drift pass

 If H_exact = false, using approximation Hamiltonian:

 px^2+py^2
 H(x,y,l,px,py,delta) = -------------
 2(1+delta)

 Otherwise, using exact Hamiltonian


 Input:
 L:  drift length
 &x:  pointer to initial vector: x

 Output:
 none

 Return:
 none

 Global variables:


 Specific functions:

 ****************************************************************************/

template<typename T>
void Drift(double L, ss_vect<T> &x) {
    T u;

    if (!globval.H_exact) {
        u = L / (1.0 + x[delta_]);
        x[ct_] += u * (sqr(x[px_]) + sqr(x[py_])) / (2.0 * (1.0 + x[delta_]));
    } else {
        u = L / get_p_s(x);
        x[ct_] += u * (1.0 + x[delta_]) - L;
    }
    x[x_] += x[px_] * u;
    x[y_] += x[py_] * u;
    if (globval.pathlength)
        x[ct_] += L;
}

template<typename T>
void Drift_Pass(CellType &Cell, ss_vect<T> &x) {
    Drift(Cell.Elem.PL, x);
}

/****************************************************************************/
/* zero_mat(const int n, double** A)

 Purpose:
 Initionize  n x n  matrix A with 0


 ****************************************************************************/
void zero_mat(const int n, double** A) {
    int i, j;

    for (i = 1; i <= n; i++)
        for (j = 1; j <= n; j++)
            A[i][j] = 0.0;
}

/****************************************************************************/
/* void identity_mat(const int n, double** A)

 Purpose:
 generate  n x n  identity matrix A


 ****************************************************************************/
void identity_mat(const int n, double** A) {
    int i, j;

    for (i = 1; i <= n; i++)
        for (j = 1; j <= n; j++)
            A[i][j] = (i == j) ? 1.0 : 0.0;
}

/****************************************************************************/
/* void det_mat(const int n, double **A)

 Purpose:
 get the determinant of  n x n matrix A


 ****************************************************************************/
double det_mat(const int n, double **A) {
    int i, *indx;
    double **U, d;

    indx = ivector(1, n);
    U = dmatrix(1, n, 1, n);

    dmcopy(A, n, n, U);
    dludcmp(U, n, indx, &d);

    for (i = 1; i <= n; i++)
        d *= U[i][i];

    free_dmatrix(U, 1, n, 1, n);
    free_ivector(indx, 1, n);

    return d;
}

/****************************************************************************/
/* void trace_mat(const int n, double **A)

 Purpose:
 get the trace of  n x n matrix A


 ****************************************************************************/
double trace_mat(const int n, double **A) {
    int i;
    double d;

    d = 0.0;
    for (i = 1; i <= n; i++)
        d += A[i][i];

    return d;
}

float K_fun(float lambda) {
    double **Id, **Lambda, **Lambda_inv, **U, **V, **K_int;

    Id = dmatrix(1, DOF, 1, DOF);
    Lambda = dmatrix(1, DOF, 1, DOF);
    Lambda_inv = dmatrix(1, DOF, 1, DOF);
    U = dmatrix(1, DOF, 1, DOF);
    V = dmatrix(1, DOF, 1, DOF);
    K_int = dmatrix(1, DOF, 1, DOF);

    identity_mat(DOF, Id);

    dmsmy(Id, DOF, DOF, lambda, U);
    //  dmsub(C_, DOF, DOF, U, Lambda);
    dmadd(C_, DOF, DOF, U, Lambda);
    dinverse(Lambda, DOF, Lambda_inv);

    dmsmy(Id, DOF, DOF, trace_mat(DOF, Lambda_inv), U);
    dmsmy(Lambda_inv, DOF, DOF, 3.0, V);
    dmsub(U, DOF, DOF, V, K_int);
    dmsmy(K_int, DOF, DOF, 2.0 * sqr(M_PI)
            * sqrt(lambda / det_mat(DOF, Lambda)), K_int);

    free_dmatrix(Id, 1, DOF, 1, DOF);
    free_dmatrix(Lambda, 1, DOF, 1, DOF);
    free_dmatrix(Lambda_inv, 1, DOF, 1, DOF);
    free_dmatrix(U, 1, DOF, 1, DOF);
    free_dmatrix(V, 1, DOF, 1, DOF);
    free_dmatrix(K_int, 1, DOF, 1, DOF);

    return K_int[i_][j_];
}

// partial template-class specialization
// primary version
template<typename T>
class is_tps {
};

// partial specialization
template<>
class is_tps<double> {
public:
    static inline void get_ps(const ss_vect<double> &x, CellType &Cell) {
        Cell.BeamPos = x;
    }

    static inline double set_prm(const int k) {
        return 1.0;
    }

    static inline double get_curly_H(const ss_vect<tps> &x) {
        cout << "get_curly_H: operation not defined for double" << endl;
        exit_(1);
        return 0.0;
    }

    static inline double get_dI4(const double h, const double b2,
            const double L, const ss_vect<tps> &x) {
        cout << "get_dI4: operation not defined for double" << endl;
        exit_(1);
        return 0.0;
    }

    static inline void emittance(const double B2, const double u,
            const double ps0, const ss_vect<double> &xp) {
    }

    static inline void do_IBS(const double L, const ss_vect<double> &A_tps) {
    }

    static inline void diff_mat(const double B2, const double u,
            const double ps0, const ss_vect<double> &xp) {
    }

};

// partial specialization
template<>
class is_tps<tps> {
public:
    static inline void get_ps(const ss_vect<tps> &x, CellType &Cell) {
        getlinmat(6, x, Cell.A);
    }

    static inline tps set_prm(const int k) {
        return tps(0.0, k);
    }

    static inline double get_curly_H(const ss_vect<tps> &A) {
        int j;
        double curly_H[2];
        ss_vect<double> eta;

        eta.zero();
        for (j = 0; j < 4; j++)
            eta[j] = A[j][delta_];

        get_twoJ(2, eta, A, curly_H);

        return curly_H[X_];
    }

    static inline double get_dI4(const ss_vect<tps> &A) {
        return A[x_][delta_];
    }

    static inline void emittance(const tps &B2, const tps &ds, const tps &ps0,
            const ss_vect<tps> &A) {
        int j;
        double B_66;
        ss_vect<tps> A_inv;

        if (B2 > 0.0) {
            B_66 = (q_fluct * pow(B2.cst(), 1.5) * pow(ps0, 4) * ds).cst();
            A_inv = Inv(A);
            // D_11 = D_22 = curly_H_x,y * B_66 / 2,
            // curly_H_x,y = eta_Fl^2 + etap_Fl^2
            for (j = 0; j < 3; j++)
                globval.D_rad[j] += (sqr(A_inv[j * 2][delta_]) + sqr(A_inv[j
                        * 2 + 1][delta_])) * B_66 / 2.0;
        }
    }

    static void do_IBS(const double L, const ss_vect<tps> &A_tps) {
        /* A is passed, compute the invariants and emittances,
         The invariants for the uncoupled case are:

         [gamma alpha]
         Sigma     ^-1 = [           ]
         x,y,z      [alpha beta ]

         Note, ps = [x, y, ct, p_x, p_y, delta]                                */

        int i, j, k;
        double **A, **Ainv, **Ainv_tp, **Ainv_tp_Ainv, **Boost, **Boost_tp;
        double **G[DOF], **M_a, **U, **C_a[DOF], **K, dln_eps[DOF];
        double beta_x, beta_y, sigma_y, a_cst, two_Lc;

        const int n = 2 * DOF;
        const int indx[] = { 1, 4, 2, 5, 6, 3 };

        const double P0 = 1e9 * globval.Energy * q_e / c0;
        const double gamma = 1e9 * globval.Energy / m_e;
        const double beta = sqrt(1.0 - 1.0 / sqr(gamma));

        const double N_e = globval.Qb / q_e;

        A = dmatrix(1, n, 1, n);
        Ainv = dmatrix(1, n, 1, n);
        Ainv_tp = dmatrix(1, n, 1, n);
        Ainv_tp_Ainv = dmatrix(1, n, 1, n);
        Boost = dmatrix(1, n, 1, n);
        Boost_tp = dmatrix(1, n, 1, n);
        U = dmatrix(1, n, 1, n);
        M_a = dmatrix(1, n, 1, n);
        for (i = 0; i < DOF; i++)
            G[i] = dmatrix(1, n, 1, n);
        for (i = 0; i < DOF; i++)
            C_a[i] = dmatrix(1, DOF, 1, DOF);
        C_ = dmatrix(1, DOF, 1, DOF);
        K = dmatrix(1, DOF, 1, DOF);

        // Compute invariants (in Floquet space): Sigma^-1 = (A^-1)^tp * A^-1

        for (i = 1; i <= n; i++)
            for (j = 1; j <= n; j++)
                A[i][j] = A_tps[i - 1][j - 1];

        dmcopy(A, n, n, U);
        dinverse(U, n, Ainv);
        dmtranspose(Ainv, n, n, Ainv_tp);
        dmmult(Ainv_tp, n, n, Ainv, n, n, Ainv_tp_Ainv);

        for (i = 0; i < DOF; i++)
            for (j = 1; j <= n; j++)
                for (k = 1; k <= n; k++)
                    G[i][indx[j - 1]][indx[k - 1]] = Ainv[2 * i + 1][j]
                            * Ainv[2 * i + 1][k] + Ainv[2 * i + 2][j] * Ainv[2
                            * i + 2][k];

        dmadd(G[0], n, n, G[1], U);
        dmadd(U, n, n, G[2], U);

        if (trace) {
            printf("\n");
            dmdump(stdout, "G_1:", G[0], n, n, "%11.3e");
            dmdump(stdout, "G_2:", G[1], n, n, "%11.3e");
            dmdump(stdout, "G_3:", G[2], n, n, "%11.3e");
            dmdump(stdout, "Ainv_tp*Ainv:", Ainv_tp_Ainv, n, n, "%11.3e");
            dmdump(stdout, "Sum_a G_a", U, n, n, "%11.3e");
        }

        /* Transform from the co-moving to COM frame:

         [ 1 0    0     0    0      0     ]
         [ 0 1    0     0    0      0     ]
         [ 0 0 1/gamma  0    0      0     ]
         [ 0 0    0    1/P0  0      0     ]
         [ 0 0    0     0   1/P0    0     ]
         [ 0 0    0     0    0   gamma/P0 ]                                  */

        identity_mat(n, Boost);
        Boost[3][3] /= gamma;
        Boost[4][4] /= P0;
        Boost[5][5] /= P0;
        Boost[6][6] *= gamma / P0;

        dmtranspose(Boost, n, n, Boost_tp);

        zero_mat(DOF, C_);
        for (i = 0; i < DOF; i++) {
            dmmult(Boost_tp, n, n, G[i], n, n, U);
            dmmult(U, n, n, Boost, n, n, M_a);

            if (trace)
                dmdump(stdout, "M_a:", M_a, n, n, "%11.3e");

            // Extract the C_a matrices from the momentum components of M_a
            for (j = 1; j <= DOF; j++)
                for (k = 1; k <= DOF; k++)
                    C_a[i][j][k] = M_a[DOF + j][DOF + k];

            dmsmy(C_a[i], DOF, DOF, sqr(P0), C_a[i]);

            if (globval.eps[i] != 0.0)
                dmsmy(C_a[i], DOF, DOF, 1.0 / globval.eps[i], U);
            else {
                cout << "*** do_IBS: zero emittance for plane " << i + 1
                        << endl;
                exit(1);
            }

            dmadd(C_, DOF, DOF, U, C_);
        }

        if (trace) {
            dmdump(stdout, "C_1:", C_a[0], DOF, DOF, "%11.3e");
            dmdump(stdout, "C_2:", C_a[1], DOF, DOF, "%11.3e");
            dmdump(stdout, "C_3:", C_a[2], DOF, DOF, "%11.3e");
            dmdump(stdout, "C:", C_, DOF, DOF, "%11.3e");
        }

        for (i = 1; i <= DOF; i++)
            for (j = 1; j <= DOF; j++) {
                // upper bound is infinity
                i_ = i;
                j_ = j;
                K[i][j] = qromb(K_fun, 0.0, 1e8);
            }

        if (trace)
            dmdump(stdout, "K:", K, DOF, DOF, "%11.3e");

        // Compute the Coulomb logarithm
        beta_x = C_a[0][1][1];
        beta_y = C_a[1][2][2];
        sigma_y = sqrt(beta_y * globval.eps[Y_]);
        two_Lc = log(sqr(gamma * globval.eps[X_] * sigma_y / (r_e * beta_x)));

        if (trace)
            printf("2(log) = %11.3e\n", two_Lc);

        // include time dilatation and scaling of C matrix
        a_cst = L * two_Lc * N_e * sqr(r_e) * c0 / (64.0 * cube(M_PI * beta)
                * pow(gamma, 4) * globval.eps[X_] * globval.eps[Y_]
                * globval.eps[Z_]);

        // dSigma_ab/dt = a_cst * K_ab, e.g. d<delta^2>/dt = a_cst K_33.
        // deps is obtained from C.

        if (trace)
            printf("dln_eps:");
        for (i = 0; i < DOF; i++) {
            dmmult(C_a[i], DOF, DOF, K, DOF, DOF, U);
            // Dt = L/c0
            //      dln_eps[i] = a_cst/globval.eps[i]*trace_mat(DOF, U);
            globval.D_IBS[i] += a_cst * trace_mat(DOF, U);
            if (trace)
                printf("%11.3e", dln_eps[i]);
        }
        if (trace)
            printf("\n");

        free_dmatrix(A, 1, n, 1, n);
        free_dmatrix(Ainv, 1, n, 1, n);
        free_dmatrix(Ainv_tp, 1, n, 1, n);
        free_dmatrix(Ainv_tp_Ainv, 1, n, 1, n);
        free_dmatrix(Boost, 1, n, 1, n);
        free_dmatrix(Boost_tp, 1, n, 1, n);
        free_dmatrix(U, 1, n, 1, n);
        free_dmatrix(M_a, 1, n, 1, n);
        for (i = 0; i < DOF; i++)
            free_dmatrix(G[i], 1, n, 1, n);
        for (i = 0; i < DOF; i++)
            free_dmatrix(C_a[i], 1, DOF, 1, DOF);
        free_dmatrix(C_, 1, DOF, 1, DOF);
        free_dmatrix(K, 1, DOF, 1, DOF);
    }

    static inline void diff_mat(const tps &B2, const tps &ds, const tps &ps0,
            ss_vect<tps> &x) {
    }

};

template<typename T>
void get_B2(const double h_ref, const T B[], const ss_vect<T> &xp, T &B2_perp,
        T &B2_par) {
    // compute |B|^2_perpendicular and |B|^2_parallel
    T xn, e[3];

    xn = 1.0 / sqrt(sqr(1.0 + xp[x_] * h_ref) + sqr(xp[px_]) + sqr(xp[py_]));
    e[X_] = xp[px_] * xn;
    e[Y_] = xp[py_] * xn;
    e[Z_] = (1e0 + xp[x_] * h_ref) * xn;

    // left-handed coordinate system
    B2_perp = sqr(B[Y_] * e[Z_] - B[Z_] * e[Y_]) + sqr(B[X_] * e[Y_] - B[Y_]
            * e[X_]) + sqr(B[Z_] * e[X_] - B[X_] * e[Z_]);

    //  B2_par = sqr(B[X_]*e[X_]+B[Y_]*e[Y_]+B[Z_]*e[Z_]);
}

template<typename T>
void radiate(ss_vect<T> &x, const double L, const double h_ref, const T B[]) {
    T ps0, ps1, ds, B2_perp = 0.0, B2_par = 0.0;
    ss_vect<T> xp;

    // large ring: conservation of x' and y'
    xp = x;
    ps0 = get_p_s(x);
    xp[px_] /= ps0;
    xp[py_] /= ps0;

    // H = -p_s => ds = H*L
    ds = (1.0 + xp[x_] * h_ref + (sqr(xp[px_]) + sqr(xp[py_])) / 2.0) * L;
    get_B2(h_ref, B, xp, B2_perp, B2_par);

    if (globval.radiation) {
        x[delta_] -= cl_rad * sqr(ps0) * B2_perp * ds;
        ps1 = get_p_s(x);
        x[px_] = xp[px_] * ps1;
        x[py_] = xp[py_] * ps1;
    }

    if (globval.emittance)
        is_tps<T>::emittance(B2_perp, ds, ps0, xp);
}

static double get_psi(double irho, double phi, double gap) {
    /* Correction for magnet gap (longitudinal fringe field)

     irho h = 1/rho [1/m]
     phi  dipole edge angle
     gap  full gap between poles

     2
     K1*gap*h*(1 + sin phi)
     psi = ----------------------- * (1 - K2*g*gap*tan phi)
     cos phi

     K1 is usually 1/2
     K2 is zero here                                                  */

    double psi;

    const double k1 = 0.5, k2 = 0.0;

    if (phi == 0.0)
        psi = 0.0;
    else
        psi = k1 * gap * irho * (1.0 + sqr(sin(dtor(phi)))) / cos(dtor(phi))
                * (1.0 - k2 * gap * irho * tan(dtor(phi)));

    return psi;
}

/****************************************************************************/
/* template<typename T>
 void thin_kick(int Order, double MB[], double L, double h_bend, double h_ref,ss_vect<T> &x)

 Purpose:
 Calculate multipole kick. The Hamiltonian is

 H = A + B where A and B are the kick part defined by
 2    2
 px + py
 A(x,y,-l,px,py,dP) = ---------
 2(1+dP)
 2 2
 B(x,y,-l,px,py,dP) = -h*x*dP + 0.5 h x + int(Re(By+iBx)/Brho)

 so this is the appproximation for large ring
 the chromatic term is missing hx*A


 The kick is given by

 e L       L delta    L x              e L
 Dp_x = - --- B_y + ------- - ----- ,    Dp_y = --- B_x
 p_0         rho     rho^2             p_0

 where
 e      1
 --- = -----
 p_0   B rho
 ====
 \
 (B_y + iB_x) = B rho  >   (ia_n  + b_n ) (x + iy)^n-1
 /
 ====

 Input:
 Order  maximum non zero multipole component
 MB     array of an and bn, magnetic field components
 L      multipole length
 h_bend   1/rho in curvilinear coordinate,
 0    in cartisian cooridinate.
 h_ref   1/rho [m^-1]
 x      initial coordinates vector

 Output:
 x      final coordinates vector

 Return:
 none

 Global variables:
 none

 Specific functions:
 none

 Comments:
 none

 **************************************************************************/
template<typename T>
void thin_kick(int Order, double MB[], double L, double h_bend, double h_ref,
        ss_vect<T> &x) {
    int j;
    T BxoBrho, ByoBrho, ByoBrho1, B[3];
    ss_vect<T> x0, cod;

    if ((h_bend != 0.0) || ((1 <= Order) && (Order <= HOMmax))) {
        x0 = x;
        /* compute field with Horner's rule */
        ByoBrho = MB[HOMmax + Order]; // normalized By, By/(p0/e)
        BxoBrho = MB[HOMmax - Order]; // normalized Bx, Bx/(p0/e)

        for (j = Order - 1; j >= 1; j--) {
            ByoBrho1 = x0[x_] * ByoBrho - x0[y_] * BxoBrho + MB[j + HOMmax];
            BxoBrho = x0[y_] * ByoBrho + x0[x_] * BxoBrho + MB[HOMmax - j];
            ByoBrho = ByoBrho1;
        }

        if (globval.radiation || globval.emittance) {
            B[X_] = BxoBrho;
            B[Y_] = ByoBrho + h_bend;
            B[Z_] = 0.0;
            radiate(x, L, h_ref, B);
        }

        if (h_ref != 0.0) {
            x[px_] -= L * (ByoBrho + (h_bend - h_ref) / 2.0 + h_ref * h_bend
                    * x0[x_] - h_ref * x0[delta_]);
            x[ct_] += L * h_ref * x0[x_];
        } else
            x[px_] -= L * (ByoBrho + h_bend);

        x[py_] += L * BxoBrho;
    }
}

/****************************************************************************/
/* template<typename T>
 static void EdgeFocus(double irho, double phi, double gap, ss_vect<T> &x)

 Purpose:
 Compute edge focusing for a dipole
 There is no radiation coming from the edge
 The standard formula used is :
 irho
 px = px0 + ------ tan(phi) *x0
 1 + dP

 irho
 pz = pz0 - ------ tan(phi - psi) *z0
 1 + dP

 for psi definition  see its function

 Input:
 irho = inverse of curvature radius (rho = 5.36 m for SOLEIL)
 phi  = entrance/exit angle of the dipole edge,usually half the
 curvature angle of a dipole
 gap  = gap of the dipole for longitudinal fringing field (see psi)
 x    = input particle coordinates

 Output:
 x    output particle coordinates

 Return:
 none

 Global variables:
 none

 Specific functions:
 none

 Comments:
 05/07/10 Add energy dependence part irho replaced by irho/(1.0+x[delta_])
 now the chromaticity attribution of the dipole edge is used
 by a simple 1.0+x[delta_], but not a complicated Hamiltonian
 expansion.
 Now chromaticities in Tracy II and Tracy III are the same.
 Modification based on Tracy II soleil version.
 ****************************************************************************/
template<typename T>
static void EdgeFocus(double irho, double phi, double gap, ss_vect<T> &x) {
    if (true) {
        // warning: => diverging Taylor map (see SSC-141)
        x[px_] += irho * tan(dtor(phi)) * x[x_] / (1.0 + x[delta_]);
        x[py_] -= irho * tan(dtor(phi) - get_psi(irho, phi, gap)) * x[y_]
                / (1.0 + x[delta_]);
    } else {
        x[px_] += irho * tan(dtor(phi)) * x[x_];
        x[py_] -= irho * tan(dtor(phi) - get_psi(irho, phi, gap)) * x[y_];
    }
}

template<typename T>
void p_rot(double phi, ss_vect<T> &x) {
    T c, s, ps, p;
    ss_vect<T> x1;

    c = cos(dtor(phi));
    s = sin(dtor(phi));
    x1 = x;
    ps = get_p_s(x);
    p = c * ps - s * x1[px_];
    x[x_] = x1[x_] * ps / p;
    x[px_] = s * ps + c * x1[px_];
    x[y_] += x1[x_] * x1[py_] * s / p;
    x[ct_] += (1.0 + x1[delta_]) * x1[x_] * s / p;
}

template<typename T>
void bend_fringe(double hb, ss_vect<T> &x) {
    T coeff, u, ps, ps2, ps3;
    ss_vect<T> x1;

    coeff = -hb / 2.0;
    x1 = x;
    ps = get_p_s(x);
    ps2 = sqr(ps);
    ps3 = ps * ps2;
    u = 1.0 + 4.0 * coeff * x1[px_] * x1[y_] * x1[py_] / ps3;
    if (u >= 0.0) {
        x[y_] = 2.0 * x1[y_] / (1.0 + sqrt(u));
        x[x_] = x1[x_] - coeff * sqr(x[y_]) * (ps2 + sqr(x1[px_])) / ps3;
        x[py_] = x1[py_] + 2.0 * coeff * x1[px_] * x[y_] / ps;
        x[ct_] = x1[ct_] - coeff * x1[px_] * sqr(x[y_]) * (1.0 + x1[delta_])
                / ps3;
    } else {
        printf("bend_fringe: *** Speed of light exceeded!\n");
        exit_(1);
    }
}

/****************************************************************************
 * template<typename T>
 void quad_fringe(double b2, ss_vect<T> &x)

 Purpose:
 Compute edge focusing for a quadrupole
 There is no radiation coming from the edge

 The standard formula used is using more general form with exponential
 form. If keep up to the 4-th order nonlinear terms, the formula with goes to the
 following:
 (see E. Forest's book (Beam Dynamics: A New Attitude and Framework), p390):
 b2
 x = x0 +/- ---------- (x0^3 + 3*z0^2*x0)
 12(1 + dP)

 b2
 px = px0 +/-  ---------- (2*x0*y0*py0 - x0^2*px0 - y0^2*py0)
 4(1 + dP)

 b2
 y = y0 -/+ ---------- (y0^3 + 3*x0^2*y0)
 12(1 + dP)

 b2
 py = py0 -/+  ---------- (2*x0*y0*px0 - y0^2*py0 - x0^2*py0)
 4(1 + dP)

 dP = dP0;


 b2
 tau = tau0 -/+ ----------- (y0^3*px - x0^3*py + 3*x0^2*y*py - 3*y0^2*x0*px)
 12(1 + dP)^2

 Input:
 b2       = quadrupole strength
 x        = input particle coordinates

 Output:
 x    output particle coordinates

 Return:
 none

 Global variables:
 none

 Specific functions:
 none

 Comments:
 Now in Tracy III, no definition "entrance" and "exit", when called in Mpole_pass,
 first call with  M --> PB[quad+HOMmax], then
 call with -M --> PB[quad+HOMmax]

 ****************************************************************************/
template<typename T>
void quad_fringe(double b2, ss_vect<T> &x) {
    T u, ps;

    u = b2 / (12.0 * (1.0 + x[delta_]));
    ps = u / (1.0 + x[delta_]);

    x[py_] /= 1.0 - 3.0 * u * sqr(x[y_]);
    x[y_] -= u * cube(x[y_]);

    if (globval.Cavity_on)
        x[ct_] -= ps * cube(x[y_]) * x[py_]; //-y^3*py

    x[px_] /= 1.0 + 3.0 * u * sqr(x[x_]); //+x^2

    if (globval.Cavity_on)
        x[ct_] += ps * cube(x[x_]) * x[px_]; //+x^3*px

    x[x_] += u * cube(x[x_]); //+x^3
    u = u * 3.0;
    ps = ps * 3.0;
    x[y_] = exp(-u * sqr(x[x_])) * x[y_]; //+x^2*y
    x[py_] = exp(u * sqr(x[x_])) * x[py_]; //+x^2*py
    x[px_] += 2.0 * u * x[x_] * x[y_] * x[py_]; //+2*x*y*py

    if (globval.Cavity_on)
        x[ct_] -= ps * sqr(x[x_]) * x[y_] * x[py_]; // -3*x^2*y*py

    x[x_] = exp(u * sqr(x[y_])) * x[x_]; //+x*y^2
    x[px_] = exp(-u * sqr(x[y_])) * x[px_]; // -x^2*px-y^2*px
    x[py_] -= 2.0 * u * x[y_] * x[x_] * x[px_]; //-2*x*y*px

    if (globval.Cavity_on)
        x[ct_] += ps * sqr(x[y_]) * x[x_] * x[px_]; // +3*y^2*x*px
}

/****************************************************************************/
/* void Mpole_Pass(CellType &Cell, ss_vect<T> &x)

 Purpose:
 multipole pass,for dipole, quadrupole,sextupole,decupole,etc
 Using DA method.

 Input:

 Output:


 Return:
 none

 Global variables:
 none

 Specific functions:
 none

 Comments:
 none

 ****************************************************************************/

template<typename T>
void Mpole_Pass(CellType &Cell, ss_vect<T> &x) {
    int seg = 0;
    double k = 0.0, dL = 0.0, dL1 = 0.0, dL2 = 0.0;
    double dkL1 = 0.0, dkL2 = 0.0, h_ref = 0.0;
    elemtype *elemp;
    MpoleType *M;

    elemp = &Cell.Elem;
    M = elemp->M;

    /* Global -> Local */
    GtoL(x, Cell.dS, Cell.dT, M->Pc0, M->Pc1, M->Ps1);

    if ((M->Pmethod == Meth_Second) || (M->Pmethod == Meth_Fourth)) { /* fringe fields */

        if (globval.quad_fringe && (M->PB[Quad + HOMmax] != 0.0) && (M->quadFF1
                == 1)) {
            quad_fringe(M->quadFFscaling * M->PB[Quad + HOMmax], x);
        }

        if (!globval.H_exact) {
            if (M->Pirho != 0.0)
                EdgeFocus(M->Pirho, M->PTx1, M->Pgap, x);
        } else {
            p_rot(M->PTx1, x);
            bend_fringe(M->Pirho, x);
        }
    }

    if (M->Pthick == thick) {
        if (!globval.H_exact || ((M->PTx1 == 0.0) && (M->PTx2 == 0.0))) {// polar coordinates,curvilinear coordinates
            h_ref = M->Pirho;
            dL = elemp->PL / M->PN;
        } else {// Cartesian coordinates
            h_ref = 0.0;
            if (M->Pirho == 0.0)
                dL = elemp->PL / M->PN;
            else
                dL = 1.0 / M->Pirho * (sin(dtor(M->PTx1)) + sin(dtor(M->PTx2)))
                        / M->PN;
        }
    }

    switch (M->Pmethod) {

    case Meth_Linear:

    case Meth_First:
        if (M->Pthick == thick) {
            /* First Linear  */
            //      LinTrans(5L, M->AU55, x);
            k = M->PB[Quad + HOMmax];
            /* retrieve normal quad component already in AU55 */
            M->PB[Quad + HOMmax] = 0.0;
            /* Kick w/o quad component */
            thin_kick(M->Porder, M->PB, elemp->PL, 0.0, 0.0, x);
            /* restore quad component */
            M->PB[Quad + HOMmax] = k;
            /* Second Linear */
            //      LinTrans(5L, M->AD55, x);
        } else
            /* thin kick */
            thin_kick(M->Porder, M->PB, 1.0, 0.0, 0.0, x);
        break;

    case Meth_Second:
        cout << "Mpole_Pass: Meth_Second not supported" << endl;
        exit_(0);
        break;

    case Meth_Fourth:
        if (M->Pthick == thick) {
            dL1 = c_1 * dL;
            dL2 = c_2 * dL;
            dkL1 = d_1 * dL;
            dkL2 = d_2 * dL;

            dcurly_H = 0.0;
            dI4 = 0.0;
            for (seg = 1; seg <= M->PN; seg++) {
                if (globval.emittance && (!globval.Cavity_on) && (M->Pirho
                        != 0.0)) {
                    dcurly_H += is_tps<tps>::get_curly_H(x);
                    dI4 += is_tps<tps>::get_dI4(x);
                }

                Drift(dL1, x);
                thin_kick(M->Porder, M->PB, dkL1, M->Pirho, h_ref, x);
                Drift(dL2, x);
                thin_kick(M->Porder, M->PB, dkL2, M->Pirho, h_ref, x);

                if (globval.emittance && (!globval.Cavity_on) && (M->Pirho
                        != 0.0)) {
                    dcurly_H += 4.0 * is_tps<tps>::get_curly_H(x);
                    dI4 += 4.0 * is_tps<tps>::get_dI4(x);
                }

                Drift(dL2, x);
                thin_kick(M->Porder, M->PB, dkL1, M->Pirho, h_ref, x);
                Drift(dL1, x);

                if (globval.emittance && (!globval.Cavity_on) && (M->Pirho
                        != 0.0)) {
                    dcurly_H += is_tps<tps>::get_curly_H(x);
                    dI4 += is_tps<tps>::get_dI4(x);
                }
            }

            if (globval.emittance && (!globval.Cavity_on) && (M->Pirho != 0)) {
                dcurly_H /= 6.0 * M->PN;
                dI4 *= M->Pirho * (sqr(M->Pirho) + 2.0
                        * M->PBpar[Quad + HOMmax]) / (6.0 * M->PN);

                I2 += elemp->PL * sqr(M->Pirho);
                I4 += elemp->PL * dI4;
                I5 += elemp->PL * fabs(cube(M->Pirho)) * dcurly_H;
            }
        } else
            thin_kick(M->Porder, M->PB, 1.0, 0.0, 0.0, x);

        break;
    }

    if ((M->Pmethod == Meth_Second) || (M->Pmethod == Meth_Fourth)) {
        /* fringe fields */
        if (!globval.H_exact) {
            if (M->Pirho != 0.0)
                EdgeFocus(M->Pirho, M->PTx2, M->Pgap, x);
        } else {
            bend_fringe(-M->Pirho, x);
            p_rot(M->PTx2, x);
        }
        if (globval.quad_fringe && (M->PB[Quad + HOMmax] != 0.0) && (M->quadFF2
                == 1))
            quad_fringe(-M->quadFFscaling * M->PB[Quad + HOMmax], x);
    }

    /* Local -> Global */
    LtoG(x, Cell.dS, Cell.dT, M->Pc0, M->Pc1, M->Ps1);
}

template<typename T>
void Marker_Pass(CellType &Cell, ss_vect<T> &X) {
    elemtype *elemp;

    elemp = &Cell.Elem;
    /* Global -> Local */
    GtoL(X, Cell.dS, Cell.dT, 0.0, 0.0, 0.0);
    /* Local -> Global */
    LtoG(X, Cell.dS, Cell.dT, 0.0, 0.0, 0.0);
}

/****************************************************************************
 * void Cav_Pass(CellType *Cell, double *X)

 Purpose:
 Tracking through a cavity

 Input:
 Cell cavity element to track through
 X    input coordinates

 Output:
 X output coordinates

 Return:
 none

 Global variables:
 none

 Specific functions:
 none

 Comments:
 none

 ****************************************************************************/
template<typename T>
void Cav_Pass(CellType &Cell, ss_vect<T> &X) {
    elemtype *elemp;
    CavityType *C;
    T delta;

    elemp = &Cell.Elem;
    C = elemp->C;
    if (globval.Cavity_on && C->Pvolt != 0.0) {
        delta = -C->Pvolt / (globval.Energy * 1e9) * sin(2.0 * M_PI * C->Pfreq
                / c0 * X[ct_] + C->phi);
        X[delta_] += delta;

        if (globval.radiation)
            globval.dE -= is_double<T>::cst(delta);

        if (globval.pathlength)
            X[ct_] -= C->Ph / C->Pfreq * c0;
    }
}

template<typename T>
inline void get_Axy(const WigglerType *W, const double z, ss_vect<T> &x,
        T AxoBrho[], T AyoBrho[])

{
    int i;
    double ky, kz_n;
    T cx, cz, sx, sz, chy, shy;

    for (i = 0; i <= 3; ++i) {
        AxoBrho[i] = 0.0;
        AyoBrho[i] = 0.0;
    }

    for (i = 0; i < W->n_harm; i++) {
        kz_n = W->harm[i] * 2.0 * M_PI / W->lambda;
        ky = sqrt(sqr(W->kxV[i]) + sqr(kz_n));
        cx = cos(W->kxV[i] * x[x_]);
        sx = sin(W->kxV[i] * x[x_]);
        chy = cosh(ky * x[y_]);
        shy = sinh(ky * x[y_]);
        sz = sin(kz_n * z);

        AxoBrho[0] += W->BoBrhoV[i] / kz_n * cx * chy * sz;
        AyoBrho[0] += W->BoBrhoV[i] * W->kxV[i] / (ky * kz_n) * sx * shy * sz;

        // derivatives with respect to x
        AxoBrho[1] -= W->BoBrhoV[i] * W->kxV[i] / kz_n * sx * chy * sz;
        AyoBrho[1] += W->BoBrhoV[i] * sqr(W->kxV[i]) / (ky * kz_n) * cx * shy
                * sz;

        // derivatives with respect to y
        AxoBrho[2] += W->BoBrhoV[i] * ky / kz_n * cx * shy * sz;
        AyoBrho[2] += W->BoBrhoV[i] * W->kxV[i] / kz_n * sx * chy * sz;

        if (globval.radiation) {
            cz = cos(kz_n * z);
            // derivatives with respect to z
            AxoBrho[3] += W->BoBrhoV[i] * cx * chy * cz;
            AyoBrho[3] += W->BoBrhoV[i] * W->kxV[i] / ky * sx * shy * cz;
        }
    }
}

/*
 template<typename T>
 inline void get_Axy_map(const FieldMapType *FM, const double z,
 const ss_vect<T> &x, T AxoBrho[], T AyoBrho[])
 {
 float  y, ax0, ax1, ax2, ay0, ay1, ay2;

 const  float dy = 1e-3, dz = 1e-3;

 y = is_double<T>::cst(x[y_]);

 if ((z < FM->s_pos[1]) || (z > FM->s_pos[FM->n_s])) {
 cout << scientific << setprecision(3)
 << "get_Axy_map: s out of range " << z << endl;
 exit_(1);
 }

 if ((y < FM->y_pos[1]) || (y > FM->y_pos[FM->m_y])) {
 cout << scientific << setprecision(3)
 << "get_Axy_map: y out of range " << y << endl;
 exit_(1);
 }

 splin2(FM->y_pos, FM->s_pos, FM->AxoBrho, FM->AxoBrho2, FM->m_y, FM->n_s,
 y, z, &ax1);
 AxoBrho[0] = FM->scl*ax1;

 splin2(FM->y_pos, FM->s_pos, FM->AyoBrho, FM->AyoBrho2, FM->m_y, FM->n_s,
 y, z, &ay1);
 AyoBrho[0] = FM->scl*ay1;

 // derivatives with respect to x
 AxoBrho[1] = FM->scl*0.0; AyoBrho[1] = FM->scl*0.0;

 // derivatives with respect to y
 splin2(FM->y_pos, FM->s_pos, FM->AxoBrho, FM->AxoBrho2, FM->m_y, FM->n_s,
 y+dy, z, &ax2);
 splin2(FM->y_pos, FM->s_pos, FM->AxoBrho, FM->AxoBrho2, FM->m_y, FM->n_s,
 y-dy, z, &ax1);
 splin2(FM->y_pos, FM->s_pos, FM->AxoBrho, FM->AxoBrho2, FM->m_y, FM->n_s,
 y, z, &ax0);
 AxoBrho[2] =
 (ax2-ax1)/(2.0*dy) + (ax2+ax1-2.0*ax0)/sqr(dy)*is_tps<T>::set_prm(y_+1);
 AxoBrho[2] *= FM->scl;

 splin2(FM->y_pos, FM->s_pos, FM->AyoBrho, FM->AyoBrho2, FM->m_y, FM->n_s,
 y+dy, z, &ay2);
 splin2(FM->y_pos, FM->s_pos, FM->AyoBrho, FM->AyoBrho2, FM->m_y, FM->n_s,
 y-dy, z, &ay1);
 splin2(FM->y_pos, FM->s_pos, FM->AyoBrho, FM->AyoBrho2, FM->m_y, FM->n_s,
 y, z, &ay0);
 AyoBrho[2] =
 (ay2-ay1)/(2.0*dy) + (ay2+ay1-2.0*ay0)/sqr(dy)*is_tps<T>::set_prm(y_+1);
 AyoBrho[2] *= FM->scl;

 if (globval.radiation) {
 // derivatives with respect to z
 splin2(FM->y_pos, FM->s_pos, FM->AxoBrho, FM->AxoBrho2, FM->m_y, FM->n_s,
 y, z+dz, &ax2);
 splin2(FM->y_pos, FM->s_pos, FM->AxoBrho, FM->AxoBrho2, FM->m_y, FM->n_s,
 y, z-dz, &ax1);
 AxoBrho[3] = (ax2-ax1)/(2.0*dz); AxoBrho[3] *= FM->scl;

 splin2(FM->y_pos, FM->s_pos, FM->AyoBrho, FM->AyoBrho2, FM->m_y, FM->n_s,
 y, z+dz, &ay2);
 splin2(FM->y_pos, FM->s_pos, FM->AyoBrho, FM->AyoBrho2, FM->m_y, FM->n_s,
 y, z-dz, &ay1);
 AyoBrho[3] = (ay2-ay1)/(2.0*dz); AyoBrho[3] *= FM->scl;
 if (false)
 cout << fixed << setprecision(5)
 << setw(8) << z << setw(9) << is_double<T>::cst(AxoBrho[3]) << endl;
 }
 }
 */

template<typename T>
void Wiggler_pass_EF(const elemtype &elem, ss_vect<T> &x) {
    // First order symplectic integrator for wiggler using expanded Hamiltonian

    int i, nstep = 0;
    double h, z;
    T AxoBrho[4], AyoBrho[4], psi, hodp, a12, a21, a22, det;
    T d1, d2, a11, c11, c12, c21, c22, x2, B[3];

    switch (elem.Pkind) {
    case Wigl:
        nstep = elem.W->PN;
        break;
    case FieldMap:
        nstep = elem.FM->n_step;
        break;
    default:
        cout << "Wiggler_pass_EF: unknown element type" << endl;
        exit_(1);
        break;
    }

    h = elem.PL / nstep;
    z = 0.0;
    for (i = 1; i <= nstep; ++i) {
        switch (elem.Pkind) {
        case Wigl:
            get_Axy(elem.W, z, x, AxoBrho, AyoBrho);
            break;
        case FieldMap:
            //      get_Axy_map(elem.FM, z, x, AxoBrho, AyoBrho);
            break;
        default:
            cout << "Wiggler_pass_EF: unknown element type" << endl;
            exit_(1);
            break;
        }

        psi = 1.0 + x[delta_];
        hodp = h / psi;
        a11 = hodp * AxoBrho[1];
        a12 = hodp * AyoBrho[1];
        a21 = hodp * AxoBrho[2];
        a22 = hodp * AyoBrho[2];
        det = 1.0 - a11 - a22 + a11 * a22 - a12 * a21;
        d1 = hodp * AxoBrho[0] * AxoBrho[1];
        d2 = hodp * AxoBrho[0] * AxoBrho[2];
        c11 = (1.0 - a22) / det;
        c12 = a12 / det;
        c21 = a21 / det;
        c22 = (1.0 - a11) / det;
        x2 = c11 * (x[px_] - d1) + c12 * (x[py_] - d2);

        x[py_] = c21 * (x[px_] - d1) + c22 * (x[py_] - d2);
        x[px_] = x2;
        x[x_] += hodp * (x[px_] - AxoBrho[0]);
        x[y_] += hodp * x[py_];
        x[ct_] += h * (sqr((x[px_] - AxoBrho[0]) / psi) + sqr((x[py_]
                - AyoBrho[0]) / psi)) / 2.0;

        if (false)
            cout << scientific << setprecision(3) << setw(8) << z << setw(11)
                    << is_double<T>::cst(x[x_]) << setw(11)
                    << is_double<T>::cst(x[px_]) << setw(11)
                    << is_double<T>::cst(x[y_]) << setw(11)
                    << is_double<T>::cst(x[py_]) << endl;

        if (globval.pathlength)
            x[ct_] += h;

        if (globval.radiation || globval.emittance) {
            B[X_] = -AyoBrho[3];
            B[Y_] = AxoBrho[3];
            B[Z_] = AyoBrho[1] - AxoBrho[2];
            radiate(x, h, 0.0, B);
        }

        z += h;
    }
}

template<typename T>
inline void get_Axy2(const double z, const double kxV, const double kxH,
        const double kz, const double BoBrhoV, const double BoBrhoH,
        const double phi, ss_vect<T> &x, T AxoBrho[], T AyoBrho[]) {
    int i;
    T cx, sx, cz1, cz2, sz1, sz2, chy, shy, kyH, kyV, chx, shx, cy, sy;

    for (i = 0; i <= 3; ++i) {
        AxoBrho[i] = 0.0;
        AyoBrho[i] = 0.0;
    }

    kyV = sqrt(sqr(kz) + sqr(kxV));
    kyH = sqrt(sqr(kz) + sqr(kxH));
    cx = cos(kxV * x[x_]);
    sx = sin(kxV * x[x_]);
    cy = cos(kxH * x[y_]);
    sy = sin(kxH * x[y_]);
    chx = cosh(kyH * x[x_]);
    shx = sinh(kyH * x[x_]);
    chy = cosh(kyV * x[y_]);
    shy = sinh(kyV * x[y_]);
    sz1 = sin(kz * z);
    sz2 = sin(kz * z + phi);

    AxoBrho[0] += BoBrhoV / kz * cx * chy * sz1;
    AxoBrho[0] -= BoBrhoH * kxH / (kyH * kz) * shx * sy * sz2;
    AyoBrho[0] += BoBrhoV * kxV / (kyV * kz) * sx * shy * sz1;
    AyoBrho[0] -= BoBrhoH / kz * chx * cy * sz2;

    /* derivatives with respect to x */
    AxoBrho[1] -= BoBrhoV * kxV / kz * sx * chy * sz1;
    AxoBrho[1] -= BoBrhoH * kxH / kz * chx * sy * sz2;
    AyoBrho[1] += BoBrhoV * sqr(kxV) / (kyV * kz) * cx * shy * sz1;
    AyoBrho[1] -= BoBrhoH * kyH / kz * shx * cy * sz2;

    /* derivatives with respect to y */
    AxoBrho[2] += BoBrhoV * kyV / kz * cx * shy * sz1;
    AxoBrho[2] -= BoBrhoH * sqr(kxH) / (kyH * kz) * shx * cy * sz2;
    AyoBrho[2] += BoBrhoV * kxV / kz * sx * chy * sz1;
    AyoBrho[2] += BoBrhoH * kxH / kz * chx * sy * sz2;

    if (globval.radiation) {
        cz1 = cos(kz * z);
        cz2 = cos(kz * z + phi);
        /* derivatives with respect to z */
        AxoBrho[3] += BoBrhoV * cx * chy * cz1;
        AxoBrho[3] -= BoBrhoH * kxH / kyH * shx * sy * cz2;
        AyoBrho[3] += BoBrhoV * kxV / kyV * sx * shy * cz1;
        AyoBrho[3] -= BoBrhoH * chx * cy * cz2;
    }
}

template<typename T>
void Wiggler_pass_EF2(int nstep, double L, double kxV, double kxH, double kz,
        double BoBrhoV, double BoBrhoH, double phi, ss_vect<T> &x) {
    // First order symplectic integrator for wiggler using expanded Hamiltonian

    int i;
    double h, z;
    T hodp, B[3], px1, px2, px3, py1, py2, AxoBrho[4], AyoBrho[4], psi;
    T px = 0.0, py = 0.0;

    h = L / nstep;
    z = 0.0;
    for (i = 1; i <= nstep; ++i) {
        get_Axy2(z, kxV, kxH, kz, BoBrhoV, BoBrhoH, phi, x, AxoBrho, AyoBrho);

        psi = 1.0 + x[delta_];
        hodp = h / psi;

        px1 = (x[px_] - (AxoBrho[0] * AxoBrho[1] + AyoBrho[0] * AyoBrho[1])
                * hodp) * (1 - AyoBrho[2] * hodp);
        px2 = (x[py_] - (AxoBrho[0] * AxoBrho[2] + AyoBrho[0] * AyoBrho[2])
                * hodp) * AyoBrho[1] * hodp;
        px3 = (1 - AxoBrho[1] * hodp) * (1 - AyoBrho[2] * hodp) - AxoBrho[2]
                * AyoBrho[1] * hodp * hodp;

        py1 = (x[py_] - (AxoBrho[0] * AxoBrho[2] + AyoBrho[0] * AyoBrho[2])
                * hodp) * (1 - AxoBrho[1] * hodp);
        py2 = (x[px_] - (AxoBrho[0] * AxoBrho[1] + AyoBrho[0] * AyoBrho[1])
                * hodp) * AxoBrho[2] * hodp;

        py = (py1 + py2) / px3;
        px = (px1 + px2) / px3;
        x[x_] += hodp * (px - AxoBrho[0]);
        x[y_] += hodp * (py - AyoBrho[0]);
        x[ct_] += h * (sqr((px - AxoBrho[0]) / psi) + sqr((py - AyoBrho[0])
                / psi)) / 2.0;

        if (globval.pathlength)
            x[ct_] += h;

        if (globval.radiation || globval.emittance) {
            B[X_] = -AyoBrho[3];
            B[Y_] = AxoBrho[3];
            B[Z_] = AyoBrho[1] - AxoBrho[2];
            radiate(x, h, 0.0, B);
        }

        z += h;
    }

    x[px_] = px;
    x[py_] = py;
}

template<typename T>
inline void get_Axy_EF3(const WigglerType *W, const double z,
        const ss_vect<T> &x, T &AoBrho, T dAoBrho[], T &dp, const bool hor) {
    int i;
    double ky, kz_n;
    T cx, sx, sz, chy, shy, cz;

    AoBrho = 0.0;
    dp = 0.0;

    for (i = 0; i < 3; i++)
        dAoBrho[i] = 0.0;

    for (i = 0; i < W->n_harm; i++) {
        kz_n = W->harm[i] * 2.0 * M_PI / W->lambda;
        ky = sqrt(sqr(W->kxV[i]) + sqr(kz_n));

        cx = cos(W->kxV[i] * x[x_]);
        sx = sin(W->kxV[i] * x[x_]);
        chy = cosh(ky * x[y_]);
        shy = sinh(ky * x[y_]);
        sz = sin(kz_n * z);

        if (hor) {
            // A_x/Brho
            AoBrho += W->BoBrhoV[i] / kz_n * cx * chy * sz;

            if (globval.radiation) {
                cz = cos(kz_n * z);
                dAoBrho[X_] -= W->BoBrhoV[i] * W->kxV[i] / kz_n * sx * chy * sz;
                dAoBrho[Y_] += W->BoBrhoV[i] * ky / kz_n * cx * shy * sz;
                dAoBrho[Z_] += W->BoBrhoV[i] * cx * chy * cz;
            }

            // dp_y
            if (W->kxV[i] == 0.0)
                dp += W->BoBrhoV[i] / kz_n * ky * x[x_] * shy * sz;
            else
                dp += W->BoBrhoV[i] / (W->kxV[i] * kz_n) * ky * sx * shy * sz;
        } else {
            // A_y/Brho
            AoBrho += W->BoBrhoV[i] * W->kxV[i] / (ky * kz_n) * sx * shy * sz;

            if (globval.radiation) {
                cz = cos(kz_n * z);
                dAoBrho[X_] += W->BoBrhoV[i] * sqr(W->kxV[i]) / (ky * kz_n)
                        * cx * shy * sz;
                dAoBrho[Y_] += W->BoBrhoV[i] * W->kxV[i] / kz_n * sx * chy * sz;
                dAoBrho[Z_] += W->BoBrhoV[i] * W->kxV[i] / ky * sx * shy * cz;
            }

            // dp_x
            dp += W->BoBrhoV[i] / kz_n * sqr(W->kxV[i] / ky) * cx * chy * sz;
        }
    }
}

template<typename T>
void Wiggler_pass_EF3(const elemtype &elem, ss_vect<T> &x) {
    /* Second order symplectic integrator for insertion devices based on:

     E. Forest, et al "Explicit Symplectic Integrator for s-dependent
     Static Magnetic Field"                                                */

    int i;
    double h, z;
    T hd, AxoBrho, AyoBrho, dAxoBrho[3], dAyoBrho[3], dpy, dpx, B[3];

    h = elem.PL / elem.W->PN;
    z = 0.0;

    for (i = 1; i <= elem.W->PN; i++) {
        hd = h / (1.0 + x[delta_]);

        // 1: half step in z
        z += 0.5 * h;

        // 2: half drift in y
        get_Axy_EF3(elem.W, z, x, AyoBrho, dAyoBrho, dpx, false);

        x[px_] -= dpx;
        x[py_] -= AyoBrho;
        x[y_] += 0.5 * hd * x[py_];
        x[ct_] += sqr(0.5) * hd * sqr(x[py_]) / (1.0 + x[delta_]);

        get_Axy_EF3(elem.W, z, x, AyoBrho, dAyoBrho, dpx, false);

        x[px_] += dpx;
        x[py_] += AyoBrho;

        // 3: full drift in x
        get_Axy_EF3(elem.W, z, x, AxoBrho, dAxoBrho, dpy, true);

        x[px_] -= AxoBrho;
        x[py_] -= dpy;
        x[x_] += hd * x[px_];
        x[ct_] += 0.5 * hd * sqr(x[px_]) / (1.0 + x[delta_]);

        if (globval.pathlength)
            x[ct_] += h;

        get_Axy_EF3(elem.W, z, x, AxoBrho, dAxoBrho, dpy, true);

        x[px_] += AxoBrho;
        x[py_] += dpy;

        // 4: a half drift in y
        get_Axy_EF3(elem.W, z, x, AyoBrho, dAyoBrho, dpx, false);

        x[px_] -= dpx;
        x[py_] -= AyoBrho;
        x[y_] += 0.5 * hd * x[py_];
        x[ct_] += sqr(0.5) * hd * sqr(x[py_]) / (1.0 + x[delta_]);

        get_Axy_EF3(elem.W, z, x, AyoBrho, dAyoBrho, dpx, false);

        x[px_] += dpx;
        x[py_] += AyoBrho;

        // 5: half step in z
        z += 0.5 * h;

        if (globval.radiation || globval.emittance) {
            get_Axy_EF3(elem.W, z, x, AyoBrho, dAyoBrho, dpx, false);
            get_Axy_EF3(elem.W, z, x, AxoBrho, dAxoBrho, dpy, true);
            B[X_] = -dAyoBrho[Z_];
            B[Y_] = dAxoBrho[Z_];
            B[Z_] = dAyoBrho[X_] - dAxoBrho[Y_];
            radiate(x, h, 0.0, B);
        }
    }
}

template<typename T>
void Wiggler_Pass(CellType &Cell, ss_vect<T> &X) {
    int seg;
    double L, L1, L2, K1, K2;
    elemtype *elemp;
    WigglerType *W;
    ss_vect<T> X1;

    elemp = &Cell.Elem;
    W = elemp->W;
    /* Global -> Local */
    GtoL(X, Cell.dS, Cell.dT, 0.0, 0.0, 0.0);
    switch (W->Pmethod) {

    case Meth_Linear:
        //    LinTrans(5L, W->W55, X);
        cout << "Wiggler_Pass: Meth_Linear not supported" << endl;
        exit_(1);
        break;

    case Meth_First:
        if ((W->BoBrhoV[0] != 0.0) || (W->BoBrhoH[0] != 0.0)) {
            if (!globval.EPU)
                Wiggler_pass_EF(Cell.Elem, X);
            else {
                Wiggler_pass_EF2(W->PN, elemp->PL, W->kxV[0], W->kxH[0], 2.0
                        * M_PI / W->lambda, W->BoBrhoV[0], W->BoBrhoH[0],
                        W->phi[0], X);
            }
        } else
            // drift if field = 0
            Drift(elemp->PL, X);
        break;

    case Meth_Second:
        if ((W->BoBrhoV[0] != 0.0) || (W->BoBrhoH[0] != 0.0)) {
            Wiggler_pass_EF3(Cell.Elem, X);
        } else
            // drift if field = 0
            Drift(elemp->PL, X);
        break;

    case Meth_Fourth: /* 4-th order integrator */
        L = elemp->PL / W->PN;
        L1 = c_1 * L;
        L2 = c_2 * L;
        K1 = d_1 * L;
        K2 = d_2 * L;
        for (seg = 1; seg <= W->PN; seg++) {
            Drift(L1, X);
            X1 = X;
            thin_kick(W->Porder, W->PBW, K1, 0.0, 0.0, X1);
            X[py_] = X1[py_];
            Drift(L2, X);
            X1 = X;
            thin_kick(W->Porder, W->PBW, K2, 0.0, 0.0, X1);
            X[py_] = X1[py_];
            Drift(L2, X);
            X1 = X;
            thin_kick(W->Porder, W->PBW, K1, 0.0, 0.0, X1);
            X[py_] = X1[py_];
            Drift(L1, X);
        }
        break;
    }
    /* Local -> Global */
    LtoG(X, Cell.dS, Cell.dT, 0.0, 0.0, 0.0);
}

#undef eps
#undef kx

template<typename T>
void FieldMap_Pass(CellType &Cell, ss_vect<T> &X) {

    GtoL(X, Cell.dS, Cell.dT, 0.0, 0.0, 0.0);

    Wiggler_pass_EF(Cell.Elem, X);

    LtoG(X, Cell.dS, Cell.dT, 0.0, 0.0, 0.0);
}

/******************************************************************** 
 void Insertion_Pass(CellType &Cell, ss_vect<T> &x)

  Purpose:
     Track vector x through an insertion
     If radiation or cavity on insertion is like a drift

     Input:
     Cell element to track through
     x initial coordinates vector

     Output:
     x final coordinates vector

     Return:
     none

     Global variables:
     none

     Specific functions:
     LinearInterpolation2
     Drft
     CopyVec

     Comments:
     Outside of interpolation table simulated by putting 1 in x[4]
     01/07/03 6D tracking activated
     10/01/05 First order kick part added                                  
     *******************************************************************/

template<typename T>
void Insertion_Pass(CellType &Cell, ss_vect<T> &x) {
    
    elemtype *elemp;
    double LN = 0.0;
    T tx1, tz1; /* thetax and thetaz retrieved from
     interpolation routine First order kick*/
    T tx2, tz2; /* thetax and thetaz retrieved from
     interpolation routine Second order Kick */
    T d;
    double alpha0 = 0.0; // 1/ brh0
    double alpha02 = 0.0; // alpha square
    int Nslice = 0;
    int i = 0;
    bool outoftable = false;

    elemp = &Cell.Elem;
    Nslice = elemp->ID->PN;
    alpha0 = c0 / globval.Energy * 1E-9 * elemp->ID->scaling1;
    alpha02 = (c0 / globval.Energy * 1E-9) * (c0 / globval.Energy * 1E-9)
            * elemp->ID->scaling2;

    //  /* Global -> Local */
    //  GtoL(X, Cell->dS, Cell->dT, 0.0, 0.0, 0.0);

    // (Nslice+1) drifts, n slice kicks
    LN = elemp->PL / (Nslice + 1);
    Drift(LN, x);

    for (i = 1; i <= Nslice; i++) {
        // First order kick map
        if (elemp->ID->firstorder) {
            if (!elemp->ID->linear) {
                //cout << "InsertionPass: Spline\n";
                SplineInterpolation2(x[x_], x[y_], tx1, tz1, Cell, outoftable,
                        1);
            } else{
                LinearInterpolation2(x[x_], x[y_], tx1, tz1, Cell, outoftable,
                        1);
            }
            if (outoftable) {
                x[x_] = 1e30;
                return;
            }

            d = alpha0 / Nslice;
            x[px_] += d * tx1;
            x[py_] += d * tz1;
        }

        // Second order kick map
        if (elemp->ID->secondorder) {
            if (!elemp->ID->linear) {
                //cout << "InsertionPass: Spline\n";
                SplineInterpolation2(x[x_], x[y_], tx2, tz2, Cell, outoftable,
                        2);
            } else {
                //cout << "InsertionPass: Linear\n";
                LinearInterpolation2(x[x_], x[y_], tx2, tz2, Cell, outoftable,
                        2);
            }
            if (outoftable) {
                x[x_] = 1e30;
                return;
            }

            d = alpha02 / Nslice / (1.0 + x[delta_]);
            x[px_] += d * tx2;
            x[py_] += d * tz2;
        }
        Drift(LN, x);
    }
    //  CopyVec(6L, x, Cell->BeamPos);

    //  /* Local -> Global */
    //  LtoG(X, Cell->dS, Cell->dT, 0.0, 0.0, 0.0);
}

template<typename T>
void sol_pass(const elemtype &elem, ss_vect<T> &x) {
    int i;
    double h, z;
    T hd, AxoBrho, AyoBrho, dAxoBrho[3], dAyoBrho[3], dpy, dpx, B[3];

    h = elem.PL / elem.Sol->N;
    z = 0.0;

    for (i = 1; i <= elem.Sol->N; i++) {
        hd = h / (1.0 + x[delta_]);

        // 1: half step in z
        z += 0.5 * h;

        // 2: half drift in y
        AyoBrho = elem.Sol->BoBrho * x[x_] / 2.0;
        dpx = elem.Sol->BoBrho * x[y_] / 2.0;
        //    get_Axy_EF3(elem.W, z, x, AyoBrho, dAyoBrho, dpx, false);

        x[px_] -= dpx;
        x[py_] -= AyoBrho;
        x[y_] += 0.5 * hd * x[py_];
        x[ct_] += sqr(0.5) * hd * sqr(x[py_]) / (1.0 + x[delta_]);

        AyoBrho = elem.Sol->BoBrho * x[x_] / 2.0;
        dpx = elem.Sol->BoBrho * x[y_] / 2.0;
        //    get_Axy_EF3(elem.W, z, x, AyoBrho, dAyoBrho, dpx, false);

        x[px_] += dpx;
        x[py_] += AyoBrho;

        // 3: full drift in x
        AxoBrho = -elem.Sol->BoBrho * x[y_] / 2.0;
        dpy = -elem.Sol->BoBrho * x[x_] / 2.0;
        //    get_Axy_EF3(elem.W, z, x, AxoBrho, dAxoBrho, dpy, true);

        x[px_] -= AxoBrho;
        x[py_] -= dpy;
        x[x_] += hd * x[px_];
        x[ct_] += 0.5 * hd * sqr(x[px_]) / (1.0 + x[delta_]);

        if (globval.pathlength)
            x[ct_] += h;

        AxoBrho = -elem.Sol->BoBrho * x[y_] / 2.0;
        dpy = -elem.Sol->BoBrho * x[x_] / 2.0;
        //    get_Axy_EF3(elem.W, z, x, AxoBrho, dAxoBrho, dpy, true);

        x[px_] += AxoBrho;
        x[py_] += dpy;

        // 4: a half drift in y
        AyoBrho = elem.Sol->BoBrho * x[x_] / 2.0;
        dpx = elem.Sol->BoBrho * x[y_] / 2.0;
        //    get_Axy_EF3(elem.W, z, x, AyoBrho, dAyoBrho, dpx, false);

        x[px_] -= dpx;
        x[py_] -= AyoBrho;
        x[y_] += 0.5 * hd * x[py_];
        x[ct_] += sqr(0.5) * hd * sqr(x[py_]) / (1.0 + x[delta_]);

        AyoBrho = elem.Sol->BoBrho * x[x_] / 2.0;
        dpx = elem.Sol->BoBrho * x[y_] / 2.0;
        //    get_Axy_EF3(elem.W, z, x, AyoBrho, dAyoBrho, dpx, false);

        x[px_] += dpx;
        x[py_] += AyoBrho;

        // 5: half step in z
        z += 0.5 * h;

        if (globval.radiation || globval.emittance) {
            dAxoBrho[X_] = 0.0;
            dAxoBrho[Y_] = -elem.Sol->BoBrho / 2.0;
            dAxoBrho[Z_] = 0.0;
            dAyoBrho[X_] = elem.Sol->BoBrho / 2.0;
            dAyoBrho[Y_] = 0.0;
            dAyoBrho[Z_] = 0.0;
            //      get_Axy_EF3(elem.W, z, x, AyoBrho, dAyoBrho, dpx, false);
            //      get_Axy_EF3(elem.W, z, x, AxoBrho, dAxoBrho, dpy, true);
            B[X_] = -dAyoBrho[Z_];
            B[Y_] = dAxoBrho[Z_];
            B[Z_] = dAyoBrho[X_] - dAxoBrho[Y_];
            radiate(x, h, 0.0, B);
        }
    }
}

template<typename T>
void Solenoid_Pass(CellType &Cell, ss_vect<T> &ps) {

    GtoL(ps, Cell.dS, Cell.dT, 0.0, 0.0, 0.0);

    sol_pass(Cell.Elem, ps);

    LtoG(ps, Cell.dS, Cell.dT, 0.0, 0.0, 0.0);
}

// Matrix model

void GtoL_M(Matrix &X, Vector2 &T) {
    Matrix R;

    /* Rotate */
    R[0][0] = T[0];
    R[0][1] = 0.0;
    R[0][2] = T[1];
    R[0][3] = 0.0;
    R[1][0] = 0.0;
    R[1][1] = T[0];
    R[1][2] = 0.0;
    R[1][3] = T[1];
    R[2][0] = -T[1];
    R[2][1] = 0.0;
    R[2][2] = T[0];
    R[2][3] = 0.0;
    R[3][0] = 0.0;
    R[3][1] = -T[1];
    R[3][2] = 0.0;
    R[3][3] = T[0];
    MulLMat(4L, R, X);
}

void LtoG_M(Matrix &X, Vector2 &T) {
    Matrix R;

    /* Rotate */
    R[0][0] = T[0];
    R[0][1] = 0.0;
    R[0][2] = -T[1];
    R[0][3] = 0.0;
    R[1][0] = 0.0;
    R[1][1] = T[0];
    R[1][2] = 0.0;
    R[1][3] = -T[1];
    R[2][0] = T[1];
    R[2][1] = 0.0;
    R[2][2] = T[0];
    R[2][3] = 0.0;
    R[3][0] = 0.0;
    R[3][1] = T[1];
    R[3][2] = 0.0;
    R[3][3] = T[0];
    MulLMat(4, R, X);
}

/****************************************************************************
 * void Drift_Pass_M(CellType *Cell, double *xref, vector *x)

 Purpose:
 matrix propagation through a drift
 x   = D55*x
 xref= drift(xref)

 Input:
 xref vector
 x    matrix

 Output:
 xref
 x

 Return:
 none

 Global variables:
 none

 Specific functions:
 MulLMat, Drft

 Comments:
 none

 ****************************************************************************/

void Drift_Pass_M(CellType &Cell, Vector &xref, Matrix &X) {

    MulLMat(5, Cell.Elem.D->D55, X);
    Drift(Cell.Elem.PL, xref);
}

void thin_kick_M(int Order, double MB[], double L, double irho, Vector &xref,
        Matrix &x) {
    int i;
    mpolArray MMB;
    Vector z;
    Matrix Mk;

    if (2 > Order || Order > HOMmax)
        return;
    for (i = 2; i <= Order; i++) {
        MMB[i + HOMmax - 1] = (i - 1) * MB[i + HOMmax];
        MMB[HOMmax - i + 1] = (i - 1) * MB[HOMmax - i];
    }
    z[0] = xref[0];
    z[1] = 0.0;
    z[2] = xref[2];
    z[3] = 0.0;
    z[4] = 0.0;
    z[5] = 0.0;
    thin_kick(Order - 1, MMB, L, 0.0, 0.0, z);
    z[1] -= L * sqr(irho);
    UnitMat(5L, Mk);
    Mk[1][0] = z[1];
    Mk[1][2] = z[3];
    Mk[3][0] = z[3];
    Mk[3][2] = -z[1];
    MulLMat(5L, Mk, x);
}

static void make3by3(Matrix &A, double a11, double a12, double a13, double a21,
        double a22, double a23, double a31, double a32, double a33) {
    /*
     Set the 3x3 matrix A to:
     (a11 a12 a13)
     A = (a21 a22 a23)
     (a31 a32 a33)
     */

    UnitMat(ss_dim, A); /* set matrix to unit 3x3 matrix */
    A[0][0] = a11;
    A[0][1] = a12;
    A[0][2] = a13;
    A[1][0] = a21;
    A[1][1] = a22;
    A[1][2] = a23;
    A[2][0] = a31;
    A[2][1] = a32;
    A[2][2] = a33;
}

/****************************************************************************
 * void make4by5(vector *A, double a11, double a12, double a15,
 double a21, double a22, double a25, double a33,
 double a34, double a35, double a43, double a44,
 double a45)
 Purpose:
 Constructor for matrix A
 All the matrix terms  are explicitly given as input

 Input:
 A matrix to initialize
 aij matrix terms

 Output:
 A initialized matrix

 Return:
 none

 Global variables:
 none

 Specific functions:
 UnitMat

 Comments:
 none

 ****************************************************************************/

static void make4by5(Matrix &A, double a11, double a12, double a15, double a21,
        double a22, double a25, double a33, double a34, double a35, double a43,
        double a44, double a45) {
    UnitMat(ss_dim, A); /* Initializes A to identity matrix */
    A[0][0] = a11;
    A[0][1] = a12;
    A[0][4] = a15;
    A[1][0] = a21;
    A[1][1] = a22;
    A[1][4] = a25;
    A[2][2] = a33;
    A[2][3] = a34;
    A[2][4] = a35;
    A[3][2] = a43;
    A[3][3] = a44;
    A[3][4] = a45;
}

static void mergeto4by5(Matrix &A, Matrix &AH, Matrix &AV) {
    /*
     merges two 3x3 matrices AH (H-plane) and AV (V-plane) into one
     big 4x5 matrix

     (ah11 ah12    0    0    ah13)
     (ah21 ah22    0    0    ah23)
     A=  (  0    0   av11 av12   av13)
     (  0    0   av21 av22   ah13)
     (  0    0     0    0       1)
     */
    int i, j;

    UnitMat(ss_dim, A);
    for (i = 1; i <= 2; i++) {
        A[i - 1][4] = AH[i - 1][2];
        A[i + 1][4] = AV[i - 1][2];
        for (j = 1; j <= 2; j++) {
            A[i - 1][j - 1] = AH[i - 1][j - 1];
            A[i + 1][j + 1] = AV[i - 1][j - 1];
        }
    }
}

void Drift_SetMatrix(int Fnum1, int Knum1) {
    /*
     Make transport matrix for drift from
     familiy Fnum1 and Kid number Knum
     L = L / (1 + dP)

     ( 1 L 0 0 0)
     D55  =  ( 0 1 0 0 0)
     ( 0 0 1 L 0)
     ( 0 0 0 1 0)
     */

    double L;
    CellType *cellp;
    elemtype *elemp;
    DriftType *D;

    if (ElemFam[Fnum1 - 1].nKid <= 0)
        return;
    cellp = &Cell[ElemFam[Fnum1 - 1].KidList[Knum1 - 1]];
    elemp = &cellp->Elem;
    D = elemp->D;
    L = elemp->PL / (1.0 + globval.dPparticle); /* L = L / (1 + dP) */
    make4by5(D->D55, 1.0, L, 0.0, 0.0, 1.0, 0.0, 1.0, L, 0.0, 0.0, 1.0, 0.0);
}

static void driftmat(Matrix &ah, double L) {
    L /= 1 + globval.dPparticle;
    make4by5(ah, 1.0, L, 0.0, 0.0, 1.0, 0.0, 1.0, L, 0.0, 0.0, 1.0, 0.0);
}

static void quadmat(Matrix &ahv, double L, double k) {
    /*
     creates the avh matrix for a quadrupole
     where av and ah are the horizontal and vertical
     focusing or defocusing matrices


     1/2                         1/2
     cos(L* (|K|)   )            sin(L* (|K|)   )
     c = ---------------          s = ---------------
     1/2                         1/2
     (1  + Dp)                    (1  + Dp)
     1/2
     sk = (|K|(1+dP))

     - if k > 0
     H plane                      V plane

     (  c   s/sk 0 )              (   ch sh/k 0 )
     ah = ( sk*s  c   0 )         av = ( sk*sh ch  0 )
     (  0    0   1 )              (   0   0   1 )


     ( ah11 ah12    0    0    ah13 )
     ( ah21 ah22    0    0    ah23 )
     avh =  (  0    0    av11 av12   av13 )
     (  0    0    av21 av22   ah13 )
     (  0    0     0    0       1  )                     */

    double t, sk, sk0, s, c;
    Matrix a, ah, av;

    if (k == 0.0) {
        /* pure drift focusing */
        driftmat(ahv, L);
        return;
    }
    sk0 = sqrt(fabs(k));
    t = L * sk0 / sqrt(1.0 + globval.dPparticle);
    c = cos(t);
    s = sin(t);
    sk = sk0 * sqrt(1.0 + globval.dPparticle);
    make3by3(a, c, s / sk, 0.0, -sk * s, c, 0.0, 0.0, 0.0, 1.0);
    if (k > 0.0)
        CopyMat(3L, a, ah);
    else
        CopyMat(3L, a, av);
    c = cosh(t);
    s = sinh(t);
    sk = sk0 * sqrt(1.0 + globval.dPparticle);
    make3by3(a, c, s / sk, 0.0, sk * s, c, 0.0, 0.0, 0.0, 1.0);
    if (k > 0.0)
        CopyMat(3L, a, av);
    else
        CopyMat(3L, a, ah);
    mergeto4by5(ahv, ah, av);
}

/****************************************************************************/
/* static void bendmat(vector *M, double L, double irho, double phi1,
 double phi2, double gap, double k)

 Purpose:  called  by Mpole_Setmatrix

 For a quadrupole  see quadmat routine for explanation

 For a dipole

 (1            0 0)
 Edge(theta) = (h*tan(theta) 1 0)
 (0            0 1)

 (1                 0 0)
 Edge(theta) = (-h*tan(theta-psi) 1 0)
 (0                 0 1)

 2
 K1*gap*h*(1 + sin phi)
 psi = -----------------------, K1 = 1/2
 cos phi

 Input:
 L   : length [m]
 irho: 1/rho [1/m]
 phi1: entrance edge angle [degres]
 phi2: exit edge angle [degres]
 K   : gradient = n/Rho

 Output:
 M transfer matrix

 Return:
 none

 Global variables:
 none

 Specific functions:
 quadmat, make3by3
 UnitMat, MulRMat, psi

 Comments:
 none

 ****************************************************************************/
static void bendmat(Matrix &M, double L, double irho, double phi1, double phi2,
        double gap, double k) {
    /*  called  by Mpole_Setmatrix

     For a quadrupole  see quadmat routine for explanation

     For a dipole

     (1            0 0)
     Edge(theta) = (h*tan(theta) 1 0)
     (0            0 1)

     (1                 0 0)
     Edge(theta) = (-h*tan(theta-psi) 1 0)
     (0                 0 1)

     2
     K1*gap*h*(1 + sin phi)
     psi = -----------------------, K1 = 1/2
     cos phi                                              */

    double r, s, c, sk, p, fk, afk;
    Matrix edge, ah, av;
    double coef, scoef;

    if (irho == 0.0) {
        /* Quadrupole matrix */
        quadmat(M, L, k);
        return;
    }

    /* For multipole w/ irho !=0 eg dipole */
    coef = 1.0 + globval.dPparticle;
    scoef = sqrt(coef);
    r = L * irho / scoef;

    if (k == 0.0) {
        /* simple vertical dipole magnet */
        /*
         H-plane
         2    2                2
         px + py              2 x
         H = --------  - h*x*dP + h ---
         2*(1+dP)               2

         2     2
         dx     h        h*dP
         --2 + ---- x = -----
         ds    1+dP      1+dP


         let be u = Lh/sqrt(1+dP) then the transfert matrix becomes:

         (                              sin(u)              1- cos(u)      )
         (          cos(u)         --------------       -----------------  )
         (                          h sqrt(1+dP)                 h         )
         (  -sin(u)*sqrt(1+dP)*h        cos(u)           sin(u)*sqrt(1+dP) )
         (            0                  0                       1         )

         */
        c = cos(r);
        s = sin(r);
        make3by3(ah, c, s / (irho * scoef), (1.0 - c) / irho,
                -s * scoef * irho, c, s * scoef, 0.0, 0.0, 1.0);
        /*
         V-plane: it is just a drift
         (        L     )
         (   1   ----  0)
         (       1+dP   )
         (   0     1   0)
         (   0     0   1)
         */
        make3by3(av, 1.0, L / coef, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0);
    } else {
        /* gradient bend, k= n/rho^2 */
        /*
         K = -k -h*h
         p = L*sqrt(|K|)/sqrt(1+dP)
         */
        fk = -k - irho * irho;
        afk = fabs(fk);
        sk = sqrt(afk);
        p = L * sk / scoef;
        if (fk < 0.0) {
            /*
             H-plane
             2    2                     2
             px + py                 2   x
             H = --------  - h*x*dP + (k+h ) ---
             2*(1+dP)                    2

             2      2
             dx    k+h        h*dP
             --2 + ---- x = -----
             ds    1+dP      1+dP


             let be u = Lsqrt(|h*h+b2|)/sqrt(1+dP)
             then the transfert matrix becomes:

             (                              sin(u)              1- cos(u)      )
             (          cos(u)         --------------       -----------------  )
             (                          sk*sqrt(1+dP)           |k+h*h|*h      )
             (  -sin(u)*sqrt(1+dP)*sk      cos(u)        h*sin(u)*sqrt(1+dP)/sk)
             (            0                  0                       1         )

             */
            c = cos(p);
            s = sin(p);
            make3by3(ah, c, s / sk / scoef, irho * (1.0 - c) / (coef * afk),
                    -scoef * sk * s, c, scoef * irho / sk * s, 0.0, 0.0, 1.0);
            sk = sqrt(fabs(k));
            p = L * sk / scoef;
            c = cosh(p);
            s = sinh(p);
            make3by3(av, c, s / sk / scoef, 0.0, sk * s * scoef, c, 0.0, 0.0,
                    0.0, 1.0);
        } else {
            /* vertically focusing */
            c = cosh(p);
            s = sinh(p);
            make3by3(ah, c, s / sk / scoef, (c - 1.0) * irho / afk, scoef * s
                    * sk, c, scoef * s * irho / sk, 0.0, 0.0, 1.0);
            sk = sqrt(fabs(k));
            p = L * sk / scoef;
            c = cos(p);
            s = sin(p);
            make3by3(av, c, s / sk / scoef, 0.0, -sk * s * scoef, c, 0.0, 0.0,
                    0.0, 1.0);
        }
    }
    /* Edge focusing, no effect due to gap between AU and AD */

    /*
     (1            0 0)
     Edge(theta) = (h*tan(theta) 1 0)
     (0            0 1)

     (1                 0 0)
     Edge(theta) = (-h*tan(theta-psi) 1 0)
     (0                 0 1)

     2
     K1*gap*h*(1 + sin phi)
     psi = -----------------------, K1 = 1/2
     cos phi

     */
    if (phi1 != 0.0 || gap > 0.0) {
        UnitMat(3L, edge);
        edge[1][0] = irho * tan(dtor(phi1));
        MulRMat(3L, ah, edge); /* ah <- ah*edge */
        if (true)
            edge[1][0] = -irho * tan(dtor(phi1) - get_psi(irho, phi1, gap))
                    / coef;
        else
            edge[1][0] = -irho * tan(dtor(phi1) - get_psi(irho, phi1, gap));
        MulRMat(3L, av, edge); /* av <- av*edge */
    } else if (phi2 != 0.0 || gap < 0.0) {
        UnitMat(3L, edge);
        edge[1][0] = irho * tan(dtor(phi2));
        MulLMat(3L, edge, ah); /* av <- edge*av */
        if (true)
            edge[1][0] = -irho * tan(dtor(phi2)
                    - get_psi(irho, phi2, fabs(gap))) / coef;
        else
            edge[1][0] = -irho * tan(dtor(phi2)
                    - get_psi(irho, phi2, fabs(gap)));
        MulLMat(3L, edge, av); /* av <- edge*av */
    }
    mergeto4by5(M, ah, av);
}

void Mpole_Setmatrix(int Fnum1, int Knum1, double K) {
    /*   Compute transfert matrix for a quadrupole magnet
     the transfert matrix A is plitted into two part
     A = AD55xAU55

     where AD55 is the downstream transfert matrix
     corresponding to a half magnet w/ an exit angle
     and no entrance angle.
     The linear frindge field is taken into account

     where AU55 is the upstream transfert matrix
     corresponding to a half magnet w/ an entrance
     angle and no exit angle.
     The linear frindge field is taken into account                    */

    CellType *cellp;
    elemtype *elemp;
    MpoleType *M;

    if (ElemFam[Fnum1 - 1].nKid <= 0) {
        printf("Mpole_Setmatrix: no kids in famile %d\n", Fnum1);
        return;
    }
    cellp = &Cell[ElemFam[Fnum1 - 1].KidList[Knum1 - 1]];
    elemp = &cellp->Elem;
    M = elemp->M;

    bendmat(M->AU55, elemp->PL / 2.0, M->Pirho, M->PTx1, 0.0, M->Pgap, K);
    bendmat(M->AD55, elemp->PL / 2.0, M->Pirho, 0.0, M->PTx2, -M->Pgap, K);
}

void Wiggler_Setmatrix(int Fnum1, int Knum1, double L, double kx, double kz,
        double k0) {
    double t, s, c, k, ky, LL;
    Matrix ah, av;
    double TEMP;
    WigglerType *W;

    LL = L / (1.0 + globval.dPparticle);
    if (kx == 0e0)
        make3by3(ah, 1.0, LL, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0);
    else {
        TEMP = kx / kz;
        k = sqrt(TEMP * TEMP * fabs(k0));
        t = LL * k;
        c = cosh(t);
        s = sinh(t);
        make3by3(ah, c, s / k, 0.0, k * s, c, 0.0, 0.0, 0.0, 1.0);
    }
    if (k0 == 0e0)
        make3by3(av, 1.0, LL, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0);
    else {
        ky = sqrt(kx * kx + kz * kz);
        TEMP = ky / kz;
        k = sqrt(TEMP * TEMP * fabs(k0));
        t = LL * k;
        c = cos(t);
        s = sin(t);
        make3by3(av, c, s / k, 0.0, -k * s, c, 0.0, 0.0, 0.0, 1.0);
    }
    W = Cell[ElemFam[Fnum1 - 1].KidList[Knum1 - 1]].Elem.W;
    mergeto4by5(W->W55, ah, av);
}

void Mpole_Pass_M(CellType &Cell, Vector &xref, Matrix &x) {
    double k;
    elemtype *elemp;
    MpoleType *M;

    elemp = &Cell.Elem;
    M = elemp->M;
    /* Global -> Local */
    GtoL_M(x, Cell.dT);
    GtoL(xref, Cell.dS, Cell.dT, M->Pc0, M->Pc1, M->Ps1);

    switch (M->Pmethod) {

    case Meth_Linear:

    case Meth_Fourth: /* Nothing */
        // Laurent
        //  case Meth_First:   /* Nothing */
        /* Tracy integrator */
        if (M->Pthick == thick) {
            /* thick element */
            /* First Linear */
            MulLMat(5, M->AU55, x);
            LinTrans(5, M->AU55, xref);
            k = M->PB[Quad + HOMmax];
            M->PB[Quad + HOMmax] = 0.0;
            /* Kick */
            thin_kick_M(M->Porder, M->PB, elemp->PL, 0.0, xref, x);
            thin_kick(M->Porder, M->PB, elemp->PL, 0.0, 0.0, xref);
            M->PB[Quad + HOMmax] = k;
            /* Second Linear */
            MulLMat(5L, M->AD55, x);
            LinTrans(5L, M->AD55, xref);
        } else {
            /* thin kick */
            thin_kick_M(M->Porder, M->PB, 1.0, 0.0, xref, x);
            thin_kick(M->Porder, M->PB, 1.0, 0.0, 0.0, xref);
        }
        break;
    }

    /* Local -> Global */
    LtoG_M(x, Cell.dT);
    LtoG(xref, Cell.dS, Cell.dT, M->Pc0, M->Pc1, M->Ps1);
}

void Wiggler_Pass_M(CellType &Cell, Vector &xref, Matrix &x) {
    elemtype *elemp;
    WigglerType *W;

    elemp = &Cell.Elem;
    W = elemp->W;

    /* Global -> Local */
    GtoL_M(x, Cell.dT);
    GtoL(xref, Cell.dS, Cell.dT, 0.0, 0.0, 0.0);

    switch (W->Pmethod) {
    case Meth_Linear: /* Nothing */
        /* Tracy integrator */
        MulLMat(5, W->W55, x);
        LinTrans(5L, W->W55, xref);
        break;
    }

    /* Local -> Global */
    LtoG_M(x, Cell.dT);
    LtoG(xref, Cell.dS, Cell.dT, 0.0, 0.0, 0.0);
}

void Insertion_SetMatrix(int Fnum1, int Knum1) {
    /* void Insertion_SetMatrix(int Fnum1, int Knum1)

     Purpose: called by Insertion_Init
     Constructs the linear matrices
     K55 kick matrix for one slice
     D55 drift matrix for one slice
     KD55 full linear transport matrix

     Input:
     Fnum1 Family number
     Knum1 Kid number

     Output:
     none

     Return:
     none

     Global variables:
     globval

     Specific functions:
     LinearInterpDeriv2

     Comments:
     04/07/03 derivative interpolation around closed orbit
     10/01/05 First order kick added

     Need to be checked energy dependence and so on.                       */

    int i = 0;
    double L = 0.0;
    CellType *cellp;
    elemtype *elemp;
    InsertionType *ID;
    double alpha0 = 0.0, alpha02 = 0.0;
    double DTHXDX = 0.0, DTHXDZ = 0.0, DTHZDX = 0.0, DTHZDZ = 0.0;
    int Nslice = 0;

    if (ElemFam[Fnum1 - 1].nKid <= 0)
        return;

    cellp = &Cell[ElemFam[Fnum1 - 1].KidList[Knum1 - 1]];
    elemp = &cellp->Elem;
    ID = elemp->ID;
    Nslice = ID->PN;
    alpha0 = c0 / globval.Energy * 1E-9 * ID->scaling1;
    alpha02 = (c0 / globval.Energy * 1E-9) * c0 / globval.Energy * 1E-9 / (1.0
            + globval.dPparticle) * ID->scaling2;

    UnitMat(6L, ID->D55);
    UnitMat(6L, ID->K55);
    UnitMat(6L, ID->KD55);

    //  if (globval.radiation == false && globval.Cavity_on == false)
    //  {
    /* (Nslice + 1) Drifts for Nslice Kicks */

    /* Drift Matrix */
    L = elemp->PL / (Nslice + 1) / (1.0 + globval.dPparticle);
    make4by5(ID->D55, 1.0, L, 0.0, 0.0, 1.0, 0.0, 1.0, L, 0.0, 0.0, 1.0, 0.0);

    /* First order Kick */
    if (ID->firstorder) {
        /* quadrupole Kick matrix linearized around closed orbit */
        if (!ID->linear) {
            //        SplineInterpDeriv3(cellp->BeamPos[0], cellp->BeamPos[2],
            //			   &DTHXDX, &DTHXDZ, &DTHZDX, &DTHZDZ, cellp);
        } else {
            //        LinearInterpDeriv2(cellp->BeamPos[0], cellp->BeamPos[2],
            //			   &DTHXDX, &DTHXDZ, &DTHZDX, &DTHZDZ, cellp, 1);
        }
        ID->K55[1][0] = ID->K55[1][0] + alpha0 * DTHXDX / Nslice;
        ID->K55[1][2] = ID->K55[1][2] + alpha0 * DTHXDZ / Nslice;
        ID->K55[3][0] = ID->K55[3][0] + alpha0 * DTHZDX / Nslice;
        ID->K55[3][2] = ID->K55[3][2] + alpha0 * DTHZDZ / Nslice;
    }

    /* Second order Kick */
    if (ID->secondorder) {
        /* quadrupole Kick matrix linearized around closed orbit */
        if (!ID->linear) {
            //        SplineInterpDeriv3(cellp->BeamPos[0], cellp->BeamPos[2],
            //			   &DTHXDX, &DTHXDZ, &DTHZDX, &DTHZDZ, cellp);
        } else {
            //        LinearInterpDeriv2(cellp->BeamPos[0], cellp->BeamPos[2],
            //			   &DTHXDX, &DTHXDZ, &DTHZDX, &DTHZDZ, cellp, 2);
        }
        ID->K55[1][0] = ID->K55[1][0] + alpha02 * DTHXDX / Nslice;
        ID->K55[1][2] = ID->K55[1][2] + alpha02 * DTHXDZ / Nslice;
        ID->K55[3][0] = ID->K55[3][0] + alpha02 * DTHZDX / Nslice;
        ID->K55[3][2] = ID->K55[3][2] + alpha02 * DTHZDZ / Nslice;
    }

    MulLMat(6L, ID->D55, ID->KD55);

    for (i = 1; i <= Nslice; i++) {
        MulLMat(6L, ID->K55, ID->KD55);
        MulLMat(6L, ID->D55, ID->KD55);
    }

    //  }
    //  else
    //  {
    //    L = elemp->PL/(1.0 + globval.dPparticle);  /* L = L/(1 + dP) */
    //    make4by5(ID->KD55,
    //	     1.0, L, 0.0, 0.0, 1.0, 0.0,
    //	     1.0, L, 0.0, 0.0, 1.0, 0.0);
    //  }
}

/********************************************************************* 
    Purpose: called by Elem_Pass_M
     matrix propagation through a insertion kick-driftlike matrix
     x   = KD55*x
     xref= insertion(xref)

     Input:
     xref vector
     x    matrix

     Output:
     xref
     x

     Return:
     none

     Global variables:
     none

     Specific functions:
     MulLMat, Drft

     Comments:
     01/07/03 6D tracking activated                                        
******************************************************************************/
void Insertion_Pass_M(CellType &Cell, Vector &xref, Matrix &M) {


    elemtype *elemp;

    elemp = &Cell.Elem;

    /* Global -> Local */
    //  GtoL_M(x, Cell->dT);
    //  GtoL(xref, Cell->dS, Cell->dT, 0.0, 0.0, 0.0);
    //  if (globval.radiation == false && globval.Cavity_on == false)
    //  {
    MulLMat(5, elemp->ID->KD55, M); /* M<-KD55*M */
    LinTrans(5, elemp->ID->KD55, xref);
    //  }
    //  else
    //  {
    //    MulLMat(5L, elemp->ID->D55, M); /* X<-D55*X */
    //    Drft(elemp->PL, elemp->PL/(1.0+xref[4]), xref);
    //  }

    /* Local -> Global */
    //  LtoG_M(x, Cell->dT);
    //  LtoG(xref, Cell->dS, Cell->dT, 0.0, 0.0, 0.0);
}

/****************************************************************************/
/* void getelem(long i, CellType *cellrec) 

 Purpose:
 assign all the information of i-th element from array Cell[i] to pointer cellrec

 Input:

 Output:
 none

 Return:
 none

 Global variables:
 none

 Specific functions:
 none

 Comments:

 ****************************************************************************/
void getelem(long i, CellType *cellrec) {
    *cellrec = Cell[i];
}
/****************************************************************************/
/* void putelem(long i, CellType *cellrec) 

 Purpose:
 assign all the information of pointer cellrec to i-th element to array Cell[i]

 Input:

 Output:
 none

 Return:
 none

 Global variables:
 none

 Specific functions:
 none

 Comments:

 ****************************************************************************/
void putelem(long i, CellType *cellrec) {
    Cell[i] = *cellrec;
}

/****************************************************************************/
/* int GetnKid(const int Fnum1)

 Purpose:
 return the number of kid in the family

 Input:
 Fnum1 :  family number


 Output:
 none

 Return:
 none

 Global variables:
 none

 Specific functions:
 none

 Comments:

 ****************************************************************************/
int GetnKid(const int Fnum1) {
    return (ElemFam[Fnum1 - 1].nKid);
}

/****************************************************************************/
/* long Elem_GetPos(const int Fnum1, const int Knum1)

 Purpose:
 get the element index in the lattice


 Input:
 Fnum1 :  family number of the element
 Knum1 :  kid number of the element in Fnum1

 Output:
 none

 Return:
 loc : element index in the lattice

 Global variables:
 none

 Specific functions:
 none

 Comments:

 ****************************************************************************/
long Elem_GetPos(const int Fnum1, const int Knum1) {
    long int loc;

    if (ElemFam[Fnum1 - 1].nKid != 0)
        loc = ElemFam[Fnum1 - 1].KidList[Knum1 - 1];
    else {
        loc = -1;
        printf("Elem_GetPos: there are no kids in family %d (%s)\n", Fnum1,
                ElemFam[Fnum1 - 1].ElemF.PName);
        exit_(0);
    }

    return loc;
}

static double thirdroot(double a) {
    /* By substitution method */
    int i;
    double x;

    x = 1.0;
    i = 0;
    do {
        i++;
        x = (x + a) / (x * x + 1e0);
    } while (i != 250);
    return x;
}

void SI_init(void) {
    /*  c_1 = 1/(2*(2-2^(1/3))),    c_2 = (1-2^(1/3))/(2*(2-2^(1/3)))
     d_1 = 1/(2-2^(1/3)),        d_2 = -2^(1/3)/(2-2^(1/3))                 */

    double C_gamma, C_u;

    c_1 = 1e0 / (2e0 * (2e0 - thirdroot(2e0)));
    c_2 = 0.5e0 - c_1;
    d_1 = 2e0 * c_1;
    d_2 = 1e0 - 2e0 * d_1;

    // classical radiation
    //  C_gamma = 8.846056192e-05;
    // C_gamma = 4 * pi * r_e [m] / ( 3 * (m_e [GeV/c^2] * c^2)^3 )
    C_gamma = 4.0 * M_PI * r_e / (3.0 * cube(1e-9 * m_e));
    // P_gamma = e^2 c^3 / 2 / pi * C_gamma (E [GeV])^2 (B [T])^2
    // p_s = P_s/P, E = P*c, B/(Brho) = p/e
    cl_rad = C_gamma * cube(globval.Energy) / (2.0 * M_PI);

    // eletron rest mass [GeV]: slightly off???
    //  m_e_ = 0.5110034e-03;
    // h_bar times c [GeV m]
    //  hbar_t_c = 1.9732858e-16;
    // quantum fluctuations
    C_u = 55.0 / (24.0 * sqrt(3.0));
    q_fluct = 3.0 * C_u * C_gamma * 1e-9 * h_bar * c0 / (4.0 * M_PI * cube(1e-9
            * m_e)) * pow(globval.Energy, 5.0);
}

static void Mpole_Print(FILE *f, int Fnum1) {
    elemtype *elemp;
    MpoleType *M;

    elemp = &ElemFam[Fnum1 - 1].ElemF;
    M = elemp->M;
    fprintf(f, "Element[%3d ] \n", Fnum1);
    fprintf(f, "   Name: %.*s,  Kind:   mpole,  L=% .8E\n", SymbolLength,
            elemp->PName, elemp->PL);
    fprintf(f, "   Method: %d, N=%4d\n", M->Pmethod, M->PN);
}

/****************************************************************************
 * void Drift_Print(FILE **f, long Fnum1)

 Purpose: called by Elem_Print
 Print out drift characteristics in a file
 Name, kind, length, method, slice number

 Input:
 Fnum1 Family number
 f     pointer on file id

 Output:
 none

 Return:
 none

 Global variables:
 none

 Specific functions:
 none

 Comments:
 none

 ****************************************************************************/
static void Drift_Print(FILE *f, int Fnum1) {
    ElemFamType *elemfamp;
    elemtype *elemp;

    elemfamp = &ElemFam[Fnum1 - 1];
    elemp = &elemfamp->ElemF;
    fprintf(f, "Element[%3d ] \n", Fnum1);
    fprintf(f, "   Name: %.*s,  Kind:   drift,  L=% .8E\n", SymbolLength,
            elemp->PName, elemp->PL);
    fprintf(f, "   nKid:%3d\n\n", elemfamp->nKid);
}

/****************************************************************************
 * void Wiggler_Print(FILE **f, long Fnum1)

 Purpose: called by Elem_Print
 Print out drift characteristics in a file
 Name, kind, length

 Input:
 Fnum1 Family number
 f     pointer on file id

 Output:
 none

 Return:
 none

 Global variables:
 none

 Specific functions:
 none

 Comments:
 none

 ****************************************************************************/
static void Wiggler_Print(FILE *f, int Fnum1) {
    elemtype *elemp;

    elemp = &ElemFam[Fnum1 - 1].ElemF;
    fprintf(f, "Element[%3d ] \n", Fnum1);
    fprintf(f, "   Name: %.*s,  Kind:   wiggler,  L=% .8E\n\n", NameLength,
            elemp->PName, elemp->PL);
}

/****************************************************************************
 * void Insertion_Print(FILE **f, long Fnum1)

 Purpose: called by Elem_Print
 Print out drift characteristics in a file
 Name, kind, length

 Input:
 Fnum1 Family number
 f     pointer on file id

 Output:
 none

 Return:
 none

 Global variables:
 none

 Specific functions:
 none

 Comments:
 none

 ****************************************************************************/
static void Insertion_Print(FILE *f, int Fnum1) {
    elemtype *elemp;

    elemp = &ElemFam[Fnum1 - 1].ElemF;
    fprintf(f, "Element[%3d ] \n", Fnum1);
    fprintf(f, "   Name: %.*s,  Kind:   wiggler,  L=% .8E\n\n", SymbolLength,
            elemp->PName, elemp->PL);
}

/****************************************************************************
 * void Insertion_SetMatrix(long Fnum1, long Knum1)

 Purpose: called by Insertion_Init
 Constructs the linear matrices
 K55 kick matrix for one slice
 D55 drift matrix for one slice
 KD55 full linear transport matrix

 Input:
 Fnum1 Family number
 Knum1 Kid number

 Output:
 none

 Return:
 none

 Global variables:
 globval

 Specific functions:
 LinearInterpDeriv2

 Comments:
 04/07/03 derivative interpolation around closed orbit
 10/01/05 First order kick added

 Need to be checked energy dependence and so on.
 ****************************************************************************/

void Elem_Print(FILE *f, int Fnum1) {
    int i;

    if (Fnum1 == 0) {
        // print all elements
        for (i = 1; i <= globval.Elem_nFam; i++)
            Elem_Print(f, i);
        return;
    }

    switch (ElemFam[Fnum1 - 1].ElemF.Pkind) {
    case drift:
        Drift_Print(f, Fnum1);
        break;

    case Mpole:
        Mpole_Print(f, Fnum1);
        break;
    case Wigl:
        Wiggler_Print(f, Fnum1);
        break;
    case FieldMap:
        break;
    case Insertion:
        Insertion_Print(f, Fnum1);
        break;
    case Cavity:
        break;
    case marker:
        break;
    case Spreader:
        break;
    case Recombiner:
        break;
    case Solenoid:
        break;
    case undef:
        break;
    }
}

double Mpole_GetPB(int Fnum1, int Knum1, int Order);

/****************************************************************************
 * double Elem_GetKval(long Fnum1, long Knum1, long Order)

 Purpose:
 Get K values

 Input:
 Fnum1 Famility number
 Knum1 Kids number
 Order mutipole component 1 for dipole, 2 for quadrupole)

 Output:
 none

 Return:
 0.0 if drift
 integrated field if multipole


 Global variables:
 ElemFam

 Specific functions:
 Mpole_GetPB

 Comments:
 01/02/03 add return = 0 for marker and cavity
 22/04/03 Insertion added

 ****************************************************************************/
double Elem_GetKval(int Fnum1, int Knum1, int Order) {
    double Result = 0.0;
    elemtype *elemp;

    if (Fnum1 > 0) {
        elemp = &Cell[ElemFam[Fnum1 - 1].KidList[Knum1 - 1]].Elem;
        switch (elemp->Pkind) {
        case drift:
            Result = 0.0;
            break;
        case marker:
            Result = 0.0;
            break;
        case Cavity:
            Result = 0.0;
            break;
        case Mpole: /* KL*/
            if (elemp->M->Pthick == thick)
                Result = elemp->PL * Mpole_GetPB(Fnum1, Knum1, Order);
            else
                Result = Mpole_GetPB(Fnum1, Knum1, Order);
            break;
        case Wigl:
            Result
                    = elemp->PL
                            * sqrt(2.0 * Cell[ElemFam[Fnum1 - 1].KidList[Knum1
                                    - 1]].Elem.W->PBW[Order + HOMmax]);
            break;
        case FieldMap:
            Result = 0.0;
            break;
        case Insertion:
            Result = 0.0;
            break;
        case Spreader:
            Result = 0.0;
            break;
        case Recombiner:
            Result = 0.0;
            break;
        case Solenoid:
            Result = 0.0;
            break;
        case undef:
            break;
        }
    } else
        Result = 0.0;

    return Result;
}

#define n               4
void LinsTrans(Matrix &A, Vector &b) {
    int j;
    Vector c;

    CopyVec(n, b, c); /* c=b */
    LinTrans(n, A, c); /* c<-A*c */
    for (j = 0; j < n; j++)
        c[j] += A[j][n] * b[n] + A[n][j];
    CopyVec(n, c, b); /* b=c */
}
#undef n

#define n               4
void MulLsMat(Matrix &A, Matrix &B) {
    int i, k;
    Matrix C;

    CopyMat(n, B, C); /* C<-B */
    MulLMat(n, A, C); /* C<-A*C */
    for (i = 0; i < n; i++) {
        C[i][n] = A[i][n];
        C[n][i] = 0.0;
        for (k = 0; k < n; k++) {
            C[i][n] += A[i][k] * B[k][n];
            C[n][i] += A[i][k] * B[n][k];
        }
    }
    C[n][n] = 1.0;
    CopyMat(n + 1, C, B); /* B<-C */
}
#undef n

/****************************************************************************
 * void Drift_Alloc(elemtype *Elem)

 Purpose:
 Dynamic memory allocation for drift element

 Input:
 Pointer on element

 Output:
 memory  space for drift in Elem->UU.D

 Return:
 none

 Global variables:
 none

 Specific functions:
 none

 Comments:
 none

 ****************************************************************************/
void Drift_Alloc(elemtype *Elem) {
    Elem->D = (DriftType *) malloc(sizeof(DriftType));
}

void Mpole_Alloc(elemtype *Elem) {
    int j;
    MpoleType *M;

    /* Memory allocation */
    Elem->M = (MpoleType *) malloc(sizeof(MpoleType));
    M = Elem->M;
    M->Pmethod = Meth_Fourth;
    M->PN = 0;
    /* Displacement errors */
    for (j = 0; j <= 1; j++) {
        M->PdSsys[j] = 0.0;
        M->PdSrms[j] = 0.0;
        M->PdSrnd[j] = 0.0;
    }
    M->PdTpar = 0.0; /* Roll angle */
    M->PdTsys = 0.0; /* systematic Roll errors */
    M->PdTrms = 0.0; /* random Roll errors */
    M->PdTrnd = 0.0; /* random seed */
    for (j = -HOMmax; j <= HOMmax; j++) {
        /* Initializes multipoles strengths to zero */
        M->PB[j + HOMmax] = 0.0;
        M->PBpar[j + HOMmax] = 0.0;
        M->PBsys[j + HOMmax] = 0.0;
        M->PBrms[j + HOMmax] = 0.0;
        M->PBrnd[j + HOMmax] = 0.0;
    }
    M->Porder = 0;
    M->n_design = 0;
    M->Pirho = 0.0; /* inverse of curvature radius */
    M->PTx1 = 0.0; /* Entrance angle */
    M->PTx2 = 0.0; /* Exit angle */
    M->Pgap = 0.0; /* Gap for fringe field ??? */

    M->Pc0 = 0.0;
    M->Pc1 = 0.0;
    M->Ps1 = 0.0;
    M->quadFF1 = 0L;
    M->quadFF2 = 0L;
    M->sextFF1 = 0L;
    M->sextFF2 = 0L;
    M->quadFFscaling = 0.0;

}

/****************************************************************************
 * void Cav_Alloc(elemtype *Elem)

 Purpose:
 Constructor for a cavity element

 Input:
 none

 Output:
 none

 Return:
 none

 Global variables:
 none

 Specific functions:
 none

 Comments:
 none

 ****************************************************************************/
void Cav_Alloc(elemtype *Elem) {
    CavityType *C;

    Elem->C = (CavityType *) malloc(sizeof(CavityType));
    C = Elem->C;
    C->Pvolt = 0.0;
    C->Pfreq = 0.0;
    C->phi = 0.0;
    C->Ph = 0;
}

void Wiggler_Alloc(elemtype *Elem) {
    int j;
    WigglerType *W;

    Elem->W = (WigglerType *) malloc(sizeof(WigglerType));
    W = Elem->W;
    W->Pmethod = Meth_Linear;
    W->PN = 0;
    for (j = 0; j <= 1; j++) {
        W->PdSsys[j] = 0.0;
        W->PdSrnd[j] = 0.0;
    }
    W->PdTpar = 0.0;
    W->PdTsys = 0.0;
    W->PdTrnd = 0.0;
    W->n_harm = 0;
    for (j = 0; j < n_harm_max; j++) {
        W->BoBrhoV[j] = 0.0;
        W->BoBrhoH[j] = 0.0;
        W->kxV[j] = 0.0;
        W->kxH[j] = 0.0;
        W->lambda = 0.0;
        W->phi[j] = 0.0;
    }
    for (j = 0; j <= HOMmax; j++)
        W->PBW[j + HOMmax] = 0.0;
    W->Porder = 0;
}

void FieldMap_Alloc(elemtype *Elem, const bool alloc_fm) {
    FieldMapType *FM;

    Elem->FM = (FieldMapType *) malloc(sizeof(FieldMapType));
    FM = Elem->FM;
    FM->n_step = 0;
    FM->n[X_] = 0;
    FM->n[Y_] = 0;
    FM->n[Z_] = 0;
    FM->scl = 1.0;

    /*  if (alloc_fm) {
     FM->AxoBrho = matrix(1, m_max_FM, 1, n_max_FM);
     FM->AxoBrho2 = matrix(1, m_max_FM, 1, n_max_FM);
     FM->AyoBrho = matrix(1, m_max_FM, 1, n_max_FM);
     FM->AyoBrho2 = matrix(1, m_max_FM, 1, n_max_FM);

     FM->Bx = matrix(1, m_max_FM, 1, n_max_FM);
     FM->By = matrix(1, m_max_FM, 1, n_max_FM);
     FM->Bz = matrix(1, m_max_FM, 1, n_max_FM);

     FM->x_pos[1] = 1e30; FM->x_pos[FM->m_x] = -1e30;
     FM->y_pos[1] = 1e30; FM->y_pos[FM->m_y] = -1e30;
     FM->s_pos[1] = 1e30; FM->s_pos[FM->n_s] = -1e30;
     }*/

    //  free_vector(FM->x_pos, 1, m_max_FM); free_vector(FM->y_pos, 1, m_max_FM);
    //  free_vector(FM->s_pos, 1, n_max_FM);
    //  free_matrix(FM->AxoBrho, 1, m_max_FM, 1, n_max_FM);
    //  free_matrix(FM->AxoBrho2, 1, m_max_FM, 1, n_max_FM);

    //  free_matrix(Bx, 1, m_max_FM, 1, n_max_FM);
    //  free_matrix(By, 1, m_max_FM, 1, n_max_FM);
    //  free_matrix(Bz, 1, m_max_FM, 1, n_max_FM);
}

/****************************************************************************
 * void Insertion_Alloc(elemtype *Elem, boolean firstflag, boolean secondflag)

 Purpose: called by Insertion_Init and Lat_DealElement
 Dynamic memory allocation for a Insertion element and various
 initializations

 Input:
 Elem Element for memory allocation
 firstflag true if first order kick map to be loaded
 secondflag true if second order kick map to be loaded

 Output:
 none

 Return:
 none

 Global variables:
 none

 Specific functions:
 none

 Comments:
 10/01/05 First order kick part added
 4 November 2010 Splitting 1st and 2nd order X and Z axes

 ****************************************************************************/

void Insertion_Alloc(elemtype *Elem) {
    int i = 0, j = 0;
    InsertionType *ID;

    Elem->ID = (InsertionType *) malloc(sizeof(InsertionType));
    ID = Elem->ID;

    ID->Pmethod = Meth_Linear;
    ID->PN = 0;
    ID->nx1 = 0;
    ID->nz1 = 0;
    ID->nx2 = 0;
    ID->nz2 = 0;

    /* Initialization thetax and thetaz to 0*/

    // first order kick map
    if (ID->firstorder) {
        for (i = 0; i < IDZMAX; i++) {
            for (j = 0; j < IDXMAX; j++) {
                ID->thetax1[i][j] = 0.0;
                ID->thetaz1[i][j] = 0.0;
            }
        }
    }

    // second order kick map
    if (ID->secondorder) {
        for (i = 0; i < IDZMAX; i++) {
            for (j = 0; j < IDXMAX; j++) {
                ID->thetax2[i][j] = 0.0;
                ID->thetaz2[i][j] = 0.0;
            }
        }
    }

    // stuffs for interpolation
    for (j = 0; j < IDXMAX; j++) {
        ID->tabx1[j] = 0.0;
        ID->tabx2[j] = 0.0;
    }

    for (j = 0; j < IDZMAX; j++) {
        ID->tabz1[j] = 0.0;
        ID->tabz2[j] = 0.0;
    }

    // filenames
    strcpy(ID->fname1, "");
    strcpy(ID->fname2, "");

    for (j = 0; j <= 1; j++) {
        ID->PdSsys[j] = 0.0;
        ID->PdSrnd[j] = 0.0;
    }
    ID->PdTpar = 0.0;
    ID->PdTsys = 0.0;
    ID->PdTrnd = 0.0;
    ID->Porder = 0;
}

void Spreader_Alloc(elemtype *Elem) {
    int k;

    Elem->Spr = (SpreaderType *) malloc(sizeof(SpreaderType));

    for (k = 0; k < Spreader_max; k++)
        Elem->Spr->Cell_ptrs[k] = NULL;
}

void Recombiner_Alloc(elemtype *Elem) {
    Elem->Rec = (RecombinerType *) malloc(sizeof(RecombinerType));
}

void Solenoid_Alloc(elemtype *Elem) {
    int j;
    SolenoidType *Sol;

    Elem->Sol = (SolenoidType *) malloc(sizeof(SolenoidType));
    Sol = Elem->Sol;
    Sol->N = 0;
    for (j = 0; j <= 1; j++) {
        Sol->PdSsys[j] = 0.0;
        Sol->PdSrms[j] = 0.0;
        Sol->PdSrnd[j] = 0.0;
    }
    Sol->dTpar = 0.0;
    Sol->dTsys = 0.0;
    Sol->dTrnd = 0.0;
}

/****************************************************************************/
/* void Drift_Init(long Fnum1)

 Purpose:
 Constructor of a drift element
 see comments in  Drift_SetMatrix

 Input:
 Fnum1 Family number

 Output:
 none

 Return:
 none

 Global variables:
 ElemFam
 Cell

 Specific functions:
 Drift_Alloc
 Drift_SetMatrix

 Comments:
 none

 ****************************************************************************/
void Drift_Init(int Fnum1) {
    int i;
    ElemFamType *elemfamp;
    CellType *cellp;

    elemfamp = &ElemFam[Fnum1 - 1];
    for (i = 1; i <= elemfamp->nKid; i++) {
        /* Get in Cell kid # i from Family Fnum1 */
        cellp = &Cell[elemfamp->KidList[i - 1]];
        /* Dynamic memory allocation for element */
        Drift_Alloc(&cellp->Elem);
        /* copy low level routine */
        memcpy(cellp->Elem.PName, elemfamp->ElemF.PName, sizeof(partsName));
        /* Set the drift length */
        cellp->Elem.PL = elemfamp->ElemF.PL;
        /* set the kind of element */
        cellp->Elem.Pkind = elemfamp->ElemF.Pkind;
        /* set pointer for the D dynamic space */
        *cellp->Elem.D = *elemfamp->ElemF.D;
        cellp->dT[0] = 1e0; /* cos = 1 */
        cellp->dT[1] = 0.0; /* sin = 0 */
        cellp->dS[0] = 0.0; /* no H displacement */
        cellp->dS[1] = 0.0; /* no V displacement */
        /* set Drift matrix */
        Drift_SetMatrix(Fnum1, i);
    }
}

static int UpdatePorder(elemtype &Elem) {
    int i, order;
    MpoleType *M;

    M = Elem.M;
    if (M->Pirho != 0.0) /* non zero curvature => bend */
        order = 1;
    else
        /* mutipole */
        order = 0;
    for (i = -HOMmax; i <= HOMmax; i++)
        if (M->PB[i + HOMmax] != 0.0 && abs(i) > order)
            order = abs(i);

    return order;
}

void Mpole_Init(int Fnum1) {
    double x;
    int i;
    ElemFamType *elemfamp;
    CellType *cellp;
    elemtype *elemp;

    /* Pointer on element */
    elemfamp = &ElemFam[Fnum1 - 1];
    memcpy(elemfamp->ElemF.M->PB, elemfamp->ElemF.M->PBpar, sizeof(mpolArray));
    /* Update the right multipole order */
    elemfamp->ElemF.M->Porder = UpdatePorder(elemfamp->ElemF);
    /* Quadrupole strength */
    x = elemfamp->ElemF.M->PBpar[Quad + HOMmax];
    for (i = 1; i <= elemfamp->nKid; i++) {
        cellp = &Cell[elemfamp->KidList[i - 1]];
        /* Memory allocation and set everything to zero */
        Mpole_Alloc(&cellp->Elem);
        memcpy(cellp->Elem.PName, elemfamp->ElemF.PName, sizeof(partsName));
        /* set length */
        cellp->Elem.PL = elemfamp->ElemF.PL;
        /* set element kind (Mpole) */
        cellp->Elem.Pkind = elemfamp->ElemF.Pkind;
        *cellp->Elem.M = *elemfamp->ElemF.M;

        elemp = &cellp->Elem;
        /* set entrance and exit angles */
        cellp->dT[0] = cos(dtor(elemp->M->PdTpar));
        cellp->dT[1] = sin(dtor(elemp->M->PdTpar));

        /* set displacement to zero */
        cellp->dS[0] = 0.0;
        cellp->dS[1] = 0.0;

        if (elemp->PL != 0.0 || elemp->M->Pirho != 0.0) {
            /* Thick element or radius non zero element */
            elemp->M->Pthick = pthicktype(thick);
            /* sin(L*irho/2) =sin(theta/2) half the angle */
            elemp->M->Pc0 = sin(elemp->PL * elemp->M->Pirho / 2e0);
            /* cos roll: sin(theta/2)*cos(dT) */
            elemp->M->Pc1 = cellp->dT[0] * elemp->M->Pc0;
            /* sin roll: sin(theta/2)*cos(dT) */
            elemp->M->Ps1 = cellp->dT[1] * elemp->M->Pc0;
            Mpole_Setmatrix(Fnum1, i, x);
        } else
            /* element as thin lens */
            elemp->M->Pthick = pthicktype(thin);
    }
}

#define order           2
void Wiggler_Init(int Fnum1) {
    int i;
    double x;
    ElemFamType *elemfamp;
    CellType *cellp;
    elemtype *elemp;

    elemfamp = &ElemFam[Fnum1 - 1];
    /* ElemF.M^.PB := ElemF.M^.PBpar; */
    elemfamp->ElemF.W->Porder = order;
    x = elemfamp->ElemF.W->PBW[Quad + HOMmax];
    for (i = 1; i <= elemfamp->nKid; i++) {
        cellp = &Cell[elemfamp->KidList[i - 1]];
        Wiggler_Alloc(&cellp->Elem);
        memcpy(cellp->Elem.PName, elemfamp->ElemF.PName, sizeof(partsName));
        cellp->Elem.PL = elemfamp->ElemF.PL;
        cellp->Elem.Pkind = elemfamp->ElemF.Pkind;
        *cellp->Elem.W = *elemfamp->ElemF.W;

        elemp = &cellp->Elem;
        cellp->dT[0] = cos(dtor(elemp->M->PdTpar));
        cellp->dT[1] = sin(dtor(elemp->M->PdTpar));

        cellp->dS[0] = 0.0;
        cellp->dS[1] = 0.0;
        Wiggler_Setmatrix(Fnum1, i, cellp->Elem.PL, cellp->Elem.W->kxV[0], 2.0
                * M_PI / cellp->Elem.W->lambda, x);
    }
}
#undef order

/*
 void get_Ax(const int m, const int n, float **By, FieldMapType *FM)
 {
 int  j, k;

 const double  Brho = 1e9*globval.Energy/c0;

 FM->m_y = m; FM->n_s = n;

 for (j = 1; j <= m; j++) {
 FM->AxoBrho[j][1] = 0.0;
 for (k = 2; k <= n; k++)
 FM->AxoBrho[j][k] =
 FM->AxoBrho[j][k-1] + By[j][k]*(FM->s_pos[k]-FM->s_pos[k-1])/Brho;
 }

 splie2(FM->y_pos, FM->s_pos, FM->AxoBrho, FM->m_y, FM->n_s, FM->AxoBrho2);
 }


 void get_Ay(const int m, const int n, float **Bx, FieldMapType *FM)
 {
 int  j, k;

 const double  Brho = 1e9*globval.Energy/c0;

 FM->m_x = m; FM->n_s = n;

 for (j = 1; j <= m; j++) {
 FM->AyoBrho[j][1] = 0.0;
 for (k = 2; k <= n; k++)
 FM->AyoBrho[j][k] =
 FM->AyoBrho[j][k-1] - Bx[j][k]*(FM->s_pos[k]-FM->s_pos[k-1])/Brho;
 }

 splie2(FM->x_pos, FM->s_pos, FM->AyoBrho, FM->m_x, FM->n_s, FM->AyoBrho2);
 }
 */

void get_B(const char *file_name, FieldMapType *FM) {
    char line[max_str];
    int i, j, k, l;
    ifstream inf;

    printf("\n");
    printf("reading field map %s\n", file_name);

    file_rd(inf, file_name);

    inf.getline(line, max_str);
    // read number of steps
    sscanf(line, "%d,%d,%d", &FM->n[X_], &FM->n[Y_], &FM->n[Z_]);
    // skip comment
    inf.getline(line, max_str);

    i = 1;
    j = 0;
    k = 1;
    while (inf.getline(line, max_str) != NULL) {
        j++;
        if (j > FM->n[Y_]) {
            k++;
            j = 1;
        }
        if (k > FM->n[Z_]) {
            i++;
            k = 1;
        }

        if ((i > i_max_FM) || (j > j_max_FM) || (k > k_max_FM)) {
            printf("get_B: max index exceeded %d %d %d (%d %d %d)\n", i, j, k,
                    i_max_FM, j_max_FM, k_max_FM);
            exit_(1);
        }

        sscanf(line, "%lf,%lf,%lf,%lf,%lf,%lf", &FM->xyz[X_][i - 1][j - 1][k
                - 1], &FM->xyz[Y_][i - 1][j - 1][k - 1], &FM->xyz[Z_][i - 1][j
                - 1][k - 1], &FM->B[X_][i - 1][j - 1][k - 1],
                &FM->B[Y_][i - 1][j - 1][k - 1],
                &FM->B[Z_][i - 1][j - 1][k - 1]);
        for (l = 0; l < 3; l++)
            FM->xyz[l][i - 1][j - 1][k - 1] *= 1e-3;

    }

    printf("no of steps: n_x = %d, n_y = %d, n_z = %d\n", FM->n[X_], FM->n[Y_],
            FM->n[Z_]);

    //  get_Ay(m, n, FM->Bx, FM); prt_Bx(FM);
}

void FieldMap_Init(int Fnum1) {
    int i;
    ElemFamType *elemfamp;
    CellType *cellp;
    elemtype *elemp;

    elemfamp = &ElemFam[Fnum1 - 1];
    for (i = 1; i <= elemfamp->nKid; i++) {
        cellp = &Cell[elemfamp->KidList[i - 1]];
        FieldMap_Alloc(&cellp->Elem, false);
        memcpy(cellp->Elem.PName, elemfamp->ElemF.PName, sizeof(partsName));
        cellp->Elem.PL = elemfamp->ElemF.PL;
        cellp->Elem.Pkind = elemfamp->ElemF.Pkind;
        *cellp->Elem.FM = *elemfamp->ElemF.FM;

        elemp = &cellp->Elem;
        cellp->dT[0] = 1.0;
        cellp->dT[1] = 0.0;
        cellp->dS[X_] = 0.0;
        cellp->dS[Y_] = 0.0;
    }
}

/****************************************************************************
 * void Cav_Init(long Fnum1)

 Purpose: called by Cell_Init()
 Constructor for a cavity
 set the RF voltage, frequency read from the lattice file

 Input:
 Fnum1 Family number

 Output:
 none

 Return:
 none

 Global variables:
 ElemFam, Cell

 Specific functions:
 none

 Comments:
 none

 ****************************************************************************/
void Cav_Init(int Fnum1) {
    int i;
    ElemFamType *elemfamp;
    elemtype *elemp;
    CellType *cellp;

    elemfamp = &ElemFam[Fnum1 - 1];
    elemp = &elemfamp->ElemF;
    for (i = 0; i < elemfamp->nKid; i++) {
        cellp = &Cell[elemfamp->KidList[i]];
        cellp->Elem = elemfamp->ElemF;
    }
}

void Marker_Init(int Fnum1) {
    int i;
    ElemFamType *elemfamp;
    elemtype *elemp;
    CellType *cellp;

    elemfamp = &ElemFam[Fnum1 - 1];
    elemp = &elemfamp->ElemF;
    for (i = 0; i < elemfamp->nKid; i++) {
        cellp = &Cell[elemfamp->KidList[i]];
        cellp->Elem = elemfamp->ElemF;
        cellp->dT[0] = 1.0;
        cellp->dT[1] = 0.0;
        cellp->dS[0] = 0.0;
        cellp->dS[1] = 0.0;
    }
}

/****************************************************************************
 *                              INSERTION                                   *
 ****************************************************************************/

/****************************************************************************
 * void Insertion_Init(long Fnum1)

 Purpose: called by Cell_Init
 Initializes the insertion
 Fills in all the parameters read in the RADIA file
 Constructs the linear matrix

 Input:
 Fnum1: family number

 Output:
 none

 Return:
 none

 Global variables:
 none

 Specific functions:
 none

 Comments:
 none

 ****************************************************************************/

void Insertion_Init(int Fnum1) {
    int i;
    ElemFamType *elemfamp;
    CellType *cellp;
    elemtype *elemp;

    elemfamp = &ElemFam[Fnum1 - 1];
    //  elemfamp->ElemF.ID->Porder = order;
    //  x = elemfamp->ElemF.ID->PBW[Quad + HOMmax];
    for (i = 1; i <= elemfamp->nKid; i++) {
        cellp = &Cell[elemfamp->KidList[i - 1]];
        Insertion_Alloc(&cellp->Elem);
        memcpy(cellp->Elem.PName, elemfamp->ElemF.PName, sizeof(partsName));
        cellp->Elem.PL = elemfamp->ElemF.PL;
        cellp->Elem.Pkind = elemfamp->ElemF.Pkind;
        *cellp->Elem.ID = *elemfamp->ElemF.ID;

        elemp = &cellp->Elem;

        cellp->dT[0] = cos(dtor(elemp->ID->PdTpar));
        cellp->dT[1] = sin(dtor(elemp->ID->PdTpar));
        cellp->dS[0] = 0.0;
        cellp->dS[1] = 0.0;

        Insertion_SetMatrix(Fnum1, i);
    }
}

void Spreader_Init(int Fnum1) {
    int i;
    ElemFamType *elemfamp;
    CellType *cellp;

    elemfamp = &ElemFam[Fnum1 - 1];
    for (i = 1; i <= elemfamp->nKid; i++) {
        /* Get in Cell kid # i from Family Fnum1 */
        cellp = &Cell[elemfamp->KidList[i - 1]];
        /* Dynamic memory allocation for element */
        Spreader_Alloc(&cellp->Elem);
        /* copy low level routine */
        memcpy(cellp->Elem.PName, elemfamp->ElemF.PName, sizeof(partsName));
        /* set the kind of element */
        cellp->Elem.Pkind = elemfamp->ElemF.Pkind;
        /* set pointer for the dynamic space */
        *cellp->Elem.Spr = *elemfamp->ElemF.Spr;
        cellp->dT[0] = 1e0; /* cos = 1 */
        cellp->dT[1] = 0.0; /* sin = 0 */
        cellp->dS[0] = 0.0; /* no H displacement */
        cellp->dS[1] = 0.0; /* no V displacement */
    }
}

void Recombiner_Init(int Fnum1) {
    int i;
    ElemFamType *elemfamp;
    CellType *cellp;

    elemfamp = &ElemFam[Fnum1 - 1];
    for (i = 1; i <= elemfamp->nKid; i++) {
        /* Get in Cell kid # i from Family Fnum1 */
        cellp = &Cell[elemfamp->KidList[i - 1]];
        /* Dynamic memory allocation for element */
        Spreader_Alloc(&cellp->Elem);
        /* copy low level routine */
        memcpy(cellp->Elem.PName, elemfamp->ElemF.PName, sizeof(partsName));
        /* set the kind of element */
        cellp->Elem.Pkind = elemfamp->ElemF.Pkind;
        /* set pointer for the dynamic space */
        *cellp->Elem.Rec = *elemfamp->ElemF.Rec;
        cellp->dT[0] = 1e0; /* cos = 1 */
        cellp->dT[1] = 0.0; /* sin = 0 */
        cellp->dS[0] = 0.0; /* no H displacement */
        cellp->dS[1] = 0.0; /* no V displacement */
    }
}

void Solenoid_Init(int Fnum1) {
    int i;
    ElemFamType *elemfamp;
    CellType *cellp;
    elemtype *elemp;

    /* Pointer on element */
    elemfamp = &ElemFam[Fnum1 - 1];
    for (i = 1; i <= elemfamp->nKid; i++) {
        cellp = &Cell[elemfamp->KidList[i - 1]];
        /* Memory allocation and set everything to zero */
        Solenoid_Alloc(&cellp->Elem);
        memcpy(cellp->Elem.PName, elemfamp->ElemF.PName, sizeof(partsName));
        /* set length */
        cellp->Elem.PL = elemfamp->ElemF.PL;
        /* set element kind */
        cellp->Elem.Pkind = elemfamp->ElemF.Pkind;
        *cellp->Elem.Sol = *elemfamp->ElemF.Sol;

        elemp = &cellp->Elem;
        /* set entrance and exit angles */
        cellp->dT[0] = 1.0;
        cellp->dT[1] = 0.0;

        /* set displacement to zero */
        cellp->dS[0] = 0.0;
        cellp->dS[1] = 0.0;
    }
}

/**************************************************************************************
 void Mpole_SetPB(int Fnum1, int Knum1, int Order)

 Purpose:
 called by Cell_SetdP
 Update full multipole composent as sum of design, systematic
 and random part; and update the maximum order of the multipole 
 component p_order.
 The ramdom error is the multiplication of PBrms and PBrnd
 Compute transport matrix if quadrupole (Order=2)
 Set multipole order to Order if multipole (Order >2)

 Input:
 Fnum1        family name
 Knum1        kid number
 Order        maximum order of the multipole

 Output:
 None

 Return:
 None

 Gloval variables:
 None

 Specific functions:

 Comments:
 None

 **************************************************************************************/
void Mpole_SetPB(int Fnum1, int Knum1, int Order) {
    /*               */

    CellType *cellp; /* pointer on the Cell */
    elemtype *elemp; /* pointer on the Elemetype */
    MpoleType *M;/* Pointer on the Multipole */

    cellp = &Cell[ElemFam[Fnum1 - 1].KidList[Knum1 - 1]];
    elemp = &cellp->Elem;
    M = elemp->M;
    M->PB[Order + HOMmax] = M->PBpar[Order + HOMmax] + M->PBsys[Order + HOMmax]
            + M->PBrms[Order + HOMmax] * M->PBrnd[Order + HOMmax];
    if (abs(Order) > M->Porder && M->PB[Order + HOMmax] != 0.0)
        M->Porder = abs(Order);
    if (M->Pmethod == Meth_Linear && Order == 2L)
        Mpole_Setmatrix(Fnum1, Knum1, M->PB[Order + HOMmax]);
    cellconcat = false;
}

/**************************************************************************************
 double Mpole_GetPB(int Fnum1, int Knum1, int Order)

 Purpose:
 Return multipole strength (of order Order) for Knum1 element of
 family Fnum1
 Order =  2 for normal quadrupole, bn components
 = -2 for skew quadrupole    an components

 Input:
 Fnum1        family name
 Knum1        kid number
 Order        order of the multipole

 Output:
 None

 Return:
 None

 Gloval variables:
 None

 Specific functions:

 Comments:
 None

 **************************************************************************************/
double Mpole_GetPB(int Fnum1, int Knum1, int Order) {

    MpoleType *M; /* Pointer on the multipole */

    M = Cell[ElemFam[Fnum1 - 1].KidList[Knum1 - 1]].Elem.M;
    return (M->PB[Order + HOMmax]);
}

void Mpole_DefPBpar(int Fnum1, int Knum1, int Order, double PBpar) {
    elemtype *elemp;
    MpoleType *M;

    elemp = &Cell[ElemFam[Fnum1 - 1].KidList[Knum1 - 1]].Elem;
    M = elemp->M;

    M->PBpar[Order + HOMmax] = PBpar;
}


void Mpole_DefPBsys(int Fnum1, int Knum1, int Order, double PBsys) {
    /*Fnum1, Knum1, Order : integer*/
    elemtype *elemp;
    MpoleType *M;

    elemp = &Cell[ElemFam[Fnum1 - 1].KidList[Knum1 - 1]].Elem;
    M = elemp->M;

    M->PBsys[Order + HOMmax] = PBsys;
}
/*********************************************************************
void Mpole_SetdS(int Fnum1, int Knum1)
		       
  Purpose:
     Set misalignment error to the element with Fnum and Knum 
  
  Input:   
     Fnum1          family number
     Knum1          kid number
    
     
**********************************************************************/
void Mpole_SetdS(int Fnum1, int Knum1) {
    int j;
    CellType *cellp;
    elemtype *elemp;
    MpoleType *M;

    cellp = &Cell[ElemFam[Fnum1 - 1].KidList[Knum1 - 1]];
    elemp = &cellp->Elem;
    M = elemp->M;
    for (j = 0; j <= 1; j++)
        cellp->dS[j] = M->PdSsys[j] + M->PdSrms[j] * M->PdSrnd[j];
    cellconcat = false;
}

/*********************************************************************
void Mpole_SetdT(int Fnum1, int Knum1)
		       
  Purpose:
     Set rotation error to the element with Fnum and Knum 
  
  Input:   
     Fnum1          family number
     Knum1          kid number
    
     
**********************************************************************/
void Mpole_SetdT(int Fnum1, int Knum1) {
    CellType *cellp;
    elemtype *elemp;
    MpoleType *M;

    cellp = &Cell[ElemFam[Fnum1 - 1].KidList[Knum1 - 1]];
    elemp = &cellp->Elem;
    M = elemp->M;
    cellp->dT[0] = cos(dtor(M->PdTpar + M->PdTsys + M->PdTrms * M->PdTrnd));
    cellp->dT[1] = sin(dtor(M->PdTpar + M->PdTsys + M->PdTrms * M->PdTrnd));
    /* Calculate simplified p_rots */
    M->Pc0 = sin(elemp->PL * M->Pirho / 2e0);
    M->Pc1 = cos(dtor(M->PdTpar)) * M->Pc0;
    M->Ps1 = sin(dtor(M->PdTpar)) * M->Pc0;
    cellconcat = false;
}

/****************************************************************************/
/* double Mpole_GetdT(long Fnum1, long Knum1)

 Purpose:
 Return total roll angle of the element
 Cell[ElemFam[Fnum1 - 1].KidList[Knum1 - 1]].Elem, which is
 a sum of a design ,a systematic error and a random error part.


 Input:
 none

 Output:
 none

 Return:
 none

 Global variables:
 none

 Specific functions:
 none

 Comments:
 none

 ****************************************************************************/
double Mpole_GetdT(int Fnum1, int Knum1) {
    elemtype *elemp;
    MpoleType *M;

    elemp = &Cell[ElemFam[Fnum1 - 1].KidList[Knum1 - 1]].Elem;
    M = elemp->M;

    return (M->PdTpar + M->PdTsys + M->PdTrms * M->PdTrnd);
}

/****************************************************************************
 * void Mpole_DefdTpar(long Fnum1, long Knum1, double PdTpar)

 Purpose:
 Set design roll angle to {\ttfamily PdTpar} degrees.

 Input:
 none

 Output:
 none

 Return:
 none

 Global variables:
 none

 Specific functions:
 none

 Comments:
 none

 ****************************************************************************/
void Mpole_DefdTpar(int Fnum1, int Knum1, double PdTpar) {
    elemtype *elemp;
    MpoleType *M;

    elemp = &Cell[ElemFam[Fnum1 - 1].KidList[Knum1 - 1]].Elem;
    M = elemp->M;

    M->PdTpar = PdTpar;
}

/****************************************************************************
 * void Mpole_DefdTsys(long Fnum1, long Knum1, double PdTsys)

 Purpose:
 Set systematic roll angle error to {\ttfamily PdTsys} degrees.

 Input:
 none

 Output:
 none

 Return:
 none

 Global variables:
 none

 Specific functions:
 none

 Comments:
 none

 ****************************************************************************/
void Mpole_DefdTsys(int Fnum1, int Knum1, double PdTsys) {
    elemtype *elemp;
    MpoleType *M;

    elemp = &Cell[ElemFam[Fnum1 - 1].KidList[Knum1 - 1]].Elem;
    M = elemp->M;

    M->PdTsys = PdTsys;
}

void Wiggler_SetPB(int Fnum1, int Knum1, int Order) {
    CellType *cellp;
    elemtype *elemp;
    WigglerType *W;

    cellp = &Cell[ElemFam[Fnum1 - 1].KidList[Knum1 - 1]];
    elemp = &cellp->Elem;
    W = elemp->W;
    if (abs(Order) > W->Porder)
        W->Porder = abs(Order);
    if (W->Pmethod == Meth_Linear && Order == 2)
        Wiggler_Setmatrix(Fnum1, Knum1, elemp->PL, W->kxV[0], 2.0 * M_PI
                / cellp->Elem.W->lambda, W->PBW[Order + HOMmax]);
    cellconcat = false;
}

void Wiggler_SetdS(int Fnum1, int Knum1) {
    int j;
    CellType *cellp;
    elemtype *elemp;
    WigglerType *W;

    cellp = &Cell[ElemFam[Fnum1 - 1].KidList[Knum1 - 1]];
    elemp = &cellp->Elem;
    W = elemp->W;
    for (j = 0; j <= 1; j++)
        cellp->dS[j] = W->PdSsys[j] + W->PdSrms[j] * W->PdSrnd[j];
    cellconcat = false;
    if (W->Pmethod == Meth_Linear)
        Wiggler_Setmatrix(Fnum1, Knum1, elemp->PL, W->kxV[0], 2.0 * M_PI
                / cellp->Elem.W->lambda, W->PBW[Quad + HOMmax]);
    cellconcat = false;
}

void Wiggler_SetdT(int Fnum1, int Knum1) {
    CellType *cellp;
    elemtype *elemp;
    WigglerType *W;

    cellp = &Cell[ElemFam[Fnum1 - 1].KidList[Knum1 - 1]];
    elemp = &cellp->Elem;
    W = elemp->W;
    cellp->dT[0] = cos(dtor(W->PdTpar + W->PdTsys + W->PdTrms * W->PdTrnd));
    cellp->dT[1] = sin(dtor(W->PdTpar + W->PdTsys + W->PdTrms * W->PdTrnd));
    if (W->Pmethod == Meth_Linear)
        Wiggler_Setmatrix(Fnum1, Knum1, elemp->PL, W->kxV[0], 2.0 * M_PI
                / cellp->Elem.W->lambda, W->PBW[Quad + HOMmax]);
    cellconcat = false;
}
