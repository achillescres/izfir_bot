from aiohttp import ClientSession, ClientConnectionError


async def get(url: str):
    res = 'null'
    try:
        async with ClientSession() as session:
            async with session.get(url) as res:
                res = await res.text(encoding='utf-8')
        await session.close()
        return res
    except ClientConnectionError:
        return 'null'
