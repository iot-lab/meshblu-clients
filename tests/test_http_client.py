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


def test_publish(api):
    payload = {
        "publish_from_device": Device.uuid,
        "to_gateway": Gateway.uuid,
    }
    api.auth = Device.auth
    target_uuid = Gateway.uuid
    ret = api.publish(target_uuid, payload)
    assert ret == None


def test_unregister_devices(api):
    api.unregister_device(Gateway.auth)
    api.unregister_device(Device.auth)


@pytest.fixture
def api(broker):
    return Client(broker.host)
