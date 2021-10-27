# Aio-Votifier ![Code Quality](https://www.codefactor.io/repository/github/iapetus-11/aio-votifier/badge) ![PYPI Version](https://img.shields.io/pypi/v/aiovotifier.svg) ![PYPI Downloads](https://img.shields.io/pypi/dw/aiovotifier?color=0FAE6E) ![Views](https://api.ghprofile.me/view?username=iapetus-11.aio-votifier&color=0FAE6E&label=views&style=flat)
*An asynchronous MInecraft server votifier client in Python*

## Example Usage:
```py
from aiovotifier import VotifierClient
import asyncio

async def main():
    client = VotifierClient("127.0.0.1", 8192, "testservicename", "token/rsa key")
    
    # VotifierClient.vote(...) automatically determines the protocol and key format
    await client.vote("username", "user address")
    await client.vote("user2")

    await client.v1_vote("username", "user address")  # only supports v1 protocol
    await client.nu_vote("username", "user address")  # only supports NuVotifier/v2 protocol

asyncio.run(main())
```

## Documentation
#### *class* aiovotifier.**VotifierClient**(host: *str*, port: *int*, service_name: *str*, secret: *str*)
- Arguments:
    - `host: str` - *The hostname or IP of the votifier server*
    - `port: int` - *The port of the votifier server, commonly 8192*
    - `service_name: str` - *The name of the service that sends the vote*
    - `secret: str` - *The public RSA key or the token found in `config.yml`*
- Methods:
    - `vote(username: str, user_address: str = "127.0.0.1")` - *sends a vote to the votifier server, automatically detects and handles the protocol and type of secret*
    - `v1_vote(username: str, user_address: str = "127.0.0.1")` - *sends a Votifier v1 vote to a votifier v1 server*
    - `nu_vote(username: str, user_address: str = "127.0.0.1") -> dict` - *sends a NuVotifier / v2 vote to a NuVotifier server, returns the response from the server*

#### *class* aiovotifier.**VotifierHeader**(header: *bytes*, version: *str*, token: *str* = None)
- Arguments:
    - `header: bytes` - *The header received from the votifier server*
    - `version: str` - *The version of the votifier server*
    - `challenge: str = None` - *The challenge, included only if the votifier server is v2/NuVotifier*
- Methods:
    - `@classmethod parse(header: bytes)` - *Returns a new `VotifierHeader`, parsed from the input bytes*

#### *function* aiovotifier.**votifier_v1_vote**(r: *asyncio.StreamReader*, w: *asyncio.StreamWriter*, service_name: *str*, username: *str*, user_address: *str*, key: *cryptography.hazmat.primitives.asymmetric.rsa.RSAPublicKey*)
- *Sends a Votifier v1 vote to a Votifier v1 server*

#### *function* aiovotifier.**nuvotifier_vote**(r: *asyncio.StreamReader*, w: *asyncio.StreamWriter*, service_name: *str*, username: *str*, user_address: *str*, token: *str*, challenge: *str*) -> *dict*
- *Sends a NuVotifier / v2 vote to a NuVotifier server*

#### *exception* aiovotifier.**VotifierError**
- *Base class that all votifier exceptions derive from*

#### *exception* aiovotifier.**VotifierHeaderError**
- *Raised when the header from the votifier server is invalid*

#### *exception* aiovotifier.**UnsupportedVersionError**
- *Raised when the votifier version is unsupported*

#### *exception* aiovotifier.**NuVotifierResponseError**
- *Raised when the response from the votifier server contains a status that is not OK*

## Credits
*aiovotifier was based off the code and documentation below*
- https://github.com/ano95/votifier2-py
- https://www.npmjs.com/package/votifier-client/v/0.1.0?activeTab=dependents
- https://github.com/vexsoftware/votifier
- https://github.com/NuVotifier/NuVotifier/wiki/Technical-QA
