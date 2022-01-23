#!/usr/bin/python
# -*- coding:utf-8 -*-

import configparser
import os
from collections import namedtuple
import traceback

def get():
    config = configparser.RawConfigParser()
    config.read(os.path.join(os.path.dirname(__file__), 'config.ini'))
    return config

def airtable():
    AirtableConfig = namedtuple("AirtableConfig", "api_key base_id")

    # try get config data from environment
    try:
        if 'AIRTABLE_API_KEY' in os.environ and 'AIRTABLE_BASE_ID' in os.environ:
            return AirtableConfig( api_key = os.environ['AIRTABLE_API_KEY'], base_id = os.environ['AIRTABLE_BASE_ID'] )
    except:
        print('Failed to read Airtable config from environment.')
        print(traceback.format_exc(), flush=True)
        return None

    # try to get data from config file
    try:
        config = get()
        data = config['Airtable']
        return AirtableConfig( api_key = data['api_key'], base_id = data['base_id'] )

    except:
        print('Whether config.ini is not found or is corrupted.')
        print(traceback.format_exc(), flush=True)
        return None
