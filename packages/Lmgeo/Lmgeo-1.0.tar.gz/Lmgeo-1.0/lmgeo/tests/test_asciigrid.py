from lmgeo.formats.asciigrid import AsciiGrid
from .test_baseraster import TestBaseRaster
import unittest

__author__ = "Steven B. Hoek"

class TestAsciiGrid(TestBaseRaster):
    # Load data from a pickle file and metadata from a header file
    # Write the data to an AsciiGrid. Close and open teh file again for reading and check
    test_class = AsciiGrid
    int_extension = 'asc'
    flt_extension = 'asc'


def suite():
    """ This defines all the tests of a module"""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestAsciiGrid))
    return suite


