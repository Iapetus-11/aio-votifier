class VotifierError(Exception):
    """Base class for votifier exceptions"""


class VotifierHeaderError(VotifierError):
    def __init__(self, header: bytes):
        super().__init__(f"Invalid header received from votifier server: {repr(header)}")
        self.header = header


class UnsupportedVersionError(VotifierError):
    def __init__(self, version: str):
        super().__init__(f"Unsupported votifier version: {repr(version)}")
        self.version = version


class NuVotifierError(VotifierError):
    """Base class for NuVotifier / Votifier v2 errors"""


class NuVotifierResponseError(NuVotifierError):
    def __init__(self, response: dict):
        super().__init__(f"Not-OK response received from votifier server: {repr(response)}")
        self.response = response
