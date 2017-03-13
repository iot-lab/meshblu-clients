import embers.meshblu.subscriber as subscriber
import threading


class OneShotSubscriber(threading.Thread):
    broker = "broker host"

    def subscribe_device(self, device):
        target_uuid, target_token = device.auth

        def on_message(sub, message):
            self.message = message
            sub.disconnect()

        sub = subscriber.get_subscriber(target_uuid)
        sub.on_message = on_message
        sub.connect(self.broker, target_token)

        self.client = sub
        self.start()

    def get_message(self):
        self.join()
        return self.message

    def run(self):
        self.client.loop_forever()
