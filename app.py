#!/usr/bin/python
# -*- coding:utf-8 -*-

from flask import Flask, request, jsonify, send_from_directory, redirect # , send_file
from flask_cors import CORS
import pdf
import lng

app = Flask(__name__)
CORS(app)

@app.route('/docs')
def send_docs_root():
    return redirect("docs/index.html", code=308)

@app.route('/docs/<path:path>')
def send_docs(path):
    return send_from_directory('docs', path)

@app.post("/extractor")
def post_extractor():
    if 'file' not in request.files:
        return jsonify({'error': 'Bad Request', 'message': 'File is missing'}), 400

    file = request.files['file']

    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        return jsonify({'error': 'Bad Request', 'message': 'No selected file'}), 400

    if not allowed_file(file.filename, {'pdf'}):
        return jsonify({'error': 'Unsupported Media Type', 'message': 'Unsupported file extension'}), 415

    text = pdf.toText(file)
    lang = lng.detect(text)
    
    return '\n'.join([lang, text]), 200

def allowed_file(filename, allowed_extensions):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions
