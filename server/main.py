from flask import Flask, render_template, request, jsonify
import subprocess
import shlex
import os
from flask_cors import CORS  # For Cross-Origin Resource Sharing

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/runcode', methods=['POST'])
def run_code():
    data = request.get_json()
    if 'code' in data:
        code = data['code']
        sanitized_code = sanitize_input(code)
        output = execute_command(sanitized_code)
        return jsonify({'output': output})
    return jsonify({'error': 'Invalid request'})

def sanitize_input(input_text):
    # Implement your input sanitization logic here
    # This is a simple example, you might need to do more depending on your use case
    return shlex.quote(input_text)

def execute_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr}"

@app.route('/get_directory_structure')
def get_directory_structure():
    directory_path = './'
    file_nodes = create_file_nodes(directory_path)
    return jsonify(file_nodes)

def create_file_nodes(directory):
    file_nodes = []
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        node = {'name': item}
        if os.path.isdir(item_path):
            node['type'] = 'directory'
            node['children'] = create_file_nodes(item_path)
        else:
            node['type'] = 'file'
        file_nodes.append(node)
    return file_nodes


if __name__ == '__main__':
    app.run(debug=True)
