'''
Created on 11/11/2015

@author: S41nz
'''

class TBTAFNodeStatus(object):
    '''
    Simple enumeration class that describes the possible status of given execution node
    '''

    #Possible status of the node
    NOT_INITIALIZED="Not initialized"
    #The node is online
    ONLINE="Online"
    #The node is offline
    OFFLINE="Offline"
    #The node is online but is busy with execution load
    BUSY= "Busy"
        