def get_devices():
    return (Gateway, Device)


def set_device(device, reg):
    device.auth = (reg['uuid'], reg['token'])
    device.uuid = reg['uuid']


class Gateway: pass
class Device: pass


from embers.meshblu.http import Client

def register_devices(broker):
    api = Client(broker.host)
    device = api.register_device()
    gateway = api.register_device()
    set_device(Device, device)
    set_device(Gateway, gateway)


def unregister_devices(broker):
    api = Client(broker.host)
    api.unregister_device(Gateway.auth)
    api.unregister_device(Device.auth)
