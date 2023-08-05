from lmgeo.formats.bitmapraster import BitmapRaster
from lmgeo.tests.test_baseraster import TestBaseRaster
import unittest

__author__ = "Steven B. Hoek"

class TestBilRaster(TestBaseRaster):
    # Load data from a pickle file and metadata from a header file
    # Write the data to an AsciiGrid. Close and open teh file again for reading and check
    test_class = BitmapRaster
    int_extension = 'bmp'

def suite():
    """ This defines all the tests of a module"""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(BitmapRaster))
    return suite

    '''
def main():
    # Test reading
    path = "./output/int4.bmp" # ./output/DecSelectorBG.bmp"  #
    br = BitmapRaster(path, "i")
    br.open('r')
    for i in range(br.nrows):
        line = br.next()
        print(line)
    br.close()
 
    # Test writing
    ag = AsciiGrid('./output/int2.asc', 'i')
    ag.open('r')
    path = "./output/int4.bmp" 
    br = BitmapRaster(path, "i", True)
    br.open('w', ag.ncols, ag.nrows, ag.xll, ag.yll, ag.cellsize, ag.nodatavalue)
    for i in range(ag.nrows):
        line = ag.next()
        br.writenext(line)
    ag.close()
    br.close()
    '''
if __name__ == "__main__":
    main()