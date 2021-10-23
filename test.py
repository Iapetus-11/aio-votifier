from aiovotifier import *
import asyncio

e = "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA2zYjTPpSz3dTvC62eAXFtWo8s9o5oGyugh9CfIMLWbQJzSJarOQKaO/8zuGqv+95NpTNtmn+J7+CkIJ6fsdPbeyuhJUnXiCOGLJTN+EZ7I4f7DISGDqV3HSChkiQyxQrGStcFQsPCsg0l0QXBBN154r/zlcyjBjYzlj705RbUvRw6AHv6/+15IG7MLCByR96TI5nmkMJgMxJfz+HmK9AZCSQPnIoBPFqd2RuubxX0lypuPf4gpfGJpoy8pW4G557NOq2S3UX2y5y7m629zqp4oH6MV/nWNuTCzY3djM16HZBbAcgLr9UGC2Q4i5KNjgw8yD5ApXG+kIUdi3CNLd1EQIDAQAB"

async def main():
    c = VotifierClient("xenon.iapetus11.me", 8192, e)

    await c.vote("Iapetus11")

asyncio.run(main())
