'''
Created on 03/11/2015

@author: S41nz
'''

from __future__ import absolute_import
from common.enums.event_type import TBTAFEventType

class TBTAFTrace(object):
    '''
    Class that encapsulates a given generated trace within the TBTAF
    '''
    
    #Attributes
    tradeData = []
    
    def __init__(self,source):
        '''
        Constructor
        '''
        self.traceSource = source
        
    def addEvent(self,newEvent):
        '''
        Method to append a given event to the trace
        '''
        self.tradeData.append(newEvent)
    
    def getErrors(self):
        '''
        Method to obtain all the errors of a given trace.
        If errors are not present, then an empty list will be retrieved
        '''
        errorList = []
        
        for traceEvent in self.tradeData:
            if traceEvent.getEventType() == TBTAFEventType.ERROR:
                errorList.append(traceEvent)
                
        return errorList
    
    def getWarnings(self):
        '''
        Method to obtain all the warnings of a given trace.
        If errors are not present, then an empty list will be retrieved
        '''
        warningList = []
        
        for traceEvent in self.tradeData:
            if traceEvent.getEventType() == TBTAFEventType.WARNING:
                warningList.append(traceEvent)
                
        return warningList
    
    def getInfo(self):
        '''
        Method to obtain all the warnings of a given trace.
        If errors are not present, then an empty list will be retrieved
        '''
        infoList = []
        
        for traceEvent in self.tradeData:
            if traceEvent.getEventType() == TBTAFEventType.INFO:
                infoList.append(traceEvent)
                
        return infoList
    
    def getTraceData(self):
        '''
        Method to obtain all the unfiltered content fo the trace
        '''
        
        return self.tradeData
                
    def getTraceSource(self):
        '''
        Method to obtain the source of the given trace.
        '''
        return self.traceSource