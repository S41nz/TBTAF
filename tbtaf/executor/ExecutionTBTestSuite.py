from threading import Thread
import time

class ExecutionTBTestSuite:
    dictionary = {}
    
    @staticmethod
    def getBySuite(tbTestSuite):
        return ExecutionTBTestSuite.dictionary.get(tbTestSuite)

    def __init__(self, tbTestSuite, testBed, testSuiteFlags, executorListener):
        self.tbTestSuite = tbTestSuite
        self.testBed = testBed
        self.testSuiteFlags = testSuiteFlags
        self.executorListener = executorListener
        self.nextIndexToExecute = 0
        self.aborted = None
        self.paused = None
        self.status = "Not started"
        ExecutionTBTestSuite.dictionary[tbTestSuite] = self
    
    def markTestCaseAsExecuted(self, tbTestCase):
        self.executedTestCases.append(tbTestCase)
        
    def clearExecutedTestCasesList(self, tbTestCase):
        self.executedTestCases = []
        
    def execute(self):
        for test in self.tbTestSuite.getTestCases():    
            test.cleanup() #Limpia por si se ejecuta la suite por segunda vez
    
        self.suiteRunner = Thread(target = self.executionThread,  args=[])
        self.suiteRunner.start()
        
    def resume(self):
        self.suiteRunner = Thread(target = self.executionThread,  args=[])
        self.suiteRunner.start()
    
    def executionThread(self):
        self.status = "Executing"
        self.tbTestSuite.getSuiteResult().setStartTimestamp(time.time())
        
        for test in self.tbTestSuite.getTestCases()[self.nextIndexToExecute:]:    
            if self.paused == True:
                self.status = "Paused"
                break
            elif self.aborted == True:
                #Se asume que INCONCLUSIVE es el Verdict default de un test case
                self.status = "Aborted"
                self.nextIndexToExecute = 0 #para poder ejecutarlo de nuevo desde 0
                self.tbTestSuite.getSuiteResult().setEndTimestamp(time.time())
                break
            else:
                test.getResult().setStartTimestamp(time.time())
                test.execute() #cuando se usaria cleanup? y que hace?
                test.getResult().setEndTimestamp(time.time())
                self.nextIndexToExecute = self.nextIndexToExecute + 1
        if self.paused == False and self.abort == False:
            self.status = "Completed"
            self.tbTestSuite.getSuiteResult().setEndTimestamp(time.time())
    
    def abort(self):
        self.aborted = True
    
    def pause(self):
        self.paused = True
    
    def getStatus(self):
        return self.status
        
    def getRunStatus(self):
        c = 0
        print 'Execution status: ' + self.getStatus()
        print 'Suite status: ' + self.tbTestSuite.getSuiteResult().getVerdict()
        count = len(self.tbTestSuite.getTestCases())
        percentage = round(self.nextIndexToExecute * 100 / count, 2)
        print 'Executed ' + str(self.nextIndexToExecute) + '/' + str(count) + ' : ' + str(percentage) + '%% completed'
        for test in self.tbTestSuite.getTestCases():
            id = test.getTestMetadata().getAssetID()
            print str(id) + ': ' + test.getResult().getVerdict()
        return self.tbTestSuite.getSuiteResult()