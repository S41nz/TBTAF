from __future__ import absolute_import
from __future__ import print_function
import unittest

from discoverer.discoverer import TBTAFDiscoverer

class PruebaArchivosPy(unittest.TestCase):
    def setUp(self):
        print("loading individual test...")
        pass
    
    def test_PathValido(self):
        try:
            pyFiles = TBTAFDiscoverer._findPyFiles('./samples')
        except ValueError as e:
            self.fail("Invalid path was provided")
        else:
            print(pyFiles)
            pass
        
    def test_PathInvalido(self):
        try:
            pyFiles = TBTAFDiscoverer._findPyFiles('./sample')
        except ValueError:
            pass
        else:
            self.fail("Valid path was provided")

if __name__ == "__main__":
    unittest.main()