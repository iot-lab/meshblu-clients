from setuptools import setup, find_packages

PACKAGE = "embers.meshblu"
VERSION = "0.1"


setup(
    name           = PACKAGE,
    version        = VERSION,
    author         = "The EMBERS consortium",
    author_email   = "dev@embers.city",
    description    = "Meshblu clients (http, mqtt, coap)",
    url            = "http://www.embers.city/",
    keywords       = ["Smart City", "Meshblu"],
    license        = "=== TBD ===",
    packages       = find_packages("src"),
    package_dir    = {"": "src"},
    namespace_packages = [PACKAGE],

    install_requires = [
        "requests",
        "paho-mqtt",
       # "git+https://github.com/iot-lab/CoAPthon.git@master",
    ],
)
