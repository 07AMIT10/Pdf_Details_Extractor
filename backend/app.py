from flask import Flask, request, jsonify
from flask_cors import CORS
from utils.pdf_processor import process_pdf
import os

app = Flask(__name__)
CORS(app)
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB limit

@app.route('/extract', methods=['POST'])
def handle_pdf():
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file uploaded'}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'error': 'Empty filename'}), 400
        
    result = process_pdf(file)
    status_code = 200 if result['success'] else 500
    return jsonify(result), status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)