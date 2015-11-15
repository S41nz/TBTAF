class ExecutionTBTestSuite:
    dictionary = {}
    
    @staticmethod
    def getBySuite(tbTestSuite):
        return dictionary.get(tbTestSuite)

    def ___init___(self, tbTestSuite, nodeURLs, testSuiteFlags, executorListener):
        self.tbTestSuite = tbTestSuite
        self.nodeURLs = nodeURLs
        self.testSuiteFlags = testSuiteFlags
        self.executorListener = executorListener
        self.nextIndexToExecute = 0
        self.aborted = None
        self.paused = None
        self.status = "Not started"
        dictionary[tbTestSuite] = self
    
    def markTestCaseAsExecuted(self, tbTestCase):
        self.executedTestCases.append(tbTestCase)
        
    def clearExecutedTestCasesList(self, tbTestCase):
        self.executedTestCases = []
        
    def execute(self):
        for test in self.tbTestSuite.getTestCases():    
            test.cleanup() #Limpia por si se ejecuta la suite por segunda vez
    
        self.suiteRunner = Thread(target = executionThread,  args=[])
        self.suiteRunner.start()
        
    def resume(self):
        self.suiteRunner = Thread(target = executionThread,  args=[])
        self.suiteRunner.start()
    
    def executionThread(self):
        self.status = "Executing"
        
        for test in self.tbTestSuite.getTestCases()[self.nextIndexToExecute]:    
            if self.paused == True:
                self.status = "Paused"
                break
            elif self.aborted == True:
                #Se asume que INCONCLUSIVE es el Verdict default de un test case
                self.status = "Aborted"
                self.nextIndexToExecute = 0 #para poder ejecutarlo de nuevo desde 0
                break
            else:
                test.execute() #cuando se usaría cleanup? y que hace?
                self.nextIndexToExecute = self.nextIndexToExecute + 1
        if self.paused == False and self.abort == False
            self.status = "Completed"
    
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
        print 'Executed ' + self.nextIndexToExecute + '/' + count + ' : ' + percentage + '%% completed'
        for test in self.tbTestSuite.getTestCases():
            name = test.getMetadata().getAssetID()
            if (c < self.nextIndexToExecute):
                print name + ': ' + test.getResult().getVerdict()
            else:
                print name + ': PENDING'