import hashlib
from enum import Enum
from typing import Callable

from asn1crypto.algos import DigestAlgorithmId


class DigestAlgorithm(Enum):
    """
    An enumeration of digest algorithms supported by TSAClient.
    """

    SHA224 = DigestAlgorithmId("2.16.840.1.101.3.4.2.4").native
    SHA256 = DigestAlgorithmId("2.16.840.1.101.3.4.2.1").native
    SHA384 = DigestAlgorithmId("2.16.840.1.101.3.4.2.2").native
    SHA512 = DigestAlgorithmId("2.16.840.1.101.3.4.2.3").native
    SHA3_224 = DigestAlgorithmId("2.16.840.1.101.3.4.2.7").native
    SHA3_256 = DigestAlgorithmId("2.16.840.1.101.3.4.2.8").native
    SHA3_384 = DigestAlgorithmId("2.16.840.1.101.3.4.2.9").native
    SHA3_512 = DigestAlgorithmId("2.16.840.1.101.3.4.2.10").native

    @property
    def implementation(self) -> Callable:
        """
        The hashlib callable that implements the specified algorithm.
        """
        return digest_algorithm_implementations[self]  # type: ignore


digest_algorithm_implementations = {
    DigestAlgorithm.SHA224: hashlib.sha224,
    DigestAlgorithm.SHA256: hashlib.sha256,
    DigestAlgorithm.SHA384: hashlib.sha384,
    DigestAlgorithm.SHA512: hashlib.sha512,
    DigestAlgorithm.SHA3_224: hashlib.sha3_224,
    DigestAlgorithm.SHA3_256: hashlib.sha3_256,
    DigestAlgorithm.SHA3_384: hashlib.sha3_384,
    DigestAlgorithm.SHA3_512: hashlib.sha3_512,
}
