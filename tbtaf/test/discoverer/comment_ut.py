'''
Created on 25/11/2015

@author: alberto
'''

from __future__ import absolute_import
import unittest

from discoverer.discoverer import TBTAFDiscoverer

class prueba_unidad(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_HayComentarioMultilinea(self):
        comment = TBTAFDiscoverer._readFirstMultilineComment('./samples/testCompleteAndValid.py')
        if comment == "":
            self.fail("File does not have multiline comment")
        else:
            pass
        
    def test_NoHayComentarioMultilinea(self):
        comment = TBTAFDiscoverer._readFirstMultilineComment('./samples/testBlank.py')
        if comment == "":
            pass
        else:
            self.fail("File has multiline comment")
    
if __name__ == "__main__":
    unittest.main()
