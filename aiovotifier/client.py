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

    async def vote(self, username: str) -> None:
        r, w = await asyncio.open_connection(self.host, self.port)

        try:
            header = await r.read(64)

            if not header:
                raise NuVotifierHeaderError(header)

            header_split = header.split()

            if len(header_split) != 3:
                raise NuVotifierHeaderError(header)

            # create packet data
            payload = json.dumps(
                {
                    "username": username,
                    "serviceName": "minecraft.global",
                    "timestamp": round(datetime.datetime.utcnow().timestamp() * 1000),
                    "address": f"{self.host}:{self.port}",
                    "challenge": header_split[2].decode(),
                }
            )
            signature = b64encode(hmac.digest(self.token.encode(), payload.encode(), hashlib.sha256)).decode()
            message = json.dumps({"signature": signature, "payload": payload}).encode()

            # write packet
            w.write(struct.pack(">HH", 0x733A, len(message)) + message)
            await w.drain()

            response = json.loads(await r.read(256))

            if response["status"] != "ok":
                raise NuVotifierResponseError(response)
        
        finally:
            w.close()
            await w.wait_closed()
