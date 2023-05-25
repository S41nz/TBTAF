'''
Created on 25/11/2015

@author: S41nz
'''
from __future__ import absolute_import
from __future__ import print_function
from orchestrator.TBTAFOrchestrator import TBTAFOrchestrator
from listener.TBTAFListener import TBTAFListener
from interpreter.TBATFInterpreterCLI import TBTAFInterpreterCLI
import sys

if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1].lower() == '-interactive':
            tbtafcli = TBTAFInterpreterCLI()
            tbtafcli.execute()
            
    else:
        testScript = './test/test02.tbtaf'
        myTBTAF = TBTAFOrchestrator()

        print("Executing the following test script: " + testScript)
        
        parseResult = myTBTAF.parseScript(testScript)

        print("Parse Status: "+parseResult.status)

        print("Parse Message"+parseResult.message)

        sys.exit()
