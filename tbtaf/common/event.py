'''
Created on 02/11/2015

@author: S41nz
'''

from __future__ import absolute_import
import time

class TBTAFEvent(object):
    '''
    Class that encapsulates the information from a given event within the TBTAF 
    '''
    
    #Fields

    def __init__(self, eventType,message,source):
        '''
        Constructor
        '''
        #Set the event Type
        self.eventType = eventType
        
        #Set the event message
        self.eventMessage = message
        
        #Assign the source of the event
        self.eventSource = source
        
        #Set the timestamp
        self.eventTimestamp = time.time()
        

    def getEventType(self):
        return self.eventType

    def getEventMessage(self):
        return self.eventMessage

    def getEventTimestamp(self):
        return self.eventTimestamp
    
    def getEventSource(self):
        return self.eventSource

   
        
    