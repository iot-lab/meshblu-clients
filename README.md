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

Copy file `config.sample.py` to `config.py` and inspect content.

Meshblu requires authentication on most request.  You will need to either
use credentials provided by an admin - for the production instance - or
create your own "auth device" - for your local instance.

To create a first "auth device" on your local Meshblu instance, use:

	./http-registry.py register

Copy values `uuid` and `token` in the result above and edit file `config.py`
to replace sample values in the `auth` dict.

Repeat registry and edit operations for the `device` dict.
