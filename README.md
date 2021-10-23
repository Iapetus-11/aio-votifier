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
    - `nu_vote(username: str, user_address: str = "127.0.0.1")` - *sends a NuVotifier / v2 vote to a NuVotifier server*

