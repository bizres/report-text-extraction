#!/usr/bin/python
# -*- coding:utf-8 -*-
import os

from flask import Flask, request, jsonify, send_from_directory, redirect, after_this_request  # , send_file
from flask_cors import CORS
from flask_httpauth import HTTPBasicAuth

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


@app.post('/extract')
@app.get('/extract')
@auth.login_required()
def post_pdfstotext():
    @after_this_request
    def add_close_action(response):
        @response.call_on_close
        def process_after_request():
            services.airtable_pdfs_to_local_txt()
        return response
    return '', 202 # Accepted

@auth.verify_password
def authenticate(username, password):
    assert ('BASIC_AUTH_USER' in os.environ)
    assert ('BASIC_AUTH_PWD' in os.environ)
    return (username == os.environ['BASIC_AUTH_USER']) and (password == os.environ['BASIC_AUTH_PWD'])
