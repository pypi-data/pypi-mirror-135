import unittest
from .test_asciigrid import suite as test_asciigrid_suite


def make_test_suite(dsn=None):
    """Assemble test suite and return it
    """
    allsuites = unittest.TestSuite([test_asciigrid_suite()
                                   ])
    return allsuites

def test_all():
    """Assemble test suite and run the test using the TextTestRunner
    """
    allsuites = make_test_suite()
    unittest.TextTestRunner(verbosity=2).run(allsuites)
    
test_all()