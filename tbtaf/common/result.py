'''
Created on 03/11/2015
@author: S41nz

Modified on 14/11/2015 by @andresmuro
Summary counters added to retrieve Suite results (passed,failed,inconclusive)
'''

class TBTAFResult(object):
    '''
    Class that encapsulates the information related to the result of the execution of a given TBTAFTestCase
    '''

    def __init__(self, testVerdict,resultSource):
        '''
        Constructor
        '''
        self.testVerdict = testVerdict
        self.resultSource = resultSource
        self.passTests = 0
        self.inconclusiveTests = 0
        self.failedTests = 0
        self.startTimestamp = None
        self.endTimestamp = None
        
    def getVerdict(self):
        return self.testVerdict
    
    def getResultSource(self):
        return self.resultSource
        
    def getPassTests(self):
        return self.passTests

    def getInconclusiveTests(self):
        return self.inconclusiveTests
        
    def getFailedTests(self):
        return self.failedTests        
    
    def setPassTests(self,passTests):
        self.passTests = passTests

    def setInconclusiveTests(self,inconclusiveTests):
        self.inconclusiveTests = inconclusiveTests
        
    def setFailedTests(self,failedTests):
        self.failedTests = failedTests
    
    def setStartTimestamp(self,startTime):
        self.startTimestamp = startTime
    
    def getStartTimestamp(self):
        return self.startTimestamp
        
    def setEndTimestamp(self,endTime):
        self.endTimestamp = endTime
    
    def getEndTimestamp(self):
        return self.endTimestamp
    
    def to_dict(self):
        # Convertir los timestamps de datetime a cadena (si están presentes)
        startTimestamp_str = self.startTimestamp.strftime("%Y-%m-%d %H:%M:%S") if self.startTimestamp else None
        endTimestamp_str = self.endTimestamp.strftime("%Y-%m-%d %H:%M:%S") if self.endTimestamp else None
        
        return {
            "testVerdict": self.testVerdict,
            "resultSource": self.resultSource,
            "passTests": self.passTests,
            "inconclusiveTests": self.inconclusiveTests,
            "failedTests": self.failedTests,
            "startTimestamp": startTimestamp_str,
            "endTimestamp": endTimestamp_str
        }