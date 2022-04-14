from __future__ import absolute_import
from __future__ import print_function
from executor.TBTAFExecutionStatus import TBTAFExecutionStatus
from common.enums.execution_status_type import TBTAFExecutionStatusType
from common.suite import TBTestSuite
from common.sample_test import TBTAFSampleTest
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
def validSetAndGetExecutionStatusType():
    tbtafExecutionStatus = TBTAFExecutionStatus()
    tbtafExecutionStatus.setExecutionStatusType(TBTAFExecutionStatusType.COMPLETED)
    result = tbtafExecutionStatus.getExecutionStatusType()
    if result != TBTAFExecutionStatusType.COMPLETED:
        raise Exception('The value returned is not the same that was set')

def validSetAndGetSuiteResult():
    tbTestSuite = TBTestSuite(1,'Sample test 1')
    for i in range(3):
        newTest = TBTAFSampleTest()
        tbTestSuite.addTestCase(newTest)

    temp = tbTestSuite.getSuiteResult()
    
    tbtafExecutionStatus = TBTAFExecutionStatus()
    tbtafExecutionStatus.setSuiteResult(temp)
    result = tbtafExecutionStatus.getSuiteResult()
    if result != temp:
        raise Exception('The value returned is not the same that was set')
        
def validGetCompletionPercentage():
    tbtafExecutionStatus = TBTAFExecutionStatus()
    tbtafExecutionStatus.setTestCasesTotal(10)
    tbtafExecutionStatus.setTestCasesExecuted(3)
    result = tbtafExecutionStatus.getCompletionPercentage()
    if result != 30.00:
        raise Exception('The calculation is wrong')
        
def validSetAndGetTestCasesTotal():
    tbtafExecutionStatus = TBTAFExecutionStatus()
    tbtafExecutionStatus.setTestCasesTotal(10)
    result = tbtafExecutionStatus.getTestCasesTotal()
    if result != 10:
        raise Exception('The value returned is not the same that was set')
        
def validSetAndGetTestCasesExecuted():
    tbtafExecutionStatus = TBTAFExecutionStatus()
    tbtafExecutionStatus.setTestCasesExecuted(3)
    result = tbtafExecutionStatus.getTestCasesExecuted()
    if result != 3:
        raise Exception('The value returned is not the same that was set')
        
def invalidGetCompletionPercentage1():
    tbtafExecutionStatus = TBTAFExecutionStatus()
    tbtafExecutionStatus.setTestCasesTotal(10)
    result = tbtafExecutionStatus.getCompletionPercentage()
        
def invalidGetCompletionPercentage2():
    tbtafExecutionStatus = TBTAFExecutionStatus()
    tbtafExecutionStatus.setTestCasesExecuted(3)
    result = tbtafExecutionStatus.getCompletionPercentage()
        
testValid('validSetAndGetExecutionStatusType')
testValid('validSetAndGetSuiteResult')
testValid('validGetCompletionPercentage')
testValid('validSetAndGetTestCasesTotal')
testValid('validSetAndGetTestCasesExecuted')
testInvalid('invalidGetCompletionPercentage1')
testInvalid('invalidGetCompletionPercentage2')

print("Passed " + str(passed) + " out of " + str(total))