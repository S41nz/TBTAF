'''
Created on 11/11/2015

@author: S41nz
'''

from __future__ import absolute_import
from common.enums.node_status import TBTAFNodeStatus

class TBTestNode(object):
    '''
    Class that contains the information of a given node that could serve to execute a given set of TBTestCases
    '''


    def __init__(self, url):
        '''
        Constructor
        '''
        self.nodeURL = url
        #Initialize the status of the node
        self.nodeStatus = TBTAFNodeStatus.NOT_INITIALIZED
        
    def getNodeURL(self):
        '''
        Method to obtain the URL from a given node
        '''
        return self.nodeURL
    
    def getNodeStatus(self):
        '''
        Method to obtain the current value of a given execution node
        '''
        return self.nodeStatus
    
    def setNodeStatus(self,newStatus):
        '''
        Method to update the status of a given execution node
        '''
        self.nodeStatus = newStatus
    