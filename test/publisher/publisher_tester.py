from common.sample_test import TBTAFSampleTest
from common.metadata import TBMetadata
from common.suite import TBTestSuite
from common.enums.suite_type import TBTAFTestSuiteType
from common.enums.metadata_type import TBTAFMetadataType
from publisher.TBTAFPublisher import TBTAFPublisher
from common.exception.IllegalArgumentException import IllegalArgumentException
from common.exception.NonSupportedFormatException import NonSupportedFormatException
import publisher_common
import datetime

''''
@author: @andresmuro , @andres.alvarado , @mestradago , @rnunezc
'''

def validTestPlan():
    try:
        metadata1 = publisher_common.setupValidMetadata(TBTAFMetadataType.TEST_CODE,"TestCase1",["UnitTest", "Release1.0", "ModuleX"],1,"Test Module X")
        metadata2 = publisher_common.setupValidMetadata(TBTAFMetadataType.PRODUCT_CODE,"TestCase2",["UnitTest", "Release1.0", "ModuleY"],2,"Test Module Y")
        testCase1 = publisher_common.createTestCase(metadata1,15)
        testCase2 = publisher_common.createTestCase(metadata2,7)
        testSuite = publisher_common.createTestSuite(TBTAFTestSuiteType.NORMAL,"TestSuite1")
        publisher_common.addTestCase(testSuite,testCase1)
        publisher_common.addTestCase(testSuite,testCase2)
        publisher = publisher_common.createPublisher()
        publisher.PublishTestPlan(testSuite, "test_plan.html", "html")
        print "Valid Test Plan : PASSED"
    except Exception as e:
        print "Valid Test Plan exception not expected but thrown: " + str(e) + " : FAILED"

def validResultReport():
    try:
        metadata1 = publisher_common.setupValidMetadata(TBTAFMetadataType.TEST_CODE,"TestCase1",["UnitTest", "Release1.0", "ModuleX"],1,"Test Module X")
        metadata2 = publisher_common.setupValidMetadata(TBTAFMetadataType.PRODUCT_CODE,"TestCase2",["UnitTest", "Release1.0", "ModuleY"],2,"Test Module Y")
        testCase1 = publisher_common.createTestCase(metadata1,15)
        testCase2 = publisher_common.createTestCase(metadata2,7)
        testSuite = publisher_common.createTestSuite(TBTAFTestSuiteType.NORMAL,"TestSuite1")
        publisher_common.addTestCase(testSuite,testCase1)
        publisher_common.addTestCase(testSuite,testCase2)
        publisher = publisher_common.createPublisher()
        publisher.PublishResultReport(testSuite, "result_report.html", "html")
        print "Valid Result Report : PASSED"
    except Exception as e:
        print "Valid Result Report exception not expected but thrown: " + str(e) + " : FAILED"
        
def invalidFormatFlagTestPlan():
    try:
        metadata1 = publisher_common.setupValidMetadata(TBTAFMetadataType.TEST_CODE,"TestCase1",["UnitTest", "Release1.0", "ModuleX"],1,"Test Module X")
        metadata2 = publisher_common.setupValidMetadata(TBTAFMetadataType.PRODUCT_CODE,"TestCase2",["UnitTest", "Release1.0", "ModuleY"],2,"Test Module Y")
        testCase1 = publisher_common.createTestCase(metadata1,15)
        testCase2 = publisher_common.createTestCase(metadata2,7)
        testSuite = publisher_common.createTestSuite(TBTAFTestSuiteType.NORMAL,"TestSuite1")
        publisher_common.addTestCase(testSuite,testCase1)
        publisher_common.addTestCase(testSuite,testCase2)
        publisher = publisher_common.createPublisher()
        publisher.PublishTestPlan(testSuite, "test_plan.pdf", "pdf")
        print "Invalid Format Flag Test Plan exception expected but not thrown : FAILED"
    except NonSupportedFormatException as e:
        print "Invalid Format Flag Test Plan : PASSED"
        
def invalidFileExtensionTestPlan():
    try:
        metadata1 = publisher_common.setupValidMetadata(TBTAFMetadataType.TEST_CODE,"TestCase1",["UnitTest", "Release1.0", "ModuleX"],1,"Test Module X")
        metadata2 = publisher_common.setupValidMetadata(TBTAFMetadataType.PRODUCT_CODE,"TestCase2",["UnitTest", "Release1.0", "ModuleY"],2,"Test Module Y")
        testCase1 = publisher_common.createTestCase(metadata1,15)
        testCase2 = publisher_common.createTestCase(metadata2,7)
        testSuite = publisher_common.createTestSuite(TBTAFTestSuiteType.NORMAL,"TestSuite1")
        publisher_common.addTestCase(testSuite,testCase1)
        publisher_common.addTestCase(testSuite,testCase2)
        publisher = publisher_common.createPublisher()
        publisher.PublishTestPlan(testSuite, "test_plan.pdf", "html")
        print "Invalid File Extension Test Plan exception expected but not thrown : FAILED"
    except NonSupportedFormatException as e:
        print "Invalid File Extension Test Plan : PASSED"

def invalidFilePathTestPlan():
    try:
        metadata1 = publisher_common.setupValidMetadata(TBTAFMetadataType.TEST_CODE,"TestCase1",["UnitTest", "Release1.0", "ModuleX"],1,"Test Module X")
        metadata2 = publisher_common.setupValidMetadata(TBTAFMetadataType.PRODUCT_CODE,"TestCase2",["UnitTest", "Release1.0", "ModuleY"],2,"Test Module Y")
        testCase1 = publisher_common.createTestCase(metadata1,15)
        testCase2 = publisher_common.createTestCase(metadata2,7)
        testSuite = publisher_common.createTestSuite(TBTAFTestSuiteType.NORMAL,"TestSuite1")
        publisher_common.addTestCase(testSuite,testCase1)
        publisher_common.addTestCase(testSuite,testCase2)
        publisher = publisher_common.createPublisher()
        publisher.PublishTestPlan(testSuite, "../invalid/test_plan.html", "html")
        print "Invalid File Path Test Plan exception expected but not thrown : FAILED"
    except IllegalArgumentException as e:
        print "Invalid File Path Test Plan : PASSED"
        
def invalidFormatFlagResultReport():
    try:
        metadata1 = publisher_common.setupValidMetadata(TBTAFMetadataType.TEST_CODE,"TestCase1",["UnitTest", "Release1.0", "ModuleX"],1,"Test Module X")
        metadata2 = publisher_common.setupValidMetadata(TBTAFMetadataType.PRODUCT_CODE,"TestCase2",["UnitTest", "Release1.0", "ModuleY"],2,"Test Module Y")
        testCase1 = publisher_common.createTestCase(metadata1,15)
        testCase2 = publisher_common.createTestCase(metadata2,7)
        testSuite = publisher_common.createTestSuite(TBTAFTestSuiteType.NORMAL,"TestSuite1")
        publisher_common.addTestCase(testSuite,testCase1)
        publisher_common.addTestCase(testSuite,testCase2)
        publisher = publisher_common.createPublisher()
        publisher.PublishResultReport(testSuite, "test_report.pdf", "pdf")
        print "Invalid Format Flag Test Plan exception expected but not thrown : FAILED"
    except NonSupportedFormatException as e:
        print "Invalid Format Flag Test Plan : PASSED"
        
def invalidFileExtensionResultReport():
    try:
        metadata1 = publisher_common.setupValidMetadata(TBTAFMetadataType.TEST_CODE,"TestCase1",["UnitTest", "Release1.0", "ModuleX"],1,"Test Module X")
        metadata2 = publisher_common.setupValidMetadata(TBTAFMetadataType.PRODUCT_CODE,"TestCase2",["UnitTest", "Release1.0", "ModuleY"],2,"Test Module Y")
        testCase1 = publisher_common.createTestCase(metadata1,15)
        testCase2 = publisher_common.createTestCase(metadata2,7)
        testSuite = publisher_common.createTestSuite(TBTAFTestSuiteType.NORMAL,"TestSuite1")
        publisher_common.addTestCase(testSuite,testCase1)
        publisher_common.addTestCase(testSuite,testCase2)
        publisher = publisher_common.createPublisher()
        publisher.PublishResultReport(testSuite, "test_report.pdf", "html")
        print "Invalid File Extension Test Plan exception expected but not thrown : FAILED"
    except NonSupportedFormatException as e:
        print "Invalid File Extension Test Plan : PASSED"

def invalidFilePathResultReport():
    try:
        metadata1 = publisher_common.setupValidMetadata(TBTAFMetadataType.TEST_CODE,"TestCase1",["UnitTest", "Release1.0", "ModuleX"],1,"Test Module X")
        metadata2 = publisher_common.setupValidMetadata(TBTAFMetadataType.PRODUCT_CODE,"TestCase2",["UnitTest", "Release1.0", "ModuleY"],2,"Test Module Y")
        testCase1 = publisher_common.createTestCase(metadata1,15)
        testCase2 = publisher_common.createTestCase(metadata2,7)
        testSuite = publisher_common.createTestSuite(TBTAFTestSuiteType.NORMAL,"TestSuite1")
        publisher_common.addTestCase(testSuite,testCase1)
        publisher_common.addTestCase(testSuite,testCase2)
        publisher = publisher_common.createPublisher()
        publisher.PublishResultReport(testSuite, "../invalid/test_report.html", "html")
        print "Invalid File Path Test Plan exception expected but not thrown : FAILED"
    except IllegalArgumentException as e:
        print "Invalid File Path Test Plan : PASSED"

validTestPlan()
validResultReport()
invalidFormatFlagTestPlan()
invalidFileExtensionTestPlan()
invalidFilePathTestPlan()
invalidFormatFlagResultReport()
invalidFileExtensionResultReport()
invalidFilePathResultReport()

