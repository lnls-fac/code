import fieldmaptrack as fmt
import sirius
import numpy as np
import math
import copy

mm = 1.0
mrad = 0.001

# initial conditions perpendicular to trajectory
s_length = 1026   * mm
drx      = 1 * 7.5747 * mm
dpx      = 1 * 2.6379 * mrad
half_dipole_length = 1150.0/2.0

# loads dipole fieldmap
fname = sirius.data_folder + 'sirius/bo/magnet_modelling/b/fieldmaps/' + '2014-09-18_Dipolo_Booster_BD_Modelo_6_-80_35mm_-1000_1000mm.txt' 
fmap = fmt.FieldMap(fname)

# calcs initial trajectory from center
beam = fmt.Beam(energy=3.0)
ref_traj = fmt.Trajectory(beam=beam, fieldmap=fmap)

# centralizes trajectory in good-field region
init_rx, init_ry, init_rz = 17.1806870213, 0.0, 0.0
init_px, init_py, init_pz = 0.0, 0.0, 1.0                     
while True:
    ref_traj.calc_trajectory(init_rx=init_rx, init_ry=init_ry, init_rz=init_rz,   
                             init_px=init_px, init_py=init_py, init_pz=init_pz, 
                             s_step         = 1.0, 
                             s_length       = s_length, 
                             force_midplane = True) 
    traj_sagitta = ref_traj.calc_sagitta(half_dipole_length)
    new_init_rx = traj_sagitta / 2.0
    change_init_rx = new_init_rx - init_rx
    if abs(change_init_rx) < 0.001:
        break
    else:
        init_rx = new_init_rx
angle = (180.0/math.pi) * math.atan(ref_traj.px[-1]/ref_traj.pz[-1])
print('sagitta: ' + str(traj_sagitta) + ' mm')
print('angle:   ' + str(angle))

# reflection of trajectory to rz < 0
ref_traj.s  = np.concatenate((-1.0*ref_traj.s[::-1], ref_traj.s))
ref_traj.rx = np.concatenate((ref_traj.rx[::-1], ref_traj.rx))
ref_traj.ry = np.concatenate((ref_traj.ry[::-1], ref_traj.ry))
ref_traj.rz = np.concatenate((-1.0*ref_traj.rz[::-1], ref_traj.rz))
ref_traj.px = np.concatenate((-1.0*ref_traj.px[::-1], ref_traj.px))
ref_traj.py = np.concatenate((ref_traj.py[::-1], ref_traj.py))
ref_traj.pz = np.concatenate((ref_traj.pz[::-1], ref_traj.pz))

# calcs initial condition
csys = fmt.SerretFrenetCoordSystem(ref_traj, 0)
init_point = csys.get_transverse_line([drx])
init_rx, init_ry, init_rz = init_point[0,0], init_point[1,0], init_point[2,0]
p_init = np.array([csys.t[0] + dpx, csys.t[1], csys.t[2]]) 
p_init /= math.sqrt(np.sum(p_init**2))
init_px, init_py, init_pz = p_init[0], p_init[1], p_init[2]

# calcs kicked trajectory 
traj = fmt.Trajectory(beam=beam, fieldmap=fmap)
traj.calc_trajectory(init_rx=init_rx, init_ry=init_ry, init_rz=init_rz,
                     init_px=init_px, init_py=init_py, init_pz=init_pz,
                     s_length=2*s_length, s_step=1.0,
                     force_midplane = True)

# calcs extraction trajectory with respect to reference trajectory 
s, drx, dpx = [], [], []
for i in range(len(ref_traj.s)):
    csys = fmt.SerretFrenetCoordSystem(ref_traj, i)
    idx, ds, dx = traj.find_intersection_point(csys) 
    if idx is not None:
        dp = traj.px[idx] + ds * (traj.px[idx+1] - traj.px[idx]) - ref_traj.px[i]
        s.append(ref_traj.s[i])
        drx.append(dx)
        dpx.append(dp)

# saves trajectory to file
fp = open('extraction_trajectory.txt','w')
fp.write('{0:^15s} {1:^15s} {2:^15s}\n'.format('s[mm]', 'drx[mm]', 'dpx[mrad]'))
for i in range(len(s)):
    fp.write('{0:^+15.4E} {1:^+15.4E} {2:^+15.4E}\n'.format(s[i], drx[i], 1e3*dpx[i]))
fp.close() 

