from passmethods import *

class marker(object):
    def __init__(self,     
         fam_name, 
         length      = 0,
         nr_steps    = 1,
         pass_method = PassMethods.pm_identity_pass,
         angle       = None,
         gap         = None,
         polynom_a   = None,
         polynom_b   = None,
         k           = None,
         kl          = None,
         s           = None,
         sl          = None,
         kick_angle  = None,
         frequency   = None,
         voltage     = None,
         energy      = None,
         t_in        = None,
         r_in        = None,
         angle_in    = None,
         fint_in     = None,
         t_out       = None,
         r_out       = None,
         angle_out   = None,
         fint_out    = None,
         **kwargs
         ):
        
        if fam_name    is not None: self.fam_name    = fam_name
        if length      is not None: self.length      = length
        if nr_steps    is not None: self.nr_steps    = nr_steps
        if pass_method is not None: self.pass_method = pass_method
        
        if angle       is not None: self.angle       = angle
        if gap         is not None: self.gap         = gap
        if polynom_a   is not None: self.polynom_a   = polynom_a
        if polynom_b   is not None: self.polynom_b   = polynom_b
        
        if k           is not None: self.k           = k
        if kl          is not None: self.kl          = kl
        if sl          is not None: self.sl          = sl
        if ikck_angle  is not None: self.kick_angle  = kick_angle
        if voltage     is not None: self.voltage     = voltage
        if frequency   is not None: self.frequency   = frequency
        if energy      is not None: self.energy      = energy
        
        if t_in        is not None: self.t_in        = t_in
        if r_in        is not None: self.r_in        = r_in
        if angle_in    is not None: self.angle_in    = angle_in
        if fint_in     is not None: self.fint_in     = fint_in
        
        if t_out       is not None: self.t_out       = t_out
        if r_out       is not None: self.r_out       = r_out
        if angle_out   is not None: self.angle_out   = angle_out 
        if fint_out    is not None: self.fint_out    = fint_out
        
    def __str__(self):
        r  = ''
        if self.fam_name is not None:
            r += '   FamName: ' + self.fam_name + '\n'
        if self.length is not None:
            r += '    Length: ' + str(self.length) + '\n'
        if self.pass_method is not None:
            r += 'PassMethod: ' + str(self.pass_method) + '\n'
        if self.angle is not None:
            r += '     Angle: ' + str(self.angle) + '\n'
        if self.angle_in is not None:
            r += '   AngleIn: ' + str(self.angle_in) + '\n'
        if self.angle_out is not None:
            r += '  AngleOut: ' + str(self.angle_out) + '\n'
        if self.gap is not None:
            r += '       Gap: ' + str(self.gap) + '\n'
        if self.polynom_a is not None:
            r += '  PolynomA: ' + str(self.polynom_a) + '\n'
        if self.polynom_b is not None:
            r += '  PolynomB: ' + str(self.polynom_b) + '\n'
        if self.k is not None:
            r += '         K: ' + str(self.k) + '\n'
        if self.kl is not None:
            r += '        KL: ' + str(self.kl) + '\n'
        if self.sl is not None:
            r += '        SL: ' + str(self.sl) + '\n'
        if self.kick_angle is not None:
            r += ' KickAngle: ' + str(self.kick_angle) + '\n'
        if self.voltage is not None:
            r += '   Voltage: ' + str(self.voltage) + '\n'
        if self.frequency is not None:
            r += ' Frequency: ' + str(self.frequency) + '\n'
        if self.energy is not None:
            r += '    Energy: ' + str(self.energy) + '\n'
        if self.t_in is not None:
            r += '       TIn: ' + str(self.t_in) + '\n'
        if self.r_in is not None:
            r += '       RIn: ' + str(self.r_in) + '\n'
        if self.fint_in is not None:
            r += '    FIntIn: ' + str(self.fint_in) + '\n'
        if self.t_out is not None:
            r += '      TOut: ' + str(self.t_out) + '\n'
        if self.r_out is not None:
            r += '      ROut: ' + str(self.r_out) + '\n'
        if self.fint_out is not None:
            r += '   FIntOut: ' + str(self.fint_out) + '\n'
        return r
    
    
class drift(marker):
    def __init__(self, pass_method = PassMethods.pm_drift_pass, **kwargs):
        marker.__init__(self, pass_method = pass_method, **kwargs)

class corrector(marker):
    def __init__(self, pass_method = PassMethods.pm_corrector_pass, kick_angle  = None, **kwargs):
        if kick_angle == None: kick_angle = [0,0]
        marker.__init__(self, pass_method = pass_method, kick_angle = kick_angle, **kwargs)
        
class rfcavity(marker):
    def __init__(self, voltage, frequency, energy, pass_method = PassMethods.pm_cavity_pass, **kwargs):
        marker.__init__(self, pass_method = pass_method, voltage = voltage, frequency = frequency, energy = energy, **kwargs)

class quadrupole(marker):
    def __init__(self, pass_method = PassMethods.pm_str_mpole_symplectic4_pass, nr_steps = 10, polynom_a = None, polynom_b = None, **kwargs): 
        if polynom_a == None: polynom_a = [0,0]
        if polynom_b == None: polynom_b = [0,0] 
        if 'k' in kwargs: 
            if ('kl' in kwargs) or (pass_method == PassMethods.pm_thinquad_pass):
                raise Exception('Inconsistent marker parameters!')
            polynom_b[1] = kwargs['k']
        if 'kl' in kwargs:
            if ('k' in kwargs) or (pass_method != PassMethods.pm_thinquad_pass):
                raise Exception('Inconsistent marker parameters!')
        marker.__init__(self, pass_method = pass_method, nr_steps = nr_steps, polynom_a = polynom_a, polynom_b = polynom_b, **kwargs)

class sextupole(marker):
    def __init__(self, pass_method = 'str_mpole_symplectic4_pass', nr_steps = 5, polynom_a = None, polynom_b = None, **kwargs): 
        if polynom_a == None: polynom_a = [0,0,0]
        if polynom_b == None: polynom_b = [0,0,0] 
        if 's' in kwargs: 
            if ('sl' in kwargs) or (pass_method == 'thinsext_pass'):
                raise Exception('Inconsistent marker parameters!')
            pass_method  = 'str_mpole_symplectic4_pass'
            polynom_b[2] = kwargs['s']
        if 'sl' in kwargs:
            if ('s' in kwargs) or (pass_method != 'thinsext_pass'):
                raise Exception('Inconsistent marker parameters!')
        marker.__init__(self, pass_method = pass_method, nr_steps = nr_steps, polynom_a = polynom_a, polynom_b = polynom_b, **kwargs)

class rbend(marker):
    def __init__(self, length, angle, pass_method = 'bnd_mpole_symplectic4_pass', nr_steps = 10, polynom_a = None, polynom_b = None, gap = 0, **kwargs):
        if polynom_a == None: polynom_a = [0,0]
        if polynom_b == None: polynom_b = [0,0]
        if 'k' in kwargs:
            polynom_b[1] = kwargs['k']
        if 'angle_in' not in kwargs:
            kwargs['angle_in'] = 0.5 * angle
        if 'angle_out' not in kwargs:
            kwargs['angle_out'] = 0.5 * angle
        marker.__init__(self, pass_method = pass_method, length = length, angle = angle, gap = gap, nr_steps = nr_steps, polynom_a = polynom_a, polynom_b = polynom_b, **kwargs)


