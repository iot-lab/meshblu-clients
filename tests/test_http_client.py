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


def test_get_devices_with_query(api):
    query = { "test_key": "test value" }
    api.auth = Gateway.auth
    ret = api.get_devices(query)

    uuids = [ device['uuid'] for device in ret['devices'] ]
    assert Device.uuid in uuids
    assert Gateway.uuid not in uuids


def test_reset_token(api):
    reg = api.register_device()

    api.auth = Gateway.auth
    reg2 = api.reset_token(reg["uuid"])

    with pytest.raises(Exception):
        api.unregister_device((reg["uuid"], reg["token"]))
    reg = reg2
    api.unregister_device((reg["uuid"], reg["token"]))


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
