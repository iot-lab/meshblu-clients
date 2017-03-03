import paho.mqtt.client as mqtt
import threading
import json


class OneShotSubscriber(threading.Thread):
    broker = "broker host"
    auth = ("uuid", "token")

    def subscribe(self, target_uuid):
        client = mqtt.Client()
        client.username_pw_set(*self.auth)
        client.on_connect = on_connect
        client.on_message = on_message
        client.target_uuid = target_uuid
        client.connect(self.broker)
        self.client = client
        self.start()

    def get_message(self):
        self.join()
        class Message:
            payload = self.client.message["payload"]
            from_uuid = self.client.message["fromUuid"]
        return Message()

    def run(self):
        self.client.loop_forever()

def on_connect(client, userdata, flags, rc):
    topic = client.target_uuid
    client.subscribe(topic)

def on_subscribe(client, userdata, mid, granted_qos):
    pass

def on_message(client, userdata, message):
    client.message = json.loads(message.payload)["data"]
    client.disconnect()
