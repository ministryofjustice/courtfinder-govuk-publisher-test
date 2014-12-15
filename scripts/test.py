#!/usr/bin/env python

import json
import urllib2

base_url='http://127.0.0.1:8000/court/'
oauth_token='foobar'
num_errors=0
put_tmpl='{"public_url":"https://www.gov.uk/prefix/%s"}'

#with open('../data/sample_court.json') as f:
#    sample_court_json = f.read()

sample_court_json_1 = '{"name":"blah","slug":"blah","updated_at": "2014-03-18T12:33:12.176Z","closed":false,"alert":"","lat":0.0,"lon":0.0,"number":"200","DX":"2039D"}'
sample_court = json.loads(sample_court_json_1)

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

def check_put(description, uuid, court_json, expected_status_code, expected_slug):
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
        fail("Different status codes: expected %d, got %d" % (expected_status_code, res['status_code']))


def http(method='GET', uuid='', auth=False, body=None, get_url=None):

    url = get_url if get_url else base_url+uuid

    opener = urllib2.build_opener(urllib2.HTTPHandler)
    request = urllib2.Request(url, data=body)
    request.get_method = lambda: method
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


if __name__ == "__main__":
    # clean up
    delete('de305d54-75b4-431b-adb2-eb6b9e546013')
    delete('de305d54-75b4-431b-adb2-eb6b9e546014')
    delete('de305d54-75b4-431b-adb2-eb6b9e546015')

    check('bad auth on put',       put('foo-bar', '[]', auth=False), 403)
    check('bad auth on delete',    delete('foo-bar', auth=False), 403)

    check_put('create a court',
              'de305d54-75b4-431b-adb2-eb6b9e546013', sample_court_json_1, 201, sample_court['slug'])

    check_put('bad json payload',
              'de305d54-75b4-431b-adb2-eb6b9e546013', 'this is not json', 400, sample_court['slug'])


    check_put('update a court',
              'de305d54-75b4-431b-adb2-eb6b9e546013', sample_court_json_1, 200, sample_court['slug'])

#    res = put('de305d54-75b4-431b-adb2-eb6b9e546013', sample_court_json_1)
#    print json.loads(res['body'])['public_url']
#    http(get_url=res['public_url'])

#    check('check single court',    get('de305d54-75b4-431b-adb2-eb6b9e546013'), 200, sample_court_json_1)
#    check('delete court',          delete('de305d54-75b4-431b-adb2-eb6b9e546013'), 200)
#
#    check('create court 2',        put('de305d54-75b4-431b-adb2-eb6b9e546014', sample_court_json_1), 201)
#    check('create a court',        put('de305d54-75b4-431b-adb2-eb6b9e546015', sample_court_json_1), 201)
#
#    check('bad uuid',              put('bad-uuid', sample_court_json_1), 400)
#    check('check PUT response',    put('de305d54-75b4-431b-adb2-eb6b9e546013', sample_court_json_1), 201, put_tmpl % 'blah')
#    check('clean up',              delete('all-the-things'), 200)
    print("done: %d errors" % num_errors)
