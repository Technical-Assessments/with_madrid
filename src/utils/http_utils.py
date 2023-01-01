# import aiohttp
# from aiohttp.client import _RequestContextManager

# class AioHttpManager:

#     def __init__(self) -> None:
#         self.session = aiohttp.ClientSession()

#     async def close(self):
#         await self.session.close()

#     async def get(self, url: str):
#         return await self.session.get(url)

#     async def content(self, response: _RequestContextManager):
#         return await response.read()