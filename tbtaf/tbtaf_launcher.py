'''
Created on 25/11/2015

@author: S41nz
'''
from __future__ import absolute_import
from __future__ import print_function
from orchestrator.TBTAFOrchestrator import TBTAFOrchestrator

if __name__ == '__main__':
    testScript = "./test/test05.tbtaf"
    print("Welcome to TBTAF Test bed")
    
    myTBTAF = TBTAFOrchestrator()
    
    print("Executing the following test script: " + testScript)
    
    parseResult = myTBTAF.parseScript(testScript)

    print("Parse Status: "+parseResult.status)

    print("Parse Message"+parseResult.message)
