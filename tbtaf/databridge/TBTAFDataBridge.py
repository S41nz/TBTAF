from __future__ import absolute_import
import os
from common.suite import TBTestSuite
from common.metadata import TBMetadata
from common.result import TBTAFResult
from common.printable_test import TBTAFPrintableTest
from publisher.TBTAFPublisher import TBTAFPublisher
from common.enums.metadata_type import TBTAFMetadataType
from abc import ABCMeta, abstractmethod

from databridge.Databridge import Databridge

class TBTAFDatabridge(Databridge):

    def __init__(self, databridgeImp: Databridge) -> None:
        self._databridgeImp = databridgeImp

    def connect(self):
        return self._databridgeImp.connect()

    def getConnection(self):
        return self._databridgeImp.getConnection

    def storeResult(self, tBTestSuiteInstance : TBTestSuite): 
        return self._databridgeImp.storeResult(tBTestSuiteInstance)

    def getTestResult(self, suiteId) -> TBTestSuite:
        return self._databridgeImp.getTestResult(suiteId)
