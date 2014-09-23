import math
from fieldmaptrack import fieldmap
import numpy as np

class Trajectory:
    
    def __init__(self,
                 beam,
                 fieldmap):
        
        self.beam     = beam
        self.fieldmap = fieldmap
        
    def calc_trajectory(self, 
                        init_rx, init_ry, init_rz,
                        init_px, init_py, init_pz,
                        s_length, 
                        s_nrpts,
                        force_midplane = False):
    
        # numerical integration (1st-order simple RK lagorithm) of the beam trajectory
        # (no approximation of the eqs of motion)
        #
        
        self.init_rx, self.init_ry, self.init_rz = init_rx, init_ry, init_rz
        self.init_px, self.init_py, self.init_pz = init_px, init_py, init_pz
        self.s_length = s_length
        self.s_nrpts = s_nrpts
        self.force_midplane = force_midplane
        self.rx, self.ry, self.rz = np.zeros(s_nrpts), np.zeros(s_nrpts), np.zeros(s_nrpts)
        self.px, self.py, self.pz = np.zeros(s_nrpts), np.zeros(s_nrpts), np.zeros(s_nrpts)
        self.s = np.zeros(s_nrpts)
        alpha = 1.0/(1000.0*self.beam.brho)/self.beam.beta
        
        rx,ry,rz = init_rx, init_ry, init_rz
        px,py,pz = init_px, init_py, init_pz
        s, s_step = 0, s_length / (self.s_nrpts - 1.0)
        for i in range(self.s_nrpts):
            try:
                bx,by,bz = self.fieldmap.interpolate(rx,ry,rz)
            except fieldmap.OutOfRangeRy:
                    bx,by,bz = 0.0,0.0,0.0
                    print('extrapolation at ' + str((rx,ry,rz)))
            drx_ds = px
            dry_ds = py
            drz_ds = pz
            dpx_ds = - alpha * (py * bz - pz * by)
            dpy_ds = - alpha * (pz * bx - px * bz)
            dpz_ds = - alpha * (px * by - py * bx)
            rx += drx_ds * s_step
            ry += dry_ds * s_step
            rz += drz_ds * s_step
            px += dpx_ds * s_step
            py += dpy_ds * s_step
            pz += dpz_ds * s_step
            if self.force_midplane:
                ry, py = 0.0,0.0
            
            self.rx[i], self.ry[i], self.rz[i] = rx, ry, rz
            self.px[i], self.py[i], self.pz[i] = px, py, pz
            self.s[i] = s
            
            s += s_step
            
        # calcs deflection angle along trajectory
        self.theta_x = np.arctan(self.rx/self.rz)
        
        # interpolates field on trajectory
        self.bx = np.zeros(self.s.shape)
        self.by = np.zeros(self.s.shape)
        self.bz = np.zeros(self.s.shape)
        for i in range(len(self.s)):
            self.bx[i], self.by[i], self.bz[i] = self.fieldmap.interpolate(self.rx[i], self.ry[i], self.rz[i])
        
    
    def __str__(self):
        
        bx,by,bz = [abs(x) for x in self.bx], [abs(x) for x in self.by], [abs(x) for x in self.bz]
        max_bx, max_by, max_bz = max(bx), max(by), max(bz)
        s_max_bx, s_max_by, s_max_bz = self.s[bx.index(max_bx)], self.s[by.index(max_by)], self.s[bz.index(max_bz)] 
        
        r  = ''
        r += '{0:<35s} {1} deg.'.format('deflection_angle:', abs((180.0/math.pi)*self.theta_x[-1]))
        r += '\n{0:<35s} {1} mm'.format('rk_s_length:', self.s_length)
        r += '\n{0:<35s} {1}'.format('rk_s_nrpts:', self.s_nrpts)
        r += '\n{0:<35s} {1} mm'.format('rk_s_step:', self.s_length/(self.s_nrpts-1)) 
        r += '\n{0:35s} {1:+f} Tesla at rz = {2} mm'.format('max_abs_bx@trajectory:', self.bx[max_bx], s_max_bx)
        r += '\n{0:35s} {1:+f} Tesla at rz = {2} mm'.format('max_abs_by@trajectory:', self.by[max_by], s_max_by)
        r += '\n{0:35s} {1:+f} Tesla at rz = {2} mm'.format('max_abs_bz@trajectory:', self.bz[max_bz], s_max_bz)
    
        return r