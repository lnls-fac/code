"""
Test_PlotSharedMemory

Afonso Haruo Carnielli Mukai (FAC - LNLS)

2013-12-17: v0.1
"""

import unittest
import PlotSharedMemory


class TestCommand(unittest.TestCase):
    
    def setUp(self):
        self.shm = PlotSharedMemory.PlotSharedMemory()
    
    def test_text_updated_not_bool(self):
        result = False
        try:
            self.shm.text_updated = 1
        except TypeError:
            result = True
        self.assertTrue(result,
                        'TypeError not raised')
    
    def test_text_updated_default(self):
        self.assertFalse(self.shm.text_updated,
                         'text_updated not False')
     
    def test_text_updated(self):
        self.shm.text_updated = True
        self.assertTrue(self.shm.text_updated,
                        'text_updated not True')
    
    def test_data_updated_not_bool(self):
        result = False
        try:
            self.shm.data_updated = 1
        except TypeError:
            result = True
        self.assertTrue(result,
                        'TypeError not raised')
    
    def test_data_updated_default(self):
        self.assertFalse(self.shm.data_updated,
                         'data_updated not False')
     
    def test_data_updated(self):
        self.shm.data_updated = True
        self.assertTrue(self.shm.data_updated,
                        'data_updated not True')
    
    def test_properties_updated_not_bool(self):
        result = False
        try:
            self.shm.properties_updated = 1
        except TypeError:
            result = True
        self.assertTrue(result,
                        'TypeError not raised')
    
    def test_properties_updated_default(self):
        self.assertFalse(self.shm.properties_updated,
                         'properties_updated not False')
     
    def test_properties_updated(self):
        self.shm.properties_updated = True
        self.assertTrue(self.shm.properties_updated,
                        'properties_updated not True')
