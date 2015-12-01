'''
Created on 04/11/2015

@author: S41nz
'''

class TBMetadata(object):
    '''
    Class that encapsulates all the metadata decoration that can be discovered within a source code asset.
    '''
    NON_INITIALIZED = -1
    
    #Fields
    #Empty list to store the discovered tags within the asset
    tags = []
    
    #Methods


    def __init__(self,metadataType):
        '''
        Constructor
        '''
        self.metadataType = metadataType
        self.assetID = self.NON_INITIALIZED
    
    def getMetadataType(self):
        return self.metadataType
    
    def setAssetID(self,assetID):
        self.assetID = assetID
        
    def getAssetID(self):
        return self.assetID
    
    def setTags(self,tags):
        self.tags = tags
    
    def getTags(self):
        return self.tags
    
    def setPriority(self,priority):
        self.priority = priority
    
    def getPriority(self):
        return self.priority
    
    def setAssetDescription(self,desc):
        self.description = desc
        
    def getAssetDescription(self):
        return self.description
    
        