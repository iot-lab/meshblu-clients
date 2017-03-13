import paho.mqtt.client as mqtt
import json


def get_subscriber(target_uuid):
    client = mqtt.Client()
    class Subscriber:
        def connect(self, broker_address, target_token):
            client.username_pw_set(target_uuid, target_token)
            client.connect(broker_address)
        def loop_forever(self):
            client.loop_forever()
        def disconnect(self):
            client.disconnect()

    subscriber = Subscriber()
    _setup_client(client, subscriber)
    _setup_subscriber(subscriber, target_uuid)
    return subscriber


def _setup_client(client, subscriber):
    client.on_connect = _on_connect
    client.on_subscribe = _on_subscribe
    client.on_message = _on_message

    client.sub = subscriber


def _setup_subscriber(sub, target_uuid):
    sub.target_uuid = target_uuid
    sub.message_count = 0
    sub.on_message = lambda sub, message: None
    sub.on_subscribe = lambda sub: None


def _on_connect(client, userdata, flags, rc):
    topic = client.sub.target_uuid
    client.subscribe(topic)

def _on_subscribe(client, userdata, mid, granted_qos):
    client.sub.on_subscribe(client.sub)

def _on_message(client, userdata, message):
    message = json.loads(message.payload)["data"]
    client.sub.message_count += 1
    class Message:
        payload = message["payload"]
        from_uuid = message["fromUuid"]
    client.sub.on_message(client.sub, Message())
