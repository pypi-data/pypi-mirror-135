from lmgeo.formats.csfraster import CsfRaster
from .test_baseraster import TestBaseRaster
import unittest

__author__ = "Steven B. Hoek"

class TestCsfRaster(TestBaseRaster):
    # Load data from a pickle file and metadata from a header file
    # Write the data to an AsciiGrid. Close and open teh file again for reading and check
    test_class = CsfRaster
    int_extension = 'map'
    flt_extension = 'map'


def suite():
    """ This defines all the tests of a module"""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestCsfRaster))
    return suite