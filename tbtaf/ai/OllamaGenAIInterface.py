# ai/OllamaGenAIInterface.py

import os
import requests
import json
from .GenAIInterface import GenAIInterface

class OllamaGenAIInterface(GenAIInterface):
    """
    A concrete implementation of the GenAIInterface for interacting with a local Ollama service.
    This class reads its configuration from environment variables.
    """
    def __init__(self):
        """
        Initializes the Ollama interface by loading configuration from environment variables.
        """
        print("Initializing Ollama Interface...")
        
        # --- CHANGE: Load configuration from environment variables ---
        # Get the API URL from the 'OLLAMA_API_URL' environment variable.
        self.api_url = os.getenv('OLLAMA_API_URL')
        
        # Get the model name from the 'OLLAMA_MODEL' environment variable.
        self.model_name = os.getenv('OLLAMA_MODEL')
        # -----------------------------------------------------------

        # --- CHANGE: Error out if the variables are not defined ---
        if not self.api_url:
            raise ValueError("Configuration Error: The 'OLLAMA_API_URL' environment variable is not set.")
        if not self.model_name:
            raise ValueError("Configuration Error: The 'OLLAMA_MODEL' environment variable is not set.")
        # -----------------------------------------------------------

        print(f"Ollama interface configured for model '{self.model_name}' at '{self.api_url}'")

    def send_prompt(self, prompt_text: str) -> str:
        """
        Sends a prompt to the configured Ollama API endpoint and returns the model's response.
        """
        headers = {"Content-Type": "application/json"}
        payload = {
            "model": self.model_name,
            "prompt": prompt_text,
            "stream": False
        }

        print(f"\n🤖 Sending prompt to {self.model_name}...")
        try:
            response = requests.post(self.api_url, headers=headers, data=json.dumps(payload))
            response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

            response_text = response.json().get('response', 'No valid response received from the model.')
            print("🤖 AI response received.")
            return response_text

        except requests.exceptions.RequestException as e:
            error_message = f"Connection Error: Could not connect to the Ollama service at {self.api_url}. Is Ollama running? Details: {e}"
            print(f"❌ {error_message}")
            # It's better to return a descriptive error than to crash the whole report generation
            return error_message

