#!/usr/bin/env python

from coap.coap import coap as coapClient
from coap.coapOption import coapOption

import json

from config import auth
from config import device
from config import broker_address

import logging
logging.basicConfig()
#logging.getLogger('coap').setLevel(logging.DEBUG)


def main():
    #client = CoapClient(broker_address)
    client = CoapClient("[::1]")
    client.set_credentials(auth["uuid"] , auth["token"])

    path = "messages"
    message = json.dumps( { "devices": [ device["uuid"] ], "payload": { "black": "on" }} )
    print("publishing: path=" + path + " message=" + message)
    client.post(path, message, on_publish)

def on_publish(client, response):
    print("published")
    client.close()


class CoapClient(coapClient):

    def __init__(self, destination):
        coapClient.__init__(self, udpPort=50000)
        self.destination = destination

    def set_credentials(self, uuid, token):
        # meshblu specific auth scheme
        self._opt_uuid = TextOption(98, uuid)
        self._opt_token = TextOption(99, token)

    def post(self, path, message, callback):
        coap_uri = "coap://{0}/{1}".format(self.destination, path)
        auth_options = [ self._opt_uuid, self._opt_token]
        response = self.POST(coap_uri, options=auth_options, payload=bytearray(message))
        callback(self, response)

class TextOption(coapOption):
    
    def __init__(self, optionNumber, value):
        coapOption.__init__(self, optionNumber)
        self.value = value
    
    def getPayloadBytes(self):
        return [ord(b) for b in self.value]


main()
