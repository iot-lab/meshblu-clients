#!/usr/bin/env python

import paho.mqtt.client as mqtt
import json

from config import auth
from config import device
from config import broker_address


def main():
	client = mqtt.Client()
	client.username_pw_set(auth["uuid"] , auth["token"])
	client.on_connect = on_connect
	client.on_publish = on_publish
	client.connect(broker_address)
	client.loop_forever()

def on_connect(client, userdata, flags, rc):
	print("connected")
	topic = "message"
	message = json.dumps( { "devices": [ device["uuid"] ], "payload": { "data": "FRANCISCO!" }} )
	print("publishing: topic=" + topic + " message=" + message)
	client.publish(topic, message)

def on_publish(client, userdata, mid):
	print("published")
	client.disconnect()


main()
