#!/usr/bin/env python

import json
import sys
import urllib2

base_url='http://127.0.0.1:8000/court/'
oauth_token='foobar'
num_errors=0
put_tmpl='{"public_url":"https://www.gov.uk/prefix/%s"}'

#with open('../data/sample_court.json') as f:
#    sample_court_json = f.read()

sample_court_json_1 = '{"name":"blah","slug":"blah","updated_at": "2014-03-18T12:33:12.176Z","closed":false,"alert":"","lat":0.0,"lon":0.0,"number":"200","DX":"2039D"}'

def same_arrays(a,b):
    for i,item in enumerate(a):
        if b[i] and b[i] != item:
            return False
    else:
        return True

def fail(message):
    global num_errors
    num_errors = num_errors + 1
    print "FAIL: "+str(message)

def check(description, response, status_code, body=None, win='WIN'):
    sys.stdout.write(description+"...")
    if response['status_code'] != status_code:
        fail("Different status codes: expected %d, got %d" % (status_code, response['status_code']))
    elif body:
        b = json.loads(body)
        r = json.loads(response['text'])
        if type(b) == type([]) and not same_arrays(r,b):
            fail("FAIL: Different arrays: expected %s, got %s" % (body, response['text']))
        elif r != b:
            fail("FAIL: Different objects: expected %s, got %s" % (body, response['text']))
        else:
            print win
    else:
        print win

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

def get(uuid, auth=True):
    return http('GET', uuid, auth)

def put(uuid, json, auth=True):
    return http('PUT', uuid, auth, json)

def list(auth=True):
    return http('GET', '', auth)

def delete(uuid, auth=True):
    return http('DELETE', uuid, auth)


if __name__ == "__main__":
    check('delete all the things', delete('all-the-things'), 200)
    check('bad auth on put',       put('foo-bar', '[]', auth=False), 403)
    check('bad auth on get',       put('foo-bar', '[]', auth=False), 403)
    check('bad auth on list',      put('foo-bar', '[]', auth=False), 403)
    check('check empty list',      list(), 200, '[]')
    check('missing court',         get('de305d54-75b4-431b-adb2-eb6b9e546013'), 404)
    check('create a court',        put('de305d54-75b4-431b-adb2-eb6b9e546013', sample_court_json_1), 201)
    check('bad json payload',      put('de305d54-75b4-431b-adb2-eb6b9e546013', 'bad json'), 400)
    check('update a court',        put('de305d54-75b4-431b-adb2-eb6b9e546013', sample_court_json_1), 200)
    check('check only one court',  list(), 200, '['+sample_court_json_1+']')
    check('check single court',    get('de305d54-75b4-431b-adb2-eb6b9e546013'), 200, sample_court_json_1)
    check('delete court',          delete('de305d54-75b4-431b-adb2-eb6b9e546013'), 200)
    check('check empty list 2',    list(), 200, '[]')
    check('create court 2',        put('de305d54-75b4-431b-adb2-eb6b9e546014', sample_court_json_1), 201)
    check('create a court',        put('de305d54-75b4-431b-adb2-eb6b9e546015', sample_court_json_1), 201)
    check('check two courts',      list(), 200, '['+sample_court_json_1+','+sample_court_json_1+']')
    check('bad uuid',              put('bad-uuid', sample_court_json_1), 400)
    check('check PUT response',    put('de305d54-75b4-431b-adb2-eb6b9e546013', sample_court_json_1), 201, put_tmpl % 'blah')
    check('clean up',              delete('all-the-things'), 200)
    print "done: %d errors" % num_errors
