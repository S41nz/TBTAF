'''
Created on 07/11/2015

@author: S41nz
'''
#import sys
from common.suite import TBTestSuite
from common.test_bed import TBTestBed
#from common.result import TBTAFResult
#from common.enums.suite_type import TBTAFTestSuiteType
#from common.enums.verdict_type import TBTAFVerdictType

class TBProject(object):
    '''
    Class that defines and encapsulates the functionality of a TBProject. This class is used in TBTAFOrchestrator.
    '''

    #Methods
	suiteID
    
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