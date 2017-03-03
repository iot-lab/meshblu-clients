#!/usr/bin/env python

from config import gateway as device
from config import broker_address

from tests.subscriber import OneShotSubscriber as Subscriber


def main():
    sub = Subscriber()
    sub.broker = broker_address
    sub.auth = (device["uuid"] , device["token"])
    sub.subscribe(device["uuid"])
    print("subscribed to: {}".format(sub.client.target_uuid))
    ret = sub.get_message()
    print(ret.payload)


main()
