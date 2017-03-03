#!/usr/bin/env python

from config import broker_address, device, gateway

import sys
import importlib
protocol = sys.argv[1] if len(sys.argv) > 1 else "http"
protocol = importlib.import_module("embers.meshblu."+protocol)


def main():

    client = protocol.Client(broker_address)

    payload = { "test key": "test value" }

    print("Publishing  to gateway: " + gateway['uuid'])
    print("           from device: " + device['uuid'])

    client.auth = (device['uuid'], device['token'])
    client.publish(target_uuid=gateway['uuid'], payload=payload)

main()
