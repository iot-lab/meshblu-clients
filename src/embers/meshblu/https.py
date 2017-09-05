import requests
import http

import logging

def set_insecure():
    # ignore (=capture) SSL warnings caused by verify=False
    logging.captureWarnings(True)
    Client.verify = False

class Client(http.Client):
    verify = True

    def __init__(self, broker_host, auth=None):
        self.broker_url = "https://{}/".format(broker_host)
        self.auth = auth

    def _call(self, method, path, json=None, auth=None):
        url = self.broker_url + path
        auth = auth or self.auth
        return http._call(url, method, auth, json=json, verify=self.verify)
