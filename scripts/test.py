#!/usr/bin/env python

import requests
import json

base_url='http://127.0.0.1:8000/court/'
court_file='../data/sample_court.json'
oauth_token='foobar'

with open('../data/sample_court.json') as f:
    sample_court_json = f.read()

headers = {'Authorization': 'Bearer '+oauth_token}

def is_in(small, big):
    s = json.loads(small)
    b = json.loads(big)
    return all(item in b.items() for item in s.items())

def check(request, status_code, body=None, win='.'):
    if request.status_code != status_code:
        print "Different status codes: expected %d, got %d" % (status_code, request.status_code)
    elif body:
        if not is_in(request.text, body):
            print "Different objects: expected %s, got %s" % (body, request.text)
    else:
        print win,


def list():
    return requests.get(base_url, headers=headers)

def get(uuid):
    return requests.get(base_url+uuid, headers=headers)

def put(uuid, json, auth=True):
    if auth:
        return requests.put(base_url+uuid, headers=headers, data=json)
    else:
        return requests.put(base_url+uuid, data=json)

def delete(uuid):
    return requests.delete(base_url+uuid, headers=headers)


if __name__ == "__main__":
    # hidden uuid to delete every court in the database
    check(delete('all-the-things'), 200)
    check(put('foo-bar', '[]', auth=False), 403)
    check(list(), 200, '[]')
    check(get('22984u-3482u49u'), 404)
    check(put('22984u-3482u49u', sample_court_json), 201)
    check(list(), 200, sample_court_json)
