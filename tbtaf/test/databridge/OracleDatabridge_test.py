from __future__ import absolute_import
import os
import pandas as pd
from unittest import mock
from common.enums.metadata_type import TBTAFMetadataType
from common.metadata import TBMetadata
from common.printable_test import TBTAFPrintableTest
from common.result import TBTAFResult
from common.suite import TBTestSuite
from databridge.TBTAFDatabridge import TBTAFDatabridge
from databridge.TBTAFOracleDatabridge import TBTAFOracleDatabridge
from test.databridge.MockOracleConnect import MockCursor
from test.databridge.MockOracleConnect import MockConnect
from test.databridge.MockOracleConnect import returned_id

import unittest
import datetime
import cx_Oracle
class Testing(unittest.TestCase):

    @mock.patch.object(cx_Oracle, "connect")
    def test_connect_database(self, mock_connect):
        os.environ['ODB_USER'] = "ODB_USER" 
        os.environ['ODB_PASS'] = "ODB_PASS" 
        os.environ['ODB_TNS'] = 'ODB_TNS'
        mock_connect.return_value = MockConnect()
        databridge = TBTAFDatabridge('TBTAFOracleDatabridge')
        databridge.connect()
        self.assertTrue(mock_connect.called)
        mock_connect.assert_called_once_with('ODB_USER', 'ODB_PASS', 'ODB_TNS')
    
    @mock.patch.object(cx_Oracle, "connect")
    def test_no_user_connect_database(self, mock_connect):
        os.environ['ODB_PASS'] = "ODB_PASS" 
        os.environ['ODB_TNS'] = 'ODB_TNS'
        mock_connect.return_value = MockConnect()
        databridge = TBTAFDatabridge('TBTAFOracleDatabridge')
        self.assertRaises(Exception, TBTAFOracleDatabridge.connect)
    
    @mock.patch.object(cx_Oracle, "connect")
    def test_no_tns_connect_database(self, mock_connect):
        os.environ['ODB_USER'] = "ODB_USER" 
        os.environ['ODB_TNS'] = 'ODB_TNS'
        mock_connect.return_value = MockConnect()
        databridge = TBTAFDatabridge('TBTAFOracleDatabridge')
        self.assertRaises(Exception, TBTAFOracleDatabridge.connect)

    @mock.patch.object(cx_Oracle, "connect")
    def test_no_pass_connect_database(self, mock_connect):
        os.environ['ODB_USER'] = "ODB_USER" 
        os.environ['ODB_PASS'] = "ODB_PASS" 
        mock_connect.return_value = MockConnect()
        databridge = TBTAFDatabridge('TBTAFOracleDatabridge')
        self.assertRaises(Exception, TBTAFOracleDatabridge.connect)

    @mock.patch.object(cx_Oracle, "connect")
    @mock.patch.object(MockCursor, "execute")
    def test_store_result(self, mock_execute, mock_connect):
        os.environ['ODB_USER'] = "ODB_USER" 
        os.environ['ODB_PASS'] = "ODB_PASS" 
        os.environ['ODB_TNS'] = 'ODB_TNS'
        mock_connect.return_value = MockConnect()
        databridge = TBTAFDatabridge('TBTAFOracleDatabridge')
        databridge.connect()
        databridge.storeResult(self.createSampleTestSuite())
        self.assertTrue(mock_execute.called)
        mock_execute.assert_any_call(self.insert_into_test_suite_expected_query, self.insert_into_test_suite_expected_map)
        mock_execute.assert_any_call(self.insert_into_test_expected_query, self.insert_into_test_expected_map)
        assert 2 == mock_execute.call_count

    @mock.patch.object(cx_Oracle, "connect")
    @mock.patch.object(MockCursor, "fetchall")
    @mock.patch.object(MockCursor, "execute")
    def test_get_result(self,mock_execute, mock_fetch, mock_connect):
        os.environ['ODB_USER'] = "ODB_USER" 
        os.environ['ODB_PASS'] = "ODB_PASS" 
        os.environ['ODB_TNS'] = 'ODB_TNS'
        mock_connect.return_value = MockConnect()
        databridge = TBTAFDatabridge('TBTAFOracleDatabridge')
        databridge.connect()
        databridge.getTestResult('1')
        mock_fetch.assert_called_once_with()
        mock_execute.assert_called_once_with(self.select_test_suite_expected, id=1)

    insert_into_test_suite_expected_query = '''INSERT INTO test_suite (
        suite_type, 
        suite_id, 
        total_test, 
        passed_test, 
        failed_test, 
        inconclusive_test, 
        success_rate, 
        start_time, 
        end_time, 
        time_elapse) 
        VALUES(            
        :suite_type, 
        :suite_id, 
        :total_test, 
        :passed_test, 
        :failed_test, 
        :inconclusive_test, 
        :success_rate, 
        :start_time, 
        :end_time, 
        :time_elapse)
        returning id into :new_id'''

    insert_into_test_suite_expected_map = {'suite_type': 'SUITE_TYPE', 'suite_id': 'SUITE_ID', 'total_test': 1, 'passed_test': 1, 'failed_test': 0, 'inconclusive_test': 0, 'success_rate': 100, 'start_time': datetime.datetime(2017, 11, 28, 23, 55, 59, 342380), 'end_time': datetime.datetime(2017, 11, 28, 23, 57, 59, 342380), 'time_elapse': '0:02:00', 'new_id': returned_id}

    insert_into_test_expected_query =  '''INSERT INTO test (
        test_id,
        description,
        tags,
        priority,
        source,
        start_time,
        end_time,
        time_elapse,
        veredict,
        suite_id)
     VALUES(            
        :test_id,
        :description,
        :tags,
        :priority,
        :source,
        :start_time,
        :end_time,
        :time_elapse,
        :veredict,
        :suite_id)'''
        
    insert_into_test_expected_map = {'test_id': '1', 'description': 'DESCRIPTION', 'tags': 'TAG1,TAG2', 'priority': '1', 'source': 'SOURCE', 'start_time': datetime.datetime(2017, 11, 28, 23, 55, 59, 342380), 'end_time': datetime.datetime(2017, 11, 28, 23, 57, 59, 342380), 'time_elapse': '0:02:00', 'veredict': 'Passed', 'suite_id': 1}
        
    select_test_suite_expected = """SELECT
        suite_type, 
        suite_id
        FROM test_suite
        WHERE id = :id"""
    def createSampleTestSuite(self):
        testSuite = TBTestSuite('SUITE_TYPE','SUITE_ID')
        testMetadata = TBMetadata(TBTAFMetadataType.PRINTABLE_CODE)
        testMetadata.setAssetDescription('DESCRIPTION')
        testMetadata.setAssetID(int(1))
        testMetadata.setPriority(int(1))
        testMetadata.setTags('TAG1,TAG2'.split(','))
        testResult = TBTAFResult(resultSource='SOURCE', testVerdict='Passed')
        testResult.setStartTimestamp(datetime.datetime(2017, 11, 28, 23, 55, 59, 342380))
        testResult.setEndTimestamp(datetime.datetime(2017, 11, 28, 23, 57, 59, 342380))
        printableTest = TBTAFPrintableTest(metadata=testMetadata, result=testResult)
        testSuite.addTestCase(printableTest)
        return testSuite

if __name__ == '__main__':
    unittest.main()