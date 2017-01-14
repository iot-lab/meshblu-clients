#!/usr/bin/env python

from coapthon import defines
from coapthon.client.coap import CoAP
from coapthon.messages.request import Request
from coapthon.messages.option import Option
from coapthon.utils import generate_random_token
from multiprocessing import Queue
import random

import json

from config import auth
from config import device
from config import broker_address

import logging
logging.basicConfig()
#logging.getLogger('coapthon').setLevel(logging.DEBUG)

# define Meshblu specific auth options
defines.OptionRegistry.LIST[98] = defines.OptionItem(98, "username", defines.STRING, False, False)
defines.OptionRegistry.LIST[99] = defines.OptionItem(99, "password", defines.STRING, False, False)


def main():
    #client = CoapClient(broker_address)
    client = CoapClient("::1")
    client.set_credentials(auth["uuid"] , auth["token"])

    path = "messages"
    message = json.dumps( { "devices": [ device["uuid"] ], "payload": { "black": "on" }} )
    print("publishing: path=" + path + " message=" + message)
    client.post(path, message, on_publish)

def on_publish(client, response):
    print("published")
    client.stop()


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


    def post(self, path, payload, callback=None):
        request = Request()
        request.destination = self.destination
        request.code = defines.Codes.POST.number
        request.add_option(self.option_username)
        request.add_option(self.option_password)
        request.token = generate_random_token(2)
        request.uri_path = path
        request.payload = payload

        self.protocol.send_message(request)
        response = self.queue.get(block=True)

        if callback:
            callback(self, response)
        else:
            return response

    def stop(self):
        self.protocol.stopped.set()
        self.queue.put(None)

    def _wait_response(self, message):
        if message.code != defines.Codes.CONTINUE.number:
            self.queue.put(message)


main()
