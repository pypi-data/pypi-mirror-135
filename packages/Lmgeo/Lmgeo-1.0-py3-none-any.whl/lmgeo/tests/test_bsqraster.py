from lmgeo.formats.bsqraster import BsqRaster
from .test_baseraster import TestBaseRaster
import unittest

__author__ = "Steven B. Hoek"

# TODO this test has limited relevance because the test is carried out with only one band (= default)

class TestBsqRaster(TestBaseRaster):
    # Load data from a pickle file and metadata from a header file
    # Write the data to an AsciiGrid. Close and open teh file again for reading and check
    test_class = BsqRaster
    int_extension = 'bsq'
    flt_extension = 'bsq'


def suite():
    """ This defines all the tests of a module"""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestBsqRaster))
    return suite