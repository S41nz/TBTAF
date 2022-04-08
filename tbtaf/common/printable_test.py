from __future__ import absolute_import
from __future__ import print_function
from common.test import TBTestCase
from common.result import TBTAFResult
from common.trace import TBTAFTrace
from common.event import TBTAFEvent
from common.enums.verdict_type import TBTAFVerdictType
from common.enums.event_type import TBTAFEventType
from common.metadata import TBMetadata
import time

class TBTAFPrintableTest(TBTestCase):
    '''
    classdocs
    '''

    
        
    def __init__(self, result, metadata):
        '''
        Constructor
        '''
        self.testResult = result
        self.testTrace = None
        self.testTimeout = 1994
        self.testMetadata = metadata
        
    def setup(self):
        TBTestCase.setup(self)
        


    def execute(self):
        TBTestCase.execute(self)


    def cleanup(self):
        TBTestCase.cleanup(self)
        print("Cleanup performed from TBTAFSampleTest")

        