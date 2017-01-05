#!/usr/bin/env python

import requests
import json
import sys

import config

broker_url = "http://" + config.broker_address

def main():
    if len(sys.argv) < 2:
        print("usage: " + sys.argv[0] +
		" [list|register|unregister <uuid> <token>])")
        return

    cmd = sys.argv[1]
    if   cmd == "list":
        list_devices()
    elif cmd == "register":
        register_device()
    elif cmd == "unregister":
        unregister_device({ "uuid": sys.argv[2], "token": sys.argv[3] })
    else:
        print("unknown command: " + cmd)
        sys.exit(1)


def list_devices():
    api = get_meshblu_api()
    devices = api.get_devices(config.auth["uuid"], config.auth["token"])
    print(json.dumps(devices))

def register_device():
    api = get_meshblu_api()
    register_payload = { "test key": "test value" }
    device = api.register_device(register_payload)
    print(json.dumps(device))

def unregister_device(device):
    api = get_meshblu_api()
    ret = api.unregister_device(device["uuid"], device["token"])
    print(json.dumps(ret))


def get_meshblu_api():
    return MeshbluHTTPClient(broker_url)

class MeshbluHTTPClient(object):
    def __init__(self, broker_url):
        self.broker_url = broker_url

    def get_devices(self, auth_uuid, auth_token):
        return self._call('GET', "devices", auth_uuid, auth_token)

    def register_device(self, payload):
        return self._call('POST', "devices", None, None, json=payload)

    def unregister_device(self, device_uuid, device_token):
        return self._call('DELETE', "devices/" + device_uuid,
                          device_uuid, device_token)

    def _call(self, method, url, auth_uuid, auth_token, json=None):
        req = requests.request(
                  method,
                  self.broker_url + "/" + url,
                  json=json,
                  headers={ 'meshblu_auth_uuid': auth_uuid,
                            'meshblu_auth_token': auth_token,
                  } if auth_uuid else None)
        req.raise_for_status()
        return req.json()


main()
