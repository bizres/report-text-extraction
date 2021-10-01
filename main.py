#!/usr/bin/python
# -*- coding:utf-8 -*-

import pdfplumber

def main():
    files = {'pdffile.pdf', 'lorem-ipsum.pdf'}
    for file in files:
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                print(text)

if __name__ == '__main__':
    main()
