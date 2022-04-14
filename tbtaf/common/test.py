'''
Created on 04/11/2015

@author: S41nz
'''

from __future__ import absolute_import
from abc import ABCMeta, abstractmethod
import six

class TBTestCase(six.with_metaclass(ABCMeta)):
    '''
    Abstract class that defines the base functionality that every test case within the TBTAF should implement
    '''

    
    #Methods
    def __init__(self):
        '''
        Constructor
        '''
        self.testTrace = None
        self.testResult = None
    
    @abstractmethod
    def setup(self):
        '''
        Method that performs the required environment setup prior to test execution
        '''    
    
    @abstractmethod
    def execute(self):
        '''
        Method that executes the actual test
        '''
        
    def verdict(self):
        '''
        Method of OPTIONAL implementation that allows to separate the test execution from the verdict calculation
        '''
        pass
    
    @abstractmethod
    def cleanup(self):
        '''
        Method that performs cleanup routines after test execution and verdict calculation. This will get the testing environment ready for the 
        next test to be executed
        '''
    
    def getResult(self):
        '''
        Method to obtain the instance of the TBTAFResult corresponding to the test case
        '''
        return self.testResult
    
    def getTestLog(self):
        '''
        Method to obtain the instance of the TBTAFTrace corresponding to the test case
        '''
        return self.testTrace
    
    def setTestMetadata(self,metadata):
        '''
        Method to set the metadata corresponding to the test case being executed
        '''
        self.testMetadata = metadata
        
    def getTestMetadata(self):
        '''
        Method to obtain the Metadata instance corresponding to the given test case
        '''
        return self.testMetadata
    
    def getTestTimeout(self):
        '''
        Method to obtain the timeout attribute to manage test execution
        '''
        return self.testTimeout
    