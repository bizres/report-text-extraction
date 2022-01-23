#!/usr/bin/python
# -*- coding:utf-8 -*-
import os

from flask import Flask, request, jsonify, send_from_directory, redirect  # , send_file
from flask_cors import CORS
from flask_httpauth import HTTPBasicAuth

import lng
import pdf
import storage
import services

app = Flask(__name__)
auth = HTTPBasicAuth()
CORS(app)


@app.route('/docs')
def send_docs_root():
    return redirect("docs/index.html", code=308)


@app.route('/docs/<path:path>')
def send_docs(path):
    return send_from_directory('docs', path)


@app.post('/pdfstotext')
@app.get('/pdfstotext')
@auth.login_required()
def post_pdfstotext():
    services.airtable_pdfs_to_local_txt()

@app.post("/extractor")
@auth.login_required()
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

    uuid = storage.save_files(file, text)

    return jsonify({'lang': lang, 'pdf': uuid + ".pdf", 'text': uuid + '.txt'}), 200


def allowed_file(filename, allowed_extensions):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions


@auth.verify_password
def authenticate(username, password):
    assert ('BASIC_AUTH_USER' in os.environ)
    assert ('BASIC_AUTH_PWD' in os.environ)
    return (username == os.environ['BASIC_AUTH_USER']) and (password == os.environ['BASIC_AUTH_PWD'])
