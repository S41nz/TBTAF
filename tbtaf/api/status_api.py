from flask import Blueprint, request, jsonify
import os
import json
from orchestrator.TBTAFOrchestrator import TBTAFOrchestrator

status_api = Blueprint('status_api', __name__)
orchestrator = TBTAFOrchestrator()

@status_api.route('/execution_status/<suite_id>', methods=['GET'])
def get_execution_status(suite_id):
    """
    Consulta los estados de ejecución parciales de una suite determinada, sin bloquear el archivo.
    """
    partial_results_file = "execution_status.json"
    
    try:
        # Verificar si el archivo existe
        if not os.path.exists(partial_results_file):
            return jsonify({"error": "No execution status available."}), 404

        # Leer y analizar el archivo
        with open(partial_results_file, "r") as file:
            try:
                current_data = json.load(file)
            except json.JSONDecodeError:
                return jsonify({"error": "Failed to read execution status. File might be corrupted."}), 500

            # Buscar el suite_id en la lista
            suite_status = next((item for item in current_data if item["suite_id"] == suite_id), None)
            if not suite_status:
                return jsonify({"error": f"No status found for suite ID: {suite_id}"}), 404

            # Retornar la información de la suite encontrada
            return jsonify({
                "status": "success",
                "latest_status": suite_status["status"],
                "last_updated": suite_status["timestamp"]
            }), 200

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
