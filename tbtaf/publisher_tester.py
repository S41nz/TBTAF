from common.metadata import TBMetadata
from common.sample_test import TBTAFSampleTest
from common.suite import TBTestSuite
from publisher.TBTAFPublisher import TBTAFPublisher

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

#create test suite and add test case
myTestSuite = TBTestSuite("SuiteType1", "SuiteID1")
myTestSuite.addTestCase(myTestCase)

#create publisher instance and publish test plan
myPublisher = TBTAFPublisher()
myPublisher.PublishTestPlan(myTestSuite, "x", "x")

