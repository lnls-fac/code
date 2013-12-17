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
_NUM_BYTES_TEXT = 80
_NUM_BYTES_COLOR = 8
_NUM_BYTES_LINE_STYLE = 2
_NUM_BYTES_LINE_WIDTH = _NUMPY_NUM_SIZE
_NUM_BYTES_MARKER = 2
_NUM_BYTES_LENGTH = _NUMPY_NUM_SIZE
_NUM_BYTES_DATA = 50000 * _NUMPY_NUM_SIZE

_POS_COMMAND = 0
_POS_TITLE = _POS_COMMAND + _NUM_BYTES_COMMAND
_POS_X_LABEL = _POS_TITLE + _NUM_BYTES_TEXT
_POS_Y_LABEL = _POS_X_LABEL + _NUM_BYTES_TEXT

_POS_DATA_LENGTH = [_POS_Y_LABEL + _NUM_BYTES_TEXT]
_POS_DATA_X = [_POS_DATA_LENGTH[0] + _NUM_BYTES_LENGTH]
_POS_DATA_Y = [_POS_DATA_X[0] + _NUM_BYTES_DATA]
_POS_COLOR = [_POS_DATA_Y[0] + _NUM_BYTES_DATA]
_POS_LINE_STYLE = [_POS_COLOR[0] + _NUM_BYTES_COLOR]
_POS_LINE_WIDTH = [_POS_LINE_STYLE[0] + _NUM_BYTES_LINE_STYLE]
_POS_MARKER = [_POS_LINE_WIDTH[0] + _NUM_BYTES_LINE_WIDTH]

_LINE_DATA_LENGTH = _POS_MARKER[0] + _NUM_BYTES_MARKER - _POS_DATA_LENGTH[0]

for i in range(1, 5):
    _POS_DATA_LENGTH.append(_POS_DATA_LENGTH[i-1] + i*_LINE_DATA_LENGTH)
    _POS_DATA_X.append(_POS_DATA_X[i-1] + i*_LINE_DATA_LENGTH)
    _POS_DATA_Y.append(_POS_DATA_Y[i-1] + i*_LINE_DATA_LENGTH)
    _POS_COLOR.append(_POS_COLOR[i-1] + i*_LINE_DATA_LENGTH)
    _POS_LINE_STYLE.append(_POS_LINE_STYLE[i-1] + i*_LINE_DATA_LENGTH)
    _POS_LINE_WIDTH.append(_POS_LINE_WIDTH[i-1] + i*_LINE_DATA_LENGTH)
    _POS_MARKER.append(_POS_MARKER[i-1] + i*_LINE_DATA_LENGTH)

_TOTAL_LENGTH = _POS_TITLE + _NUM_BYTES_TEXT

_MASK_COMMAND_TEXT = 1
_MASK_COMMAND_DATA = _MASK_COMMAND_TEXT << 1
_MASK_COMMAND_PROPERTIES = _MASK_COMMAND_DATA << 1
_MASK_COMMAND_LINE1_ON = _MASK_COMMAND_PROPERTIES << 1
_MASK_COMMAND_LINE2_ON = _MASK_COMMAND_LINE1_ON << 1
_MASK_COMMAND_LINE3_ON = _MASK_COMMAND_LINE2_ON << 1
_MASK_COMMAND_LINE4_ON = _MASK_COMMAND_LINE3_ON << 1
_MASK_COMMAND_LINE5_ON = _MASK_COMMAND_LINE4_ON << 1


class PlotSharedMemory(object):
    
    def __init__(self):
        self._shm = mmap.mmap(-1, _TOTAL_LENGTH)
        
        self.data_updated = False
        self.properties_updated = False
    
    @property
    def text_updated(self):
        return self._get_command_with_mask(_MASK_COMMAND_TEXT)

    @text_updated.setter
    def text_updated(self, value):
        self._set_command_with_mask(value, _MASK_COMMAND_TEXT)
    
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
