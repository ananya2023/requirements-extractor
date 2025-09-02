from flask import Flask, render_template, request, jsonify
import json
import sys
import os

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from simple_ai_client import SimpleAIClient
from requirements_parser import RequirementsParser

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Initialize clients
ai_client = SimpleAIClient()
parser = RequirementsParser()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/extract', methods=['POST'])
def extract_requirements():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not file.filename.endswith('.json'):
            return jsonify({'error': 'Please upload a JSON file'}), 400
        
        # Parse JSON
        json_data = json.load(file)
        
        # Extract requirements using AI
        ai_response = ai_client.extract_requirements(json_data)
        
        # Parse the response
        requirements = parser.parse_requirements(ai_response)
        
        return jsonify({
            'functional': requirements['functional'],
            'non_functional': requirements['non_functional']
        })
        
    except json.JSONDecodeError:
        return jsonify({'error': 'Invalid JSON file'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)