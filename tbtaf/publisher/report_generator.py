'''
Created on 04/11/2022

@author: @brody7u7
'''
from .generators.HTMLReportGenerator import HTMLReportGenerator
from .generators.PDFReportGenerator import PDFReportGenerator
from common.exception.NonSupportedFormatException import NonSupportedFormatException

class TBTAFReportGeneratorFactory:
    '''
    Factory to get TBTAFReportGenerator implementations
    '''

    def __init__(self):
        self._builders = {}
        self._builders['HTML'] = HTMLReportGenerator
        self._builders['PDF'] = PDFReportGenerator

    def create(self, format):
        builder = self._builders.get(format.upper())
        if not builder:
            raise NonSupportedFormatException("NonSupportedFormatException with format {0} in TBTAFReportGeneratorFactory".format(format))
        return builder()