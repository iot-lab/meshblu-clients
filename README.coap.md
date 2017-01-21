CoAP auth in Meshblu
====================

Most Meshblu API calls require auth in the form of
uuid/token pairs sent along requests.

The Meshblu CoAP server relies on CoAP options to
implement a mechanism similar to "basic auth" for CoAP.

- option 98 (non-standard) = username (uuid)
- option 99 (non-standard) = password (token)

While CoAP options specification is part of the standard,
(see https://tools.ietf.org/html/rfc7252#section-5.4)
options numbers 98 and 99, used by Meshblu for passing
username (uuid) and password (token) respectively,
are not defined or reserved by the standard.

https://github.com/octoblu/coap-cli/commit/d9fb8596


CoAP and Python
===============

Basic production grade python support for CoAP is yet to be found.
Everyone uses their preferred framework and implementation and no
single generally accepted (or maintained) CoAP implementation exists.
As of Jan 2017, the following is available via pip:

    $ pip search coap
    aiocoap (0.3)         - Python CoAP library
    openwsn-coap (0.0.2)  - A CoAP Python library
    CoAPy (4.0.2)         - CoAPy is a python implementation for the CoAP protocol.
    pushcoapi (0.0.1)     - Python library for Push.co
    pycolo (0.0.1)        - Python CoAP lightweight Operator.
    txThings (0.2.0)      - CoAP protocol implementation for Twisted Framework

The two basic non-framework-oriented implementation have their gotchas:
- openwsn-coap 0.0.2 does not provide support for the observe specification
- CoAPy 4.0.2 (coapthon) causes crash on the Meshblu server when using observe


CoAP subscriber (observe)
=========================

The current implementation of `coap-subscriber.py` is based on coapthon
and is working more-or-less as expected, except that notifications stop
being received after some time (of inactivity).
