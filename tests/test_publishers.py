import pytest

import env

protocols = ["http", "mqtt", "coap" ]


def test_setup_devices(broker):
    env.register_devices(broker)


@pytest.mark.parametrize("protocol", protocols)
def test_publish(broker, subscriber, protocol):

    Gateway, Device = env.get_devices()
    subscriber.subscribe_device(Gateway)

    api = import_client(protocol)(broker.host)

    payload = { "test key": "test value" }

    api.auth = Device.auth
    api.publish(Gateway.uuid, payload)

    msg = subscriber.get_message()
    assert msg.payload == payload
    assert msg.from_uuid == Device.uuid


def test_remove_devices(broker):
    env.unregister_devices(broker)

def import_client(protocol):
    return __import__("embers.meshblu." + protocol,
                      fromlist=["Client"]).Client
