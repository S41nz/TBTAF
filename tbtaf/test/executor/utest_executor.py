from __future__ import absolute_import
from __future__ import print_function
from executor.Executor import TBTAFExecutor
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

        
def invalidInputExecuteTests():
    ejecutor = TBTAFExecutor()
    ejecutor.executeTests(None)
    
def validInputExecuteTests():
    ejecutor = TBTAFExecutor()
    suite = TBTestSuite(1,'Sample test')
    for i in range(3):
        newTest = TBTAFSampleTest()
        suite.addTestCase(newTest)
    ejecutor.executeTests(suite)
    
    waitingComplete = True
    while waitingComplete:
        result = ejecutor.getStatus(suite)
        time.sleep(5)
        waitingComplete = result.getExecutionStatusType() != TBTAFExecutionStatusType.COMPLETED

def invalidInputAbortExecution():
    ejecutor = TBTAFExecutor()
    suite = TBTestSuite(1,'Sample test')
    for i in range(3):
        newTest = TBTAFSampleTest()
        suite.addTestCase(newTest)
    ejecutor.abortExecution(suite)
    
def validInputAbortExecution():
    ejecutor = TBTAFExecutor()
    suite = TBTestSuite(1,'Sample test 2')
    for i in range(3):
        newTest = TBTAFSampleTest()
        suite.addTestCase(newTest)
    ejecutor.executeTests(suite)
    time.sleep(10)
    ejecutor.abortExecution(suite)
    ejecutor.getStatus(suite)

def invalidInputPauseExecution():
    ejecutor = TBTAFExecutor()
    suite = TBTestSuite(1,'Sample test 3')
    for i in range(3):
        newTest = TBTAFSampleTest()
        suite.addTestCase(newTest)
    ejecutor.pauseExecution(suite)

def invalidInputResumeExecution():
    ejecutor = TBTAFExecutor()
    suite = TBTestSuite(1,'Sample test 4')
    for i in range(3):
        newTest = TBTAFSampleTest()
        suite.addTestCase(newTest)
    ejecutor.resumeExecution(suite)
    
def validInputPauseResumeExecution():
    ejecutor = TBTAFExecutor()
    suite = TBTestSuite(1,'Sample test 5')
    for i in range(3):
        newTest = TBTAFSampleTest()
        suite.addTestCase(newTest)
    ejecutor.executeTests(suite)
    time.sleep(10)
    ejecutor.pauseExecution(suite)
    ejecutor.getStatus(suite)
    time.sleep(10)
    ejecutor.getStatus(suite)
    ejecutor.resumeExecution(suite)
    
    waitingComplete = True
    while waitingComplete:
        result = ejecutor.getStatus(suite)
        time.sleep(5)
        waitingComplete = result.getExecutionStatusType() != TBTAFExecutionStatusType.COMPLETED
    
def invalidInputGetStatus():
    ejecutor = TBTAFExecutor()
    ejecutor.getStatus(None)

testInvalid('invalidInputExecuteTests')
testValid('validInputExecuteTests')
testInvalid('invalidInputAbortExecution')
testValid('validInputAbortExecution')
testInvalid('invalidInputPauseExecution')
testInvalid('invalidInputResumeExecution')
testValid('validInputPauseResumeExecution')
testInvalid('invalidInputGetStatus')
print("Passed " + str(passed) + " out of " + str(total))