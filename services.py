#!/usr/bin/python
# -*- coding:utf-8 -*-

import config
import requests
import os
import io
import storage
import urllib3
import pdf
from pathlib import Path


def airtable_pdfs_to_local_txt():
    airtable_config = config.airtable()
    print(airtable_config)

    url = 'https://api.airtable.com/v0/' + airtable_config.base_id + '/' + 'CrawlResults' + '?fields%5B%5D=PDF'

    headers = {"Authorization": "Bearer " + airtable_config.api_key}

    target_dir = os.path.join(storage.dir(), 'txt')

    # collect all records first as otherwise offset is not valid after certain amount of time
    records = []
    offset = ''
    while True:
        response = requests.get(url + offset, headers=headers)
        response.raise_for_status()

        if 200 != response.status_code:
            print(response)
            return

        airtable_response = response.json()

        # pagination
        if 'offset' in airtable_response:
            offset = '&offset=' + airtable_response['offset']
        else:
            offset = ''

        records.extend(airtable_response['records'])

        if '' == offset:
            # no more pages
            break


    print('Records to process', len(records))

    # process all single records
    [process_record(rec, target_dir) for rec in records]


def process_record(rec, target_dir):
    print('----------')
    id = rec['id']
    print(id)

    filepath = os.path.join(target_dir, id + '.txt')
    if os.path.isfile(filepath):
        # already exists -> skip
        return

    fields = rec['fields']

    if not 'PDF' in fields:
        return

    text = fetch_pdf(fields)

    if text is None:
        return

    directory = os.path.dirname(filepath)
    Path(directory).mkdir(parents=True, exist_ok=True)

    with open(filepath, 'w', encoding="utf8") as f:
        f.write(text)
    

def fetch_pdf(fields):
    url = fields['PDF'][0]['url']
    # file_name = fields['PDF'][0]['filename']
    http = urllib3.PoolManager()
    r = http.request('GET', url)
    print(r.status)
    # print(type(r.data))
    file = io.BytesIO(r.data)
    # print(type(file))
    text = pdf.to_text(file)
    return text