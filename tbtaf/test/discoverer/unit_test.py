'''
Created on 25/11/2015

@author: pvicenci
'''
from __future__ import absolute_import
import unittest

from discoverer.discoverer import TBTAFDiscoverer
class TestDiscoverer(unittest.TestCase):


    def setUp(self):
        pass
    
    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')
      
      
    def CorrectPath(self):
        try:
            TBTAFDiscoverer.LoadTests(r'./\\\\\samples/\//')
        except ValueError:
            self.fail('This is a correct Path')
        else:
            pass
        
    def test_afunction_throws_exception(self):
        try:
            TBTAFDiscoverer.LoadTests(r'./\\\\\samplesi/\//')
        except ValueError:
            pass
      
    def test_nonvalidPathpy(self):
        try:
            TBTAFDiscoverer.LoadTests(r'D:\\ITESM\\Aseguramiento de la Calidad\\DiscovererN\\Samples\\testBlanck.py')
        except ValueError:
            pass   
        
    

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()