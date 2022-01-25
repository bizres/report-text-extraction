#!/usr/bin/python
# -*- coding:utf-8 -*-

from pdfminer.high_level import extract_text
import io


def to_text(data):
    file = data
    if isinstance(file, io.BytesIO):
        file.seek(0)
    else:
        file = io.BytesIO(file.read())

    try:
        text = extract_text(file)
    except:
        text = None
        
    return text
