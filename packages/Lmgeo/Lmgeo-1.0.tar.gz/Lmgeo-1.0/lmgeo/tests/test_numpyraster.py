from lmgeo.formats.numpyraster import NumpyRaster
from test_baseraster import TestBaseRaster
import unittest

__author__ = "Steven B. Hoek"

class TestNumpyRaster(TestBaseRaster):
    # Load data from a pickle file and metadata from a header file
    # Write the data to an AsciiGrid. Close and open teh file again for reading and check
    test_class = NumpyRaster
    int_extension = 'npy'
    flt_extension = 'npy'

def suite():
    """ This defines all the tests of a module"""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestNumpyRaster))
    return suite