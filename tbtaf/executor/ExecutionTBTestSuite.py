from __future__ import absolute_import
from __future__ import print_function
from .TBTAFExecutionStatus import TBTAFExecutionStatus
from common.enums.execution_status_type import TBTAFExecutionStatusType
from threading import Thread
import time
import datetime

class ExecutionTBTestSuite:
    dictionary = {}
    
    @staticmethod
    def getBySuite(tbTestSuite):
        if tbTestSuite is None:
            raise ValueError('Invalid Argument Exception')
        return ExecutionTBTestSuite.dictionary.get(tbTestSuite)

    def __init__(self, tbTestSuite, testBed='dummy', testSuiteFlags=[], executorListener=[]):
        if tbTestSuite is None or testBed is None or testSuiteFlags is None or executorListener is None:
            raise ValueError('Invalid Argument Exception')
        self.tbTestSuite = tbTestSuite
        self.testBed = testBed
        self.testSuiteFlags = testSuiteFlags
        self.executorListener = executorListener
        self.nextIndexToExecute = 0
        self.aborted = False
        self.paused = False
        self.status = TBTAFExecutionStatusType.NOT_STARTED
        self.statusWrapper = TBTAFExecutionStatus()
        ExecutionTBTestSuite.dictionary[tbTestSuite] = self
    
    def execute(self):
        if self.status != TBTAFExecutionStatusType.NOT_STARTED and self.status != TBTAFExecutionStatusType.ABORTED:
            raise Exception('The suite is already being executed or it is paused')
        
        for test in self.tbTestSuite.getTestCases():    
            test.setup()
    
        self.suiteRunner = Thread(target = self.executionThread,  args=[])
        self.suiteRunner.start()
        
    def resume(self):
        if self.status != TBTAFExecutionStatusType.PAUSED:
            raise Exception('The suite is not paused')
        self.paused = False
        self.suiteRunner = Thread(target = self.executionThread,  args=[])
        self.suiteRunner.start()
    
    def executionThread(self):
        self.status = TBTAFExecutionStatusType.EXECUTING
        #self.tbTestSuite.getSuiteResult().setStartTimestamp(datetime.datetime.now()) #per Muro
        
        for test in self.tbTestSuite.getTestCases()[self.nextIndexToExecute:]:    
            if self.paused == True:
                self.status = TBTAFExecutionStatusType.PAUSED
                break
            elif self.aborted == True:
                #Se asume que INCONCLUSIVE es el Verdict default de un test case
                self.status = TBTAFExecutionStatusType.ABORTED
                self.nextIndexToExecute = 0 #para poder ejecutarlo de nuevo desde 0
                #self.tbTestSuite.getSuiteResult().setEndTimestamp(datetime.datetime.now()) #per Muro
                self.aborted = False
                break
            else:
                # Don't call test.getResult().setStartTimestamp() method here due to some TBTestCase classes 
                # reset testResult property on their execute() method.
                startTime = datetime.datetime.now()
                try:    
                    test.execute()
                except Exception as e:
                    print('Exception found while executing test ' + str(test.getTestMetadata().getAssetID()) + '. The exception thrown was: ' + str(e))
                test.getResult().setStartTimestamp(startTime)
                test.getResult().setEndTimestamp(datetime.datetime.now())
                test.verdict()
                self.nextIndexToExecute = self.nextIndexToExecute + 1
        if self.status != TBTAFExecutionStatusType.PAUSED and self.status != TBTAFExecutionStatusType.ABORTED:
            self.status = TBTAFExecutionStatusType.COMPLETED
            #self.tbTestSuite.getSuiteResult().setEndTimestamp(datetime.datetime.now()) #per Muro
        
        if self.status == TBTAFExecutionStatusType.COMPLETED or self.status == TBTAFExecutionStatusType.ABORTED:
            for test in self.tbTestSuite.getTestCases():    
                test.cleanup()
    
    def abort(self):
        if self.status != TBTAFExecutionStatusType.EXECUTING:
            raise Exception('The suite is not executing')
        self.status = TBTAFExecutionStatusType.ABORTING
        self.aborted = True
    
    def pause(self):
        if self.status != TBTAFExecutionStatusType.EXECUTING:
            raise Exception('The suite is not executing')
        self.status = TBTAFExecutionStatusType.PAUSING
        self.paused = True
    
    def getStatus(self):
        return self.status
        
    def getRunStatus(self):
        c = 0
        #print 'Execution status: ' + self.getStatus()
        #print 'Suite status: ' + self.tbTestSuite.getSuiteResult().getVerdict()
        count = len(self.tbTestSuite.getTestCases())
        if count < 1:
            raise Exception('The suite does not have test cases')
        percentage = round(self.nextIndexToExecute * 100.0 / count, 2)
        print('Executed ' + str(self.nextIndexToExecute) + '/' + str(count) + ' : ' + str(percentage) + '% completed')
        '''for test in self.tbTestSuite.getTestCases():
            try:
                id = test.getTestMetadata().getAssetID()
                print str(id) + ': ' + test.getResult().getVerdict()
            except:
                print 'Cannot get result for test: ' + str(id)'''
        
        self.statusWrapper.setExecutionStatusType(self.getStatus())
        self.statusWrapper.setSuiteResult(self.tbTestSuite.getSuiteResult())
        self.statusWrapper.setTestCasesTotal(count)
        self.statusWrapper.setTestCasesExecuted(self.nextIndexToExecute)
        
        return self.statusWrapper;