#!/usr/bin/python
# -*- coding:utf-8 -*-

import pdfplumber

def toText(file):
    with pdfplumber.open(file) as pdf:
        return '\n'.join([page.extract_text() for page in pdf.pages])
