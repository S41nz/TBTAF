from __future__ import absolute_import
from executor.Executor import TBTAFExecutor
from common.suite import TBTestSuite
from common.sample_test import TBTAFSampleTest
import time
from six.moves import range

def sample_run():
    ejecutor = TBTAFExecutor()
    suite = TBTestSuite(1,'A')
    for i in range(5):
        newTest = TBTAFSampleTest()
        suite.addTestCase(newTest)
    ejecutor.executeTests(suite)
    
    while True:
        ejecutor.getStatus(suite)
        time.sleep(10)
        
sample_run()