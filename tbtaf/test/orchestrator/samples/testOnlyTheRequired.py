'''
<TBTAF>
<TestID>2021</TestID>
<Tags>TBTAF,Discoverer,Textbook</Tags>
</TBTAF>
'''
'''
Created on 06/11/2015

@author: Nander
'''
from __future__ import absolute_import
from __future__ import print_function
from common.test import TBTestCase
from common.result import TBTAFResult
from common.trace import TBTAFTrace
from common.event import TBTAFEvent
from common.enums.verdict_type import TBTAFVerdictType
from common.enums.event_type import TBTAFEventType


class DiscovererOnlyTheRequiredTest(TBTestCase):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.testTimeout = 1984

    def setup(self):
        TBTestCase.setup(self)
        print("Setup performed from DiscovererOnlyTheRequiredTest")
        self.testTrace = TBTAFTrace("DiscovererOnlyTheRequiredTest")
        self.testTrace.addEvent(TBTAFEvent(TBTAFEventType.INFO,"Setup performed from DiscovererOnlyTheRequiredTest",self.testTrace.getTraceSource()))
        


    def execute(self):
        TBTestCase.execute(self)
        print("Execute performed from DiscovererOnlyTheRequiredTest")
        self.testResult = TBTAFResult(TBTAFVerdictType.PASS,"DiscovererOnlyTheRequiredTest")


    def cleanup(self):
        TBTestCase.cleanup(self)
        print("Cleanup performed from DiscovererOnlyTheRequiredTest")

        