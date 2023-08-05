from lmgeo.formats.floatingpointraster import FloatingPointRaster
from .test_baseraster import TestBaseRaster 
import unittest

__author__ = "Steven B. Hoek"

class TestFloatingPointRaster(TestBaseRaster):
    # Load data from a pickle file and metadata from a header file
    # Write the data to an AsciiGrid. Close and open teh file again for reading and check
    test_class = FloatingPointRaster
    int_extension = 'int'
    flt_extension = 'flt'
    
def suite():
    """ This defines all the tests of a module"""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestFloatingPointRaster))
    return suite