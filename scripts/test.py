#!/usr/bin/env python

import json
import sys
import urllib2

base_url='http://127.0.0.1:8000/court/'
oauth_token='foobar'

#with open('../data/sample_court.json') as f:
#    sample_court_json = f.read()

sample_court_json_1 = '{"name":"blah","slug":"blah","updated_at": "2014-03-18T12:33:12.176Z","closed":false,"alert":"","lat":0.0,"lon":0.0,"number":"200","DX":"2039D"}'

def same_arrays(a,b):
    for i,item in enumerate(a):
        if b[i] and b[i] != item:
            return False
    else:
        return True

def check(response, status_code, body=None, win='.'):
    if response['status_code'] != status_code:
        print "Different status codes: expected %d, got %d" % (status_code, response['status_code'])
    elif body:
        b = json.loads(body)
        r = json.loads(response['text'])
        if type(b) == type([]) and not same_arrays(r,b):
            print "Different arrays: expected %s, got %s" % (body, response['text'])
        elif r != b:
            print "Different objects: expected %s, got %s" % (body, response['text'])
        else:
            sys.stdout.write(win)
    else:
        sys.stdout.write(win)


def get(uuid, auth=True):
    return http('GET', uuid, auth)

def put(uuid, json, auth=True):
    return http('PUT', uuid, auth, json)

def http(method='GET', uuid='', auth=False, body=None):
    opener = urllib2.build_opener(urllib2.HTTPHandler)
    request = urllib2.Request(base_url+uuid, data=body)
    request.get_method = lambda: method
    if auth:
        request.add_header('Authorization', 'Bearer ' + oauth_token)
    try:
        response = opener.open(request)
    except urllib2.HTTPError as e:
        response = e
    return {'status_code': response.getcode(), 'text': response.read()};


def list(auth=True):
    return http('GET', '', auth)


def delete(uuid, auth=True):
    return http('DELETE', uuid, auth)


if __name__ == "__main__":
    check(delete('all-the-things'), 200)
    check(put('foo-bar', '[]', auth=False), 403)
    check(list(), 200, '[]')
    check(get('22984u-3482u49u'), 404)
    check(put('22984u-3482u49u', sample_court_json_1), 201)
    check(put('22984u-3482u49u', 'bad json'), 400)
    check(put('22984u-3482u49u', sample_court_json_1), 200)
    check(list(), 200, '['+sample_court_json_1+']')
    check(get('22984u-3482u49u'), 200, sample_court_json_1)
    check(list(), 200, '['+sample_court_json_1+']')
    check(delete('22984u-3482u49u'), 200)
    check(list(), 200, '[]')
    check(delete('all-the-things'), 200)
    print "done"
