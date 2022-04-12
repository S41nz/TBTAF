from __future__ import absolute_import
import os
from common.suite import TBTestSuite
from common.metadata import TBMetadata
from common.result import TBTAFResult
from common.printable_test import TBTAFPrintableTest
from publisher.TBTAFPublisher import TBTAFPublisher
from common.enums.metadata_type import TBTAFMetadataType
from abc import ABCMeta, abstractmethod


class Databridge:
    __metaclass__ = ABCMeta

    @property
    @abstractmethod
    def connection(self):
        pass

    @abstractmethod
    def getConnection(self): raise NotImplementedError

    @abstractmethod
    def storeResult(self, tBTestSuiteInstance): raise NotImplementedError

    @abstractmethod
    def connect(self): raise NotImplementedError

    @abstractmethod
    def getTestResult(self, suiteId): raise NotImplementedError
