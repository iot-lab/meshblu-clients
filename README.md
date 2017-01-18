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

Meshblu requires authentication on most request.  You will need to either
use credentials provided by an admin - for the production instance - or
create your own "auth device" - for your local instance.

To create a first "auth device" on your local Meshblu instance, use:

	curl -X POST -d "type=example" http://localhost/devices

The command above should produce a json result showing "uuid" and "token"
values that can be used as credentials for subsequent Meshblu api calls.

Copy file `config.sample.py` to `config.py` and paste in there the values
of `uuid` and `token` into the `auth` dict replacing sample values.
