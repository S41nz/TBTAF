'''
Created on 07/11/2015

@author: S41nz
'''
import sys
from common.suite import TBTestSuite
from common.result import TBTAFResult
from common.enums.suite_type import TBTAFTestSuiteType
from common.enums.verdict_type import TBTAFVerdictType

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
    
    
    def getTestCases(self,targetTags):
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
                        if testTags is not None and targetTag in testTags:
                            #There is a tag match, however we need to confirm if it has not been added yet to the result set
                            if candidateTest not in resultTestCases:
                                resultTestCases.append(candidateTest)
                            
        return resultTestCases
    
    
    def getSuiteResult(self,tags):
        '''
        Method to obtain the TBTAF result based on a specific set of tags
        '''
        TBTestSuite.getSuiteResult(self)
        #Obtain the test cases based on the tag query
        selectedTestCases = self.getTestCases(tags)
        
        candidateVerdict = TBTAFVerdictType.INCONCLUSIVE
        startTimestamp = sys.maxsize
        endTimestamp = 0
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
                    if startTimestamp > currentResult.getStartTimestamp():
                        startTimestamp = currentResult.getStartTimestamp()
                        
                    if endTimestamp < currentResult.getEndTimestamp():
                        endTimestamp = currentResult.getEndTimestamp()
                    
                else:
                    inconclusiveTests = inconclusiveTests + 1
                    
        #With the gathered data we create the result of the overall suite
        # First the verdict
        if len(selectedTestCases) == passTests and len(selectedTestCases) > 0:
            candidateVerdict = TBTAFVerdictType.PASS
        elif failedTests is not 0:
            candidateVerdict = TBTAFVerdictType.FAIL
        else:
            candidateVerdict = TBTAFVerdictType.INCONCLUSIVE
        
        #Then create the result instance for the suite
        suiteResult = TBTAFResult(candidateVerdict,self.suiteID)
        suiteResult.setStartTimestamp(startTimestamp)
        suiteResult.setEndTimestamp(endTimestamp)
        
        return suiteResult