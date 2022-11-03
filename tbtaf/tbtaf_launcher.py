'''
Created on 25/11/2015

@author: S41nz
'''
from __future__ import absolute_import
from __future__ import print_function
from orchestrator.TBTAFOrchestrator import TBTAFOrchestrator
from listener.TBTAFListener import TBTAFListener

if __name__ == '__main__':
    listener = TBTAFListener() 
    listener.check_push_events('./test/test05.tbtaf')
