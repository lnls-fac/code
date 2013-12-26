import fieldmap
import numpy

def test():
    
    fm = fieldmap.Fieldmap('/home/ximenes/fmap.txt')
    pos = numpy.zeros((3,2))
    pos[:,0] = [0.,0.,0.0]
    pos[:,1] = [0.,0.,1.0]
    field = fm.interpolate(pos)
    print(field)
    
    
test()
    