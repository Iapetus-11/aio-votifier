from base64 import b64encode
import datetime
import asyncio
import hashlib
import struct
import hmac
import json

from .errors import NuVotifierHeaderError, NuVotifierResponseError, ClientNotConnectedError


class NuVotifierClient:
    def __init__(self, host: str, port: int, token: str):
        self.host = host
        self.port = port
        self.token = token

        self._ready = False

        self._reader = None
        self._writer = None

        self._header = None
        self._header_split = None

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, *args, **kwargs):
        await self.close()

    async def connect(self) -> "NuVotifierClient":
        if self._ready:
            return

        self._reader, self._writer = await asyncio.open_connection(self.host, self.port)
        self._ready = True

        self._header = await self._reader.read(64)

        if not self._header:
            raise NuVotifierHeaderError(self._header)

        self._header_split = self._header.split()

        if len(self._header_split) != 3:
            raise NuVotifierHeaderError(self._header)

    async def close(self) -> None:
        if self._ready:
            self._writer.close()
            await self._writer.wait_closed()

            self._reader = None
            self._writer = None

            self._ready = False

            self._header = None
            self._header_split = None

    async def vote(self, username: str) -> None:
        if not self._ready:
            raise ClientNotConnectedError

        # create packet data
        payload = json.dumps(
            {
                "username": username,
                "serviceName": "minecraft.global",
                "timestamp": round(datetime.datetime.utcnow().timestamp() * 1000),
                "address": f"{self.host}:{self.port}",
                "challenge": self._header_split[2].decode(),
            }
        )
        signature = b64encode(hmac.digest(self.token.encode(), payload.encode(), hashlib.sha256)).decode()
        message = json.dumps({"signature": signature, "payload": payload}).encode()

        # write packet
        self._writer.write(struct.pack(">HH", 0x733A, len(message)) + message)
        await self._writer.drain()

        response = json.loads(await self._reader.read(256))

        if response["status"] != "ok":
            raise NuVotifierResponseError(response)
