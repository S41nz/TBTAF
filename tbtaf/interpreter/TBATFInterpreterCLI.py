from __future__ import absolute_import
from __future__ import print_function
import os as _os
import sys
import importlib.util

currentPath = _os.path.dirname(_os.path.abspath(__file__))
rootFolder = _os.path.abspath(_os.path.join(currentPath, ".."))
scriptPath = _os.path.join(rootFolder, "orchestrator", "TBTAFOrchestrator.py")
sys.path.append(rootFolder)
spec = importlib.util.spec_from_file_location("TBTAFOrchestrator.py", scriptPath)
modulo = importlib.util.module_from_spec(spec)
spec.loader.exec_module(modulo)

class TBTAFInterpreterCLI(object):
    def __init__(self):
        self.myTBTAF = modulo.TBTAFOrchestrator()
        self.command = ""
        self.path = './temp.tbtaf'
        try:
            with open(self.path, 'w') as tempFile:
                tempFile.write(self.command)
                return
            
        except:
            return
        
    def commandInterpreter(self):
        if self.command == 'quit()' or self.command == 'Quit()' or self.command == 'QUIT()':
            print('exiting interpreter.')
            _os.remove("temp.tbtaf")
            sys.exit()
        elif self.command == 'execute()' or self.command == 'Execute()' or self.command == 'EXECUTE()':
            try:
                if _os.path.getsize(self.path) > 0:
                    parseResult = self.myTBTAF.parseScript(self.path)
                    print("Parse Status: "+parseResult.status)
                    print("Parse Message"+parseResult.message)
                else:
                    print("No commands found")
            except:
                print("No commands found")
        # elif self.command == 'clear' or self.command == 'Clear' or self.command == 'CLEAR':
        #     _os.remove("temp.tbtaf")

        else:
            try:
                with open(self.path, 'a') as tempFile:
                    tempFile.write(self.command + "\n")
                    return 1
                
            except:
                return 0

    def main(self):
        while True:
            self.command = input('>>> ')

            self.commandInterpreter()
