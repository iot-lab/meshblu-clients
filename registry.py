#!/usr/bin/env python

import json
import sys

import embers.meshblu.http as http


def main():
    if len(sys.argv) < 2:
        prog = sys.argv[0]
        print("usage: " + prog + " list|register|unregister <uuid> <token>")
        print("       " + prog + " init_config [<broker address>]")
        return

    cmd = sys.argv[1]
    if   cmd == "list":
        list_devices()
    elif cmd == "register":
        register_device()
    elif cmd == "unregister":
        unregister_device({ "uuid": sys.argv[2], "token": sys.argv[3] })
    elif cmd == "init_config":
        broker_address = sys.argv[2] if len(sys.argv) > 2 else "127.0.0.1"
        init_config(broker_address)
    else:
        print("unknown command: " + cmd)
        sys.exit(1)


def list_devices():
    config = get_config()
    api = get_meshblu_api()
    api.auth = (config.gateway['uuid'], config.gateway['token'])
    devices = api.get_devices()
    print(json.dumps(devices))


def register_device():
    api = get_meshblu_api()
    register_payload = { "test key": "test value" }
    device = api.register_device(register_payload)
    print("uuid: {}\ntoken: {}".format(device["uuid"], device["token"]))


def unregister_device(device):
    api = get_meshblu_api()
    device_auth = (device["uuid"], device["token"])
    ret = api.unregister_device(device_auth)
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
    return http.Client(config.broker_address)


main()
