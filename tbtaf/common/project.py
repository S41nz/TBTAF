'''
Created on 07/11/2015

@author: 
'''
from __future__ import absolute_import
from common.suite import TBTestSuite
from common.test_bed import TBTestBed

class TBProject(object):
    '''
    Class that defines and encapsulates the functionality of a TBProject. This class is used in TBTAFOrchestrator.
    '''

    #Methods
    
    def __init__(self, tbTestSuite, tbTestBed, projectName):
        '''
        Constructor
        '''
        self.tbTestSuite = tbTestSuite
        self.tbTestBed = tbTestBed
        self.projectName = projectName
    
    def getTBTestSuite(self):
        '''
        
        '''
        return self.tbTestSuite
        
    def getTBTestBed(self):
        '''
        
        '''
        return self.tbTestBed
        
    def getProjectName(self):
        '''
        
        '''
        return self.projectName
        
    def setTBTestSuite(tbTestSuite):
        '''
        
        '''
        self.tbTestSuite = tbTestSuite
        
    def setTBTestBed(tbTestBed):
        '''
        
        '''
        self.tbTestBed = tbTestBed
        
    def setProjectName(self, projectName):
        '''
        
        '''
        self.projectName = projectName
