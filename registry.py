#!/usr/bin/env python

import json
import sys

import embers.meshblu.http as http


def main():
    if len(sys.argv) < 2:
        prog = sys.argv[0]
        print("usage: " + prog + " list|register|unregister <uuid>|reset <uuid>")
        print("       " + prog + " update <uuid> <key=value> [key=value]...")
        print("       " + prog + " init_config [<broker address>]")
        return

    cmd = sys.argv[1]
    if   cmd == "list":
        query = dict([ x.split("=") for x in sys.argv[2:] ])
        list_devices(query)
    elif cmd == "register":
        register_device()
    elif cmd == "unregister":
        unregister_device(uuid=sys.argv[2])
    elif cmd == "reset":
        reset_token(device_uuid=sys.argv[2])
    elif cmd == "update":
        uuid = sys.argv[2]
        query = dict([ x.split("=") for x in sys.argv[3:] ])
        update_device(uuid=uuid, metadata=query)
    elif cmd == "init_config":
        broker_address = sys.argv[2:3] or "127.0.0.1"
        init_config(broker_address)
    else:
        print("unknown command: " + cmd)
        sys.exit(1)


def list_devices(query=None):
    api = get_meshblu_api()
    devices = api.get_devices(query)
    print(json.dumps(devices))


def register_device():
    api = get_meshblu_api()
    register_payload = { "test key": "test value" }
    device = api.register_device(register_payload)
    device = { "uuid": device["uuid"], "token": device["token"] }
    print(json.dumps(device))


def unregister_device(uuid):
    api = get_meshblu_api()
    ret = api.unregister_device(uuid)
    print(json.dumps(ret))


def update_device(uuid, metadata):
    api = get_meshblu_api()
    ret = api.update_metadata(uuid, metadata)
    # ret == null


def reset_token(device_uuid):
    api = get_meshblu_api()
    ret = api.reset_token(device_uuid)
    print(json.dumps(ret))


def init_config(broker_address):
    api = http.Client(broker_address)
    device = api.register_device({"device":"test_device"})
    gateway = api.register_device({"device":"gateway"})

    device = { "uuid": device['uuid'], "token": device['token'] }
    gateway = { "uuid": gateway['uuid'], "token": gateway['token'] }

    conf = "gateway = {}\ndevice = {}\nbroker_address = '{}'\n"
    open("config.py", 'w') \
        .write(conf.format(gateway, device, broker_address))


def get_config():
    class config: pass  # namespace
    execfile("config.py", config.__dict__)
    return config()


def get_meshblu_api():
    config = get_config()
    auth = (config.gateway['uuid'], config.gateway['token'])
    return http.Client(config.broker_address, auth)


main()
