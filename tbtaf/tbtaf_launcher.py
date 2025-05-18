'''
Created on 25/11/2015

@author: S41nz
'''
from __future__ import absolute_import
from __future__ import print_function
from orchestrator.TBTAFOrchestrator import TBTAFOrchestrator
from listener.TBTAFListener import TBTAFListener
from interpreter.TBATFInterpreterCLI import TBTAFInterpreterCLI
from databridge.TBTAFSqliteDatabridge import TBTAFSqliteDatabridge
from databridge.TBTAFOracleDatabridge import TBTAFOracleDatabridge
import sys

if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1].lower() == '-interactive':
            tbtafcli = TBTAFInterpreterCLI()
            tbtafcli.execute()
            
    else:
        # Interactive mode: show steps and options with defaults
        print("Interactive configuration:")
        default_test_script = '5'
        default_target_databridge = None
        
        # Prompt for the test script path
        input_test_script = input("Enter test option between 1 to 5 [{}]: Default 5\n".format(default_test_script)).strip()

        # Map user selections to test script paths
        test_script_mapping = {
            "1": './test/test01.tbtaf',
            "2": './test/test02.tbtaf',
            "3": './test/test03.tbtaf',
            "4": './test/test04.tbtaf',
            "5": './test/test05.tbtaf'
        }

        testScript = test_script_mapping.get(input_test_script)
        if not testScript:
            print("Option not valid, please choose a number between 1 and 5.")
            sys.exit(1)
        print(f"Test script set to: {testScript}")
        
        # Prompt for the target databridge option
        input_target = input("Enter target databridge (sqlite/oracle) Default: None [{}]: \n".format(default_target_databridge)).strip()
        targetDatabridgeChoice = input_target if input_target else default_target_databridge

        if targetDatabridgeChoice == "sqlite":
            targetDatabridgeChoice = TBTAFSqliteDatabridge()
        elif targetDatabridgeChoice == "oracle":
            targetDatabridgeChoice = TBTAFOracleDatabridge()
        elif targetDatabridgeChoice == "":
            targetDatabridgeChoice = None
        else:
            print("Invalid target databridge choice. Please choose 'sqlite', 'oracle' or leave empty to choose None.")
            sys.exit(1)
        print("Target databridge set to: {}".format(targetDatabridgeChoice))


        myTBTAF = TBTAFOrchestrator(targetDatabridge=targetDatabridgeChoice)

        print("Executing the following test script: " + testScript)
        
        parseResult = myTBTAF.parseScript(testScript)

        print("Parse Status: "+parseResult.status)

        print("Parse Message: "+parseResult.message)

        sys.exit()
