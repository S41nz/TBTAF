'''
Created on 25/11/2015

@author: S41nz
'''
from __future__ import absolute_import
from __future__ import print_function
from orchestrator.TBTAFOrchestrator import TBTAFOrchestrator
from listener.TBTAFListener import TBTAFListener
from interpreter.TBATFInterpreterCLI import TBTAFInterpreterCLI
from flask import Flask
from api.executor_api import executor_api
from api.status_api import status_api
from api.results_api import results_api

import sys

def create_flask_app():
    """Crea la aplicación Flask y registra las rutas de las APIs"""
    app = Flask(__name__)

    # Registrar las rutas de las APIs
    app.register_blueprint(executor_api)
    app.register_blueprint(status_api)
    app.register_blueprint(results_api)

    return app

if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1].lower() == '-interactive':
            tbtafcli = TBTAFInterpreterCLI()
            tbtafcli.execute()
        elif sys.argv[1].lower() == '-flask':
            app = create_flask_app()
            print("Starting Flask server...")
            app.run(debug=True)  # Inicia el servidor en modo debug
        else:
            print("Invalid argument. Use '-interactive' for CLI mode or '-flask' to start the Flask API.")
    else:
        testScript = './test/test05.tbtaf'
        myTBTAF = TBTAFOrchestrator()

        print("Executing the following test script: " + testScript)
        
        parseResult = myTBTAF.parseScript(testScript)

        print("Parse Status: "+parseResult.status)

        print("Parse Message"+parseResult.message)

        sys.exit()
