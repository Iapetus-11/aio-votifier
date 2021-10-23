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

    await client.v1_vote("username", "user address")  # only supports v1
    await client.nu_vote("username", "user address")  # only supports NuVotifier/v2

asyncio.run(main())
```
