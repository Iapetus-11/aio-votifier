# aio-votifier
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
