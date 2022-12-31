import aiohttp
from aiohttp.client import _RequestContextManager

class Aio:

    def __init__(self) -> None:
        self.session = aiohttp.ClientSession()

    async def get(self, url: str):
        self.response = await self.session.get(url)

    @property
    async def content(self):
        return await self.response.read()