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


class NuVotifierResponseError(VotifierError):
    """Raised when the response from the votifier server contains a status that is not OK"""

    def __init__(self, response: dict):
        super().__init__(f"Not-OK response received from votifier server: {repr(response)}")
        self.response = response
