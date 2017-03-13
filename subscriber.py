#!/usr/bin/env python

from config import gateway
from config import broker_address

import embers.meshblu.subscriber as subscriber
import sys


def main():
    sub = subscriber.get_subscriber(gateway["uuid"])
    sub.on_message = on_message
    sub.on_subscribe = on_subscribe
    sub.connect(broker_address, gateway["token"])
    sys.stdout.write("subscribing...")
    sys.stdout.flush()
    try:
        sub.loop_forever()
    except KeyboardInterrupt:
        print("interrupted")


def on_message(sub, message):
    print(message.payload)
    sub.disconnect()


def on_subscribe(sub):
    print("\rsubscribed to: " + sub.target_uuid)


main()
