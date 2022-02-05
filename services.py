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
import uuid
import json


def airtable_pdfs_to_local_txt():
    airtable_config = config.airtable()
    # print(airtable_config)

    url = 'https://api.airtable.com/v0/' + airtable_config.base_id + '/' + 'CrawlResults' + '?fields%5B%5D=PDF&fields%5B%5D=ExtractedID'

    headers = {"Authorization": "Bearer " + airtable_config.api_key}

    target_dirs = storage.dirs()

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

    # patch airtable with bulk updates x10 records
    payload = None
    i = 0
    for rec in records:
        res = process_record(rec, target_dirs)

        if not res is None:
            if payload is None:
                payload = {'records': []}

            fields = {}
            if 'id' in res:
                fields['ExtractedID'] = res['id']
            if 'status' in res:
                fields['ExtractedStatus'] = res['status']

            if len(fields) > 0:
                i = i + 1
                payload['records'].append({
                            'id': res['air_id'],
                            'fields': fields,
                        }
                )

            if 10 == i:
                i = 0
                flush(payload, airtable_config)
                payload = None

    if not payload is None:
        if len(payload['records']) > 0:
            flush(payload, airtable_config)

    print('Done')
        

def flush(payload, airtable_config):
    headers = {"Authorization": "Bearer " + airtable_config.api_key}
    url_patch = "https://api.airtable.com/v0/" + airtable_config.base_id + "/" + 'CrawlResults'
    resp = requests.patch(url_patch, json=payload, headers=headers)
    resp.raise_for_status()
    # print(resp.json())


def process_record(rec, target_dirs):
    print('----------')
    air_id = rec['id']
    print(air_id)
    res = {'air_id': air_id}

    fields = rec['fields']

    id = ''
    e_id = ''
    pdf_file_path = None
    # if pdf was already extracted on another client - reuse id
    if 'ExtractedID' in fields:
        id = fields['ExtractedID']
        e_id = id
        # print('ExtractedId', id)
        pdf_file_path = os.path.join(target_dirs.pdf, id + '.pdf')
        if os.path.isfile(pdf_file_path):
            # already extracted
            return None

    # get unique not yet existing id
    if '' == id:
        while True:
            id = str(uuid.uuid4())
            pdf_file_path = os.path.join(target_dirs.pdf, id + '.pdf')
            if not os.path.isfile(pdf_file_path):
                break
    print(id)

    if not 'PDF' in fields:
        # respond with code 'NO PDF'
        res['status'] = '01 - No PDF'
        return res

    pdf_bytes, text = fetch_pdf(fields)

    if text is None:
        # respond with code 'Failed to extract text'
        res['status'] = '02 - Failed to extract text'
        return res

    storage.ensure_path(pdf_file_path)
    pdf_bytes.seek(0)
    with open(pdf_file_path, 'wb') as f:
        f.write(pdf_bytes.getbuffer())

    txt_file_path = os.path.join(target_dirs.txt, id + '.txt')
    storage.ensure_path(txt_file_path)
    with open(txt_file_path, 'w', encoding='utf8') as f:
        f.write(text)
    
    meta = {'air_id': air_id,
            'id': id,
            'filename': fields['PDF'][0]['filename']}
    meta_file_path = os.path.join(target_dirs.meta, id + '.json')
    storage.ensure_path(meta_file_path)
    with open(meta_file_path, 'w', encoding='utf8') as f:
        json.dump(meta, f, ensure_ascii=False, indent=4)

    if id == e_id:
        # reused existing id
        return

    # upload id to airtable
    res['id'] = id
    return res


def fetch_pdf(fields):
    url = fields['PDF'][0]['url']
    # file_name = fields['PDF'][0]['filename']
    http = urllib3.PoolManager()
    r = http.request('GET', url)
    print(r.status)
    pdf_bytes = io.BytesIO(r.data)
    text = pdf.to_text(pdf_bytes)
    return pdf_bytes, text