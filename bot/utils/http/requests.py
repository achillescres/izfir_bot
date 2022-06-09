import aiohttp
from aiohttp import ClientSession


async def get_http(url: str):
    try:
        async with ClientSession() as session:
            async with session.get(url) as res:
                return await res.text()
    except aiohttp.ClientConnectionError:
        return "null"
