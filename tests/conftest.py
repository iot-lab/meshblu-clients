import pytest

from subscriber import OneShotSubscriber


class Broker:
    host = "127.0.0.1"
    auth = None

@pytest.fixture
def broker():
    return Broker()

@pytest.fixture
def subscriber(broker):
    sub = OneShotSubscriber()
    sub.broker = broker.host
    return sub
