#!/usr/bin/env python

import sys
import json
import urllib2
import os,binascii

oauth_token='foobar'
num_errors=0

with open('../data/sample_court_1.json') as f:
    sample_court_json_1 = f.read()
sample_court_1 = json.loads(sample_court_json_1)
with open('../data/sample_court_2.json') as f:
    sample_court_json_2 = f.read()
sample_court_2 = json.loads(sample_court_json_2)
with open('../data/sample_court_3.json') as f:
    sample_court_json_3 = f.read()
sample_court_3 = json.loads(sample_court_json_3)

def same_arrays(a,b):
    for i,item in enumerate(a):
        if b[i] and b[i] != item:
            return False
    else:
        return True

def fail(message):
    global num_errors
    num_errors = num_errors + 1
    print("FAIL: "+str(message))

def check(description, response, status_code, body=None):
    print(description+"..."),
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
            print("OK")
    else:
        print("OK")

def check_put(description, uuid, court_json, expected_status_code, expected_slug=None):
    res = put(uuid, court_json)
    print(description+"... "),
    if res['status_code'] == expected_status_code:
        if res['status_code'] in (200,201):
            if res.get('public_url'):
                if expected_slug in res['public_url']:
                    print("OK")
                else:
                    print("Wrong URL %s. Slug should be %s.", (res['public_url'], expected_slug))
            else:
                print("Response didn't include public_url: "+str(res))
        else:
            print("OK")
    else:
        fail("Different status codes: expected %d, got %d (%s)" % (expected_status_code, res['status_code'], res['body']))

def check_published(description, slug, name):
    print(description),
    response = http(get_url=base_url+'courts/'+slug)['text']
    if name in response:
        print("OK")
    else:
        print("Error. Court was not correctly published. Received: "+response)

def http(method='GET', uuid='', auth=False, body=None, get_url=None):

    url = get_url if get_url else base_url+'courts/'+uuid
    opener = urllib2.build_opener(urllib2.HTTPHandler)
    request = urllib2.Request(url, data=body)
    request.get_method = lambda: method
    request.add_header('Content-type', 'application/json')
    request.add_header('Accept', 'application/json')
    if auth:
        request.add_header('Authorization', 'Bearer ' + oauth_token)
    try:
        response = opener.open(request)
    except urllib2.HTTPError as e:
        response = e
    return {'status_code': response.getcode(), 'text': response.read()};


def get(url, auth=True):
    return http('GET', uuid, auth)


def put(uuid, json_request, auth=True):
    response = http('PUT', uuid, auth, json_request)
    code = response['status_code']
    body = response['text']
    result = {'status_code':code, 'body':body}
    if code==200 or code==201:
        result['public_url'] = json.loads(body)['public_url']
    return result


def delete(uuid, auth=True):
    return http('DELETE', uuid, auth)


def random_uuid():
    return (binascii.b2a_hex(os.urandom(4)) +
            "-" +
            binascii.b2a_hex(os.urandom(2)) +
            "-1000-8000-" +
            binascii.b2a_hex(os.urandom(6)))

if __name__ == "__main__":
    global base_url
    if len(sys.argv) != 2:
        print "usage: %s <api_endpoint_url>" % sys.argv[0]
        print "For example, https://safe-garden-8494.herokuapp.com/"
        sys.exit(-1)
    else:
        base_url = sys.argv[1]

    uuid1 = random_uuid()
    uuid2 = random_uuid()

 #   check('bad auth on put',       put('foo-bar', '[]', auth=False), 403)
 #   check('bad auth on delete',    delete('foo-bar', auth=False), 403)

    check_put('create a court',
              uuid1, sample_court_json_1, 201, sample_court_1['slug'])

    check_put('bad json payload',
              uuid1, 'this is not json', 400, sample_court_1['slug'])

    check_put('update a court',
              uuid1, sample_court_json_1, 200, sample_court_1['slug'])

    check_published('check if court correctly published', sample_court_1['slug'], sample_court_1['name'])

    check_put('create another court',
              uuid2, sample_court_json_2, 201, sample_court_2['slug'])

    check_put('create a court with a bad uuid',
              'bad-uuid', sample_court_json_3, 400)

    check('delete court 1',
          delete(uuid1), 200)
    check('delete court 2',
          delete(uuid2), 200)

    print("done: %d errors" % num_errors)
