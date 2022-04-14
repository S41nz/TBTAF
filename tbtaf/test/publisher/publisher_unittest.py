from __future__ import absolute_import
from __future__ import print_function
from common.enums.suite_type import TBTAFTestSuiteType
from common.enums.metadata_type import TBTAFMetadataType
from publisher.TBTAFPublisher import TBTAFPublisher
from common.exception.IllegalArgumentException import IllegalArgumentException
from common.exception.NonSupportedFormatException import NonSupportedFormatException
import publisher_common
import unittest

class PublisherUnitTest(unittest.TestCase):
    
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
            publisher.PublishTestPlan(testSuite, "test_plan.pdf", "PDF")
            print("Valid Test Plan : PASSED")
        except Exception as e:
            print("Valid Test Plan exception not expected but thrown: " + str(e) + " : FAILED")

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
            publisher.PublishResultReport(testSuite, "result_report.pdf", "PDF")
            print("Valid Result Report : PASSED")
        except Exception as e:
            print("Valid Result Report exception not expected but thrown: " + str(e) + " : FAILED")
        
    def invalidFlagFormatTestPlan():
        try:
            metadata1 = publisher_common.setupValidMetadata(TBTAFMetadataType.TEST_CODE,"TestCase1",["UnitTest", "Release1.0", "ModuleX"],1,"Test Module X")
            metadata2 = publisher_common.setupValidMetadata(TBTAFMetadataType.PRODUCT_CODE,"TestCase2",["UnitTest", "Release1.0", "ModuleY"],2,"Test Module Y")
            testCase1 = publisher_common.createTestCase(metadata1,15)
            testCase2 = publisher_common.createTestCase(metadata2,7)
            testSuite = publisher_common.createTestSuite(TBTAFTestSuiteType.NORMAL,"TestSuite1")
            publisher_common.addTestCase(testSuite,testCase1)
            publisher_common.addTestCase(testSuite,testCase2)
            publisher = publisher_common.createPublisher()
            publisher.PublishTestPlan(testSuite, "test_plan.pdf", "YAML")
            print("Invalid Format Flag Test Plan exception expected but not thrown : FAILED")
        except NonSupportedFormatException as e:
            print("Invalid Format Flag Test Plan : PASSED")
        
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
            publisher.PublishTestPlan(testSuite, "test_plan.yaml", "PDF")
            print("Invalid File Extension Test Plan exception expected but not thrown : FAILED")
        except NonSupportedFormatException as e:
            print("Invalid File Extension Test Plan : PASSED")
        
    def invalidFlagFormatResultReport():
        try:
            metadata1 = publisher_common.setupValidMetadata(TBTAFMetadataType.TEST_CODE,"TestCase1",["UnitTest", "Release1.0", "ModuleX"],1,"Test Module X")
            metadata2 = publisher_common.setupValidMetadata(TBTAFMetadataType.PRODUCT_CODE,"TestCase2",["UnitTest", "Release1.0", "ModuleY"],2,"Test Module Y")
            testCase1 = publisher_common.createTestCase(metadata1,15)
            testCase2 = publisher_common.createTestCase(metadata2,7)
            testSuite = publisher_common.createTestSuite(TBTAFTestSuiteType.NORMAL,"TestSuite1")
            publisher_common.addTestCase(testSuite,testCase1)
            publisher_common.addTestCase(testSuite,testCase2)
            publisher = publisher_common.createPublisher()
            publisher.PublishResultReport(testSuite, "test_report.pdf", "YAML")
            print("Invalid Format Flag Test Plan exception expected but not thrown : FAILED")
        except NonSupportedFormatException as e:
            print("Invalid Format Flag Test Plan : PASSED")
        
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
            publisher.PublishResultReport(testSuite, "test_report.yaml", "PDF")
            print("Invalid File Extension Test Plan exception expected but not thrown : FAILED")
        except NonSupportedFormatException as e:
            print("Invalid File Extension Test Plan : PASSED")

if __name__ == '__main__':  
    unittest.main()