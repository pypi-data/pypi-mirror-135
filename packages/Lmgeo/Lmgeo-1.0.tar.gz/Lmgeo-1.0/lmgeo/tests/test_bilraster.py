from lmgeo.formats.bilraster import BilRaster
from .test_baseraster import TestBaseRaster
import unittest

__author__ = "Steven B. Hoek"

# TODO this test has limited relevance because the test is carried out with only one band (= default)

class TestBilRaster(TestBaseRaster):
    # Load data from a pickle file and metadata from a header file
    # Write the data to an AsciiGrid. Close and open teh file again for reading and check
    test_class = BilRaster
    int_extension = 'bil'
    flt_extension = 'bil'


def suite():
    """ This defines all the tests of a module"""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestBilRaster))
    return suite