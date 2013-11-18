import passmethods

PassMethods = passmethods.PassMethods

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
        
        self.fam_name    = fam_name
        self.length      = length
        self.nr_steps    = nr_steps
        self.pass_method = pass_method
        
        if angle      is not None: self.angle       = angle
        if gap        is not None: self.gap         = gap
        if polynom_a  is not None: self.polynom_a   = polynom_a
        if polynom_b  is not None: self.polynom_b   = polynom_b
        
        if k          is not None: self.k           = k
        if kl         is not None: self.kl          = kl
        if sl         is not None: self.sl          = sl
        if kick_angle is not None: self.kick_angle  = kick_angle
        if voltage    is not None: self.voltage     = voltage
        if frequency  is not None: self.frequency   = frequency
        if energy     is not None: self.energy      = energy
        
        if t_in       is not None: self.t_in        = t_in
        if r_in       is not None: self.r_in        = r_in
        if angle_in   is not None: self.angle_in    = angle_in
        if fint_in    is not None: self.fint_in     = fint_in
        
        if t_out      is not None: self.t_out       = t_out
        if r_out      is not None: self.r_out       = r_out
        if angle_out  is not None: self.angle_out   = angle_out 
        if fint_out   is not None: self.fint_out    = fint_out
        
    def __str__(self):
        r  = ''
        try: r += '   FamName: ' + self.fam_name + '\n' 
        except: pass
        try: r += '    Length: ' + str(self.length) + '\n'
        except: pass
        try: r += 'PassMethod: ' + str(self.pass_method) + '\n'
        except: pass
        try: r += '     Angle: ' + str(self.angle) + '\n'
        except: pass
        try: r += '   AngleIn: ' + str(self.angle_in) + '\n'
        except: pass
        try: r += '  AngleOut: ' + str(self.angle_out) + '\n'
        except: pass
        try: r += '       Gap: ' + str(self.gap) + '\n'
        except: pass
        try: r += '  PolynomA: ' + str(self.polynom_a) + '\n'
        except: pass
        try: r += '  PolynomB: ' + str(self.polynom_b) + '\n'
        except: pass
        try: r += '         K: ' + str(self.k) + '\n'
        except: pass
        try: r += '        KL: ' + str(self.kl) + '\n'
        except: pass
        try: r += '        SL: ' + str(self.sl) + '\n'
        except: pass
        try: r += ' KickAngle: ' + str(self.kick_angle) + '\n'
        except: pass
        try: r += '   Voltage: ' + str(self.voltage) + '\n'
        except: pass
        try: r += ' Frequency: ' + str(self.frequency) + '\n'
        except: pass
        try: r += '    Energy: ' + str(self.energy) + '\n'
        except: pass
        try: r += '       TIn: ' + str(self.t_in) + '\n'
        except: pass
        try: r += '       RIn: ' + str(self.r_in) + '\n'
        except: pass
        try: r += '    FIntIn: ' + str(self.fint_in) + '\n'
        except: pass
        try: r += '      TOut: ' + str(self.t_out) + '\n'
        except: pass
        try: r += '      ROut: ' + str(self.r_out) + '\n'
        except: pass
        try: r += '   FIntOut: ' + str(self.fint_out) + '\n'
        except: pass
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


