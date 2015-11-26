class TBTAFExecutionStatus:
    
    def __init__(self):
        self.executionStatusType=None
        self.suiteResult=None
        self.testCasesTotal=None
        self.testCasesExecuted=None
    
    def setExecutionStatusType(self,executionStatusType):
        self.executionStatusType=executionStatusType
    
    def getExecutionStatusType(self):
        return self.executionStatusType
        
    def setSuiteResult(self,suiteResult):
        self.suiteResult=suiteResult
    
    def getSuiteResult(self):
        return self.suiteResult
        
    def getCompletionPercentage(self):
        if self.testCasesExecuted is None:
            raise Exception("testCasesExecuted value must be set before using this method")
        if self.testCasesTotal is None:
            raise Exception("testCasesTotal value must be set before using this method")
        percentage = round(self.testCasesExecuted * 100 / self.testCasesTotal, 2)
        return percentage
    
    def setTestCasesTotal(self,testCasesTotal):
        self.testCasesTotal=testCasesTotal
    
    def getTestCasesTotal(self):
        return self.testCasesTotal
        
    def setTestCasesExecuted(self,testCasesExecuted):
        self.testCasesExecuted=testCasesExecuted
    
    def getTestCasesExecuted(self):
        return self.testCasesExecuted