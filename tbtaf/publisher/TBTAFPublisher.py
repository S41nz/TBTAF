'''
Created on 07/11/2015

@author: @andresmuro , @andres.alvarado , @mestradago , @rnunezc
'''
from __future__ import absolute_import
from __future__ import print_function
from common.exception.IllegalArgumentException import IllegalArgumentException
from common.exception.NonSupportedFormatException import NonSupportedFormatException
from .report_generator import TBTAFReportGeneratorFactory
class TBTAFPublisher(object):
    '''
    The TBTAF Publisher is in charge of generating all the test 
    execution related documentation.
    '''

    def __init__(self):
        self._factory = TBTAFReportGeneratorFactory()

    def PublishTestPlan(self, tBTestSuiteInstance, filePath, formatFlag):
        generator = self._factory.create(formatFlag)
        generator.publishTestPlan(tBTestSuiteInstance, filePath)

    def PublishResultReport(self, tBTestSuiteInstance, filePath, formatFlag):
        generator = self._factory.create(formatFlag)
        generator.publishResultReport(tBTestSuiteInstance, filePath)
