class VotifierError(Exception):
    """Base class for votifier exceptions"""


class NuVotifierError(VotifierError):
    """Base class for NuVotifier exceptions"""


class NuVotifierHeaderError(NuVotifierError):
    def __init__(self, header: bytes):
        super().__init__("Invalid header received from votifier server.")
        self.header = header


class NuVotifierResponseError(NuVotifierError):
    def __init__(self, response: dict):
        super().__init__("Response from votifier server was not OK.")
        self.response = response
