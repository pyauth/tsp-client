tsp-client: An IETF Time-Stamp Protocol (TSP) (RFC 3161) client
===============================================================
tsp-client is an implementation of the `RFC 3161 <https://www.rfc-editor.org/rfc/rfc3161.html>`_ TSP protocol in Python.

Installation
------------
::

    pip install tsp-client

Synopsis
--------

.. code-block:: python

    from tsp_client import TSPSigner, TSPVerifier

    # Sign a message online by transmitting its digest to the timestamp authority
    message = b"abc"
    signer = TSPSigner()
    signed = signer.sign(message)  # Returns raw bytes of the verified timestamp token.

    # Verify a presented timestamp token offline using the original message
    verified = TSPVerifier().verify(signed, message=message)

    # Or verify using the message digest (digest algorithm may vary)
    import hashlib

    digest = hashlib.sha512(message).digest()
    verified = TSPVerifier().verify(signed, message_digest=digest)

    print(verified.tst_info)  # Parsed TSTInfo (CMS SignedData) structure
    print(verified.signed_attrs)  # Parsed CMS SignedAttributes structure

Specifying a custom TSA
~~~~~~~~~~~~~~~~~~~~~~~
By default, tsp-client uses the `DigiCert TSA server
<https://knowledge.digicert.com/generalinformation/INFO4231.html>`_. To use a different TSA, set the
``SigningSettings.tsp_server`` attribute as follows:

.. code-block:: python

    from tsp_client import TSPSigner, TSPVerifier, SigningSettings
    signing_settings = SigningSettings(tsp_server="http://tsa.quovadisglobal.com/TSS/HttpTspServer")
    signer = TSPSigner()
    signed = signer.sign(message, signing_settings=signing_settings)


Authors
-------
* Andrey Kislyuk

Links
-----
* `Project home page (GitHub) <https://github.com/pyauth/tsp-client>`_
* `Documentation <https://pyauth.github.io/tsp-client/>`_
* `Package distribution (PyPI) <https://pypi.python.org/pypi/tsp-client>`_
* `Change log <https://github.com/pyauth/tsp-client/blob/master/Changes.rst>`_
* `IETF RFC 3161: Time-Stamp Protocol (TSP) <https://www.rfc-editor.org/rfc/rfc3161.html>`_

Bugs
~~~~
Please report bugs, issues, feature requests, etc. on `GitHub <https://github.com/pyauth/tsp-client/issues>`_.

License
-------
Licensed under the terms of the `Apache License, Version 2.0 <http://www.apache.org/licenses/LICENSE-2.0>`_.
