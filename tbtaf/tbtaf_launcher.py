'''
Created on 25/11/2015

@author: S41nz
'''
from __future__ import absolute_import
from __future__ import print_function
from orchestrator.TBTAFOrchestrator import TBTAFOrchestrator
from listener.TBTAFListener import Listener

if __name__ == '__main__':
    listener = Listener() 
    #myTBTAF = TBTAFOrchestrator()
    listener.check_push_events()
