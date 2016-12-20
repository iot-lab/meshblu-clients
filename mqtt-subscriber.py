#!/usr/bin/env python

import paho.mqtt.client as mqtt
import json

from config import device
from config import broker_address


def main():
	client = mqtt.Client()
	client.username_pw_set(device["uuid"] , device["token"])
	client.on_connect = on_connect
	client.on_message = on_message
	client.connect(broker_address)
	client.loop_forever()

def on_connect(client, userdata, flags, rc):
	print("connected")
	topic = device["uuid"]
	print("subscribing to topic " + topic)
	client.subscribe(topic)

def on_subscribe(client, userdata, mid, granted_qos):
	print("subscribed")

def on_message(client, userdata, message):
	print("message: %s, qos: %d" % (message.payload, message.qos))
	#client.disconnect()


main()
