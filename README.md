# Aio-Votifier ![Code Quality](https://www.codefactor.io/repository/github/iapetus-11/aio-votifier/badge) ![PYPI Version](https://img.shields.io/pypi/v/aio-votifier.svg) ![PYPI Downloads](https://img.shields.io/pypi/dw/aio-votifier?color=0FAE6E) ![Views](https://api.ghprofile.me/view?username=iapetus-11.aio-votifier&color=0FAE6E&label=views&style=flat)
*An asynchronous MInecraft server votifier client in Python*

## Example Usage:
```py
from aiovotifier import NuVotifierClient
import asyncio

async def main():
    async with NuVotifierClient("127.0.0.1", 8192, "token") as client:
        await client.vote("Iapetus11")

asyncio.run(main())
```
or
```py
from aiovotifier import NuVotifierClient
import asyncio

async def main():
    client = NuVotifierClient("127.0.0.1", 8192, "token")
    await client.connect()

    await client.vote("Iapetus11")

    await client.close()

asyncio.run(main())
```
