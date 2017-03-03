This is the Meshblu clients sample repository

Installing
----------

To run these sample clients, install the required libs
e.g. in a dedicated python virtual env:

	mkvirtualenv py
	pip install -r requirements.txt


You will need a running instance of Meshblu.
Either use the production instance at `data.embers.city`,
or install and run your own local instance.

To install and run a local instance of Meshblu,
see https://github.com/iotlab/meshblu


Configuring
-----------

The EMBERS use-case of Meshblu requires the following:

- a "gateway" device, the target of events publishing
- a "sensor"  device, the origin of events


To configure the Meshblu instance, use:

	./registry.py init_config


This will create both devices on the (local) Meshblu instance
and a file `config.py` with devices info and a reference to the broker.

(you can specify the prod instance address on the command line)


Checking it works
-----------------

To check things work, use the sample cli programs:

	./registry.py list
	./subscriber.py  # (run in separate terminal)
	./publisher.py

or run the test:

	pytest -v
