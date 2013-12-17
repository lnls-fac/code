"""
PlotSharedMemory
    Shared memory for InteractivePlot. 

Afonso Haruo Carnielli Mukai (FAC - LNLS)

2013-12-17: v0.1
"""

import mmap
import numpy


_NUMPY_NUM_SIZE = len(numpy.array([0.0]).tostring())

_NUM_BYTES_COMMAND = _NUMPY_NUM_SIZE
_NUM_BYTES_LENGTH = _NUMPY_NUM_SIZE
_NUM_BYTES_DATA = 50000 * _NUMPY_NUM_SIZE
_NUM_BYTES_COLOR = 8
_NUM_BYTES_LINE_STYLE = 2
_NUM_BYTES_LINE_WIDTH = _NUMPY_NUM_SIZE
_NUM_BYTES_MARKER = 2
_NUM_BYTES_X_LABEL = 80
_NUM_BYTES_Y_LABEL = 80
_NUM_BYTES_TITLE = 80

_POS_COMMAND = 0
_POS_DATA_LEN = _NUM_BYTES_COMMAND
_POS_DATA_X = _POS_DATA_LEN + _NUM_BYTES_LENGTH
_POS_DATA_Y = _POS_DATA_X + _NUM_BYTES_DATA
_POS_COLOR = _POS_DATA_Y + _NUM_BYTES_DATA
_POS_LINE_STYLE = _POS_COLOR + _NUM_BYTES_COLOR
_POS_LINE_WIDTH = _POS_LINE_STYLE + _NUM_BYTES_LINE_STYLE
_POS_MARKER = _POS_LINE_WIDTH + _NUM_BYTES_LINE_WIDTH
_POS_X_LABEL = _POS_MARKER + _NUM_BYTES_MARKER
_POS_Y_LABEL = _POS_X_LABEL + _NUM_BYTES_X_LABEL
_POS_TITLE = _POS_Y_LABEL + _NUM_BYTES_Y_LABEL

_TOTAL_LENGTH = _POS_TITLE + _NUM_BYTES_TITLE

_MASK_COMMAND_DATA = 1
_MASK_COMMAND_PROPERTIES = _MASK_COMMAND_DATA << 1
_MASK_COMMAND_X_LABEL = _MASK_COMMAND_PROPERTIES << 1
_MASK_COMMAND_Y_LABEL = _MASK_COMMAND_X_LABEL << 1
_MASK_COMMAND_TITLE = _MASK_COMMAND_Y_LABEL << 1


class PlotSharedMemory(object):
    
    def __init__(self):
        self._shm = mmap.mmap(-1, _TOTAL_LENGTH)
        
        self.data_updated = False
        self.properties_updated = False
    
    @property
    def data_updated(self):
        return self._get_command_with_mask(_MASK_COMMAND_DATA)

    @data_updated.setter
    def data_updated(self, value):
        self._set_command_with_mask(value, _MASK_COMMAND_DATA)
    
    @property
    def properties_updated(self):
        return self._get_command_with_mask(_MASK_COMMAND_PROPERTIES)

    @properties_updated.setter
    def properties_updated(self, value):
        self._set_command_with_mask(value, _MASK_COMMAND_PROPERTIES)
    
    def _check_if_boolean(self, value):
        if not isinstance(value, bool):
            raise TypeError('Value must be a bool')
    
    def _get_command_with_mask(self, mask):
        args_read = (_POS_COMMAND, 'int')
        command = self._get_value_in_pos(*args_read)
        if command & mask:
            return True
        else:
            return False
    
    def _set_command_with_mask(self, value, mask):
        self._check_if_boolean(value)                
        args_read = (_POS_COMMAND, 'int')
        command = self._get_value_in_pos(*args_read)                
        if value:
            new_command = command | mask
        else:
            new_command = command & ~mask            
        args_write = (new_command, _POS_COMMAND, 'int')
        self._set_value_in_pos(*args_write)
    
    def _get_value_in_pos(self, pos, type_='float'):
        self._shm.seek(pos)
        command_array = numpy.fromstring(self._shm.read(_NUMPY_NUM_SIZE),
                                         dtype=type_)
        return command_array[0]
    
    def _set_value_in_pos(self, value, pos, type_='float'):        
        array = numpy.array([value], dtype=type_)
        self._shm.seek(pos)
        self._shm.write(array.tostring())
        
    def _get_array_in_pos(self, pos, length, type_='float'):
        self._shm.seek(pos)
        command_array = numpy.fromstring(self._shm.read(length),
                                         dtype=type_)
        return command_array
