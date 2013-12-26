import fieldmapcpp
import numpy

    
class Fieldmap:
    
    def __init__ (self, filename):
        r = fieldmapcpp.load(filename)         
        self.filename = filename
        self.id       = r[0]
        (self.nx, self.xmin, self.xmax) = (r[1],r[2],r[3])
        (self.nz, self.zmin, self.zmax) = (r[4],r[5],r[6])
        
    
    def __del__(self):
        try:
            fieldmapcpp.unload(self.id)
        except:
            pass
        
    def interpolate(self, pos):
        py_pos = _Aux.num2py(pos)
        py_field = fieldmapcpp.interpolate(self.id, py_pos)
        numpy_field = _Aux.py3_2_num(py_field)
        return numpy_field 
    
    def electron_trajectory(self, energy, si = 0, sf = None, nrpts = 1000, init_state = None):
        if sf == None:
            sf = self.zmax
        if init_state == None:
            init_state = numpy.array([[0.],[0.],[0.],[0.],[0.],[1.]])
        py_init_state = _Aux.num2py(init_state)
        py_traj = fieldmapcpp.odeint_const(self.id, energy, si, sf, nrpts, py_init_state)
        traj = _Aux.py7_2_num(py_traj)
        return traj
         
     
    @property 
    def nx(self): return self.nx
    @property 
    def xmin(self): return self.xmin
    @property 
    def xmax(self): return self.xmax
    @property 
    def nz(self): return self.nz
    @property 
    def zmin(self): return self.zmin
    @property 
    def zmax(self): return self.zmax
    
    @staticmethod
    def clear_all():
        fieldmapcpp.clear()
    
clear_all = Fieldmap.clear_all

class _Aux:
    
    @staticmethod
    def num2py(pos):
        return numpy.reshape(pos, pos.size, order='F').tolist()
    
    @staticmethod
    def py3_2_num(pos):
        return numpy.reshape(numpy.array(pos), (3,-1), order='F')  
    @staticmethod
    def py7_2_num(pos):
        return numpy.reshape(numpy.array(pos), (7,-1), order='F') 