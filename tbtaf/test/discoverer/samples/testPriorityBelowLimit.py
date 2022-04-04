'''
<TBTAF>
<TestID>2021</TestID>
<Tags>TBTAF,Discoverer,Textbook</Tags>
<Priority>0</Priority>
<Description>Priority above limit.</Description>
</TBTAF>
'''
# '''
# Created on 06/11/2015

# @author: Nander
# '''
from __future__ import absolute_import
from __future__ import print_function
from common.test import TBTestCase
from common.result import TBTAFResult
from common.trace import TBTAFTrace
from common.event import TBTAFEvent
from common.enums.verdict_type import TBTAFVerdictType
from common.enums.event_type import TBTAFEventType


class TestPriorityBelowLimit(TBTestCase):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.testTimeout = 1984
        self.testName = self.__class__.__name__

    def setup(self):
        TBTestCase.setup(self)
        print("Setup performed from " + self.testName)
        self.testTrace = TBTAFTrace(self.testName)
        setup_str = "Setup performed from " + self.testName
        self.testTrace.addEvent(TBTAFEvent(TBTAFEventType.INFO,
                                           setup_str,
                                           self.testTrace.getTraceSource()))

    def execute(self):
        TBTestCase.execute(self)
        print("Execute performed from " + self.testName)
        self.testResult = TBTAFResult(TBTAFVerdictType.PASS,
                                      self.testName)

    def cleanup(self):
        TBTestCase.cleanup(self)
        print("Cleanup performed from " + self.testName)
        