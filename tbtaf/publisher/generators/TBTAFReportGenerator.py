'''
Created on 04/11/2022

@author: @brody7u7
'''
from abc import ABCMeta, abstractmethod

class TBTAFReportGenerator:
    '''
    Base class that all report generators must implement
    '''

    __metaclass__ = ABCMeta

    @abstractmethod
    def publishTestPlan(self, tBTestSuiteInstance, filePath): raise NotImplementedError

    @abstractmethod
    def publishResultReport(self, tBTestSuiteInstance, filePath): raise NotImplementedError
