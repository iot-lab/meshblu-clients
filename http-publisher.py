#!/usr/bin/env python

import requests
import json

from config import broker_address as HOST
from config import device as DEVICE
from config import auth as GATEWAY

def main():
    headers = {
        'Content-Type': 'application/json'
    }

    body = {
            'devices': DEVICE['uuid'],
            'payload': {
                        "example_key":"example_value"
            }
    }

    print "Publishing to gateway (uuid): {}\n".format(GATEWAY['uuid'])
    print "Publishing from device (uuid): {}\n".format(DEVICE['uuid'])

    try:
        response = requests.request("POST", "http://{}/messages".format(HOST), headers=headers, data=json.dumps(body), auth=(GATEWAY['uuid'], GATEWAY['token']))
    except requests.ConnectionError:
        print "Couldn't publish to EMBERS"
        exit(1)

    if response.status_code is 204:
        print "Message sent with success"
    else:
        print "Something went wrong. Status Code returned: {}".format(response.status_code)

main()
