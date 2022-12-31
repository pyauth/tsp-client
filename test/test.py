#!/usr/bin/env python

import hashlib
import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tsp_client import (  # noqa:E402
    DigestMismatchError,
    InvalidTimeStampToken,
    NonceMismatchError,
    SigningSettings,
    TSPSigner,
    TSPVerifier,
)


class TestTSPClient(unittest.TestCase):
    tsp_servers = [
        "http://timestamp.digicert.com",
        "http://timestamp.identrust.com",
        "http://timestamp.entrust.net/TSS/RFC3161sha2TS",
        "http://rfc3161timestamp.globalsign.com/advanced",  # throttling or high RTT
        "http://tsa.quovadisglobal.com/TSS/HttpTspServer",  # throttling or high RTT
        "https://timestamp.sectigo.com",  # applies throttling
    ]

    def setUp(self):
        self.signer = TSPSigner()
        self.verifier = TSPVerifier()

    def test_basic_tsp_client_operations(self):
        message = b"abc"
        signed = self.signer.sign(message)
        verified = self.verifier.verify(signed, message=message)
        digest = hashlib.sha512(message).digest()
        verified = self.verifier.verify(signed, message_digest=digest)

        self.assertTrue(verified.tst_info)
        self.assertTrue(verified.signed_attrs)

        with self.assertRaises(DigestMismatchError):
            self.verifier.verify(signed, message=message + b"def")

        with self.assertRaises(DigestMismatchError):
            self.verifier.verify(signed, message=b"")

        with self.assertRaises(DigestMismatchError):
            self.verifier.verify(signed, message_digest=reversed(digest))

        with self.assertRaises(NonceMismatchError):
            self.verifier.verify(signed, message_digest=digest, nonce=123)

    def test_set_custom_tsa(self):
        message = b"abc"
        for tsp_server in self.tsp_servers:
            signing_settings = SigningSettings(tsp_server=tsp_server)
            signed = self.signer.sign(message, signing_settings=signing_settings)
            self.verifier.verify(signed, message=message)


if __name__ == "__main__":
    unittest.main()
