from asyncio import TimeoutError
from aiohttp import ClientSession, ClientTimeout


max_timeout = 6
response_error = 'null'


async def get(url: str):
    try:
        session_timeout = ClientTimeout(total=max_timeout, connect=max_timeout, sock_connect=max_timeout, sock_read=max_timeout)
        async with ClientSession(timeout=session_timeout) as session:
            async with session.get(url) as res:
                if res.ok:
                    resp = await res.text(encoding='utf-8')
                else:
                    resp = response_error
        return resp
    except TimeoutError:
        return response_error
    finally:
        return response_error
