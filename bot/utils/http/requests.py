from aiohttp import ClientSession, ClientConnectionError


async def get_http(url: str):
    try:
        async with ClientSession() as session:
            async with session.get(url) as res:
                return await res.text()
    except aiohttp.ClientConnectionError:
        return 'null'
