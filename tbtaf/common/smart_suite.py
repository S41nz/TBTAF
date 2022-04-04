'''
Created on 07/11/2015

@author: S41nz
'''
from __future__ import absolute_import
import sys
from common.suite import TBTestSuite
from common.result import TBTAFResult
from common.enums.suite_type import TBTAFTestSuiteType
from common.enums.verdict_type import TBTAFVerdictType
from common.enums.filter_type import TBTAFFilterType

class TBSmartTestSuite(TBTestSuite):
    '''
    Class that defines and encapsulates the functionality of a smart test suite
    for a tag-based test management
    '''

    #Methods
    
    def __init__(self, suiteID):
        '''
        Constructor
        '''
        self.suiteType = TBTAFTestSuiteType.SMART
        self.suiteID = suiteID
        self.suiteTestCases = []
    
    
    def getTestCasesByTags(self,targetTags,queryFilter=None):
        '''
        Method to obtain the tests that contain at least one of the given tags on the input list
        '''
        dataSet = TBTestSuite.getTestCases(self)
        resultTestCases = []
        
        #Check if the base data set is not None
        if dataSet is not None and targetTags is not None:
            #Iterate for each tag
            for targetTag in targetTags:
                for candidateTest in dataSet:
                    #Fetch the test metadata
                    testMetadata = candidateTest.getTestMetadata()
                    if testMetadata is not None:
                        testTags = testMetadata.getTags()
                        if self.appendTestCase(testTags, targetTag, queryFilter):
                            #There is a tag match, however we need to confirm if it has not been added yet to the result set
                            if candidateTest not in resultTestCases:
                                resultTestCases.append(candidateTest)
                            
        return resultTestCases
    
    def appendTestCase(self,testTags,targetTag,queryFilter):
        '''
        Method to determine whether or not a given test case should be included or not 
        for a given query
        '''
        if targetTag in testTags:
            if(queryFilter == None or queryFilter == TBTAFFilterType.IN):
                return True
            else:
                return False
        else:
            if(queryFilter == None or queryFilter == TBTAFFilterType.IN):
                return False
            else:
                return True
        
        
    def getSuiteResult(self,tags,queryFilter=None):
        '''
        Method to obtain the TBTAF result based on a specific set of tags
        '''
        TBTestSuite.getSuiteResult(self)
        #Obtain the test cases based on the tag query
        selectedTestCases = self.getTestCases(tags,queryFilter)
        
        candidateVerdict = TBTAFVerdictType.INCONCLUSIVE
        startTimestamp = datetime.datetime.max
        endTimestamp = datetime.datetime.min
        passTests = 0
        inconclusiveTests = 0
        failedTests = 0
        
        if selectedTestCases is not None and len(selectedTestCases) > 0:
            
            for suiteTestCase in selectedTestCases:
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
        if len(selectedTestCases) == passTests and len(selectedTestCases) > 0:
            candidateVerdict = TBTAFVerdictType.PASS
        elif failedTests != 0:
            candidateVerdict = TBTAFVerdictType.FAIL
        else:
            candidateVerdict = TBTAFVerdictType.INCONCLUSIVE
        
        #Then create the result instance for the suite
        suiteResult = TBTAFResult(candidateVerdict,self.suiteID)
        suiteResult.setStartTimestamp(startTimestamp)
        suiteResult.setEndTimestamp(endTimestamp)
        #Set the summary results at the suite level
        suiteResult.setInconclusiveTests(inconclusiveTests)
        suiteResult.setFailedTests(failedTests)
        suiteResult.setPassTests(passTests)
        
        return suiteResult