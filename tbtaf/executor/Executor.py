'''
Execution class
'''

import datetime
import time
from threading import Thread
from time import sleep

class TBTAFExecutor:

    def ExecuteTests(tbTestSuite, nodeURLs=[], testSuiteFlags=[], executorListener=[]):
  
        #Si estos son opcionales ¿no deberían ser distintas estas condiciones?
        if tbTestSuite is None or nodeURLs is None or testSuiteFlags is None or executorListener is None:
            raise ValueError('Invalid Argument Exception')
        if not checkURLsExist(nodeURLs): #Dummy method
            raise ValueError('Invalid Node Exception')
        if not checkFlagsExist(testSuiteFlags): #Dummy method
            raise ValueError('Invalid Option Exception')
        
        executionTBTestSuite = ExecutionTBTestSuite.getBySuite(tbTestSuite)
        if executionTBTestSuite is None:
            executionTBTestSuite = ExecutionTBTestSuite(tbTestSuite, nodeURLs, testSuiteFlags, executorListener)
        
        if executionTBTestSuite.getStatus() != 'Executing':
            executionTBTestSuite.Execute()
        else:
            raise ValueError('Already Executing Exception')
        
        return tbTestSuite.getSuiteResult()
            
    
    def getStatus(tbTestSuite):
        executionTBTestSuite = ExecutionTbTestSuite.getBySuite(tbTestSuite)
        if executionTBTestSuite is None:
            raise ValueError('Invalid Argument Exception')
        else:
            return executionTBTestSuite.getRunStatus()

        
    def abortExecution(tbTestSuite, background=False):
        executionTBTestSuite = ExecutionTbTestSuite.getBySuite(tbTestSuite)
        status = executionTBTestSuite.getStatus()
        
        if status is None or status != 'Executing':
            raise ValueError('Invalid Argument Exception')
        else:
            if background: '''This doesn't make any sense'''
                thread = Thread(target = abortTestCases,  args=[executionTBTestSuite]) 
                thread.start()
            else:
                abortTestCases(executionTBTestSuite)
            
            return tbTestSuite.getResult()
        
    def abortTestCases(executionTBTestSuite):
        executionTBTestSuite.abort()
        
    
    def pauseExcecution(tbTestSuite, background=False):
        executionTBTestSuite = ExecutionTbTestSuite.getBySuite(tbTestSuite)
        status = executionTBTestSuite.getStatus()
        
        if status is None or status != 'Executing':
            raise ValueError('Invalid Argument Exception')
        else:
            if background: '''This doesn't make any sense'''
                thread = Thread(target = pauseTestCases,  args=[executionTBTestSuite]) 
                thread.start()
            else:
                pauseTestCases(executionTBTestSuite)
            return tbTestSuite.getResult()
        
    def pauseTestCases(executionTBTestSuite):
        executionTBTestSuite.paused = True

        
    def resumeExcecution(tbTestSuite, background=False):
        executionTBTestSuite = ExecutionTbTestSuite.getBySuite(tbTestSuite)
        status = executionTBTestSuite.getStatus()
        
        if status is None or status != 'Paused':
            raise ValueError('Invalid Argument Exception')
        else:
            '''Revisar bien el uso del código de Thread'''
            if background: '''This doesn't make any sense'''
                thread = Thread(target = resumeTestCases,  args=[executionTBTestSuite]) 
                thread.start()
            else:
                resumeTestCases(tbTestSuite)
            
    def resumeTestCases(executionTBTestSuite):
        executionTBTestSuite.resume()