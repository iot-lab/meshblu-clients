import pytest

from embers.meshblu.http import Client

import env
Gateway, Device = env.get_devices()


def test_register_gw_device(api):
    ret = api.register_device()
    assert ret["uuid"]
    assert ret["token"]
    assert ret["meshblu"]["createdAt"]
    env.set_device(Gateway, ret)


def test_register_device(api):
    metadata = { "test_key": "test value" }
    ret = api.register_device(payload=metadata)
    assert ret["test_key"] == "test value"
    env.set_device(Device, ret)


def test_get_devices(api):
    api.auth = Gateway.auth
    ret = api.get_devices()
    uuids = [ device['uuid'] for device in ret['devices'] ]
    assert Gateway.uuid in uuids
    assert Device.uuid in uuids

    device = [ d for d in ret['devices'] if d["uuid"] == Device.uuid ][0]
    assert device.has_key("test_key")
    assert device["test_key"] == "test value"


def test_publish(api, subscriber):
    payload = {
        "publish_from_device": Device.uuid,
        "to_gateway": Gateway.uuid,
    }

    subscriber.subscribe_device(Gateway)

    api.auth = Device.auth
    api.publish(Gateway.uuid, payload)

    msg = subscriber.get_message()
    assert msg.payload == payload
    assert msg.from_uuid == Device.uuid


def test_unregister_devices(api):
    api.unregister_device(Gateway.auth)
    api.unregister_device(Device.auth)


@pytest.fixture
def api(broker):
    return Client(broker.host)
