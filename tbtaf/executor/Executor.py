'''
Execution class
'''

import datetime
import time
from threading import Thread
from time import sleep
from ExecutionTBTestSuite import ExecutionTBTestSuite

class TBTAFExecutor:

    def validateTestBed(self, parameter):
        return True
        
    def checkFlagsExist(self, parameter):
        return True

    def executeTests(self, tbTestSuite, testBed='dummy', testSuiteFlags=[], executorListener=[]):
  
        #Si estos son opcionales no deberian ser distintas estas condiciones?
        if tbTestSuite is None or testBed is None or testSuiteFlags is None or executorListener is None:
            raise ValueError('Invalid Argument Exception')
        if not self.validateTestBed(testBed): #Dummy method
            raise ValueError('Invalid Node Exception')
        if not self.checkFlagsExist(testSuiteFlags): #Dummy method
            raise ValueError('Invalid Option Exception')
        
        executionTBTestSuite = ExecutionTBTestSuite.getBySuite(tbTestSuite)
        if executionTBTestSuite is None:
            executionTBTestSuite = ExecutionTBTestSuite(tbTestSuite, testBed, testSuiteFlags, executorListener)
        
        if executionTBTestSuite.getStatus() != 'Executing':
            executionTBTestSuite.execute()
        else:
            raise ValueError('Already Executing Exception')
        
        return tbTestSuite.getSuiteResult()
            
    
    def getStatus(self, tbTestSuite):
        executionTBTestSuite = ExecutionTBTestSuite.getBySuite(tbTestSuite)
        if executionTBTestSuite is None:
            raise ValueError('Invalid Argument Exception')
        else:
            return executionTBTestSuite.getRunStatus()

        
    def abortExecution(self, tbTestSuite, background=False):
        executionTBTestSuite = ExecutionTbTestSuite.getBySuite(tbTestSuite)
        status = executionTBTestSuite.getStatus()
        
        if status is None or status != 'Executing':
            raise ValueError('Invalid Argument Exception')
        else:
            '''
            This doesn't make any sense
            '''
            if background: 
                thread = Thread(target = abortTestCases, args=[executionTBTestSuite])
                thread.start()
            else:
                abortTestCases(executionTBTestSuite)
            
            return tbTestSuite.getResult()
        
    def abortTestCases(self, executionTBTestSuite):
        executionTBTestSuite.abort()
        
    
    def pauseExcecution(self, tbTestSuite, background=False):
        executionTBTestSuite = ExecutionTbTestSuite.getBySuite(tbTestSuite)
        status = executionTBTestSuite.getStatus()
        
        if status is None or status != 'Executing':
            raise ValueError('Invalid Argument Exception')
        else:
            '''
            This doesn't make any sense
            '''
            if background: 
                thread = Thread(target = pauseTestCases,  args=[executionTBTestSuite]) 
                thread.start()
            else:
                pauseTestCases(executionTBTestSuite)
            return tbTestSuite.getResult()
        
    def pauseTestCases(self, executionTBTestSuite):
        executionTBTestSuite.paused = True

        
    def resumeExcecution(self, tbTestSuite, background=False):
        executionTBTestSuite = ExecutionTbTestSuite.getBySuite(tbTestSuite)
        status = executionTBTestSuite.getStatus()
        
        if status is None or status != 'Paused':
            raise ValueError('Invalid Argument Exception')
        else:
            '''
            Revisar bien el uso del codigo de Thread
            '''
            if background:
                thread = Thread(target = resumeTestCases,  args=[executionTBTestSuite]) 
                thread.start()
            else:
                resumeTestCases(tbTestSuite)
            
    def resumeTestCases(self, executionTBTestSuite):
        executionTBTestSuite.resume()

        executionTBTestSuite.resume()