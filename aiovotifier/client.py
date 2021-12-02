from asyncio.streams import StreamReader, StreamWriter
from typing import Tuple, List, Optional
from base64 import b64encode
import datetime
import asyncio
import hashlib
import struct
import hmac
import json
import time

from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.primitives.asymmetric.padding import PKCS1v15
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey

from .errors import NuVotifierResponseError, VotifierHeaderError, UnsupportedVersionError
from .utils import ensure_pem_format

__all__ = ("votifier_v1_vote", "nuvotifier_vote", "VotifierHeader", "VotifierClient")


async def votifier_v1_vote(
    r: StreamReader, w: StreamWriter, service_name: str, username: str, user_address: str, key: RSAPublicKey
) -> None:
    data = "\n".join(
        [
            "VOTE",
            service_name,
            username,
            user_address,
            str(round(time.time())),
        ]
    ).encode()

    encrypted = key.encrypt(data, PKCS1v15())

    w.write(encrypted)
    await w.drain()


async def nuvotifier_vote(
    r: StreamReader, w: StreamWriter, service_name: str, username: str, user_address: str, token: str, challenge: str
) -> dict:
    # create packet data
    payload = json.dumps(
        {
            "username": username,
            "serviceName": service_name,
            "timestamp": round(datetime.datetime.utcnow().timestamp() * 1000),
            "address": user_address,
            "challenge": challenge,
        }
    )
    signature = b64encode(hmac.digest(token.encode(), payload.encode(), hashlib.sha256)).decode()
    message = json.dumps({"signature": signature, "payload": payload}).encode()

    # write packet
    w.write(struct.pack(">HH", 0x733A, len(message)) + message)
    await w.drain()

    response = json.loads(await r.read(256))

    if response.get("status", "").lower() != "ok":
        raise NuVotifierResponseError(response)

    return response


class VotifierHeader:
    """Used for parsing and storing the votifier header data"""

    __slots__ = ("header", "version", "challenge")

    def __init__(self, header: bytes, version: str, challenge: str = None):
        self.header = header
        self.version = version
        self.challenge = challenge

    @classmethod
    def parse(cls, header: bytes) -> "VotifierHeader":
        header_split = header.decode().split()
        split_length = len(header_split)

        if 3 < split_length < 2:
            raise VotifierHeaderError(header)

        if header_split[0] != "VOTIFIER":
            raise VotifierHeaderError(header)

        version = header_split[1]

        if version == "2" and split_length != 3:
            raise VotifierHeaderError(header)

        return cls(header, version, (header_split[2].rstrip("\n") if split_length == 3 else None))


class VotifierClient:
    __slots__ = ("host", "port", "service_name", "secret", "_rsa_pub_key", "_rsa_pub_key_exc")

    def __init__(self, host: str, port: int, service_name: str, secret: str):
        self.host = host
        self.port = port
        self.service_name = service_name
        self.secret = secret

        self._rsa_pub_key: Optional[RSAPublicKey] = None
        self._rsa_pub_key_exc: Optional[Exception] = None

        try:
            self._rsa_pub_key = load_pem_public_key(ensure_pem_format(secret).encode())
        except Exception as e:
            self._rsa_pub_key_exc = e

    async def _connect(self) -> Tuple[StreamReader, StreamWriter, VotifierHeader]:
        r, w = await asyncio.open_connection(self.host, self.port)

        try:
            header = VotifierHeader.parse(await r.read(64))
        except:
            w.close()
            await w.wait_closed()
            raise

        return r, w, header

    async def vote(self, username: str, user_address: str = "127.0.0.1") -> None:
        """Sends a vote to the votifier server, automatically determining the protocol to use"""

        r, w, header = await self._connect()

        try:
            if header.version == "1":
                if self._rsa_pub_key_exc:
                    raise self._rsa_pub_key_exc

                await votifier_v1_vote(r, w, self.service_name, username, user_address, self._rsa_pub_key)
            elif header.version == "2":
                if self._rsa_pub_key:
                    # even tho it's v2, the user passed in an rsa key which is only used in v1
                    await votifier_v1_vote(r, w, self.service_name, username, user_address, self._rsa_pub_key)
                else:
                    await nuvotifier_vote(r, w, self.service_name, username, user_address, self.secret, header.challenge)
            else:
                raise UnsupportedVersionError(header.version)
        finally:
            w.close()
            await w.wait_closed()

    async def v1_vote(self, username: str, user_address: str = "127.0.0.1") -> None:
        """Sends a Votifier v1 vote to the votifier server"""

        r, w, header = await self._connect()

        try:
            if header.version != "1":
                raise UnsupportedVersionError(header.version)

            if self._rsa_pub_key_exc:
                raise self._rsa_pub_key_exc

            await votifier_v1_vote(r, w, self.service_name, username, user_address, self._rsa_pub_key)
        finally:
            w.close()
            await w.wait_closed()

    async def nu_vote(self, username: str, user_address: str = "127.0.0.1") -> dict:
        r, w, header = await self._connect()

        try:
            if header.version != "2":
                raise UnsupportedVersionError(header.version)

            return await nuvotifier_vote(r, w, self.service_name, username, user_address, self.secret, header.challenge)
        finally:
            w.close()
            await w.wait_closed()
