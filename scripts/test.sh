#!/bin/bash

BASE_URL=http://127.0.0.1:8000/court/
COURT_FILE=../data/sample_court.json
OAUTH_TOKEN='foobar'

list() {
    curl -v -H "Authorization: Bearer $OAUTH_TOKEN"  -s "${BASE_URL}" 2>&1 | grep "HTTP/1.0"
}
get() {
    curl -v -H "Authorization: Bearer $OAUTH_TOKEN"  -s "${BASE_URL}$1" 2>&1 | grep "HTTP/1.0"
}
put() {
    curl -v -H "Authorization: Bearer $OAUTH_TOKEN"  -s -T ${COURT_FILE}  "${BASE_URL}$1" 2>&1 | grep "HTTP/1.0"
}
delete() {
    curl -v -H "Authorization: Bearer $OAUTH_TOKEN"  -s -X DELETE "${BASE_URL}$1" 2>&1 | grep "HTTP/1.0"
}


put "eed8f7c0-7ff1-11e4-a98a-0002a5d5c51b"
delete "eed8f7c0-7ff1-11e4-a98a-0002a5d5c51b"
list

put "eed8f7c0-7ff1-11e4-a98a-0002a5d5c51c"
put "eed8f7c0-7ff1-11e4-a98a-0002a5d5c51c"
put "eed8f7c0-7ff1-11e4-a98a-0002a5d5c51c"
delete "eed8f7c0-7ff1-11e4-a98a-0002a5d5c51b"
list
