#!/usr/bin/python
# -*- coding:utf-8 -*-

import pycld2 as cld2
import traceback

def detect(text):
    try:
        isReliable, textBytesFound, details = cld2.detect( text )

        if not isReliable:
            return "--"

        lng = details[0][1]

        return lng

    except Exception as e:
        print(traceback.format_exc())
        return "--"
