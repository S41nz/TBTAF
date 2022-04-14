'''
Created on 05/11/2015

@author: S41nz
'''
from __future__ import absolute_import
import sys
import datetime
from common.result import TBTAFResult
from common.enums.verdict_type import TBTAFVerdictType

class TBTestSuite(object):
    '''
    Class that encapsulates the functionality of a Test suite that will contain test cases to be executed by the TBTAF
    '''

    #Fields
    
    #List of test cases that corresponds to a given test suite
    #suiteTestCases = []
    
    def __init__(self,suiteType,suiteID):
        '''
        Constructor
        '''
        self.suiteType = suiteType
        self.suiteID = suiteID
        self.suiteTestCases = []
        
    def getTestSuiteType(self):
        '''
        Method to obtain the type of test suite that has been created
        '''
        return self.suiteType
    
    def getSuiteID(self):
        '''
        Method to get the ID of a given Test suite
        '''
        return self.suiteID
    
    def getTestCases(self):
        '''
        Method to obtain the test cases of a given suite
        '''
        return self.suiteTestCases
    
    def addTestCase(self,newTestCase):
        '''
        Method to add a test case to a given suite
        '''
        self.suiteTestCases.append(newTestCase)

    def addTestCaseList(self,newTestCaseList):
        '''
        Method to add a test case list to a given suite
        '''
        for newTestCase in newTestCaseList:
            self.suiteTestCases.append(newTestCase)

    def clearTestCaseList(self):
        self.suiteTestCases = []
    
    def getSuiteTrace(self):
        '''
        Method to obtain all the traces of the executed test cases
        '''
        self.testTraces = []
        
        if self.suiteTestCases is not None:
            
            for suiteTestCase in self.suiteTestCases:
                #Check if the trace is not null
                currentTrace = suiteTestCase.getTestLog()
                
                if currentTrace is not None:
                    #Append the list to the result collection
                    self.testTraces.append(currentTrace)
                    
        return self.testTraces

    def getSuiteResult(self):
        '''
        Method to obtain the result of a test suite execution
        '''
        candidateVerdict = TBTAFVerdictType.INCONCLUSIVE
        startTimestamp = datetime.datetime.max
        endTimestamp = datetime.datetime.min
        passTests = 0
        inconclusiveTests = 0
        failedTests = 0

        if self.suiteTestCases is not None:
            
            for suiteTestCase in self.suiteTestCases:
                #Check if the trace is not null
                currentResult = suiteTestCase.getResult()
                
                if currentResult is not None:
                    #Check the test verdict
                    testVerdict = currentResult.getVerdict()
                    if testVerdict == TBTAFVerdictType.INCONCLUSIVE:
                        inconclusiveTests = inconclusiveTests + 1
                    elif testVerdict == TBTAFVerdictType.FAIL:
                        failedTests = failedTests + 1
                    elif testVerdict == TBTAFVerdictType.PASS:
                        passTests = passTests + 1
                    #Calculate the timestamps
                    if currentResult.getStartTimestamp() is not None:
                        if startTimestamp > currentResult.getStartTimestamp():
                            startTimestamp = currentResult.getStartTimestamp()
                            
                    if currentResult.getEndTimestamp() is not None: 
                        if endTimestamp < currentResult.getEndTimestamp():
                            endTimestamp = currentResult.getEndTimestamp()
                    
                else:
                    inconclusiveTests = inconclusiveTests + 1
                    
        #With the gathered data we create the result of the overall suite
        # First the verdict
        if len(self.suiteTestCases) == passTests:
            candidateVerdict = TBTAFVerdictType.PASS
        elif failedTests != 0:
            candidateVerdict = TBTAFVerdictType.FAIL
        else:
            candidateVerdict = TBTAFVerdictType.INCONCLUSIVE
        
        #Then create the result instance for the suite
        suiteResult = TBTAFResult(candidateVerdict,self.suiteID)
        suiteResult.setStartTimestamp(startTimestamp)
        suiteResult.setEndTimestamp(endTimestamp)
        #Store the summary indicators on the result object
        suiteResult.setInconclusiveTests(inconclusiveTests)
        suiteResult.setFailedTests(failedTests)
        suiteResult.setPassTests(passTests)
        
        return suiteResult
