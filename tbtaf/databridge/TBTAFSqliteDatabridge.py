from __future__ import absolute_import
import sqlite3
import os
from datetime import datetime
from common.suite import TBTestSuite
from common.metadata import TBMetadata
from common.result import TBTAFResult
from common.printable_test import TBTAFPrintableTest
from common.enums.metadata_type import TBTAFMetadataType
from databridge.Databridge import Databridge


class TBTAFSqliteDatabridge(Databridge):

    connection = None
    
    def __init__(self):
        pass
    
    def getConnection(self):
        return self.connection
    
    def connect(self, db_path=None):
        try:
            db_path = db_path or os.environ.get('SQLITE_DB_PATH', ':memory:')
            self.connection = sqlite3.connect(db_path)
            self.connection.row_factory = sqlite3.Row
        except Exception as e:
            raise ConnectionError(f"Failed to connect to SQLite database: {str(e)}")

    def storeResult(self, tBTestSuiteInstance):
        cursor = self.connection.cursor()
        
        # Get summary result from the test suite instance
        summaryTestSuite = tBTestSuiteInstance.getSuiteResult()
        totalTests = len(tBTestSuiteInstance.suiteTestCases)
        successRate = (float(summaryTestSuite.passTests) / float(totalTests)) * 100 if totalTests > 0 else 0

        # Insert test suite summary
        testSuiteSqlParams = (
            str(tBTestSuiteInstance.getTestSuiteType()),
            str(tBTestSuiteInstance.getSuiteID()),
            int(totalTests),
            int(summaryTestSuite.passTests),
            int(summaryTestSuite.failedTests),
            int(summaryTestSuite.inconclusiveTests),
            float(successRate),
            summaryTestSuite.getStartTimestamp().isoformat(),
            summaryTestSuite.getEndTimestamp().isoformat(),
            str(summaryTestSuite.getEndTimestamp() - summaryTestSuite.getStartTimestamp())
        )

        cursor.execute(TBTAFSqliteDatabridge.testSuiteInsertSql, testSuiteSqlParams)
        newest_id = cursor.lastrowid

        # Insert test cases
        testCasesList = tBTestSuiteInstance.getTestCases()
        for testCase in testCasesList:
            testMetaData = testCase.getTestMetadata()
            testTags = testMetaData.getTags()
            tagsConcatenated = ",".join(testTags) if testTags else ""
            
            testResult = testCase.getResult()
            time_elapsed = testResult.getEndTimestamp() - testResult.getStartTimestamp()

            testSqlParams = (
                str(testMetaData.getAssetID()),
                testMetaData.getAssetDescription(),
                tagsConcatenated,
                int(testMetaData.getPriority()),
                testResult.getResultSource(),
                testResult.getStartTimestamp().isoformat(),
                testResult.getEndTimestamp().isoformat(),
                str(time_elapsed),
                str(testResult.getVerdict()),
                newest_id
            )
            
            cursor.execute(TBTAFSqliteDatabridge.testInsertSql, testSqlParams)

        self.connection.commit()
        cursor.close()
        return newest_id

    def getTestResult(self, suiteId):
        cursor = self.connection.cursor()
        testSuite = None

        try:
            # Get test suite summary
            cursor.execute(TBTAFSqliteDatabridge.testSuiteSelectSql, (suiteId,))
            suite_row = cursor.fetchone()
            
            if suite_row:
                testSuite = TBTestSuite(suite_row['suite_type'], suite_row['suite_id'])

                # Get associated test cases
                cursor.execute(TBTAFSqliteDatabridge.testSelectSql, (suiteId,))
                for test_row in cursor.fetchall():
                    testMetadata = TBMetadata(TBTAFMetadataType.PRINTABLE_CODE)
                    testMetadata.setAssetDescription(test_row['description'])
                    testMetadata.setAssetID(test_row['test_id'])
                    testMetadata.setPriority(test_row['priority'])
                    if test_row['tags']:
                        testMetadata.setTags(test_row['tags'].split(','))

                    testResult = TBTAFResult(
                        resultSource=test_row['source'],
                        testVerdict=test_row['veredict']
                    )
                    testResult.setStartTimestamp(datetime.fromisoformat(test_row['start_time']))
                    testResult.setEndTimestamp(datetime.fromisoformat(test_row['end_time']))

                    printableTest = TBTAFPrintableTest(metadata=testMetadata, result=testResult)
                    testSuite.addTestCase(printableTest)

        finally:
            cursor.close()

        return testSuite

    # SQL statements updated for SQLite
    testSuiteInsertSql = """INSERT INTO test_suite (
        suite_type, 
        suite_id, 
        total_test, 
        passed_test, 
        failed_test, 
        inconclusive_test, 
        success_rate, 
        start_time, 
        end_time, 
        time_elapse
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""

    testInsertSql = """INSERT INTO test (
        test_id,
        description,
        tags,
        priority,
        source,
        start_time,
        end_time,
        time_elapse,
        veredict,
        suite_id
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""

    testSuiteSelectSql = """SELECT 
        suite_type, 
        suite_id 
        FROM test_suite 
        WHERE id = ?"""

    testSelectSql = """SELECT 
        test_id,
        description,
        tags,
        priority,
        source,
        start_time,
        end_time,
        time_elapse,
        veredict,
        suite_id
        FROM test 
        WHERE suite_id = ?"""