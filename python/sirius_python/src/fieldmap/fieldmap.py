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
        numpy_field = _Aux.py2num(py_field)
        return numpy_field 
     
    
class _Aux:
    
    @staticmethod
    def num2py(pos):
        return numpy.reshape(pos, pos.size, order='F').tolist()
    
    @staticmethod
    def py2num(pos):
        return numpy.reshape(numpy.array(pos), (3,-1), order='F')   