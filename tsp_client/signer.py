import secrets
import sys
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Callable, Optional

import requests
from asn1crypto import algos, tsp

from .algorithms import DigestAlgorithm
from .exceptions import TSPClientSigningError, InvalidInput
from .verifier import TSPVerifier, VerifyResult


@dataclass(frozen=True)
class SigningSettings:
    tsp_server: str = "http://timestamp.digicert.com"
    digest_algorithm: DigestAlgorithm = DigestAlgorithm.SHA512
    transport: Callable = requests.post
    policy: Optional[str] = None


class TSPSigner:
    headers = {"Content-Type": "application/timestamp-query", "Accept": "application/timestamp-reply"}
    max_clock_drift = timedelta(minutes=1)

    def __init__(self) -> None:
        self._verifier = TSPVerifier()

    def _verify_timestamp(self, verify_result: VerifyResult):
        now = datetime.now(tz=timezone.utc)
        if verify_result.tst_info["gen_time"] < now - self.max_clock_drift:
            raise TSPClientSigningError("Timestamp returned by server is too far in the past")
        if verify_result.tst_info["gen_time"] > now + self.max_clock_drift:
            raise TSPClientSigningError("Timestamp returned by server is too far in the future")

    def sign(self, message=None, *, message_digest=None, signing_settings: SigningSettings = SigningSettings()) -> bytes:
        if not message and not message_digest:
            raise InvalidInput("Expected at least one of message or message_digest to be set")
        if message is not None and message_digest is not None:
            raise InvalidInput("Expected only one of message and message_digest to be set")

        hasher = signing_settings.digest_algorithm.implementation()

        if message:
            hasher.update(message)
            message_digest = hasher.digest()

        nonce = int.from_bytes(secrets.token_bytes(), byteorder=sys.byteorder)
        tsp_request = tsp.TimeStampReq(
            {
                "version": 1,
                "message_imprint": tsp.MessageImprint(
                    {
                        "hash_algorithm": algos.DigestAlgorithm({"algorithm": hasher.name}),
                        "hashed_message": message_digest,
                    }
                ),
                "cert_req": True,
                "nonce": nonce,
            }
        )
        res = signing_settings.transport(signing_settings.tsp_server, headers=self.headers, data=tsp_request.dump())
        res.raise_for_status()
        tsp_response = tsp.TimeStampResp.load(res.content)
        if tsp_response["status"]["status"].native != "granted":
            raise TSPClientSigningError(
                f'{tsp_response["status"]["status"].native}: '
                f'{tsp_response["status"]["status_string"].native}, '
                f'{tsp_response["status"]["fail_info"].native}'
            )
        tst = tsp_response["time_stamp_token"].dump()
        verify_result = self._verifier.verify(tst, nonce=nonce, message_digest=message_digest)
        self._verify_timestamp(verify_result)
        return tst
