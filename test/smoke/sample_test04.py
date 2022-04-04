'''
<TBTAF>
<TestID>1004</TestID>
<Tags>TBTAF,Smoke</Tags>
<Priority>4</Priority>
<Description>Hello from Sample test 1004</Description>
</TBTAF>
'''
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

class TBTAFSampleTest(TBTestCase):
    '''
    classdocs
    '''

    
        
    def __init__(self):
        '''
        Constructor
        '''
        self.testResult = TBTAFResult(TBTAFVerdictType.INCONCLUSIVE,"TBTAFSampleTest")
        self.testTrace = None
        self.testTimeout = 1984
        self.testMetadata = TBMetadata('TEST')
        
    def setup(self):
        TBTestCase.setup(self)
        print("Setup performed from TBTAFSampleTest")
        self.testTrace = TBTAFTrace("TBTAFSampleTest")
        self.testTrace.addEvent(TBTAFEvent(TBTAFEventType.INFO,"Setup performed from TBTAFSampleTest",self.testTrace.getTraceSource()))
        


    def execute(self):
        time.sleep(7)
        TBTestCase.execute(self)
        print("Execute performed from TBTAFSampleTest")
        self.testResult = TBTAFResult(TBTAFVerdictType.PASS,"TBTAFSampleTest")


    def cleanup(self):
        TBTestCase.cleanup(self)
        print("Cleanup performed from TBTAFSampleTest")

        