'''
Created on 25/11/2015

@author: S41nz
'''
from orchestrator.TBTAFOrchestrator import TBTAFOrchestrator

if __name__ == '__main__':
    
    testScript = "D:\\tbtaf\\tbtaf\\test\\test03.tbtaf"
    print "Welcome to TBTAF Test bed"
    
    myTBTAF = TBTAFOrchestrator()
    
    print "Executing the following test script: " + testScript
    
    parseResult = myTBTAF.parseScript(testScript)

    print "Parse Status: "+parseResult.status

    print "Parse Message"+parseResult.message
