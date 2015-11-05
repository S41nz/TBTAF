'''
Created on 04/11/2015

@author: psainza
'''
from common.test import TBTestCase
from common.result import TBTAFResult
from common.trace import TBTAFTrace
from common.event import TBTAFEvent
from common.enums.verdict_type import TBTAFVerdictType
from common.enums.event_type import TBTAFEventType

class TBTAFSampleTest(TBTestCase):
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
        print "Setup performed from TBTAFSampleTest"
        self.testTrace = TBTAFTrace("TBTAFSampleTest")
        self.testTrace.addEvent(TBTAFEvent(TBTAFEventType.INFO,"Setup performed from TBTAFSampleTest",self.testTrace.getTraceSource()))
        


    def execute(self):
        TBTestCase.execute(self)
        print "Execute performed from TBTAFSampleTest"
        self.testResult = TBTAFResult(TBTAFVerdictType.PASS,"TBTAFSampleTest")


    def cleanup(self):
        TBTestCase.cleanup(self)
        print "Cleanup performed from TBTAFSampleTest"

        