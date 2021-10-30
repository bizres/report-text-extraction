#!/usr/bin/python
# -*- coding:utf-8 -*-
import os
import uuid

DEFAULT_STORAGE_DIR = './data'


def save_files(pdf, text):
    digest = uuid.uuid4()
    save_text(digest, text)
    save_pdf(digest, pdf)
    return str(digest)


def save_pdf(digest, file):
    file.save(create_file_name(digest, 'pdf'))


def save_text(digest, file):
    write_file(file, create_file_name(digest, 'txt'))


def create_file_name(digest, extension):
    storage_dir = os.environ['STORAGE_DIR'] if 'STORAGE_DIR' in os.environ else DEFAULT_STORAGE_DIR
    return "{dir}/{hash}.{ext}".format(dir=storage_dir, hash=digest, ext=extension)


def write_file(file, file_name):
    with open(file_name, 'w') as f:
        f.write(file)
