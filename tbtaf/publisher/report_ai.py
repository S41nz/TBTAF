# publisher/ai_analyzer.py

import requests
import json

# Constantes para la configuración de Ollama
OLLAMA_API_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3" # O el modelo que hayas descargado, ej: "codellama"

def get_report_ai(prompt_text: str) -> str:
    """
    Envía un prompt a la API local de Ollama y retorna la respuesta del modelo.
    """
    headers = {"Content-Type": "application/json"}
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt_text,
        "stream": False  # Para recibir la respuesta completa de una vez
    }    

    print(f"\n🤖 Enviando prompt a {OLLAMA_MODEL}...")
    try:        
        response = requests.post(OLLAMA_API_URL, headers=headers, data=json.dumps(payload))
        response.raise_for_status()  # Lanza una excepción si la respuesta es un error (ej. 4xx, 5xx)

        # La respuesta de Ollama viene en un JSON, extraemos el texto de la respuesta.
        response_text = response.json().get('response', 'No se recibió una respuesta válida del modelo.')
        print("🤖 Respuesta recibida de la IA.")
        return response_text

    except requests.exceptions.RequestException as e:
        error_message = f"Error de conexión con el servicio de Ollama en {OLLAMA_API_URL}. ¿Está Ollama en ejecución? Detalle: {e}"
        print(f"❌ {error_message}")
        return error_message