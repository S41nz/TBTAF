from flask import Blueprint, request, jsonify
import os
import json
from orchestrator.TBTAFOrchestrator import TBTAFOrchestrator

results_api = Blueprint('results_api', __name__)
orchestrator = TBTAFOrchestrator()

def get_execution_state(filename='execution_results.json'):
    try:
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                return json.load(file)
        return []
    except Exception as e:
        print(f"Error al leer el estado de ejecución: {e}")
        return []

@results_api.route('/results/<suite_id>', methods=['GET'])
def get_result_by_source(suite_id):
    """
    Obtiene el resultado de un `resultSource` específico.
    """
    try:
        results = get_execution_state()
        for result in results:
            if result.get("resultSource") == suite_id:
                return jsonify(result), 200
        return jsonify({'error': 'resultSource not found'}), 404
    except Exception as e:
        return jsonify({'error': f'Error retrieving results: {str(e)}'}), 500