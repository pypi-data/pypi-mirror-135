import unittest
from . import test_asciigrid 
from . import test_floatingpointraster
from . import test_bilraster
from . import test_bsqraster
from . import test_csfraster
from . import test_numpyraster
#from . import test_rowtiffraster


def make_test_suite(dsn=None):
    """Assemble test suite and return it
    """
    allsuites = unittest.TestSuite([test_asciigrid.suite(), 
                                   test_floatingpointraster.suite(),
                                   test_bilraster.suite(),
                                   test_bsqraster.suite(),
                                   test_csfraster.suite(),
                                   test_numpyraster.suite(),
                                   #test_rowtiffraster()
                                   ])
    return allsuites

def test_all():
    """Assemble test suite and run the test using the TextTestRunner
    """
    allsuites = make_test_suite()
    unittest.TextTestRunner(verbosity=2).run(allsuites)
