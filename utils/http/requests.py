from aiohttp import ClientSession


async def get_http(url: str):
    async with ClientSession() as session:
        async with session.get(url) as res:
            return await res.text()
