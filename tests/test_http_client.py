import pytest

from embers.meshblu.http import Client

import env
Gateway, Device = env.get_devices()


def test_register_gw_device(api):
    ret = api.register_device()
    env.set_device(Gateway, ret)


def test_register_device(api):
    payload = { "test_key": "test value" }
    ret = api.register_device(payload)
    env.set_device(Device, ret)


def test_get_devices(api):
    api.auth = Gateway.auth
    ret = api.get_devices()
    uuids = [ device['uuid'] for device in ret['devices'] ]
    assert Gateway.uuid in uuids
    assert Device.uuid in uuids


def test_publish(api, subscriber):
    payload = {
        "publish_from_device": Device.uuid,
        "to_gateway": Gateway.uuid,
    }
    api.auth = Device.auth

    subscriber.auth = Gateway.auth
    subscriber.subscribe(Gateway.uuid)

    ret = api.publish(Gateway.uuid, payload)
    assert ret == None

    msg = subscriber.get_message()
    assert msg.payload == payload
    assert msg.from_uuid == Device.uuid


def test_unregister_devices(api):
    api.unregister_device(Gateway.auth)
    api.unregister_device(Device.auth)


@pytest.fixture
def api(broker):
    return Client(broker.host)
