#!/usr/bin/python
# -*- coding:utf-8 -*-
import os
from collections import namedtuple
from pathlib import Path

DEFAULT_STORAGE_DIR = './data'


def dir():
    return os.environ['STORAGE_DIR'] if 'STORAGE_DIR' in os.environ else DEFAULT_STORAGE_DIR

def txt_dir():
    return os.path.join(dir(), 'txt')

def pdf_dir():
    return os.path.join(dir(), 'pdf')

def meta_dir():
    return os.path.join(dir(), 'meta')

def dirs():
    DirsTuple = namedtuple('Dirs', 'pdf txt meta')
    return DirsTuple(pdf=pdf_dir(), txt=txt_dir(), meta=meta_dir())

def ensure_path(file_path):
    directory = os.path.dirname(file_path)
    Path(directory).mkdir(parents=True, exist_ok=True)
