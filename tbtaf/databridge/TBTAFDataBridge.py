from __future__ import absolute_import
import os
from tokenize import String
from common.suite import TBTestSuite
from common.metadata import TBMetadata
from common.result import TBTAFResult
from common.printable_test import TBTAFPrintableTest
from publisher.TBTAFPublisher import TBTAFPublisher
from common.enums.metadata_type import TBTAFMetadataType

from databridge.Databridge import Databridge
from databridge.TBTAFOracleDatabridge import TBTAFOracleDatabridge

class TBTAFDatabridge(Databridge):

    def __init__(self, databridgeType: String) -> None:
        if(databridgeType == 'TBTAFOracleDatabridge'):
            self._databridgeImp = TBTAFOracleDatabridge()

    def connect(self):
        try:
            return self._databridgeImp.connect()
        except Exception:
            raise 
        
    def getConnection(self):
        return self._databridgeImp.getConnection

    def storeResult(self, tBTestSuiteInstance : TBTestSuite): 
        return self._databridgeImp.storeResult(tBTestSuiteInstance)

    def getTestResult(self, suiteId) -> TBTestSuite:
        return self._databridgeImp.getTestResult(suiteId)
