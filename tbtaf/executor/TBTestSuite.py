from TBTAFTrace import *
from TBTestCase import *
class TBTestSuite:
    ''' getSuiteResult() --- addTestCase(TBTestCase) --- getTestCases():TBTestCase[] --- getSuiteTrace():TBTAFTrace[] '''
    
    def getSuiteResult(self):
        return "This is a result"
    
    def addTestCase(self,TBTestCase):
        return "Test case added"
    
    def getTestCases(self):
        result = [TBTestCase(), TBTestCase()]
        return result
    
    def getSuiteTrace(self):
        '''Array of TBTAFTrace'''
        result = [TBTAFTrace(), TBTAFTrace()]
        return result
        
testCaseStub = TBTestCase()
test = TBTestSuite()
print test.getSuiteResult()
print test.addTestCase(testCaseStub)
print test.getTestCases()
print test.getSuiteTrace()