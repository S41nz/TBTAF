'''
Created on 03/11/2015

@author: S41nz
'''

class TBTAFResult(object):
    '''
    Class that encapsulates the information related to the result of the execution of a given TBTAFTestCase
    '''
    

    def __init__(self, testVerdict,resultSource):
        '''
        Constructor
        '''
        self.testVerdict = testVerdict
        self.resultSource = resultSource
        
    def getVerdict(self):
        return self.testVerdict
    
    def getResultSource(self):
        return self.resultSource
    
    def setStartTimestamp(self,startTime):
        self.startTimestamp = startTime
    
    def getStartTimestamp(self):
        return self.startTimestamp
        
    def setEndTimestamp(self,endTime):
        self.endTimestamp = endTime
    
    def getEndTimestamp(self):
        return self.endTimestamp