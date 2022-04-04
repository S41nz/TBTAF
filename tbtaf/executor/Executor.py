'''
Execution class
'''

from __future__ import absolute_import
import datetime
import time
from threading import Thread
from time import sleep
from .ExecutionTBTestSuite import ExecutionTBTestSuite

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
        executionTBTestSuite = ExecutionTBTestSuite.getBySuite(tbTestSuite)
        status = executionTBTestSuite.getStatus()
        
        if status is None or status != 'Executing':
            raise ValueError('Invalid Argument Exception')
        else:
            '''
            This doesn't make any sense
            '''
            if background: 
                thread = Thread(target = self.abortTestCases, args=[executionTBTestSuite])
                thread.start()
            else:
                self.abortTestCases(executionTBTestSuite)
            
            return tbTestSuite.getSuiteResult()
        
    def abortTestCases(self, executionTBTestSuite):
        executionTBTestSuite.abort()
        
    
    def pauseExecution(self, tbTestSuite, background=False):
        executionTBTestSuite = ExecutionTBTestSuite.getBySuite(tbTestSuite)
        status = executionTBTestSuite.getStatus()
        
        if status is None or status != 'Executing':
            raise ValueError('Invalid Argument Exception')
        else:
            '''
            This doesn't make any sense
            '''
            if background: 
                thread = Thread(target = self.pauseTestCases,  args=[executionTBTestSuite]) 
                thread.start()
            else:
                self.pauseTestCases(executionTBTestSuite)
            return tbTestSuite.getSuiteResult()
        
    def pauseTestCases(self, executionTBTestSuite):
        executionTBTestSuite.pause()

        
    def resumeExecution(self, tbTestSuite, background=False):
        executionTBTestSuite = ExecutionTBTestSuite.getBySuite(tbTestSuite)
        status = executionTBTestSuite.getStatus()
        
        if status is None or status != 'Paused':
            raise ValueError('Invalid Argument Exception')
        else:
            '''
            Revisar bien el uso del codigo de Thread
            '''
            if background:
                thread = Thread(target = self.resumeTestCases,  args=[executionTBTestSuite]) 
                thread.start()
            else:
                self.resumeTestCases(executionTBTestSuite)
            
    def resumeTestCases(self, executionTBTestSuite):
        executionTBTestSuite.resume()