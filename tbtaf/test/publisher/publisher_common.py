from __future__ import absolute_import
from common.metadata import TBMetadata
from common.sample_test import TBTAFSampleTest
from common.suite import TBTestSuite
from common.enums.metadata_type import TBTAFMetadataType
from common.enums.suite_type import TBTAFTestSuiteType
from publisher.TBTAFPublisher import TBTAFPublisher
import datetime

''''
@author: @andresmuro , @andres.alvarado , @mestradago , @rnunezc
'''

def setupValidMetadata(type,id,tags,priority,description):
    #create metadata for a test case
    myMetadata = TBMetadata(type)
    myMetadata.setAssetID(id)
    myMetadata.setTags(tags)
    myMetadata.setPriority(priority)
    myMetadata.setAssetDescription(description)
    return myMetadata

def createTestCase(metadata,delta):
    #create test case and add its metadata
    myTestCase = TBTAFSampleTest()
    myTestCase.setTestMetadata(metadata)
    myTestCase.getResult().setStartTimestamp(datetime.datetime.now())
    myTestCase.getResult().setEndTimestamp(datetime.datetime.now() + datetime.timedelta(seconds = delta))
    return myTestCase

def createTestSuite(type,id):
    #create test suite
    myTestSuite = TBTestSuite(type,id)
    return myTestSuite
    
def addTestCase(testSuite,testCase):
    #add test case
    testSuite.addTestCase(testCase)

def createPublisher():
    #create publisher instance and publish test plan
    myPublisher = TBTAFPublisher()
    return myPublisher

