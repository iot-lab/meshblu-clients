import pytest

from embers.meshblu.coap import Client

import env
Gateway, Device = env.get_devices()


def test_setup_devices(broker):
    env.register_devices(broker)


def test_mqtt_publish(broker, subscriber):
    api = Client(broker.host)
    api.auth = Device.auth

    subscriber.auth = Gateway.auth
    subscriber.subscribe(Gateway.uuid)

    payload = {}
    ret = api.publish(Gateway.uuid, payload)
    assert ret == None

    msg = subscriber.get_message()
    assert msg.payload == payload
    assert msg.from_uuid == Device.uuid


def test_remove_devices(broker):
    env.unregister_devices(broker)
