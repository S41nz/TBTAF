'''
<TBTAF>
<TestID>2021</TestID>
<Tags>TBTAF,Discoverer,Textbook</Tags>
<Priority>4</Priority>
<Description>Sample Test, currently incomplete, don't trust the name, the cake is a lie!</Description>
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


class DiscovererCompleteAndValidTest(TBTestCase):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.testTimeout = 1984
        self.testResult = None
        self.testTrace = None

    def setup(self):
        TBTestCase.setup(self)
        print("Setup performed from DiscovererCompleteAndValidTest")
        self.testTrace = TBTAFTrace("DiscovererCompleteAndValidTest")
        self.testTrace.addEvent(TBTAFEvent(TBTAFEventType.INFO,"Setup performed from DiscovererCompleteAndValidTest",self.testTrace.getTraceSource()))
        


    def execute(self):
        TBTestCase.execute(self)
        print("Execute performed from DiscovererCompleteAndValidTest")
        self.testResult = TBTAFResult(TBTAFVerdictType.PASS,"DiscovererCompleteAndValidTest")


    def cleanup(self):
        TBTestCase.cleanup(self)
        print("Cleanup performed from DiscovererCompleteAndValidTest")

        