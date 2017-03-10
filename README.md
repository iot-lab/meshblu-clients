This is the Python [Meshblu](https://meshblu.readme.io/) clients sample repository.

Installing
----------

To run these sample clients, install the required libs
listed in requirements.txt, then install the package itself,
e.g. in a dedicated python virtual env:

	mkvirtualenv py
	pip install -r requirements.txt
	pip install .


You will need a running instance of Meshblu.
Either use the production instance at `data.embers.city`,
or install and run your own local instance.

To install and run a local instance of Meshblu,
see https://github.com/iot-lab/meshblu


Configuring
-----------

The EMBERS use-case of Meshblu revolves around a "gateway"
device, the target of events publishing, and a "sensor" device,
the origin of events.  These devices need to be created on the
Meshblu instance prior to further using the sample clients.

To configure the Meshblu instance, use:

	./registry.py init_config


This will create the devices and generate file `config.py` with
devices info (uuid, token) and a reference to the (local) broker.
This configuration is in turn loaded by the sample cli programs.

To specify an alternate Meshblu instance for the configuration,
use the following:

	./registry.py init_config <meshblu_broker_address>


Checking it works
-----------------

To check things work, use the sample cli programs:

	./registry.py list
	./registry.py list device=gateway
	./subscriber.py  # (run in separate terminal)
	./publisher.py

Publisher script use HTTP protocol by default. You can specify another protocol as below
	
	./publisher.py [coap|mqtt]


Meshblu API implementation
--------------------------

| Meshblu request     |      Protocol      |
|---------------------|:------------------:|
| Register device     |   HTTP             |
| Unregister device   |   HTTP             |
| List devices        |   HTTP             |
| Reset device token  |   HTTP             |
| Send message        |   HTTP/CoAP/MQTT   |
| Subscribe           |   MQTT             |


Running the tests
-----------------

The tests essentially mirror the 'Checking it works' scenario,
hitting in turn on both the lib and cli tools.

To run the tests:

	pip install pytest
	pytest -v
