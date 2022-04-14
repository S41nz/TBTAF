from __future__ import absolute_import
from __future__ import print_function
from executor.Executor import TBTAFExecutor
from executor.ExecutionTBTestSuite import ExecutionTBTestSuite
from common.suite import TBTestSuite
from common.sample_test import TBTAFSampleTest
from common.enums.execution_status_type import TBTAFExecutionStatusType
import time
import sys
from six.moves import range

total = 0
passed = 0

def testInvalid(method):
    global total
    global passed
    total = total + 1
    try:
        save_stdout = sys.stdout
        sys.stdout = open('trash', 'w')
        globals()[method]()
        sys.stdout = save_stdout
        print(method + ': exception expected but not thrown')
    except:
        sys.stdout = save_stdout
        print(method + ": PASSED")
        passed = passed + 1

def testValid(method):
    global total
    global passed
    total = total + 1
    #globals()[method]()
    try:
        save_stdout = sys.stdout
        sys.stdout = open('trash', 'w')
        globals()[method]()
        sys.stdout = save_stdout
        print(method + ": PASSED")
        passed = passed + 1
    except Exception as e:
        sys.stdout = save_stdout
        print(method + ': exception not expected but thrown: ' + str(e))

# TESTS #
def invalidGetBySuite():
    tbTestSuite = None
    executionTBTestSuite = ExecutionTBTestSuite.getBySuite(tbTestSuite)

def validGetBySuiteAndInit():
    tbTestSuite = TBTestSuite(1,'Sample test')
    for i in range(3):
        newTest = TBTAFSampleTest()
        tbTestSuite.addTestCase(newTest)

    executionTBTestSuite = ExecutionTBTestSuite.getBySuite(tbTestSuite)
    if executionTBTestSuite is None:
        executionTBTestSuite = ExecutionTBTestSuite(tbTestSuite)

def invalidInit():
    tbTestSuite = None
    executionTBTestSuite = ExecutionTBTestSuite(tbTestSuite)

def validExecute():
    tbTestSuite = TBTestSuite(1,'Sample test 1')
    for i in range(3):
        newTest = TBTAFSampleTest()
        tbTestSuite.addTestCase(newTest)

    executionTBTestSuite = ExecutionTBTestSuite(tbTestSuite)
    executionTBTestSuite.execute()
    
    waitingComplete = True
    while waitingComplete:
        result = executionTBTestSuite.getStatus()
        time.sleep(5)
        waitingComplete = result != TBTAFExecutionStatusType.COMPLETED

def invalidExecute():
    tbTestSuite = TBTestSuite(1,'Sample test 2')
    for i in range(3):
        newTest = TBTAFSampleTest()
        tbTestSuite.addTestCase(newTest)

    executionTBTestSuite = ExecutionTBTestSuite(tbTestSuite)
    executionTBTestSuite.execute()
    time.sleep(1)
    executionTBTestSuite.execute()

def invalidResume():
    tbTestSuite = TBTestSuite(1,'Sample test 2')
    for i in range(3):
        newTest = TBTAFSampleTest()
        tbTestSuite.addTestCase(newTest)

    executionTBTestSuite = ExecutionTBTestSuite(tbTestSuite)
    executionTBTestSuite.resume()
    
def validPauseResume():
    tbTestSuite = TBTestSuite(1,'Sample test 2')
    for i in range(3):
        newTest = TBTAFSampleTest()
        tbTestSuite.addTestCase(newTest)

    executionTBTestSuite = ExecutionTBTestSuite(tbTestSuite)
    executionTBTestSuite.execute()
    time.sleep(1)
    executionTBTestSuite.pause()
    time.sleep(10)
    executionTBTestSuite.resume()
    
    waitingComplete = True
    while waitingComplete:
        result = executionTBTestSuite.getStatus()
        time.sleep(5)
        waitingComplete = result != TBTAFExecutionStatusType.COMPLETED

def invalidPause():
    tbTestSuite = TBTestSuite(1,'Sample test 3')
    for i in range(3):
        newTest = TBTAFSampleTest()
        tbTestSuite.addTestCase(newTest)

    executionTBTestSuite = ExecutionTBTestSuite(tbTestSuite)
    executionTBTestSuite.pause()
    
def invalidAbort():
    tbTestSuite = TBTestSuite(1,'Sample test 3')
    for i in range(3):
        newTest = TBTAFSampleTest()
        tbTestSuite.addTestCase(newTest)

    executionTBTestSuite = ExecutionTBTestSuite(tbTestSuite)
    executionTBTestSuite.abort()
    
def validAbortRestart():
    tbTestSuite = TBTestSuite(1,'Sample test 2')
    for i in range(3):
        newTest = TBTAFSampleTest()
        tbTestSuite.addTestCase(newTest)

    executionTBTestSuite = ExecutionTBTestSuite(tbTestSuite)
    executionTBTestSuite.execute()
    time.sleep(1)
    executionTBTestSuite.abort()
    time.sleep(10)
    executionTBTestSuite.execute()
    
    waitingComplete = True
    while waitingComplete:
        result = executionTBTestSuite.getStatus()
        time.sleep(5)
        waitingComplete = result != TBTAFExecutionStatusType.COMPLETED
        
def validGetRunStatus():
    tbTestSuite = TBTestSuite(1,'Sample test 3')
    for i in range(3):
        newTest = TBTAFSampleTest()
        tbTestSuite.addTestCase(newTest)
    executionTBTestSuite = ExecutionTBTestSuite(tbTestSuite)
    executionTBTestSuite.getRunStatus() #before
    executionTBTestSuite.execute()
    waitingComplete = True
    while waitingComplete:
        result = executionTBTestSuite.getStatus()
        time.sleep(5)
        waitingComplete = result != TBTAFExecutionStatusType.COMPLETED
    
    executionTBTestSuite.getRunStatus() #and after

def invalidGetRunStatus():
    tbTestSuite = TBTestSuite(1,'Sample test 4')
    executionTBTestSuite = ExecutionTBTestSuite(tbTestSuite)
    executionTBTestSuite.getRunStatus()
    
    
    
testInvalid('invalidGetBySuite')
testValid('validGetBySuiteAndInit')
testInvalid('invalidInit')
testValid('validExecute')
testInvalid('invalidExecute')
testInvalid('invalidResume')
testValid('validPauseResume')
testInvalid('invalidPause')
testInvalid('invalidAbort')
testValid('validAbortRestart')
testValid('validGetRunStatus')
testInvalid('invalidGetRunStatus')

print("Passed " + str(passed) + " out of " + str(total))