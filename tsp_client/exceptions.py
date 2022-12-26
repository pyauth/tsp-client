class TSPClientError(Exception):
    pass


class InvalidInput(TSPClientError):
    pass


class TSPClientSigningError(TSPClientError):
    pass


class TSPClientVerifyingError(TSPClientError):
    pass


class InvalidTimeStampToken(TSPClientVerifyingError):
    pass


class NonceMismatchError(InvalidTimeStampToken):
    pass


class DigestMismatchError(InvalidTimeStampToken):
    pass
