from common.metadata import TBMetadata
from common.sample_test import TBTAFSampleTest
from common.suite import TBTestSuite
from publisher.TBTAFPublisher import TBTAFPublisher
import datetime

''''
@author: mestradago
'''

#create metadata for a test case
myMetadata = TBMetadata("TestCase")
myMetadata.setAssetID("TestCase1")
myMetadata.setTags(["function", "integer", "loop"])
myMetadata.setPriority("High")
myMetadata.setAssetDescription("Test function x")

#create test case and add its metadata
myTestCase = TBTAFSampleTest()
myTestCase.setTestMetadata(myMetadata)
myResult = myTestCase.getResult()
myResult.setStartTimestamp(datetime.datetime.now())
myResult.setEndTimestamp(datetime.datetime.now() + datetime.timedelta(seconds = 5))
print myResult.getStartTimestamp()
print myResult.getEndTimestamp()

#create test suite and add test case
myTestSuite = TBTestSuite("SuiteType1", "SuiteID1")
myTestSuite.addTestCase(myTestCase)

#create metadata for a test case
myMetadata2 = TBMetadata("TestCase")
myMetadata2.setAssetID("TestCase2")
myMetadata2.setTags(["unit test", "function", "initializer"])
myMetadata2.setPriority("2")
myMetadata2.setAssetDescription("Test function y")



#create test case and add its metadata
myTestCase2 = TBTAFSampleTest()
myTestCase2.setTestMetadata(myMetadata2)
myResult2 = myTestCase2.getResult()
myResult2.setStartTimestamp(datetime.datetime.now())
myResult2.setEndTimestamp(datetime.datetime.now() + datetime.timedelta(seconds = 7))

myTestSuite.addTestCase(myTestCase2)

#create publisher instance and publish test plan
myPublisher = TBTAFPublisher()

#test IllegalArgumentException
#myPublisher.PublishTestPlan(myTestSuite, "/asd/asd.html", "html")

myPublisher.PublishTestPlan(myTestSuite, "test_plan.html", "html")

#publishResultReport
myPublisher.PublishResultReport(myTestSuite, "result_report.html", "html")


