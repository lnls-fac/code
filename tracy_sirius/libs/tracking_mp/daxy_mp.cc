// DAXY_MP
// =======
// Rotina que paraleliza o cálculo de abertura dinâmica 'daxy'
//
// 2014-06-16	Ximenes R. Resende


#include "daxy_mp.h"

static double  daxy_mp_energy;
static int     daxy_mp_nturn;

void tracking_mp_daxy(int cpu_id, int data_id, void *data_in, void *shm_data_out);

void daxy_mp(int nr_cpus, long Nbx, long Nbz, long Nbtour, double x0, double xmax,
		  double z0, double zmax, double energy)
{

	double tiny_amp = 1e-6;  // meters

	int    nr_pnts;
	double *points;
	double *result;
	const char fic[] = "daxy.out";
	long   lastpos;

	nr_pnts = Nbx * Nbz;

	points = (double*) malloc (2 * nr_pnts * sizeof(double));

   	/* Get closed orbit */
    getcod(0.0, lastpos);

	int k = 0;
	for(int i=0; i<Nbx; ++i) {
		double x = x0 + i * (xmax - x0) / (Nbx - 1);
		if (fabs(x) < tiny_amp) { x = tiny_amp; }
		for(int j=0; j<Nbz; ++j) {
			double z = z0 + j * (zmax - z0) / (Nbz - 1);
			if (fabs(z) < tiny_amp) { z = tiny_amp; }
			points[2*k+0] = x;
			points[2*k+1] = z;
			k++;
		}
	}

	result = (double*) malloc (2 * nr_pnts * sizeof(double));

	daxy_mp_energy    = energy;
	daxy_mp_nturn     = Nbtour;
	mp_task_mgr(nr_cpus, nr_pnts, (void*) points, (void*) result, 2*nr_pnts*sizeof(double), tracking_mp_daxy);

	// salva resultado em arquivo
	FILE * outf;
	/* Opening file */
	if ((outf = fopen(fic, "w")) == NULL) {
		fprintf(stdout, "daxy: error while opening file %s\n", fic);
		exit(1);
	}
	
	fprintf(outf,   "# TRACY III SYNCHROTRON LNLS -- %s -- %s\n", fic, "");
	fprintf(outf,   "#     x               y                 lost               turn_lost     s_lost\n");
	fprintf(outf,   "#    [m]             [m]         (-1=not_lost, 0=lost)         #           [m]\n");
    fprintf(stdout, "# TRACY III SYNCHROTRON LNLS -- %s -- %s\n", fic, "");
	fprintf(stdout, "#     x               y                 lost               turn_lost     s_lost\n");
	fprintf(stdout, "#    [m]             [m]         (-1=not_lost, 0=lost)         #           [m]\n");
	
	k = 0;
	for(int i=0; i<Nbx; ++i) {
		for(int j=Nbz-1; j>=0; --j) {
		    k = Nbz*i + j;
			double x = points[2*k+0];
			double z = points[2*k+1];
			int lost_turn = (int) result[2*k+0];
			int lost_idx  = (int) result[2*k+1];
            if ((lost_turn == Nbtour) && (lost_idx == globval.Cell_nLoc)){
			    fprintf(outf,   "%-15.6e %-15.6e %12d %22d %15.5f \n", x, z, -1, lost_turn, Cell[lost_idx].S);
			    fprintf(stdout, "%-15.6e %-15.6e %12d %22d %15.5f \n", x, z, -1, lost_turn, Cell[lost_idx].S);

			} else {
			    fprintf(outf,   "%-15.6e %-15.6e %12d %22d %15.5f \n", x, z, 0, lost_turn, Cell[lost_idx].S);
			    fprintf(stdout, "%-15.6e %-15.6e %12d %22d %15.5f \n", x, z, 0, lost_turn, Cell[lost_idx].S);
			}
		}
	}
	fclose(outf);
	free(points);
	free(result);

}


void tracking_mp_daxy(int cpu_id, int data_id, void *data_in, void *shm_data_out) {

    double x = ((double*)data_in)[data_id * 2 + 0];
	double z = ((double*)data_in)[data_id * 2 + 1];
	double energy = daxy_mp_energy;
	int    Nbtour = daxy_mp_nturn;
    long   lost_turn, lost_idx;

    Trac_COD(x, 0.0, z, 0.0, energy, 0.0, Nbtour, lost_turn, lost_idx);
    
    ((double*)shm_data_out)[2*data_id + 0] = (double) lost_turn;
	((double*)shm_data_out)[2*data_id + 1] = (double) lost_idx;
	
	printf("<daxy_mp: cpu %i, data %i> %10.6e %10.6e\n", cpu_id, data_id, x, z);

}



	
