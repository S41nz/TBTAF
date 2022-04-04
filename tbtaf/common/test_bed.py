'''
Created on 11/11/2015

@author: S41nz
'''
from __future__ import absolute_import
from common.node import TBTestNode

class TBTestBed(object):
    '''
    Class that encapsulates the information required to create and manage the infrastructure required for test content execution
    '''


    def __init__(self, executionNodes = []):
        '''
        Constructor
        '''
        self.bedNodes = executionNodes
        
    def addExecutionNode(self,url):
        '''
        Method to add an execution node to the test bed
        '''
        newNode = TBTestNode(url)
        self.bedNodes.append(newNode)
        
    def removeExecutionNode(self,url):
        '''
        Method to remove a node from a given test bed
        '''
        deletionCandidate = self.getTestBedNode(url)
        
        if deletionCandidate is not None:
            #Delete the execution node
            self.bedNodes.remove(deletionCandidate)
        
    
    def getTestBedNodes(self):
        '''
        Method to obtain a direct reference of the list of nodes
        '''
        return self.bedNodes
    
    def getTestBedNode(self,url):
        '''
        Method to obtain the reference of TBTestNode given a specific URL
        '''
        nodeMatch = None
        
        for targetNode in self.bedNodes:
            if targetNode.getNodeURL() == url:
                nodeMatch = targetNode
                break
        
        return nodeMatch
        
        