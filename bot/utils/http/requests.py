import logging

import ujson
from aiohttp import ClientSession, ClientTimeout, ClientConnectionError

max_timeout = 1.5
response_error = 'err'


async def get(url: str):
    try:
        session_timeout = ClientTimeout(total=max_timeout, connect=max_timeout, sock_connect=max_timeout,
                                        sock_read=max_timeout)
        
        async with ClientSession(timeout=session_timeout) as session:
            for _ in range(3):
                async with session.get(url) as res:
                    if res.ok:
                        resp = await res.text(encoding='utf-8')
                        break
                    else:
                        resp = response_error
            await session.close()
        return resp
    except:
        return response_error


async def post(url: str, data: dict):
    try:
        session_timeout = ClientTimeout(total=max_timeout, connect=max_timeout, sock_connect=max_timeout,
                                        sock_read=max_timeout)
        
        async with ClientSession(json_serialize=ujson.dumps, timeout=session_timeout) as session:
            headers = {
                'Content-Type': 'application/json',
                'accept': 'application/json'
            }
            for _ in range(3):
                async with session.post(url, json=data, headers=headers) as res:
                    if res.ok:
                        resp = await res.text(encoding='utf-8')
                        break
                    else:
                        resp = response_error
            await session.close()
        return resp
    except ClientConnectionError:
        logging.info('Unable to post message')
        return response_error
