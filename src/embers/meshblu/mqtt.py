import paho.mqtt.client as mqtt
import json


class Client:
    def __init__(self, broker_host, auth=None):
	client = mqtt.Client()
	client.on_connect = on_connect
	client.on_publish = on_publish
        self.client = client

        self.broker = broker_host
        self.auth = auth

    def publish(self, target_uuid, payload):
        self.client.payload = payload
        self.client.target_uuid = target_uuid

	self.client.username_pw_set(*self.auth)
	self.client.connect(self.broker)
	self.client.loop_forever()


def on_connect(client, userdata, flags, rc):
    topic = "message"
    message = {
        "devices": [ client.target_uuid ],
        "payload": client.payload,
    }
    message = json.dumps(message)
    client.publish(topic, message)

def on_publish(client, userdata, mid):
    client.disconnect()
