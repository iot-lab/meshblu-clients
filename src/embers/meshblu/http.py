import requests
import json


class Client:
    def __init__(self, broker_host, auth=None):
        self.broker_url = "http://{}/".format(broker_host)
        self.auth = auth

    def get_devices(self):
        return self._call('GET', "devices")

    def register_device(self, payload=None):
        return self._call('POST', "devices", json=payload)

    def unregister_device(self, device_auth):
        uuid = device_auth[0]
        return self._call('DELETE', "devices/" + uuid, auth=device_auth)

    def publish(self, target_uuid, payload):
        body = {
                 'devices': [target_uuid],
                 'payload': payload,
        }
        return self._call('POST', "messages", json=body)

    def _call(self, method, path, json=None, auth=None):
        url = self.broker_url + path
        auth = auth or self.auth
        return _call(url, method, auth, json=json)


def _call(url, method, auth, json=None):
    req = requests.request(
              url=url,
              method=method,
              json=json,
              auth=auth,
    )
    req.raise_for_status()
    return req.json() if req.text else None
