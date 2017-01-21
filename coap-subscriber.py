#!/usr/bin/env python

from coapthon import defines
from coapthon.client.coap import CoAP
from coapthon.messages.request import Request
from coapthon.messages.request import Message
from coapthon.messages.option import Option
from multiprocessing import Queue
import random
import time

import json

from config import auth
from config import device
from config import broker_address

import logging
logging.basicConfig()
logging.getLogger('coapthon').setLevel(logging.WARNING)

# define Meshblu specific auth options
defines.OptionRegistry.LIST[98] = defines.OptionItem(98, "username", defines.STRING, False, False)
defines.OptionRegistry.LIST[99] = defines.OptionItem(99, "password", defines.STRING, False, False)


def main():
    client = CoapClient(broker_address)
    client.set_credentials(device["uuid"] , device["token"])

    path = "subscribe"
    print("subscribing: path=" + path + " device=" + device["uuid"])
    response = client.observe(path)
    on_subscribe(client, response)
    while True:
        try:
            response = client.queue.get(block=True)
            on_observe(client, response.payload)
        except KeyboardInterrupt:
            client.cancel_observe(response)
            client.stop()
            break

def on_subscribe(client, response):
    print("subscribed")

def on_observe(client, response):
    print("published: response={}".format(response))


class CoapClient(object):

    def __init__(self, broker_addr):
        self.destination = (broker_addr, 5683)
        self.protocol = CoAP(self.destination, random.randint(1, 65535), self._wait_response)
        self.queue = Queue()

    def set_credentials(self, username, password):
        # code below is Meshblu specific
        self.option_username = Option()
        self.option_password = Option()
        self.option_username.number = 98
        self.option_username.value = username
        self.option_password.number = 99
        self.option_password.value = password


    def observe(self, path, callback=None):
        request = Request()
        request.destination = self.destination
        request.code = defines.Codes.GET.number
        request.add_option(self.option_username)
        request.add_option(self.option_password)
        request.uri_path = path
        request.observe = 0

        self.protocol.send_message(request)
        response = self.queue.get(block=True)

        if callback:
            callback(self, response)
        else:
            return response

    def cancel_observe(self, response):
        message = Message()
        message.destination = self.destination
        message.code = defines.Codes.EMPTY.number
        message.type = defines.Types["RST"]
        message.token = response.token
        message.mid = response.mid

        self.protocol.send_message(message)

    def stop(self):
        self.protocol.stopped.set()
        self.queue.put(None)

    def _wait_response(self, message):
        if message.code != defines.Codes.CONTINUE.number:
            self.queue.put(message)


main()
