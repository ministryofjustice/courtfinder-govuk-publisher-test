#!/usr/bin/env python

import requests
import json
import sys

base_url='http://127.0.0.1:8000/court/'
oauth_token='foobar'

#with open('../data/sample_court.json') as f:
#    sample_court_json = f.read()

sample_court_json_1 = '{"name":"blah","slug":"blah","updated_at": "2014-03-18T12:33:12.176Z","closed":false,"alert":"","lat":0.0,"lon":0.0,"number":"200","DX":"2039D"}'

headers = {'Authorization': 'Bearer '+oauth_token}

def same_arrays(a,b):
    for i,item in enumerate(a):
        if b[i] and b[i] != item:
            return False
    else:
        return True

def check(request, status_code, body=None, win='.'):
    if request.status_code != status_code:
        print "Different status codes: expected %d, got %d" % (status_code, request.status_code)
        print request.text
    elif body:
        b = json.loads(body)
        r = json.loads(request.text)
        if type(b) == type([]) and not same_arrays(r,b):
            print "Different arrays: expected %s, got %s" % (body, request.text)
        elif r != b:
            print "Different objects: expected %s, got %s" % (body, request.text)
        else:
            sys.stdout.write(win)
    else:
        sys.stdout.write(win)


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
    check(delete('all-the-things'), 200)
    check(put('foo-bar', '[]', auth=False), 403)
    check(list(), 200, '[]')
    check(get('22984u-3482u49u'), 404)
    check(put('22984u-3482u49u', sample_court_json_1), 201)
    check(put('22984u-3482u49u', sample_court_json_1), 200)
    check(list(), 200, '['+sample_court_json_1+']')
    check(get('22984u-3482u49u'), 200, sample_court_json_1)
    check(list(), 200, '['+sample_court_json_1+']')
    check(delete('22984u-3482u49u'), 200)
    check(list(), 200, '[]')
    print "done"
