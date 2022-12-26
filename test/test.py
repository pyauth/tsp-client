#!/usr/bin/env python

import hashlib
import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tsp_client import InvalidTimeStampToken, SigningSettings, TSPSigner, TSPVerifier  # noqa:E402


class TestTSPClient(unittest.TestCase):
    def test_basic_tsp_client_operations(self):
        message = b"abc"
        signer = TSPSigner()
        signed = signer.sign(message)

        verified = TSPVerifier().verify(signed, message=message)

        digest = hashlib.sha512(message).digest()
        verified = TSPVerifier().verify(signed, message_digest=digest)

        self.assertTrue(verified.tst_info)
        self.assertTrue(verified.signed_attrs)

        with self.assertRaises(InvalidTimeStampToken):
            TSPVerifier().verify(signed, message=message + b"def")

        with self.assertRaises(InvalidTimeStampToken):
            TSPVerifier().verify(signed, message=b"")

        with self.assertRaises(InvalidTimeStampToken):
            TSPVerifier().verify(signed, message_digest=reversed(digest))

    def test_set_custom_tsa(self):
        message = b"abc"
        signing_settings = SigningSettings(tsp_server="http://tsa.quovadisglobal.com/TSS/HttpTspServer")
        signer = TSPSigner()
        signed = signer.sign(message, signing_settings=signing_settings)
        TSPVerifier().verify(signed, message=message)


if __name__ == "__main__":
    unittest.main()
