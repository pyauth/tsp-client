tsp-client: An IETF Time-Stamp Protocol (TSP) (RFC 3161) client
===============================================================
tsp-client is an implementation of the `RFC 3161 <https://www.rfc-editor.org/rfc/rfc3161.html>`_ TSP protocol in Python.

TSP is used for point-in-time attestation and non-repudiation as part of various electronic signature and code signing
schemes, including `eIDAS <https://en.wikipedia.org/wiki/EIDAS>`_ `XAdES <https://en.wikipedia.org/wiki/XAdES>`_
(tsp-client is used by `SignXML <https://github.com/XML-Security/signxml>`_ to implement XAdES).

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
To provide a timestamped signature with non-repudiation verifiable via a chain of trust, TSP requires the use of a TSA
(time-stamp authority) server when generating timestamp tokens. TSA servers can be thought of as digital notaries.
Verification of tokens can be done offline using your system's certificate authority (CA) trust store.

By default, tsp-client uses the `DigiCert TSA server
<https://knowledge.digicert.com/generalinformation/INFO4231.html>`_ when signing tokens. To use a different TSA, set the
``SigningSettings.tsp_server`` attribute as follows:

.. code-block:: python

    from tsp_client import TSPSigner, TSPVerifier, SigningSettings
    signing_settings = SigningSettings(tsp_server="http://timestamp.identrust.com")
    signer = TSPSigner()
    signed = signer.sign(message, signing_settings=signing_settings)

There is currently no credible public TSA that offers HTTPS transport security and does not apply throttling. DigiCert
provides a relatively high throughput public TSA endpoint, but your message digests and tokens will be transmitted
unencrypted over the network. As an alternative, Sectigo offers an HTTPS TSA (``https://timestamp.sectigo.com``) but
applies throttling so is only suitable for low throughput applications.

The European Union maintains a list of trusted TSAs as part of the `eIDAS dashboard
<https://esignature.ec.europa.eu/efda/tl-browser/>`_, however this list only serves as a root of trust and does not link
directly to the TSA endpoints of listed providers.

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
Copyright 2022-2023, Andrey Kislyuk and tsp-client contributors. Licensed under the terms of the
`Apache License, Version 2.0 <http://www.apache.org/licenses/LICENSE-2.0>`_. Distribution of the LICENSE and NOTICE
files with source copies of this package and derivative works is **REQUIRED** as specified by the Apache License.
