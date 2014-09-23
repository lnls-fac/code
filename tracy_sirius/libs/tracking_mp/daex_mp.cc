// DAEX_MP
// =======
// Rotina que paraleliza o cálculo de abertura dinâmica 'daex'
//
// 2014-06-16	Ximenes R. Resende


#include "daex_mp.h"

static double  daex_mp_z0;
static int     daex_mp_nturn;

void tracking_mp_daex(int cpu_id, int data_id, void *data_in, void *shm_data_out);


void daex_mp(int nr_cpus, long Nbx, long Nbe, long Nbtour, double e0, double emax, double x0, double xmax, double z0) {

	double tiny_amp = 1e-6;  // meters

	int    nr_pnts;
	double *points;
	double *result;
	const char fic[] = "daex.out";
	long   lastpos;

	nr_pnts = Nbx * Nbe;

	points = (double*) malloc (2 * nr_pnts * sizeof(double));

   	/* Get closed orbit */
    getcod(0.0, lastpos);

	int k = 0;
	for(int i=0; i<Nbe; ++i) {
		double e = e0 + i * (emax - e0) / (Nbe - 1.0);
		for(int j=0; j<Nbx; ++j) {
		    double x = x0 + j * (xmax - x0) / (Nbx - 1.0);
			if (fabs(x) < tiny_amp) { x = tiny_amp; }
			points[2*k+0] = e;
			points[2*k+1] = x;
			k++;
		}
	}
	
	result = (double*) malloc (2 * nr_pnts * sizeof(double));

	daex_mp_z0        = z0;
	daex_mp_nturn     = Nbtour;
	mp_task_mgr(nr_cpus, nr_pnts, (void*) points, (void*) result, 2*nr_pnts*sizeof(double), tracking_mp_daex);


	// salva resultado em arquivo
	FILE * outf;
	/* Opening file */
	if ((outf = fopen(fic, "w")) == NULL) {
		fprintf(stdout, "daex: error while opening file %s\n", fic);
		exit(1);
	}
	
	fprintf(outf,  "# TRACY III SYNCHROTRON LNLS -- %s -- %s\n", fic, "");
	fprintf(outf,  "#     dp               x                 plane_lost         turn_lost     s_lost\n");
	fprintf(outf,  "#    [%%]             [m]         (-1=not_lost, 0=lost)         #           [m]\n");
   	fprintf(stdout,"# TRACY III SYNCHROTRON LNLS -- %s -- %s\n", fic, "");
	fprintf(stdout,"#     dp               x                 plane_lost         turn_lost     s_lost\n");
	fprintf(stdout,"#    [%%]             [m]         (-1=not_lost, 0=lost)         #           [m]\n");

	k = 0;
	for(int i=0; i<Nbe; ++i) {
	    for(int j=0; j<Nbx; ++j) {
		    k = Nbx*i + j;
			double e = points[2*k+0];
			double x = points[2*k+1];
			int lost_turn = (int) result[2*k+0];
			int lost_idx  = (int) result[2*k+1];
            if ((lost_turn == Nbtour) && (lost_idx == globval.Cell_nLoc)){
			    fprintf(outf,  "%-15.6e %-15.6e %12d %22d %15.5f \n", e, x, -1, lost_turn, Cell[lost_idx].S);
			    fprintf(stdout,"%-15.6e %-15.6e %12d %22d %15.5f \n", e, x, -1, lost_turn, Cell[lost_idx].S);
			}else{
			    fprintf(outf,  "%-15.6e %-15.6e %12d %22d %15.5f \n", e, x, 0, lost_turn, Cell[lost_idx].S);
			    fprintf(stdout,"%-15.6e %-15.6e %12d %22d %15.5f \n", e, x, 0, lost_turn, Cell[lost_idx].S);
			    
			}
		}
	}
	fclose(outf);
	free(points);
	free(result);

}


void tracking_mp_daex(int cpu_id, int data_id, void *data_in, void *shm_data_out) {

    double e = ((double*)data_in)[data_id * 2 + 0];
	double x = ((double*)data_in)[data_id * 2 + 1];
	double z0 = daex_mp_z0;
	int    Nbtour = daex_mp_nturn;
    long   lost_turn, lost_idx;

    Trac_COD(x, 0.0, z0, 0.0, e, 0.0, Nbtour, lost_turn, lost_idx);
    
    ((double*)shm_data_out)[2*data_id + 0] = (double) lost_turn;
	((double*)shm_data_out)[2*data_id + 1] = (double) lost_idx;
	
	printf("<daex_mp: cpu %i, data %i> %10.6e %10.6e\n", cpu_id, data_id, e, x);

}



	
