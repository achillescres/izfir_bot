import logging

import ujson
from aiohttp import ClientSession, ClientConnectionError

from data.config import SERVER_API


URL = f'{SERVER_API}/fromBot/cancelChat/'


async def _send_cancel_with_session(session: ClientSession, data):
    for i in range(3):
        async with session.post(URL, json=data) as resp:
            logging.info((await resp.json()).strip())
            if (await resp.json()).strip() == 'ok':
                logging.info('URA   CLOSED')
                return True

    return False


async def cancel(operator_id, user_id):
    try:
        async with ClientSession(json_serialize=ujson.dumps) as session:
            data = {
                'operator_id': operator_id,
                'user_id': user_id,
                'message': 'cancelling message',
            }

            sent = await _send_cancel_with_session(session, data)
            await session.close()

            if not sent:
                logging.info('Failed to cancel chat with operator')
                return 'err'

            return True
    except ClientConnectionError:
        return 'err'
